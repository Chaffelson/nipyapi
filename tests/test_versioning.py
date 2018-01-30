#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from tests import conftest
from nipyapi import registry, config, nifi, versioning, canvas


def test_create_registry_client():
    # First remove any leftover test client connections
    [versioning.delete_registry_client(li) for
     li in versioning.list_registry_clients().registries
     if conftest.test_registry_client_name in li.component.name
     ]
    r = versioning.create_registry_client(
        name=conftest.test_registry_client_name,
        uri=conftest.test_docker_registry_endpoint,
        description='a test connection'
    )
    assert isinstance(r, nifi.RegistryClientEntity)
    # test duplicate catch result
    with pytest.raises(ValueError):
        _ = versioning.create_registry_client(
            name=conftest.test_registry_client_name,
            uri=conftest.test_docker_registry_endpoint,
            description='who cares?'
        )


def test_list_registry_clients(fixture_reg_client):
    r = versioning.list_registry_clients()
    assert isinstance(r, nifi.RegistryClientsEntity)


def test_delete_registry_client(fixture_reg_client):
    r = versioning.delete_registry_client(fixture_reg_client)
    assert isinstance(r, nifi.RegistryClientEntity)
    assert r.uri is None
    assert r.component.name == conftest.test_registry_client_name
    # TODO Add test for when a PG is attached to the client


def test_get_registry_client(fixture_reg_client):
    r1 = versioning.get_registry_client(conftest.test_registry_client_name)
    assert isinstance(r1, nifi.RegistryClientEntity)
    assert r1.component.name == conftest.test_registry_client_name
    r2 = versioning.get_registry_client(r1.id, 'id')
    assert r2.id == r1.id


def test_list_registry_buckets(fixture_registry_bucket):
    b1 = fixture_registry_bucket.generate()
    r = versioning.list_registry_buckets()
    assert isinstance(r, list)
    assert len(r) >= 1


def test_create_registry_bucket(fixture_reg_client):
    r = versioning.create_registry_bucket(conftest.test_bucket_name)
    assert isinstance(r, registry.Bucket)
    assert r.name == conftest.test_bucket_name
    # Bucket names are unique
    with pytest.raises(ValueError) as v:
        _ = versioning.create_registry_bucket(conftest.test_bucket_name)


def test_delete_registry_bucket(fixture_registry_bucket):
    b1, c1 = fixture_registry_bucket.generate()
    r = versioning.delete_registry_bucket(b1)
    assert r.identifier == b1.identifier
    with pytest.raises(ValueError):
        _ = versioning.get_registry_bucket(b1.identifier, 'id')


def test_get_registry_bucket(fixture_registry_bucket):
    b1, c1 = fixture_registry_bucket.generate()
    r1 = versioning.get_registry_bucket(conftest.test_bucket_name)
    assert r1.name == conftest.test_bucket_name
    r2 = versioning.get_registry_bucket(r1.identifier, 'id')
    assert r2.name == r1.name
    with pytest.raises(ValueError):
        _ = versioning.get_registry_bucket('Irrelevant', 'Invalid')
    r3 = versioning.get_registry_bucket('NonExistantProbably')
    assert r3 is None


def test_save_flow_ver(fixture_registry_bucket, fixture_pg, fixture_processor):
    test_pg = fixture_pg.generate()
    test_b, test_rc = fixture_registry_bucket.generate()
    r1 = versioning.save_flow_ver(
        process_group=test_pg,
        registry_client=test_rc,
        bucket=test_b,
        flow_name=conftest.test_versioned_flow_name,
        comment='a test comment',
        desc='a test description'
    )
    assert isinstance(r1, nifi.VersionControlInformationEntity)
    # Next we validate you can't duplicate a flow name in a bucket
    with pytest.raises(ValueError):
        _ = versioning.save_flow_ver(
            process_group=test_pg,
            registry_client=test_rc,
            bucket=test_b,
            flow_name=conftest.test_versioned_flow_name,
            comment='NiPyApi Test',
            desc='NiPyApi Test'
        )
    # Add a processor, refresh status, and save a new version
    fixture_processor.generate(parent_pg=test_pg)
    test_pg = canvas.get_process_group(test_pg.id, 'id')
    r2 = versioning.save_flow_ver(
        process_group=test_pg,
        registry_client=test_rc,
        bucket=test_b,
        flow_id=r1.version_control_information.flow_id,
        comment='a test comment'
    )
    assert isinstance(r2, nifi.VersionControlInformationEntity)
    assert r2.version_control_information.version > \
           r1.version_control_information.version


