"""Tests for `nipyapi` versioning package - NiFi-only tests.

These tests work with NiFi alone and do not require a NiFi Registry service.
They cover registry client management (NiFi API), Git-based registry clients
(GitHub, GitLab), and process group export/import functionality.

Registry-specific tests are in test_versioning_registry.py.
"""

import pytest
from tests import conftest
from nipyapi import nifi, versioning, canvas


def test_list_registry_clients():
    r = versioning.list_registry_clients()
    assert isinstance(r, nifi.FlowRegistryClientsEntity)


def test_get_registry_client():
    # This test requires at least one registry client to exist
    # Create a temporary one for testing
    client_name = conftest.test_registry_client_name + '_get_test'

    # Clean up any existing
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create a GitHub client (doesn't require Registry service)
    created = versioning.create_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        description='Test client for get test',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'test-owner',
            'Repository Name': 'test-repo',
            'Authentication Type': 'NONE',
            'Default Branch': 'main'
        }
    )

    # Test get by name
    r1 = versioning.get_registry_client(client_name)
    assert isinstance(r1, nifi.FlowRegistryClientEntity)
    assert r1.component.name == client_name

    # Test get by id
    r2 = versioning.get_registry_client(r1.id, 'id')
    assert r2.id == r1.id

    # Test invalid identifier type
    with pytest.raises(ValueError):
        _ = versioning.get_registry_client('', 'NotIDorName')

    # Clean up
    versioning.delete_registry_client(created)


def test_update_flow_ver():
    # This function is tested in test_complex_template_versioning
    pass


def test_list_flow_versions():
    # TODO: Implement test
    pass


def test_create_registry_client_with_properties():
    """Test create_registry_client with properties parameter for Git-based registries."""
    client_name = conftest.test_registry_client_name + '_github_properties'

    # Clean up any existing client
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create GitHub client with properties in one call
    result = versioning.create_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        description='Test GitHub client',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'test-owner',
            'Repository Name': 'test-repo',
            'Authentication Type': 'NONE',
            'Default Branch': 'main'
        }
    )

    assert isinstance(result, nifi.FlowRegistryClientEntity)
    assert result.component.name == client_name
    assert result.component.type == 'org.apache.nifi.github.GitHubFlowRegistryClient'
    assert result.component.properties['Repository Owner'] == 'test-owner'
    assert result.component.properties['Repository Name'] == 'test-repo'
    assert result.component.properties['Default Branch'] == 'main'

    # Clean up
    versioning.delete_registry_client(result)


def test_update_registry_client():
    """Test update_registry_client updates properties on existing client."""
    client_name = conftest.test_registry_client_name + '_update_test'

    # Clean up any existing client
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create initial client
    initial = versioning.create_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        description='Initial description',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'test-owner',
            'Repository Name': 'test-repo',
            'Authentication Type': 'NONE',
            'Default Branch': 'main'
        }
    )

    assert initial.component.properties['Default Branch'] == 'main'

    # Update the branch property
    updated = versioning.update_registry_client(
        initial,
        properties={'Default Branch': 'feature-branch'}
    )

    assert isinstance(updated, nifi.FlowRegistryClientEntity)
    assert updated.component.properties['Default Branch'] == 'feature-branch'
    # Other properties should be preserved
    assert updated.component.properties['Repository Owner'] == 'test-owner'
    assert updated.component.properties['Repository Name'] == 'test-repo'

    # Clean up
    versioning.delete_registry_client(updated)


def test_ensure_registry_client_updates_existing():
    """Test ensure_registry_client updates existing client when properties provided."""
    client_name = conftest.test_registry_client_name + '_ensure_update'

    # Clean up any existing client
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create initial client via ensure
    initial = versioning.ensure_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'test-owner',
            'Repository Name': 'test-repo',
            'Authentication Type': 'NONE',
            'Default Branch': 'main'
        }
    )

    assert initial.component.properties['Default Branch'] == 'main'

    # Call ensure again with different properties - should update
    updated = versioning.ensure_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        properties={
            'Default Branch': 'develop'
        }
    )

    assert updated.component.properties['Default Branch'] == 'develop'
    # Client ID should be the same (updated, not recreated)
    assert updated.id == initial.id

    # Clean up
    versioning.delete_registry_client(updated)


