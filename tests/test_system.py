"""Tests for `nipyapi` package."""

import pytest
from tests import conftest
from nipyapi import system, config, nifi
from nipyapi.nifi import models as nifi_models


def test_get_system_diagnostics():
    """Test system diagnostics retrieval and structure validation."""
    result = system.get_system_diagnostics()

    # Verify return type and structure
    assert isinstance(result, nifi_models.system_diagnostics_entity.SystemDiagnosticsEntity)
    assert hasattr(result, 'system_diagnostics')
    assert result.system_diagnostics is not None

    # Verify aggregate snapshot data structure
    snapshot = result.system_diagnostics.aggregate_snapshot
    assert snapshot is not None
    assert hasattr(snapshot, 'version_info')
    assert hasattr(snapshot, 'available_processors')
    assert hasattr(snapshot, 'total_threads')

    # Verify version info is embedded and accessible
    version_info = snapshot.version_info
    assert version_info is not None
    assert hasattr(version_info, 'ni_fi_version')
    assert version_info.ni_fi_version is not None
    assert len(version_info.ni_fi_version) > 0


def test_get_nifi_version_info():
    """Test NiFi version info retrieval with fallback logic."""
    result = system.get_nifi_version_info()

    # Verify return type and required fields
    assert isinstance(result, nifi_models.version_info_dto.VersionInfoDTO)
    result_dict = result.to_dict()
    assert "ni_fi_version" in result_dict.keys()
    assert result.ni_fi_version is not None
    assert len(result.ni_fi_version) > 0

    # Verify version format (should be something like "2.5.0")
    version_parts = result.ni_fi_version.split('.')
    assert len(version_parts) >= 2  # At least major.minor
    assert all(part.isdigit() for part in version_parts)


@conftest.requires_registry
def test_get_registry_version_info():
    """Test Registry version info retrieval."""
    result = system.get_registry_version_info()

    # Should return a simple string version
    assert isinstance(result, str)
    assert len(result) > 0

    # Verify version format (should be something like "2.5.0")
    version_parts = result.split('.')
    assert len(version_parts) >= 2  # At least major.minor


def test_get_cluster_single_user_mode():
    """Test cluster info in single-user mode (should fail expectedly)."""
    # In single-user mode, cluster endpoints should fail with specific error
    with pytest.raises(ValueError) as exc_info:
        system.get_cluster()

    # Should get the expected cluster error message
    error_msg = str(exc_info.value)
    assert "Only a node connected to a cluster can process the request" in error_msg


def test_get_node_single_user_mode():
    """Test node info in single-user mode (should fail expectedly)."""
    # In single-user mode, node endpoints should fail with specific error
    with pytest.raises(ValueError) as exc_info:
        system.get_node("any-node-id")

    # Should get the expected cluster error message
    error_msg = str(exc_info.value)
    assert "Only a node connected to a cluster can process the request" in error_msg


def test_get_node_invalid_id():
    """Test node retrieval with invalid node ID."""
    # Even with invalid ID, should get cluster error in single-user mode
    with pytest.raises(ValueError) as exc_info:
        system.get_node("invalid-node-id-123")

    error_msg = str(exc_info.value)
    assert "Only a node connected to a cluster can process the request" in error_msg


def test_get_cluster_availability():
    """Test cluster status check logic (tests the conditional logic)."""
    # This tests the function call path without depending on cluster setup
    try:
        result = system.get_cluster()
        # If we get here, we're in a cluster - result should be ClusterEntity
        assert isinstance(result, nifi_models.cluster_entity.ClusterEntity)
        assert hasattr(result, 'cluster')
    except ValueError as e:
        # Expected in single-user mode
        assert "Only a node connected to a cluster can process the request" in str(e)


def test_system_diagnostics_data_integrity():
    """Test that system diagnostics contains expected data types."""
    result = system.get_system_diagnostics()
    snapshot = result.system_diagnostics.aggregate_snapshot

    # Test numeric fields are numeric
    assert isinstance(snapshot.available_processors, int)
    assert snapshot.available_processors > 0

    assert isinstance(snapshot.total_threads, int)
    assert snapshot.total_threads > 0

    # Test memory fields exist and are reasonable
    assert hasattr(snapshot, 'used_heap_bytes')
    assert hasattr(snapshot, 'max_heap_bytes')
    assert isinstance(snapshot.used_heap_bytes, int)
    assert isinstance(snapshot.max_heap_bytes, int)
    assert snapshot.used_heap_bytes > 0
    assert snapshot.max_heap_bytes > 0
    assert snapshot.used_heap_bytes <= snapshot.max_heap_bytes


def test_nifi_version_fallback_logic():
    """Test the fallback logic when about endpoint returns None values."""
    # This test ensures coverage of the fallback from about -> diagnostics
    # The function should work even if about endpoint has limited data
    result = system.get_nifi_version_info()

    # Should always return a valid VersionInfoDTO even with fallback
    assert isinstance(result, nifi_models.version_info_dto.VersionInfoDTO)
    assert result.ni_fi_version is not None

    # Verify the version info structure
    version_dict = result.to_dict()
    required_fields = ['ni_fi_version', 'build_tag', 'build_branch',
                      'build_revision', 'build_timestamp', 'java_vendor',
                      'java_version', 'os_architecture', 'os_name', 'os_version']

    for field in required_fields:
        assert field in version_dict


@conftest.requires_registry
def test_registry_connection_and_response():
    """Test Registry connectivity and response format."""
    result = system.get_registry_version_info()

    # Test that we get a meaningful version string
    assert isinstance(result, str)
    assert len(result.strip()) > 0

    # Version should not be an error message
    assert "error" not in result.lower()
    assert "exception" not in result.lower()
    assert "404" not in result

    # Should match semantic version pattern
    import re
    version_pattern = r'^\d+\.\d+(\.\d+)?'
    assert re.match(version_pattern, result), f"Version '{result}' doesn't match expected pattern"