def test_stop_flow_ver(fixture_versioned_flow):
    test_rc, test_rb, test_pg, test_p, test_vf = fixture_versioned_flow
    r1 = versioning.stop_flow_ver(test_pg)
    assert isinstance(r1, nifi.VersionControlInformationEntity)
    assert r1.version_control_information is None
    with pytest.raises(ValueError,
                       match='not currently under Version Control'):
        _ = versioning.stop_flow_ver(test_pg)


def test_revert_flow_ver(fixture_versioned_flow):
    test_rc, test_rb, test_pg, test_p, test_vf = fixture_versioned_flow
    r1 = versioning.revert_flow_ver(test_pg)
    assert isinstance(r1, nifi.VersionedFlowUpdateRequestEntity)
    # TODO: Add Tests for flows with data loss on reversion


def test_list_flows_in_bucket(fixture_versioned_flow):
    test_rc, test_rb, test_pg, test_p, test_vf = fixture_versioned_flow
    r1 = versioning.list_flows_in_bucket(test_rb.identifier)
    assert isinstance(r1, list)
    assert isinstance(r1[0], registry.VersionedFlow)
    with pytest.raises(ValueError, match='Bucket does not exist'):
        _ = versioning.list_flows_in_bucket('NiPyApi-FakeNews')


def test_get_flow_in_bucket(fixture_versioned_flow):
    test_rc, test_rb, test_pg, test_p, test_vf = fixture_versioned_flow
    r1 = versioning.get_flow_in_bucket(
        test_rb.identifier,
        test_vf.version_control_information.flow_id,
        'id'
    )
    assert isinstance(r1, registry.VersionedFlow)
    assert r1.identifier == test_vf.version_control_information.flow_id
    with pytest.raises(ValueError, match='Versioned flow does not exist'):
        _ = versioning.get_flow_in_bucket(test_rb.identifier, 'fakenews', 'id')


def test_get_latest_flow_ver(fixture_versioned_flow):
    test_rc, test_rb, test_pg, test_p, test_vf_info = fixture_versioned_flow
    r1 = versioning.get_latest_flow_ver(
        test_rb.identifier,
        test_vf_info.version_control_information.flow_id
    )
    assert isinstance(r1, registry.VersionedFlowSnapshot)
    with pytest.raises(ValueError, match='Versioned flow does not exist'):
        _ = versioning.get_latest_flow_ver(test_rb.identifier, 'fakenews')


def test_update_flow_ver():
    # This function is more complicated than expected
    # Will implement in a future version
    pass


def test_get_version_info(fixture_versioned_flow):
    test_rc, test_rb, test_pg, test_p, test_vf = fixture_versioned_flow
    r1 = versioning.get_version_info(test_pg)
    assert isinstance(r1, nifi.VersionControlInformationEntity)


def test_create_flow(fixture_versioned_flow):
    test_rc, test_rb, test_pg, test_p, test_vf_info = fixture_versioned_flow
    r1 = versioning.create_flow(
        bucket_id=test_rb.identifier,
        flow_name=conftest.test_cloned_ver_flow_name,
    )
    assert isinstance(r1, registry.VersionedFlow)
    assert r1.name == conftest.test_cloned_ver_flow_name
    # test duplicate behavior
    with pytest.raises(ValueError):
        _ = versioning.create_flow(
            bucket_id=test_rb.identifier,
            flow_name=conftest.test_cloned_ver_flow_name,
        )


def test_create_flow_version(fixture_versioned_flow):
    test_rc, test_rb, test_pg, test_p, test_vf_info = fixture_versioned_flow
    new_ver_stub = versioning.create_flow(
        bucket_id=test_rb.identifier,
        flow_name=conftest.test_cloned_ver_flow_name,
    )
    ver_flow_snapshot = versioning.get_latest_flow_ver(
        test_rb.identifier, test_vf_info.version_control_information.flow_id
    )
    r1 = versioning.create_flow_version(
        bucket_id=test_rb.identifier,
        flow=new_ver_stub,
        flow_snapshot=ver_flow_snapshot
    )
    assert isinstance(r1, registry.VersionedFlowSnapshot)

