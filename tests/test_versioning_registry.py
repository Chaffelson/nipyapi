"""Tests for `nipyapi` versioning package - NiFi Registry specific tests.

These tests require a running NiFi Registry service and are skipped when
using the github-cicd profile which only has NiFi (no Registry).
"""

import pytest
from deepdiff import DeepDiff
from tests import conftest
from nipyapi import registry, nifi, versioning, canvas, utils, parameters

# Skip all tests in this module when Registry is not available
pytestmark = pytest.mark.skipif(
    conftest.ACTIVE_PROFILE == 'github-cicd',
    reason='Test requires NiFi Registry service (not available in github-cicd profile)'
)


def test_create_registry_client():
    # First remove any leftover test client connections
    [versioning.delete_registry_client(li) for
     li in versioning.list_registry_clients().registries
             if conftest.test_registry_client_name in li.component.name
     ]
    # Use versioning.ensure_registry_client directly
    r = versioning.ensure_registry_client(
        name=conftest.test_registry_client_name,
        uri=conftest.ACTIVE_CONFIG['registry_internal_url'],
        description=f"Test Registry Client -> {conftest.ACTIVE_CONFIG['registry_internal_url']}"
    )
    assert isinstance(r, nifi.FlowRegistryClientEntity)


def test_delete_registry_client():
    f_reg_client = versioning.get_registry_client(
        conftest.test_registry_client_name
    )
    r1 = versioning.delete_registry_client(f_reg_client)
    assert isinstance(r1, nifi.FlowRegistryClientEntity)
    assert r1.component.name == conftest.test_registry_client_name
    r2 = versioning.get_registry_client(
        conftest.test_registry_client_name
    )
    assert r2 is None
    with pytest.raises(AssertionError):
        _ = versioning.delete_registry_client('FakeClient')


def test_list_registry_buckets(fix_bucket):
    _ = fix_bucket()
    r = versioning.list_registry_buckets()
    assert isinstance(r, list)
    assert len(r) >= 1


def test_create_registry_bucket(fix_bucket):
    # We include fix_bucket to handle the cleanup
    r = versioning.create_registry_bucket(conftest.test_bucket_name)
    assert isinstance(r, registry.Bucket)
    assert r.name == conftest.test_bucket_name
    # Bucket names are unique
    with pytest.raises(ValueError) as v:
        _ = versioning.create_registry_bucket(conftest.test_bucket_name)


def test_delete_registry_bucket(fix_bucket):
    f_bucket = fix_bucket()
    r = versioning.delete_registry_bucket(f_bucket)
    assert r.identifier == f_bucket.identifier
    with pytest.raises(ValueError):
        _ = versioning.delete_registry_bucket('FakeNews')


def test_get_registry_bucket(fix_bucket):
    f_bucket = fix_bucket()
    r1 = versioning.get_registry_bucket(f_bucket.name)
    assert r1.name == conftest.test_bucket_name
    r2 = versioning.get_registry_bucket(r1.identifier, 'id')
    assert r2.name == r1.name
    with pytest.raises(ValueError):
        _ = versioning.get_registry_bucket('Irrelevant', 'Invalid')
    r3 = versioning.get_registry_bucket('NonExistantProbably')
    assert r3 is None


