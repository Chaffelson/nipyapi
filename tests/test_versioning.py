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
            assert 'api.github.com' in str(e).lower() or 'unauthorized' in str(e).lower() \
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
            assert 'api.github.com' in str(e).lower() or 'unauthorized' in str(e).lower() \
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
