"""LDAP-specific integration tests for nipyapi security module."""

import pytest
from tests import conftest
import nipyapi

# LDAP profile integration tests
pytestmark = pytest.mark.skipif(not conftest.TEST_LDAP, reason='LDAP profile not enabled')

# Useful for manual testing
# if conftest.test_ldap:
#     test_host = nipyapi.config.default_host
#     nipyapi.utils.set_endpoint('https://' + test_host + ':18443/nifi-registry-api', True, True)
#     nipyapi.utils.set_endpoint('https://' + test_host + ':9443/nifi-api', True, True)


def test_create_service_user_integration(fix_users):
    """Integration test for creating service users on LDAP profile"""
    n_user, r_user = fix_users()
    assert isinstance(n_user, nipyapi.nifi.UserEntity)
    assert isinstance(r_user, nipyapi.registry.User)


def test_remove_service_user_integration(fix_users):
    """Integration test for removing service users on LDAP profile"""
    n_user, r_user = fix_users()
    r1 = nipyapi.security.remove_service_user(n_user)
    assert nipyapi.security.get_service_user(n_user.component.identity) is None
    assert isinstance(r1, nipyapi.nifi.UserEntity)
    r2 = nipyapi.security.remove_service_user(r_user, 'registry')
    assert nipyapi.security.get_service_user(r_user.identity, service='registry') is None
    assert isinstance(r2, nipyapi.registry.User)
    # test remove non-existent user with strict=False
    r3 = nipyapi.security.remove_service_user(n_user, strict=False)
    assert r3 is None
    # test remove non-existent user with strict=True
    with pytest.raises(ValueError):
        nipyapi.security.remove_service_user(n_user, strict=True)


def test_create_service_user_group_integration(fix_user_groups):
    """Integration test for creating service user groups on LDAP profile"""
    # fix_user_groups already creates users internally, so we don't need fix_users
    n_user_group, r_user_group = fix_user_groups()
    # Test that groups were created
    assert isinstance(n_user_group, nipyapi.nifi.UserGroupEntity)
    assert isinstance(r_user_group, nipyapi.registry.UserGroup)
    # Test that groups have users (they were added by the fixture)
    assert len(n_user_group.component.users) > 0
    assert len(r_user_group.users) > 0
    
    # Test that we can retrieve the created groups
    retrieved_nifi_group = nipyapi.security.get_service_user_group(
        n_user_group.component.identity, service="nifi"
    )
    assert retrieved_nifi_group.id == n_user_group.id
    
    retrieved_registry_group = nipyapi.security.get_service_user_group(
        r_user_group.identity, service="registry"
    )
    assert retrieved_registry_group.identifier == r_user_group.identifier


def test_list_service_user_groups_integration(fix_user_groups):
    """Integration test for listing service user groups on LDAP profile"""
    n_user_group, r_user_group = fix_user_groups()
    r1 = nipyapi.security.list_service_user_groups()
    assert isinstance(r1, list)
    # Compare by ID instead of direct object comparison
    group_ids = [group.id for group in r1]
    assert n_user_group.id in group_ids
    
    r2 = nipyapi.security.list_service_user_groups('registry')
    assert isinstance(r2, list)
    # Compare by identifier for registry groups
    registry_group_identifiers = [group.identifier for group in r2]
    assert r_user_group.identifier in registry_group_identifiers


def test_get_service_user_group_integration(fix_user_groups):
    """Integration test for getting service user groups on LDAP profile"""
    n_user_group, r_user_group = fix_user_groups()
    r1 = nipyapi.security.get_service_user_group(n_user_group.component.identity)
    assert isinstance(r1, nipyapi.nifi.UserGroupEntity)
    assert r1.component.identity == n_user_group.component.identity
    r2 = nipyapi.security.get_service_user_group(
        r_user_group.identity, service='registry'
    )
    assert isinstance(r2, nipyapi.registry.UserGroup)
    assert r2.identity == r_user_group.identity
    # Test non-matching search
    r3 = nipyapi.security.get_service_user_group('NoSuchGroup')
    assert r3 is None


def test_remove_service_user_group_integration(fix_user_groups):
    """Integration test for removing service user groups on LDAP profile"""
    n_user_group, r_user_group = fix_user_groups()
    r1 = nipyapi.security.remove_service_user_group(n_user_group)
    assert nipyapi.security.get_service_user_group(n_user_group.component.identity) is None
    assert isinstance(r1, nipyapi.nifi.UserGroupEntity)
    r2 = nipyapi.security.remove_service_user_group(r_user_group, 'registry')
    assert nipyapi.security.get_service_user_group(r_user_group.identity, service='registry') is None
    assert isinstance(r2, nipyapi.registry.UserGroup)
    # test remove non-existent group with strict=False
    r3 = nipyapi.security.remove_service_user_group(n_user_group, strict=False)
    assert r3 is None
    # test remove non-existent group with strict=True
    with pytest.raises(ValueError):
        nipyapi.security.remove_service_user_group(n_user_group, strict=True)


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
    # CRITICAL: Save the original authentication state before logout
    current_config = nipyapi.config.nifi_config
    original_api_key = current_config.api_key.copy()
    original_api_key_prefix = current_config.api_key_prefix.copy()
    
    try:
        # Test logout functionality
        r1 = nipyapi.security.service_logout()
        assert r1 is True
        # Verify token was actually cleared
        assert 'bearerAuth' not in current_config.api_key
        
    finally:
        # CRITICAL: Restore authentication for subsequent tests
        current_config.api_key.clear()
        current_config.api_key.update(original_api_key)
        current_config.api_key_prefix.clear()
        current_config.api_key_prefix.update(original_api_key_prefix)


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