def test_export_process_group_definition(fix_pg, fix_proc):
    """Test export_process_group_definition function"""
    # Create a process group with a processor inside it
    pg = fix_pg.generate()
    proc = fix_proc.generate(parent_pg=pg)

    # Test export to string (JSON)
    json_export = versioning.export_process_group_definition(pg, mode='json')
    assert isinstance(json_export, str)
    assert len(json_export) > 0
    assert '"flowContents"' in json_export

    # Verify it contains the processor
    assert proc.component.name in json_export

    # Test export to string (YAML)
    yaml_export = versioning.export_process_group_definition(pg, mode='yaml')
    assert isinstance(yaml_export, str)
    assert len(yaml_export) > 0
    # YAML should have different format
    assert yaml_export != json_export

    # Test invalid mode
    with pytest.raises(AssertionError):
        versioning.export_process_group_definition(pg, mode='xml')

    # Test invalid process_group type
    with pytest.raises(AssertionError):
        versioning.export_process_group_definition("not a pg", mode='json')


def test_import_process_group_definition(fix_pg, fix_proc):
    """Test import_process_group_definition function"""
    # Create a process group with a processor inside it
    pg = fix_pg.generate()
    proc = fix_proc.generate(parent_pg=pg)

    # Export it first
    flow_json = versioning.export_process_group_definition(pg, mode='json')
    assert len(flow_json) > 0

    # Import to a new location
    root_pg = canvas.get_process_group(canvas.get_root_pg_id(), 'id')
    imported_pg = versioning.import_process_group_definition(
        parent_pg=root_pg,
        flow_definition=flow_json,
        position=(1000, 1000)
    )

    # Verify the import
    assert isinstance(imported_pg, nifi.ProcessGroupEntity)
    assert imported_pg.component.position.x == 1000.0
    assert imported_pg.component.position.y == 1000.0

    # Verify it contains processors
    processors = [p for p in canvas.list_all_processors()
                  if p.component.parent_group_id == imported_pg.id]
    assert len(processors) > 0

    # Cleanup
    canvas.schedule_process_group(imported_pg.id, scheduled=False)
    canvas.delete_process_group(imported_pg, force=True)


# =============================================================================
# Git-based Registry Functions Tests
# =============================================================================


def test_list_git_registry_buckets():
    """Test list_git_registry_buckets returns expected structure."""
    client_name = conftest.test_registry_client_name + '_git_buckets'

    # Clean up any existing client
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create a GitHub client (with NONE auth for structure testing)
    client = versioning.create_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        description='Test Git registry client',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'test-owner',
            'Repository Name': 'test-repo',
            'Authentication Type': 'NONE',
            'Default Branch': 'main'
        }
    )

    try:
        # Test the function call works (may fail to connect, but API call should work)
        try:
            result = versioning.list_git_registry_buckets(client.id)
            # If we get here, check the structure
            assert hasattr(result, 'buckets')
        except ValueError as e:
            # Expected to fail with NONE auth - that's OK for structure test
            assert 'unauthorized' in str(e).lower() \
                or 'bad credentials' in str(e).lower() or 'not found' in str(e).lower()
    finally:
        versioning.delete_registry_client(client)


def test_list_git_registry_flows():
    """Test list_git_registry_flows returns expected structure."""
    client_name = conftest.test_registry_client_name + '_git_flows'

    # Clean up any existing client
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create a GitHub client
    client = versioning.create_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        description='Test Git registry client',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'test-owner',
            'Repository Name': 'test-repo',
            'Authentication Type': 'NONE',
            'Default Branch': 'main'
        }
    )

    try:
        # Test the function call works
        try:
            result = versioning.list_git_registry_flows(client.id, 'test-bucket')
            assert hasattr(result, 'versioned_flows')
        except ValueError as e:
            # Expected to fail with NONE auth
            assert 'unauthorized' in str(e).lower() \
                or 'bad credentials' in str(e).lower() or 'not found' in str(e).lower()
    finally:
        versioning.delete_registry_client(client)


def test_get_git_registry_bucket_not_found():
    """Test get_git_registry_bucket returns None when bucket not found."""
    client_name = conftest.test_registry_client_name + '_git_get_bucket'

    # Clean up any existing client
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create a GitHub client
    client = versioning.create_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        description='Test Git registry client',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'test-owner',
            'Repository Name': 'test-repo',
            'Authentication Type': 'NONE',
            'Default Branch': 'main'
        }
    )

    try:
        # Test the function - may fail to connect with NONE auth
        result = versioning.get_git_registry_bucket(
            client.id, 'nonexistent-bucket', greedy=False
        )
        assert result is None
    except ValueError:
        # Expected to fail with NONE auth
        pass
    finally:
        versioning.delete_registry_client(client)


