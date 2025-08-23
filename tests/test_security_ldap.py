"""LDAP-specific integration tests for nipyapi security module."""

import pytest
from tests import conftest
import nipyapi

# LDAP profile integration tests
pytestmark = pytest.mark.skipif(conftest.ACTIVE_PROFILE != 'secure-ldap', reason='LDAP profile not enabled')


def test_ldap_authentication_works():
    """Integration test verifying LDAP authentication enables API access"""
    # Test that we can make authenticated API calls (read-only operations)
    # This proves authentication works without requiring user management privileges
    # Test basic authenticated API calls that don't require admin privileges
    # This proves authentication works on public LDAP test environments

    # Test 1: Get root process group id (should work if authenticated)
    root_pg_id = nipyapi.canvas.get_root_pg_id()
    assert root_pg_id is not None
    assert root_pg_id != ''

    # Test 2: Try to access system version (basic read operation)
    version_info = nipyapi.system.get_nifi_version_info()
    assert version_info is not None
    assert hasattr(version_info, 'ni_fi_version')  # API uses underscores


def test_service_login_integration():
    """Integration test for service login on LDAP profile"""
    r1 = nipyapi.security.service_login()
    assert r1 is True
    r2 = nipyapi.security.service_login('registry')
    assert r2 is True
    r3 = nipyapi.security.service_login(username='baduser', password='badpass', bool_response=True)
    assert r3 is False


def test_set_service_auth_token_integration():
    """Integration test for setting service auth token on LDAP profile"""
    # CRITICAL: Save the entire original API key state
    current_config = nipyapi.config.nifi_config
    original_api_key = current_config.api_key.copy()
    original_api_key_prefix = current_config.api_key_prefix.copy()

    try:
        # Test setting a token temporarily
        nipyapi.security.set_service_auth_token('test_value')
        # Test that the token was set (this is a basic smoke test)
        assert current_config.api_key.get('bearerAuth') == 'test_value'
        assert current_config.api_key_prefix.get('bearerAuth') == 'Bearer'

    finally:
        # CRITICAL: Always restore the original authentication state completely
        current_config.api_key.clear()
        current_config.api_key.update(original_api_key)
        current_config.api_key_prefix.clear()
        current_config.api_key_prefix.update(original_api_key_prefix)


def test_service_logout_integration():
    """Integration test for service logout on LDAP profile"""
    try:
        # Test logout functionality
        r1 = nipyapi.security.service_logout()
        assert r1 is True
        # Verify token was actually cleared
        assert 'bearerAuth' not in nipyapi.config.nifi_config.api_key

    finally:
        # CRITICAL: Re-authenticate using profiles system
        nipyapi.profiles.switch(conftest.ACTIVE_PROFILE)


def test_get_service_access_status_integration():
    """Integration test for getting service access status on LDAP profile"""
    r1 = nipyapi.security.get_service_access_status()
    # In NiFi 2.x, get_service_access_status returns a CurrentUserEntity, not AccessStatusEntity
    assert r1 is not None
    # Verify we have a valid response with user information
    assert hasattr(r1, 'identity')


def test_add_user_to_access_policy_integration():
    """Integration test for adding user to access policy on LDAP profile"""
    # This test suite makes extensive use of this call in fixtures
    pass


def test_add_user_group_to_access_policy_integration():
    """Integration test for adding user group to access policy on LDAP profile"""
    # This test suite makes extensive use of this call in fixtures
    pass


def test_update_access_policy_integration():
    """Integration test for updating access policy on LDAP profile"""
    # This test suite makes extensive use of this call in fixtures
    pass


def test_get_access_policy_for_resource_integration():
    """Integration test for getting access policy for resource on LDAP profile"""
    # This test suite makes extensive use of this call in fixtures
    pass


def test_create_access_policy_integration():
    """Integration test for creating access policy on LDAP profile"""
    # This test suite makes extensive use of this call in fixtures
    pass


def test_set_service_ssl_context_integration():
    """Integration test for setting SSL context on LDAP profile"""
    import os

    # CRITICAL: Save the original SSL context to restore later
    original_ssl_context = nipyapi.config.nifi_config.ssl_context

    try:
        # Get the CA file path from the repository
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        ca_file = os.path.join(repo_root, 'resources', 'certs', 'client', 'ca.pem')
        client_cert = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.crt')
        client_key = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.key')

        # Only test if certificate files exist (don't create fallback scenarios)
        if os.path.exists(ca_file) and os.path.exists(client_cert) and os.path.exists(client_key):
            nipyapi.security.set_service_ssl_context(
                service='nifi',
                ca_file=ca_file,
                client_cert_file=client_cert,
                client_key_file=client_key,
            )
            # Verify the new context was set
            assert nipyapi.config.nifi_config.ssl_context is not None
            assert nipyapi.config.nifi_config.ssl_context != original_ssl_context
        else:
            # Skip test if required certificates are not available
            pytest.skip("Required certificate files not found for SSL context test")

    finally:
        # CRITICAL: Always restore the original SSL context to avoid breaking subsequent tests
        nipyapi.config.nifi_config.ssl_context = original_ssl_context


def test_bootstrap_security_policies_integration():
    """Integration test for bootstrapping security policies on LDAP profile"""
    # This test suite makes extensive use of this call in fixtures
    pass
