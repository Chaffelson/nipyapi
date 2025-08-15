"""Tests for nipyapi security module."""

import pytest
from tests import conftest
import nipyapi

# Tells pytest to skip this module of security testing if not enabled.
pytestmark = pytest.mark.skipif(not conftest.TEST_LDAP, reason='LDAP profile not enabled')

# Useful for manual testing
# if conftest.test_ldap:
#     test_host = nipyapi.config.default_host
#     nipyapi.utils.set_endpoint('https://' + test_host + ':18443/nifi-registry-api', True, True)
#     nipyapi.utils.set_endpoint('https://' + test_host + ':9443/nifi-api', True, True)


def test_list_service_users():
    # This test suite makes extensive use of this call in fixtures
    pass


def test_get_service_user():
    # This test suite makes extensive use of this call in fixtures
    pass


def test_create_service_user():
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user(service='bob', identity='pie')
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user(service='nifi', identity=dict())
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user(service='nifi', identity='pie', strict=str())
    r1 = nipyapi.security.create_service_user(conftest.test_basename)
    assert isinstance(r1, nipyapi.nifi.UserEntity)
    r2 = nipyapi.security.create_service_user(conftest.test_basename, 'registry')
    assert isinstance(r2, nipyapi.registry.User)
    with pytest.raises(ValueError):
        nipyapi.security.create_service_user(conftest.test_basename, strict=True)
    r3 = nipyapi.security.create_service_user(conftest.test_basename, strict=False)
    assert isinstance(r3, nipyapi.nifi.UserEntity)
    assert r3.component.identity == conftest.test_basename


def test_remove_service_user(fix_users):
    n_user, r_user = fix_users()
    r1 = nipyapi.security.remove_service_user(n_user)
    assert nipyapi.security.get_service_user(n_user.component.identity) is None
    assert isinstance(r1, nipyapi.nifi.UserEntity)
    r2 = nipyapi.security.remove_service_user(r_user, 'registry')
    assert nipyapi.security.get_service_user(r_user.identity, service='registry') is None
    assert isinstance(r2, nipyapi.registry.User)
    with pytest.raises(ValueError):
        nipyapi.security.remove_service_user(n_user)
    with pytest.raises(ValueError):
        nipyapi.security.remove_service_user(r_user, 'registry')
    r3 = nipyapi.security.remove_service_user(n_user, strict=False)
    assert r3 is None
    r4 = nipyapi.security.remove_service_user(r_user, 'registry', strict=False)
    assert r4 is None


def test_create_service_user_group(fix_users, fix_user_groups):
    # fix_user_groups provides the cleanup after testing
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user_group(identity=dict())
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user_group(
            conftest.test_user_group_name,
            service='bob'
        )
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user_group(
            conftest.test_user_group_name,
            service='nifi',
            users=['bob']
        )
    n_user, r_user = fix_users()
    r1 = nipyapi.security.create_service_user_group(
        conftest.test_user_group_name,
        service='nifi',
        users=[n_user],
        strict=True
    )
    assert isinstance(r1, nipyapi.nifi.UserGroupEntity)
    r2 = nipyapi.security.create_service_user_group(
        conftest.test_user_group_name,
        service='registry',
        users=[r_user],
        strict=True
    )
    assert isinstance(r2, nipyapi.registry.UserGroup)
    with pytest.raises(ValueError):
        nipyapi.security.create_service_user_group(
            conftest.test_user_group_name,
            service='nifi',
            users=[n_user],
            strict=True
        )
    with pytest.raises(ValueError):
        nipyapi.security.create_service_user_group(
            conftest.test_user_group_name,
            service='registry',
            users=[r_user],
            strict=True
        )
    r3 = nipyapi.security.create_service_user_group(
        conftest.test_user_group_name,
        service='nifi',
        users=[n_user],
        strict=False
    )
    assert isinstance(r3, nipyapi.nifi.UserGroupEntity)
    r4 = nipyapi.security.create_service_user_group(
        conftest.test_user_group_name,
        service='registry',
        users=[r_user],
        strict=False
    )
    assert isinstance(r4, nipyapi.registry.UserGroup)


def test_list_service_user_groups(fix_user_groups):
    n_group, r_group = fix_user_groups()
    with pytest.raises(AssertionError):
        nipyapi.security.list_service_user_groups(service='bob')
    r1 = nipyapi.security.list_service_user_groups()
    assert isinstance(r1[0], nipyapi.nifi.UserGroupEntity)
    assert n_group.id in [x.id for x in r1]
    r2 = nipyapi.security.list_service_user_groups('registry')
    assert isinstance(r2[0], nipyapi.registry.UserGroup)
    assert r_group.identifier in [x.identifier for x in r2]


def test_get_service_user_group(fix_user_groups):
    n_group, r_group = fix_user_groups()
    with pytest.raises(AssertionError):
        nipyapi.security.get_service_user_group(identifier=dict())
    with pytest.raises(AssertionError):
        nipyapi.security.get_service_user_group(
            identifier='bob',
            identifier_type=dict())
    with pytest.raises(AssertionError):
        nipyapi.security.get_service_user_group(
            identifier='bob',
            identifier_type='id',
            service='bob')
    r1 = nipyapi.security.get_service_user_group(conftest.test_user_group_name)
    assert isinstance(r1, nipyapi.nifi.UserGroupEntity)
    assert r1.id == n_group.id
    r2 = nipyapi.security.get_service_user_group(
        identifier=conftest.test_user_group_name,
        service='registry'
    )
    assert isinstance(r2, nipyapi.registry.UserGroup)
    assert r2.identifier == r_group.identifier