def test_save_flow_ver(fix_bucket, fix_pg, fix_proc):
    f_reg_client = versioning.ensure_registry_client(
        name=conftest.test_registry_client_name,
        uri=conftest.ACTIVE_CONFIG['registry_internal_url'],
        description=f"Test Registry Client -> {conftest.ACTIVE_CONFIG['registry_internal_url']}"
    )
    f_bucket = fix_bucket()
    f_pg = fix_pg.generate()
    test_bucket = versioning.get_registry_bucket(f_bucket.identifier, 'id')
    assert test_bucket.name == conftest.test_bucket_name
    r1 = versioning.save_flow_ver(
        process_group=f_pg,
        registry_client=f_reg_client,
        bucket=test_bucket,
        flow_name=conftest.test_versioned_flow_name,
        comment='a test comment',
        desc='a test description'
    )
    assert isinstance(r1, nifi.VersionControlInformationEntity)
    # Next we validate you can't duplicate a flow name in a bucket
    with pytest.raises(ValueError):
        _ = versioning.save_flow_ver(
            process_group=f_pg,
            registry_client=f_reg_client,
            bucket=f_bucket,
            flow_name=conftest.test_versioned_flow_name,
            comment='NiPyApi Test',
            desc='NiPyApi Test'
        )
    # Add a processor, refresh status, and save a new version
    fix_proc.generate(parent_pg=f_pg)
    f_pg = canvas.get_process_group(f_pg.id, 'id')
    r2 = versioning.save_flow_ver(
        process_group=f_pg,
        registry_client=f_reg_client,
        bucket=f_bucket,
        flow_id=r1.version_control_information.flow_id,
        comment='a test comment'
    )
    assert isinstance(r2, nifi.VersionControlInformationEntity)
    assert r2.version_control_information.version > \
           r1.version_control_information.version
    with pytest.raises(ValueError):
        _ = versioning.save_flow_ver(
            process_group=f_pg,
            registry_client=f_reg_client,
            bucket=f_bucket,
            flow_name=conftest.test_versioned_flow_name,
            comment='a test comment',
            desc='a test description',
            refresh=False
        )
    # shortcut to clean up the test objects when not using the fixture
    conftest.cleanup_reg()


def test_stop_flow_ver(fix_ver_flow):
    r1 = versioning.stop_flow_ver(fix_ver_flow.pg)
    assert isinstance(r1, nifi.VersionControlInformationEntity)
    assert r1.version_control_information is None
    with pytest.raises(ValueError,
                       match='not currently under Version Control'):
        _ = versioning.stop_flow_ver(fix_ver_flow.pg)
    with pytest.raises(ValueError):
        _ = versioning.stop_flow_ver(fix_ver_flow.pg, refresh=False)


def test_revert_flow_ver(fix_ver_flow):
    r1 = versioning.revert_flow_ver(fix_ver_flow.pg)
    assert isinstance(r1, nifi.VersionedFlowUpdateRequestEntity)
    # TODO: Add Tests for flows with data loss on reversion
    with pytest.raises(AssertionError):
        _ = versioning.revert_flow_ver('NotAPg')


def test_list_flows_in_bucket(fix_ver_flow):
    r1 = versioning.list_flows_in_bucket(fix_ver_flow.bucket.identifier)
    assert isinstance(r1, list)
    assert isinstance(r1[0], registry.VersionedFlow)
    with pytest.raises(ValueError, match='does not exist'):
        _ = versioning.list_flows_in_bucket('NiPyApi-FakeNews')


def test_get_flow_in_bucket(fix_ver_flow):
    r1 = versioning.get_flow_in_bucket(
        fix_ver_flow.bucket.identifier,
        fix_ver_flow.flow.identifier,
        'id'
    )
    assert isinstance(r1, registry.VersionedFlow)
    assert r1.identifier == fix_ver_flow.info.version_control_information. \
        flow_id
    r2 = versioning.get_flow_in_bucket(fix_ver_flow.bucket.identifier,
                                       'fakenews', 'id')
    assert r2 is None


def test_get_latest_flow_ver(fix_ver_flow):
    r1 = versioning.get_latest_flow_ver(
        fix_ver_flow.bucket.identifier,
        fix_ver_flow.flow.identifier
    )
    assert isinstance(r1, registry.VersionedFlowSnapshot)
    with pytest.raises(ValueError, match='does not exist'):
        _ = versioning.get_latest_flow_ver(
            fix_ver_flow.bucket.identifier,
            'fakenews'
        )


def test_get_version_info(fix_ver_flow):
    r1 = versioning.get_version_info(fix_ver_flow.pg)
    assert isinstance(r1, nifi.VersionControlInformationEntity)
    with pytest.raises(AssertionError):
        _ = versioning.get_version_info('NotAPG')


def test_create_flow(fix_ver_flow):
    r1 = versioning.create_flow(
        bucket_id=fix_ver_flow.bucket.identifier,
        flow_name=conftest.test_cloned_ver_flow_name,
    )
    assert isinstance(r1, registry.VersionedFlow)
    assert r1.name == conftest.test_cloned_ver_flow_name
    # test duplicate behavior
    with pytest.raises(ValueError):
        _ = versioning.create_flow(
            bucket_id=fix_ver_flow.bucket.identifier,
            flow_name=conftest.test_cloned_ver_flow_name,
        )


