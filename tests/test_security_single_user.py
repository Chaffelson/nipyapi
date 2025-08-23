"""Single-user profile specific tests for nipyapi security module."""

import pytest
from tests import conftest
import nipyapi

# Single-user profile specific tests
pytestmark = pytest.mark.skipif(conftest.ACTIVE_PROFILE != 'single-user', reason='Single-user profile not enabled')


def test_service_auth_token_single_user():
    """Test token management on single-user profile"""
    # First, ensure we have a proper authentication token by doing a login
    # The conftest setup should have already authenticated, but let's verify
    login_result = nipyapi.security.service_login(service="nifi", bool_response=True)
    if not login_result:
        # If login fails, try with explicit credentials
        login_result = nipyapi.security.service_login(
            service="nifi",
            username=conftest.ACTIVE_CONFIG['nifi_user'],
            password=conftest.ACTIVE_CONFIG['nifi_pass'],
            bool_response=True
        )

    # Test getting access status on single-user profile (should work with proper auth)
    status = nipyapi.security.get_service_access_status(service="nifi", bool_response=True)
    # When successful, get_service_access_status returns the access status object, not a boolean
    # bool_response=True only affects error handling (returns False instead of raising)
    assert status is not False  # False indicates failure, anything else indicates success

    # Test that we can manually set a token
    # Set a test token temporarily
    nipyapi.security.set_service_auth_token(token="test_token", service="nifi")

    try:
        # Test logout on single-user profile (this should clear the token)
        result = nipyapi.security.service_logout(service="nifi")
        assert result is True
    finally:
        # CRITICAL: Re-authenticate using profiles system
        nipyapi.profiles.switch(conftest.ACTIVE_PROFILE)


def test_single_user_basic_auth_integration():
    """Test that basic auth works properly on single-user profile"""
    # Single-user profile should support username/password authentication
    # This test verifies the auth works (through conftest.py setup)

    try:
        # This should work with the single-user credentials
        status = nipyapi.security.get_service_access_status(service="nifi")
        assert status is not None
    except Exception as e:
        pytest.fail(f"Single-user basic auth failed: {e}")


def test_single_user_registry_http_integration():
    """Test that Registry works over HTTP in single-user profile"""
    # Single-user profile typically has Registry over HTTP, not HTTPS

    try:
        # Registry should be accessible over HTTP in single-user mode
        status = nipyapi.security.get_service_access_status(
            service="registry",
            bool_response=True
        )
        # When successful, returns the service status object, not a boolean
        assert status is not False  # False indicates failure, anything else indicates success
    except Exception as e:
        pytest.fail(f"Registry HTTP access failed in single-user profile: {e}")


def test_single_user_ssl_context_nifi():
    """Test SSL context configuration for NiFi in single-user profile"""
    # Single-user profile uses HTTPS for NiFi but with simpler SSL setup
    import os

    # CRITICAL: Save the original SSL context to restore later
    original_ssl_context = nipyapi.config.nifi_config.ssl_context

    try:
        # Test that we can set SSL context without client certs
        # (single-user typically doesn't require client certificates)
        # Get the CA file path from the repository
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        ca_file = os.path.join(repo_root, 'resources', 'certs', 'client', 'ca.pem')

        if os.path.exists(ca_file):
            nipyapi.security.set_service_ssl_context(
                service='nifi',
                ca_file=ca_file,
                check_hostname=False  # Common in development setups
            )
            assert nipyapi.config.nifi_config.ssl_context is not None
            assert nipyapi.config.nifi_config.ssl_context != original_ssl_context
        else:
            # Skip test if required certificates are not available
            pytest.skip("Required certificate files not found for SSL context test")

    except Exception as e:
        pytest.fail(f"SSL context setup failed for single-user NiFi: {e}")
    finally:
        # CRITICAL: Always restore the original SSL context
        nipyapi.config.nifi_config.ssl_context = original_ssl_context


def test_single_user_no_complex_policies():
    """Test that single-user profile doesn't require complex policy setup"""
    # Single-user profile should work without extensive policy bootstrapping

    try:
        # In single-user mode, NiFi typically doesn't internally manage users/groups/policies
        # This is expected behavior - single-user mode uses simpler authentication
        users = nipyapi.security.list_service_users(service="nifi")
        assert isinstance(users, list)

    except ValueError as e:
        # Expected: Single-user mode doesn't internally manage users/policies
        if "not configured to internally manage users, groups, or policies" in str(e):
            # This is the expected behavior for single-user mode
            pass
        else:
            # If we get other permission errors, the single-user setup might be wrong
            if "Access is denied" in str(e) or "Forbidden" in str(e):
                pytest.fail(f"Single-user profile has unexpected permission restrictions: {e}")
            raise

    # Should be able to access basic system info regardless
    status = nipyapi.security.get_service_access_status(service="nifi")
    assert status is not None