def test_remove_service_user_group(fix_user_groups):
    n_group, r_group = fix_user_groups()
    r1 = nipyapi.security.remove_service_user_group(n_group)
    assert nipyapi.security.get_service_user_group(n_group.component.identity) is None
    assert isinstance(r1, nipyapi.nifi.UserGroupEntity)
    r2 = nipyapi.security.remove_service_user_group(r_group, 'registry')
    assert nipyapi.security.get_service_user_group(r_group.identity, service='registry') is None
    assert isinstance(r2, nipyapi.registry.UserGroup)
    with pytest.raises(ValueError):
        nipyapi.security.remove_service_user_group(n_group)
    with pytest.raises(ValueError):
        nipyapi.security.remove_service_user_group(r_group, 'registry')
    r3 = nipyapi.security.remove_service_user_group(n_group, strict=False)
    assert r3 is None
    r4 = nipyapi.security.remove_service_user_group(r_group, 'registry', strict=False)
    assert r4 is None


def test_service_login():
    with pytest.raises(AssertionError):
        nipyapi.security.service_login(service='bob')
    with pytest.raises(AssertionError):
        nipyapi.security.service_login(username=dict())
    with pytest.raises(AssertionError):
        nipyapi.security.service_login(password=dict())
    with pytest.raises(AssertionError):
        nipyapi.security.service_login(bool_response='bob')
    # This test suite makes extensive use of this call in fixtures


def test_set_service_auth_token():
    # This test suite makes extensive use of this call in fixtures
    pass


def test_service_logout():
    # This test suite makes extensive use of this call in fixtures
    pass


def test_get_service_access_status():
    # This test suite makes extensive use of this call in fixtures
    pass


def test_add_user_to_access_policy():
    # ~ user = nipyapi.security.create_service_user(
    # ~ identity='testuser',
    # ~ service='nifi'
    # ~ )

    # ~ assert isinstance(user, nipyapi.nifi.UserEntity)
    # ~ policy = nipyapi.security.add_user_to_access_policy(
    # ~ user=user,
    # ~ service='nifi'
    # ~ )
    # ~ assert isinstance(policy, nipyapi.nifi.AccessPolicyEntity)
    pass


def test_add_user_group_to_access_policy():
    # ~ user_group = nipyapi.security.create_service_user_group(
    # ~ identity='testuser_group',
    # ~ service='nifi'
    # ~ )
    # ~ assert isinstance(user_group, nipyapi.nifi.UserGroupEntity)
    # ~ policy = nipyapi.security.add_user_group_to_access_policy(
    # ~ user_group=user_group,
    # ~ service='nifi'
    # ~ )
    # ~ assert isinstance(policy, nipyapi.nifi.AccessPolicyEntity)
    pass


def test_update_access_policy():
    pass


def test_get_access_policy_for_resource():
    # This test suite makes extensive use of this call in fixtures
    pass


def test_create_access_policy():
    # This test suite makes extensive use of this call in fixtures
    pass


def test_set_service_ssl_context():
    """Test setting SSL context with different purposes"""
    import ssl
    from nipyapi import config

    # Test default behavior (no purpose specified)
    # Use repo-local test CA if configured; default demo paths are deprecated
    ca = config.nifi_config.ssl_ca_cert or config.registry_config.ssl_ca_cert
    if not ca:
        import os
        ca_candidate = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'certs', 'client', 'ca.pem')
        ca = ca_candidate if os.path.exists(ca_candidate) else None
    nipyapi.security.set_service_ssl_context(service='nifi', ca_file=ca)
    assert isinstance(nipyapi.config.nifi_config.ssl_context, ssl.SSLContext)

    # Test with explicit SERVER_AUTH purpose
    nipyapi.security.set_service_ssl_context(service='nifi', ca_file=ca, purpose=ssl.Purpose.SERVER_AUTH)
    assert isinstance(nipyapi.config.nifi_config.ssl_context, ssl.SSLContext)

    # Test with CLIENT_AUTH purpose
    nipyapi.security.set_service_ssl_context(service='nifi', ca_file=ca, purpose=ssl.Purpose.CLIENT_AUTH)
    assert isinstance(nipyapi.config.nifi_config.ssl_context, ssl.SSLContext)

    # Test with full client cert configuration
    # Full client cert config (use test certs if present)
    import os
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    client_crt = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.crt')
    client_key = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.key')
    if os.path.exists(client_crt) and os.path.exists(client_key):
        nipyapi.security.set_service_ssl_context(
            service='nifi',
            ca_file=ca,
            client_cert_file=client_crt,
            client_key_file=client_key,
        )
        assert nipyapi.config.nifi_config.ssl_context is not None


def test_bootstrap_security_policies():
    # This test suite makes extensive use of this call in fixtures
    pass

# TODO: Test adding users to existing set of users and ensuring no clobber