def test_create_flow_version(fix_ver_flow):
    new_ver_stub = versioning.create_flow(
        bucket_id=fix_ver_flow.bucket.identifier,
        flow_name=conftest.test_cloned_ver_flow_name,
    )
    ver_flow_snapshot_0 = versioning.get_latest_flow_ver(
        fix_ver_flow.bucket.identifier,
        fix_ver_flow.flow.identifier
    )
    r1 = versioning.create_flow_version(
        flow=new_ver_stub,
        flow_snapshot=ver_flow_snapshot_0
    )
    assert isinstance(r1, registry.VersionedFlowSnapshot)
    assert DeepDiff(
        ver_flow_snapshot_0.flow_contents,
        r1.flow_contents,
        ignore_order=False,
        verbose_level=2
    ) == {}
    # Write it again to increment the version, check it's consistent
    r2 = versioning.create_flow_version(
        flow=new_ver_stub,
        flow_snapshot=ver_flow_snapshot_0
    )
    assert isinstance(r2, registry.VersionedFlowSnapshot)
    assert DeepDiff(
        ver_flow_snapshot_0.flow_contents,
        r2.flow_contents,
        ignore_order=False,
        verbose_level=2
    ) == {}


def test_export_flow_version(fix_flow_serde):
    # Test we can turn a flow snapshot into a json string
    r1 = versioning.export_flow_version(
        fix_flow_serde.bucket.identifier,
        fix_flow_serde.flow.identifier
    )
    assert isinstance(r1, str)
    # Test writing it to a file
    r2 = versioning.export_flow_version(
        fix_flow_serde.bucket.identifier,
        fix_flow_serde.flow.identifier,
        file_path=fix_flow_serde.filepath + '_test.json'
    )
    assert isinstance(r2, str)
    r2l = utils.load(r2)
    assert isinstance(r2l, dict)
    assert r2l['snapshotMetadata'].__contains__('flowIdentifier')
    # read in the file
    r2f = utils.fs_read(fix_flow_serde.filepath + '_test.json')
    DeepDiff(
        r2,
        r2f,
        ignore_order=False,
        verbose_level=2
    )
    # Test yaml dump
    r3 = versioning.export_flow_version(
        fix_flow_serde.bucket.identifier,
        fix_flow_serde.flow.identifier,
        mode='yaml'
    )
    assert isinstance(r3, str)
    r3l = utils.load(r3)
    assert isinstance(r3l, dict)
    assert r3l['snapshotMetadata'].__contains__('flowIdentifier')


def test_import_flow_version(fix_flow_serde):
    compare_obj = fix_flow_serde.snapshot
    test_obj = fix_flow_serde.raw
    # Test that our test_obj serialises and deserialises through the layers of
    # json reformatting. This is because we load the NiFi Java json object,
    # dump it using the Python json library, and load it again using
    # PyYAML.
    assert DeepDiff(
        compare_obj,
        utils.load(
            utils.dump(
                utils.load(
                    obj=test_obj
                ),
                mode='json'
            ),
            dto=fix_flow_serde.dto
        ),
        ignore_order=False,
        verbose_level=2
    ) == {}
    # Test that we can issue a simple create_flow with this object
    r0 = versioning.create_flow_version(
        flow=fix_flow_serde.flow,
        flow_snapshot=utils.load(
            obj=fix_flow_serde.json,
            dto=fix_flow_serde.dto
        )
    )
    assert isinstance(r0, registry.VersionedFlowSnapshot)
    assert DeepDiff(
        compare_obj.flow_contents,
        r0.flow_contents,
        ignore_order=False,
        verbose_level=2
    ) == {}
    # Test we can import from a String in memory
    # Test we can import as new version in existing bucket
    r1 = versioning.import_flow_version(
        bucket_id=fix_flow_serde.bucket.identifier,
        encoded_flow=fix_flow_serde.json,
        flow_id=fix_flow_serde.flow.identifier
    )
    assert isinstance(r1, registry.VersionedFlowSnapshot)
    assert DeepDiff(
        compare_obj.flow_contents,
        r1.flow_contents,
        ignore_order=False,
        verbose_level=2
    ) == {}
    # Test we can also import from a file
    r2 = versioning.import_flow_version(
        bucket_id=fix_flow_serde.bucket.identifier,
        file_path=fix_flow_serde.filepath + '.yaml',
        flow_id=fix_flow_serde.flow.identifier
    )
    assert isinstance(r2, registry.VersionedFlowSnapshot)
    assert DeepDiff(
        compare_obj.flow_contents,
        r2.flow_contents,
        ignore_order=False,
        verbose_level=2
    ) == {}
    # Test import into another bucket as first version
    f_bucket_2 = versioning.create_registry_bucket(
        conftest.test_bucket_name + '_02'
    )
    r3 = versioning.import_flow_version(
        bucket_id=f_bucket_2.identifier,
        encoded_flow=fix_flow_serde.yaml,
        flow_name=conftest.test_cloned_ver_flow_name + '_01'
    )
    assert isinstance(r3, registry.VersionedFlowSnapshot)
    assert DeepDiff(
        compare_obj.flow_contents,
        r3.flow_contents,
        ignore_order=False,
        verbose_level=2
    ) == {}


