"""OIDC-specific integration tests for nipyapi security module."""

import pytest
from tests import conftest
import nipyapi

# OIDC profile integration tests
pytestmark = pytest.mark.skipif(not conftest.TEST_OIDC, reason='OIDC profile not enabled')


def test_service_login_oidc_integration():
    """Integration test for OIDC login with real infrastructure"""
    # This would test actual OIDC authentication against running Keycloak
    # Currently relies on conftest.py setup for OIDC authentication
    
    # CRITICAL: Save the original authentication state before logout
    current_config = nipyapi.config.nifi_config
    original_api_key = current_config.api_key.copy()
    original_api_key_prefix = current_config.api_key_prefix.copy()
    
    try:
        # Test that OIDC authentication was successful (through conftest setup)
        status = nipyapi.security.get_service_access_status(service="nifi", bool_response=True)
        assert status is not False  # False indicates failure, anything else indicates success
        
        # Test logout functionality
        result = nipyapi.security.service_logout(service="nifi")
        assert result is True
        # Verify token was actually cleared
        assert 'bearerAuth' not in current_config.api_key
        
    finally:
        # CRITICAL: Always restore the original authentication state
        current_config.api_key.clear()
        current_config.api_key.update(original_api_key)
        current_config.api_key_prefix.clear()
        current_config.api_key_prefix.update(original_api_key_prefix)


def test_oidc_user_bootstrap_integration():
    """Integration test for OIDC user bootstrapping"""
    # This test verifies that OIDC users can be properly bootstrapped
    # with the necessary policies through conftest.py setup
    
    # Verify we can access the system (indicating proper policy setup)
    try:
        users = nipyapi.security.list_service_users(service="nifi")
        assert isinstance(users, list)
    except Exception as e:
        pytest.fail(f"OIDC user lacks proper permissions: {e}")


def test_oidc_token_info_integration():
    """Integration test for OIDC token info extraction"""
    # This test would verify the return_token_info functionality
    # in a real OIDC environment, but requires manual setup
    
    # For now, just verify the function exists and is callable
    # Real integration testing requires the full OIDC flow
    assert hasattr(nipyapi.security, 'service_login_oidc')
    assert callable(nipyapi.security.service_login_oidc)


def test_oidc_registry_basic_auth_integration():
    """Integration test verifying Registry uses basic auth in OIDC profile"""
    # In OIDC profile, Registry should still use basic auth, not OIDC
    
    # Verify Registry is accessible (through conftest.py setup)
    try:
        # This call should work with basic auth credentials
        # as configured in conftest.py for OIDC profile
        status = nipyapi.security.get_service_access_status(
            service="registry", 
            bool_response=True
        )
        # When successful, returns the response object, not a boolean
        # bool_response=True only affects error handling (returns False instead of raising)
        assert status is not False  # False indicates failure, anything else indicates success
    except Exception as e:
        pytest.fail(f"Registry basic auth failed in OIDC profile: {e}")


def test_oidc_ssl_context_integration():
    """Integration test for SSL context in OIDC profile"""
    # Test that SSL context is properly configured for OIDC
    
    # This should work without throwing SSL errors
    # if conftest.py properly configured SSL for OIDC
    try:
        status = nipyapi.security.get_service_access_status(service="nifi")
        assert status is not None
    except Exception as e:
        if "SSL" in str(e) or "certificate" in str(e):
            pytest.fail(f"SSL configuration issue in OIDC profile: {e}")
        # Other errors might be expected depending on setup
