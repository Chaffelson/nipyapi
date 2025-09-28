"""General tests for nipyapi security module (profile-agnostic)."""

import pytest
from unittest.mock import patch, MagicMock
from tests import conftest
import nipyapi

# These tests run on any profile - no profile restriction


def test_list_service_users_validation():
    """Test parameter validation for list_service_users"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.list_service_users(service="invalid_service")


def test_get_service_user_validation():
    """Test parameter validation for get_service_user"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.get_service_user(
            identifier="test",
            service="invalid_service"
        )

    # Test invalid identifier type
    with pytest.raises(AssertionError):
        nipyapi.security.get_service_user(
            identifier=123,  # Should be string
            service="nifi"
        )

    # Test invalid identifier_type
    with pytest.raises(AssertionError):
        nipyapi.security.get_service_user(
            identifier="test",
            identifier_type=123,  # Should be string
            service="nifi"
        )


def test_create_service_user_validation():
    """Test parameter validation for create_service_user"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user(service='invalid_service', identity='test')

    # Test invalid identity type
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user(service='nifi', identity=dict())

    # Test invalid strict type
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user(service='nifi', identity='test', strict=str())


def test_remove_service_user_validation():
    """Test parameter validation for remove_service_user"""
    # Test invalid strict type
    with pytest.raises(AssertionError):
        # Create a mock user object
        mock_user = MagicMock()
        mock_user.id = "test_id"
        mock_user.revision.version = 1
        nipyapi.security.remove_service_user(mock_user, service='nifi', strict=str())


def test_create_service_user_group_validation():
    """Test parameter validation for create_service_user_group"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user_group(
            identity="test_group",
            service="invalid_service"
        )

    # Test invalid identity type
    with pytest.raises(AssertionError):
        nipyapi.security.create_service_user_group(
            identity=123,  # Should be string
            service="nifi"
        )


def test_list_service_user_groups_validation():
    """Test parameter validation for list_service_user_groups"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.list_service_user_groups(service="invalid_service")


def test_get_service_user_group_validation():
    """Test parameter validation for get_service_user_group"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.get_service_user_group(
            identifier="test",
            service="invalid_service"
        )


def test_service_login_validation():
    """Test parameter validation for service_login"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.service_login(service="invalid_service")

    # Test invalid username type
    with pytest.raises(AssertionError):
        nipyapi.security.service_login(service="nifi", username=123)

    # Test invalid password type
    with pytest.raises(AssertionError):
        nipyapi.security.service_login(service="nifi", password=123)




def test_set_service_auth_token_validation():
    """Test parameter validation for set_service_auth_token"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.set_service_auth_token(
            token="test_token",
            service="invalid_service"
        )

    # Test invalid token type
    with pytest.raises(AssertionError):
        nipyapi.security.set_service_auth_token(
            token=123,  # Should be string
            service="nifi"
        )

    # Test invalid token_name type
    with pytest.raises(AssertionError):
        nipyapi.security.set_service_auth_token(
            token="test_token",
            token_name=123,  # Should be string
            service="nifi"
        )


def test_service_logout_validation():
    """Test parameter validation for service_logout"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.service_logout(service="invalid_service")


def test_get_service_access_status_validation():
    """Test parameter validation for get_service_access_status"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.get_service_access_status(service="invalid_service")


def test_create_access_policy_validation():
    """Test parameter validation for create_access_policy"""
    # Test invalid action
    with pytest.raises(AssertionError):
        nipyapi.security.create_access_policy(
            resource="/test",
            action="invalid_action",  # Should be read/write/delete
            service="nifi"
        )

    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.create_access_policy(
            resource="/test",
            action="read",
            service="invalid_service"
        )


def test_set_service_ssl_context_validation():
    """Test parameter validation for set_service_ssl_context"""
    # Test invalid service
    with pytest.raises(AssertionError):
        nipyapi.security.set_service_ssl_context(service="invalid_service")


def test_set_service_ssl_context_file_errors():
    """Test SSL context file error handling"""
    # Test file not found errors
    with pytest.raises(FileNotFoundError, match="Unable to read keyfile"):
        nipyapi.security.set_service_ssl_context(
            service='nifi',
            client_cert_file='/nonexistent/cert.pem',
            client_key_file='/nonexistent/key.pem'
        )