def test_issue_229(fix_bucket, fix_pg, fix_context):
    # test we can deploy an imported flow, issue 229
    reg_client = versioning.ensure_registry_client(
        name=conftest.test_registry_client_name,
        uri=conftest.ACTIVE_CONFIG['registry_internal_url'],
        description=f"Test Registry Client -> {conftest.ACTIVE_CONFIG['registry_internal_url']}"
    )
    bucket = fix_bucket()
    pg = fix_pg.generate()
    context = fix_context.generate()
    parameters.assign_context_to_process_group(pg, context.id)
    save_flow_ver = versioning.save_flow_ver(
        process_group=pg,
        registry_client=reg_client,
        bucket=bucket,
        flow_name=conftest.test_versioned_flow_name,
        comment='NiPyApi Test',
        desc='NiPyApi Test'
    )
    flow_raw = versioning.get_flow_version(
        bucket_id=bucket.identifier,
        flow_id=save_flow_ver.version_control_information.flow_id,
        export=True
    )
    # Check that it is being exported correctly
    # Older registries (<2.x) are unsupported; proceed unconditionally
    imported_flow = versioning.import_flow_version(
        bucket_id=bucket.identifier,
        encoded_flow=flow_raw,
        flow_name=conftest.test_versioned_flow_name + '_229'
    )
    deployed_flow = versioning.deploy_flow_version(
        parent_id=canvas.get_root_pg_id(),
        location=(0, 0),
        bucket_id=bucket.identifier,
        flow_id=imported_flow.flow.identifier,
        reg_client_id=reg_client.id,
        version=None
    )
    assert isinstance(deployed_flow, nifi.ProcessGroupEntity)


def test_deploy_flow_version(fix_ver_flow):
    r1 = versioning.deploy_flow_version(
        parent_id=canvas.get_root_pg_id(),
        location=(0, 0),
        bucket_id=fix_ver_flow.bucket.identifier,
        flow_id=fix_ver_flow.flow.identifier,
        reg_client_id=fix_ver_flow.client.id,
        version=1
    )
    assert isinstance(r1, nifi.ProcessGroupEntity)
    r2 = versioning.deploy_flow_version(
        parent_id=canvas.get_root_pg_id(),
        location=(0, 0),
        bucket_id=fix_ver_flow.bucket.identifier,
        flow_id=fix_ver_flow.flow.identifier,
        reg_client_id=fix_ver_flow.client.id,
        version=None
    )
    assert isinstance(r2, nifi.ProcessGroupEntity)
    with pytest.raises(ValueError):
        # can't deploy a pg inside itself
        _ = versioning.deploy_flow_version(
            parent_id=fix_ver_flow.pg.id,
            location=(0, 0),
            bucket_id=fix_ver_flow.bucket.identifier,
            flow_id=fix_ver_flow.flow.identifier,
            reg_client_id=fix_ver_flow.client.id,
            version=None
        )


def test_ensure_registry_client_create_new():
    """Test ensure_registry_client creates new client when none exists."""
    client_name = conftest.test_registry_client_name + '_ensure_new'

    # Clean up any existing client (following established pattern)
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Test creating new client
    result = versioning.ensure_registry_client(
        name=client_name,
        uri=conftest.ACTIVE_CONFIG['registry_internal_url'],
        description='Test ensure function'
    )

    assert isinstance(result, nifi.FlowRegistryClientEntity)
    assert result.component.name == client_name
    assert conftest.ACTIVE_CONFIG['registry_internal_url'] in result.component.properties['url']

    # Clean up (following established pattern)
    versioning.delete_registry_client(result)