def test_get_git_registry_flow_not_found():
    """Test get_git_registry_flow returns None when flow not found."""
    client_name = conftest.test_registry_client_name + '_git_get_flow'

    # Clean up any existing client
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create a GitHub client
    client = versioning.create_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        description='Test Git registry client',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'test-owner',
            'Repository Name': 'test-repo',
            'Authentication Type': 'NONE',
            'Default Branch': 'main'
        }
    )

    try:
        # Test the function with greedy=False for exact match
        try:
            result = versioning.get_git_registry_flow(
                client.id, 'test-bucket', 'nonexistent-flow', greedy=False
            )
            assert result is None
        except ValueError:
            # Expected to fail with NONE auth
            pass
    finally:
        versioning.delete_registry_client(client)


def test_list_git_registry_flow_versions():
    """Test list_git_registry_flow_versions calls list_flow_versions correctly."""
    client_name = conftest.test_registry_client_name + '_git_versions'

    # Clean up any existing client
    existing_clients = versioning.list_registry_clients().registries
    for client in existing_clients:
        if client_name in client.component.name:
            versioning.delete_registry_client(client)

    # Create a GitHub client
    client = versioning.create_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        description='Test Git registry client',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'test-owner',
            'Repository Name': 'test-repo',
            'Authentication Type': 'NONE',
            'Default Branch': 'main'
        }
    )

    try:
        # Test the function
        try:
            result = versioning.list_git_registry_flow_versions(
                client.id, 'test-bucket', 'test-flow'
            )
            assert hasattr(result, 'versioned_flow_snapshot_metadata_set')
        except ValueError:
            # Expected to fail with NONE auth
            pass
    finally:
        versioning.delete_registry_client(client)


# =============================================================================
# update_git_flow_ver Tests
# =============================================================================
# These tests require a GitHub PAT via GH_REGISTRY_TOKEN environment variable.
# They use fixtures from conftest.py: fix_git_reg_client, fix_deployed_git_flow
# Test fixtures are in the nipyapi-actions repository (tests/flows/cicd-demo-flow).


def test_update_git_flow_ver_specific_version(fix_deployed_git_flow):
    """Test changing to a specific version by SHA."""
    vci = versioning.get_version_info(fix_deployed_git_flow.pg)
    initial_version = vci.version_control_information.version

    # Switch to the other version
    target = conftest.GIT_REGISTRY_VERSION_V1 \
        if initial_version == conftest.GIT_REGISTRY_VERSION_LATEST \
        else conftest.GIT_REGISTRY_VERSION_LATEST

    result = versioning.update_git_flow_ver(fix_deployed_git_flow.pg, target)

    assert result is not None
    new_vci = versioning.get_version_info(fix_deployed_git_flow.pg)
    assert new_vci.version_control_information.version == target


def test_update_git_flow_ver_to_latest(fix_deployed_git_flow):
    """Test changing to latest version (None target)."""
    # First ensure we're not at latest
    versioning.update_git_flow_ver(
        fix_deployed_git_flow.pg, conftest.GIT_REGISTRY_VERSION_V1
    )

    # Now change to latest
    result = versioning.update_git_flow_ver(fix_deployed_git_flow.pg, None)

    new_vci = versioning.get_version_info(fix_deployed_git_flow.pg)
    assert new_vci.version_control_information.version == conftest.GIT_REGISTRY_VERSION_LATEST


def test_update_git_flow_ver_same_version_noop(fix_deployed_git_flow):
    """Test that changing to current version is a no-op."""
    vci = versioning.get_version_info(fix_deployed_git_flow.pg)
    current_version = vci.version_control_information.version

    result = versioning.update_git_flow_ver(fix_deployed_git_flow.pg, current_version)

    # Should return VCI (not update request) indicating no-op
    assert isinstance(result, nifi.VersionControlInformationEntity)