def test_bootstrap_security_policies_validation():
    """Test parameter validation for bootstrap_security_policies"""
    # Test invalid service list
    with pytest.raises(AssertionError):
        nipyapi.security.bootstrap_security_policies(
            service=["invalid_service"]
        )


class TestEnsureSSLContext:
    """Test ensure_ssl_context convenience function."""

    @patch('nipyapi.canvas.get_controller')
    @patch('nipyapi.security.create_ssl_context_controller_service')
    @patch('nipyapi.canvas.schedule_controller')
    def test_ensure_ssl_context_create_new(self, mock_schedule, mock_create, mock_get):
        """Test ensure_ssl_context creates new SSL context when none exists."""
        # Mock no existing SSL context found
        mock_get.return_value = None

        # Mock SSL context creation
        mock_ssl_context = MagicMock()
        mock_ssl_context.id = 'test-ssl-context-id'
        mock_create.return_value = mock_ssl_context

        # Test creating new SSL context
        result = nipyapi.security.ensure_ssl_context(
            parent_pg=MagicMock(),
            name='test-ssl-context',
            keystore_file='/test/keystore.p12',
            keystore_password='password',
            truststore_file='/test/truststore.p12',
            truststore_password='password'
        )

        assert result == mock_ssl_context
        mock_create.assert_called_once()
        mock_schedule.assert_called_once_with(mock_ssl_context, scheduled=True, refresh=True)

    @patch('nipyapi.canvas.get_controller')
    @patch('nipyapi.canvas.schedule_controller')
    def test_ensure_ssl_context_return_existing(self, mock_schedule, mock_get):
        """Test ensure_ssl_context returns existing SSL context."""
        # Mock existing SSL context found
        mock_existing = MagicMock()
        mock_existing.id = 'existing-ssl-context-id'
        mock_get.return_value = mock_existing

        # Test returning existing SSL context
        result = nipyapi.security.ensure_ssl_context(
            parent_pg=MagicMock(),
            name='existing-ssl-context',
            keystore_file='/test/keystore.p12',
            keystore_password='password',
            truststore_file='/test/truststore.p12',
            truststore_password='password'
        )

        assert result == mock_existing
        # Should ensure it's scheduled but not create new one
        mock_schedule.assert_called_once_with(mock_existing, scheduled=True, refresh=True)

    @patch('nipyapi.canvas.get_controller')
    @patch('nipyapi.security.create_ssl_context_controller_service')
    @patch('nipyapi.canvas.schedule_controller')
    def test_ensure_ssl_context_race_condition(self, mock_schedule, mock_create, mock_get):
        """Test ensure_ssl_context handles race condition gracefully."""
        # Mock race condition: service created between check and creation
        mock_get.side_effect = [None, MagicMock()]  # First call finds none, second finds existing

        # Mock creation failure due to duplicate
        mock_create.side_effect = Exception("already exists")

        # Should handle race condition and return existing service
        result = nipyapi.security.ensure_ssl_context(
            parent_pg=MagicMock(),
            name='race-ssl-context',
            keystore_file='/test/keystore.p12',
            keystore_password='password',
            truststore_file='/test/truststore.p12',
            truststore_password='password'
        )

        assert result is not None
        # Should have tried to create but then handled the race condition
        mock_create.assert_called_once()


def test_set_ssl_warning_suppression():
    """Test SSL warning suppression control"""
    # Test enabling suppression
    nipyapi.security.set_ssl_warning_suppression(True)
    # No exception should be raised

    # Test disabling suppression (note: urllib3 limitation means we can't re-enable)
    nipyapi.security.set_ssl_warning_suppression(False)
    # No exception should be raised

    # Test invalid parameter
    with pytest.raises(AssertionError, match="suppress_warnings must be boolean"):
        nipyapi.security.set_ssl_warning_suppression("invalid")