def test_ensure_registry_client_return_existing():
    """Test ensure_registry_client returns existing client."""
    client_name = conftest.test_registry_client_name + '_ensure_existing'

    # Clean up any existing client
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create initial client
    original = versioning.create_registry_client(
        name=client_name,
        uri=conftest.ACTIVE_CONFIG['registry_internal_url'],
        description='Original client'
    )

    # Test ensure returns existing
    result = versioning.ensure_registry_client(
        name=client_name,
        uri=conftest.ACTIVE_CONFIG['registry_internal_url'],
        description='This should not overwrite'
    )

    assert result.id == original.id
    assert result.component.description == 'Original client'  # Should not be overwritten

    # Clean up
    versioning.delete_registry_client(result)


def test_ensure_registry_client_update_uri_mismatch():
    """Test ensure_registry_client updates when URI differs."""
    client_name = conftest.test_registry_client_name + '_ensure_update'

    # Clean up
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create client with different URI
    original = versioning.create_registry_client(
        name=client_name,
        uri='http://different-registry:18080',
        description='Original with different URI'
    )

    # Ensure with correct URI should update
    result = versioning.ensure_registry_client(
        name=client_name,
        uri=conftest.ACTIVE_CONFIG['registry_internal_url'],
        description='Updated client'
    )

    # Should be different instance (recreated)
    assert result.id != original.id
    assert conftest.ACTIVE_CONFIG['registry_internal_url'] in result.component.properties['url']

    # Clean up
    versioning.delete_registry_client(result)


def test_ensure_registry_bucket_create_new(fix_bucket):
    """Test ensure_registry_bucket creates new bucket when none exists."""
    bucket_name = conftest.test_bucket_name + '_ensure_new'

    # Clean up any existing bucket
    try:
        existing = versioning.get_registry_bucket(bucket_name)
        if existing:
            versioning.delete_registry_bucket(existing)
    except ValueError:
        pass  # Bucket doesn't exist, which is what we want

    # Test creating new bucket
    result = versioning.ensure_registry_bucket(
        name=bucket_name,
        description='Test ensure bucket function'
    )

    assert isinstance(result, registry.Bucket)
    assert result.name == bucket_name
    assert result.description == 'Test ensure bucket function'

    # Clean up
    versioning.delete_registry_bucket(result)


def test_ensure_registry_bucket_return_existing(fix_bucket):
    """Test ensure_registry_bucket returns existing bucket."""
    bucket_name = conftest.test_bucket_name + '_ensure_existing'

    # Clean up
    try:
        existing = versioning.get_registry_bucket(bucket_name)
        if existing:
            versioning.delete_registry_bucket(existing)
    except ValueError:
        pass

    # Create initial bucket
    original = versioning.create_registry_bucket(
        name=bucket_name,
        description='Original bucket'
    )

    # Test ensure returns existing
    result = versioning.ensure_registry_bucket(
        name=bucket_name,
        description='This should not overwrite'
    )

    assert result.identifier == original.identifier
    assert result.description == 'Original bucket'  # Should not be overwritten

    # Clean up
    versioning.delete_registry_bucket(result)


def test_ensure_registry_bucket_race_condition_handling(fix_bucket):
    """Test that ensure_registry_bucket handles race conditions gracefully."""
    bucket_name = conftest.test_bucket_name + '_ensure_race'

    # Clean up
    try:
        existing = versioning.get_registry_bucket(bucket_name)
        if existing:
            versioning.delete_registry_bucket(existing)
    except ValueError:
        pass

    # This test simulates the race condition by creating the bucket
    # and then immediately calling ensure again
    result1 = versioning.ensure_registry_bucket(
        name=bucket_name,
        description='First call'
    )

    # Second call should return the existing bucket, not fail
    result2 = versioning.ensure_registry_bucket(
        name=bucket_name,
        description='Second call'
    )

    assert result1.identifier == result2.identifier

    # Clean up
    versioning.delete_registry_bucket(result1)