def test_update_git_flow_ver_invalid_version(fix_deployed_git_flow):
    """Test that invalid version raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        versioning.update_git_flow_ver(
            fix_deployed_git_flow.pg, 'invalid-sha-not-exists'
        )

    assert 'not found' in str(exc_info.value).lower()
    assert 'Available versions' in str(exc_info.value)


def test_update_git_flow_ver_unversioned_pg(fix_pg):
    """Test that unversioned process group raises ValueError."""
    test_pg = fix_pg.generate(suffix='_git_unversioned')

    with pytest.raises(ValueError) as exc_info:
        versioning.update_git_flow_ver(test_pg)

    assert 'not under version control' in str(exc_info.value).lower()


def test_update_git_flow_ver_locally_modified_requires_revert(fix_deployed_git_flow):
    """Test that version change requires revert when PG has local modifications.

    NiFi enforces that local changes must be reverted before switching versions.
    This test verifies that behavior and shows the proper workflow.
    """
    # Add a processor to create local modifications
    proc_type = canvas.get_processor_type('GenerateFlowFile')
    canvas.create_processor(
        parent_pg=fix_deployed_git_flow.pg,
        processor=proc_type,
        location=(100, 100),
        name=conftest.test_basename + '_local_mod'
    )

    # Verify state is LOCALLY_MODIFIED
    vci = versioning.get_version_info(fix_deployed_git_flow.pg)
    assert vci.version_control_information.state == 'LOCALLY_MODIFIED'

    # Determine target version
    current_version = vci.version_control_information.version
    target = conftest.GIT_REGISTRY_VERSION_V1 \
        if current_version == conftest.GIT_REGISTRY_VERSION_LATEST \
        else conftest.GIT_REGISTRY_VERSION_LATEST

    # Attempt to change version - should fail due to local modifications
    with pytest.raises(ValueError) as exc_info:
        versioning.update_git_flow_ver(fix_deployed_git_flow.pg, target)

    assert 'modified' in str(exc_info.value).lower()
    assert 'revert' in str(exc_info.value).lower()

    # Now revert and try again - should work
    # Use wait=True to ensure revert completes before proceeding
    revert_result = versioning.revert_flow_ver(fix_deployed_git_flow.pg, wait=True)
    assert isinstance(revert_result, nifi.VersionControlInformationEntity)
    assert revert_result.version_control_information.state == 'UP_TO_DATE'

    # Get fresh PG reference after revert completes
    refreshed_pg = canvas.get_process_group(fix_deployed_git_flow.pg.id, 'id')

    # Version change should now work
    result = versioning.update_git_flow_ver(refreshed_pg, target)

    # Verify version changed (state will be STALE if switched to older version,
    # or UP_TO_DATE if switched to latest - both are valid post-update states)
    final_pg = canvas.get_process_group(fix_deployed_git_flow.pg.id, 'id')
    new_vci = versioning.get_version_info(final_pg)
    assert new_vci.version_control_information.version == target
    assert new_vci.version_control_information.state in ('UP_TO_DATE', 'STALE')


# =============================================================================
# revert_flow_ver Tests (with wait parameter)
# =============================================================================


def test_revert_flow_ver_wait_true(fix_deployed_git_flow):
    """Test revert_flow_ver with wait=True returns final state."""
    # Make a local modification
    proc_type = canvas.get_processor_type('GenerateFlowFile')
    canvas.create_processor(
        parent_pg=fix_deployed_git_flow.pg,
        processor=proc_type,
        location=(150, 150),
        name=conftest.test_basename + '_revert_test'
    )

    # Verify state is LOCALLY_MODIFIED
    vci = versioning.get_version_info(fix_deployed_git_flow.pg)
    assert vci.version_control_information.state == 'LOCALLY_MODIFIED'

    # Revert with wait=True
    result = versioning.revert_flow_ver(fix_deployed_git_flow.pg, wait=True)

    # Should return VCI with UP_TO_DATE state
    assert isinstance(result, nifi.VersionControlInformationEntity)
    assert result.version_control_information.state == 'UP_TO_DATE'


def test_revert_flow_ver_wait_false(fix_deployed_git_flow):
    """Test revert_flow_ver with wait=False returns request entity immediately."""
    # Make a local modification
    proc_type = canvas.get_processor_type('GenerateFlowFile')
    canvas.create_processor(
        parent_pg=fix_deployed_git_flow.pg,
        processor=proc_type,
        location=(150, 150),
        name=conftest.test_basename + '_revert_nowait'
    )

    # Revert with wait=False (default)
    result = versioning.revert_flow_ver(fix_deployed_git_flow.pg, wait=False)

    # Should return the request entity (async)
    assert isinstance(result, nifi.VersionedFlowUpdateRequestEntity)
    assert result.request is not None


def test_revert_flow_ver_already_up_to_date(fix_deployed_git_flow):
    """Test revert on flow that's already UP_TO_DATE."""
    # Ensure flow is UP_TO_DATE
    vci = versioning.get_version_info(fix_deployed_git_flow.pg)
    assert vci.version_control_information.state == 'UP_TO_DATE'

    # Revert should still work (effectively a no-op)
    result = versioning.revert_flow_ver(fix_deployed_git_flow.pg, wait=True)

    # Should return VCI still at UP_TO_DATE
    assert isinstance(result, nifi.VersionControlInformationEntity)
    assert result.version_control_information.state == 'UP_TO_DATE'
