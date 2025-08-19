"""mTLS-specific integration tests for nipyapi security module."""

import pytest
from tests import conftest
import nipyapi

# mTLS profile integration tests
pytestmark = pytest.mark.skipif(not conftest.TEST_MTLS, reason='mTLS profile not enabled')


def test_mtls_client_certificate_auth():
    """Test that mTLS client certificate authentication works"""
    # mTLS profile should authenticate using client certificates
    
    try:
        # This should work with client certificate auth (through conftest.py setup)
        status = nipyapi.security.get_service_access_status(service="nifi")
        assert status is not None
    except Exception as e:
        if "SSL" in str(e) or "certificate" in str(e):
            pytest.fail(f"mTLS client certificate authentication failed: {e}")
        raise


def test_mtls_ssl_context_with_client_certs():
    """Test SSL context configuration with client certificates for mTLS"""
    import os
    
    # CRITICAL: Save the original SSL contexts for BOTH services
    original_nifi_ssl_context = nipyapi.config.nifi_config.ssl_context
    original_registry_ssl_context = nipyapi.config.registry_config.ssl_context
    
    try:
        # Get the certificate file paths from the repository
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        ca_file = os.path.join(repo_root, 'resources', 'certs', 'client', 'ca.pem')
        client_cert = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.crt')
        client_key = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.key')
        
        # Only test if ALL required certificate files exist
        if all(os.path.exists(f) for f in [ca_file, client_cert, client_key]):
            # Test NiFi SSL context
            nipyapi.security.set_service_ssl_context(
                service='nifi',
                ca_file=ca_file,
                client_cert_file=client_cert,
                client_key_file=client_key,
            )
            assert nipyapi.config.nifi_config.ssl_context is not None
            assert nipyapi.config.nifi_config.ssl_context != original_nifi_ssl_context
            
            # Test Registry SSL context
            nipyapi.security.set_service_ssl_context(
                service='registry',
                ca_file=ca_file,
                client_cert_file=client_cert,
                client_key_file=client_key,
            )
            assert nipyapi.config.registry_config.ssl_context is not None
            assert nipyapi.config.registry_config.ssl_context != original_registry_ssl_context
        else:
            # Skip test if required certificates are not available
            pytest.skip("Required certificate files not found for mTLS SSL context test")
            
    except Exception as e:
        pytest.fail(f"mTLS SSL context setup failed: {e}")
    finally:
        # CRITICAL: Always restore the original SSL contexts for BOTH services
        nipyapi.config.nifi_config.ssl_context = original_nifi_ssl_context
        nipyapi.config.registry_config.ssl_context = original_registry_ssl_context


def test_mtls_registry_https():
    """Test that Registry works over HTTPS in mTLS profile"""
    # mTLS profile should have both NiFi and Registry over HTTPS
    
    try:
        status = nipyapi.security.get_service_access_status(
            service="registry", 
            bool_response=True
        )
        # When successful, returns the response object, not a boolean
        # bool_response=True only affects error handling (returns False instead of raising)
        assert status is not False  # False indicates failure, anything else indicates success
    except Exception as e:
        pytest.fail(f"Registry HTTPS access failed in mTLS profile: {e}")


def test_mtls_no_username_password():
    """Test that mTLS doesn't rely on username/password auth"""
    # mTLS profile should authenticate purely via certificates
    # This is more of a configuration verification test
    
    # The fact that we can access services without explicit username/password
    # login calls indicates mTLS is working
    try:
        users = nipyapi.security.list_service_users(service="nifi")
        assert isinstance(users, list)
    except Exception as e:
        if "Unauthorized" in str(e) or "Authentication" in str(e):
            pytest.fail(f"mTLS certificate authentication appears to have failed: {e}")
        raise


def test_mtls_policy_management():
    """Test that policy management works in mTLS environment"""
    # mTLS environments often have more complex policy requirements
    
    try:
        # Should be able to access policies (indicates proper cert-based permissions)
        # This is typically set up through conftest.py bootstrapping
        users = nipyapi.security.list_service_users(service="nifi")
        assert isinstance(users, list)
        
        # Should be able to check access status
        status = nipyapi.security.get_service_access_status(service="nifi")
        assert status is not None
        
    except Exception as e:
        if "Access is denied" in str(e) or "Forbidden" in str(e):
            pytest.fail(f"mTLS user lacks required policies: {e}")
        raise