@patch('nipyapi.security.service_logout')
def test_reset_service_connections_both_services(mock_logout):
    """Test resetting connections for both services"""
    # Store original API clients
    original_nifi_client = nipyapi.config.nifi_config.api_client
    original_registry_client = nipyapi.config.registry_config.api_client

    try:
        # Set mock clients to verify they get reset
        nipyapi.config.nifi_config.api_client = MagicMock()
        nipyapi.config.registry_config.api_client = MagicMock()

        # Test reset all services (default)
        nipyapi.security.reset_service_connections()

        # Should have called logout for both services
        assert mock_logout.call_count == 2
        mock_logout.assert_any_call('nifi')
        mock_logout.assert_any_call('registry')

        # Should have reset both API clients
        assert nipyapi.config.nifi_config.api_client is None
        assert nipyapi.config.registry_config.api_client is None

    finally:
        # Restore original clients
        nipyapi.config.nifi_config.api_client = original_nifi_client
        nipyapi.config.registry_config.api_client = original_registry_client


@patch('nipyapi.security.service_logout')
def test_reset_service_connections_single_service(mock_logout):
    """Test resetting connections for a single service"""
    # Store original API clients
    original_nifi_client = nipyapi.config.nifi_config.api_client
    original_registry_client = nipyapi.config.registry_config.api_client

    try:
        # Set mock clients to verify selective reset
        nipyapi.config.nifi_config.api_client = MagicMock()
        nipyapi.config.registry_config.api_client = MagicMock()

        # Test reset only NiFi service
        nipyapi.security.reset_service_connections(service='nifi')

        # Should have called logout only for NiFi
        mock_logout.assert_called_once_with('nifi')

        # Should have reset only NiFi API client
        assert nipyapi.config.nifi_config.api_client is None
        assert nipyapi.config.registry_config.api_client is not None  # Should remain

    finally:
        # Restore original clients
        nipyapi.config.nifi_config.api_client = original_nifi_client
        nipyapi.config.registry_config.api_client = original_registry_client


def test_reset_service_connections_invalid_service():
    """Test reset with invalid service parameter"""
    with pytest.raises(ValueError, match="Invalid service 'invalid'"):
        nipyapi.security.reset_service_connections(service='invalid')


@patch('nipyapi.security.service_logout')
def test_reset_service_connections_logout_error_handling(mock_logout):
    """Test that reset continues even if logout fails"""
    # Store original API clients
    original_nifi_client = nipyapi.config.nifi_config.api_client

    try:
        # Set mock client
        nipyapi.config.nifi_config.api_client = MagicMock()

        # Make logout raise an exception
        mock_logout.side_effect = Exception("Logout failed")

        # Should not raise exception despite logout failure
        nipyapi.security.reset_service_connections(service='nifi')

        # Should still reset the API client
        assert nipyapi.config.nifi_config.api_client is None

    finally:
        # Restore original client
        nipyapi.config.nifi_config.api_client = original_nifi_client


# SSL Configuration Tests

def test_simplified_ssl_approach():
    """Test simplified SSL approach: verify_ssl=True/False controls everything"""
    from nipyapi.nifi.rest import RESTClientObject

    try:
        # Test verify_ssl=False: should use CERT_NONE with no ca_certs
        nipyapi.config.nifi_config.host = 'https://localhost:8443/nifi-api'
        nipyapi.config.nifi_config.verify_ssl = False

        client = RESTClientObject()
        assert client.pool_manager.connection_pool_kw.get("cert_reqs") == 0  # ssl.CERT_NONE
        assert client.pool_manager.connection_pool_kw.get("ca_certs") is None

        # Test verify_ssl=True: should use CERT_REQUIRED with ca_certs
        nipyapi.config.nifi_config.verify_ssl = True

        client = RESTClientObject()
        assert client.pool_manager.connection_pool_kw.get("cert_reqs") == 2  # ssl.CERT_REQUIRED
        assert client.pool_manager.connection_pool_kw.get("ca_certs") is not None

    finally:
        # CRITICAL: Always restore configuration using profiles system to avoid breaking subsequent tests
        nipyapi.profiles.switch(conftest.ACTIVE_PROFILE)


# TODO: Add more edge case tests for policy manipulation functions
# TODO: Add tests for SSL error conditions (wrong password, etc.)
