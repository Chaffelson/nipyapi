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


def test_service_login_oidc_validation():
    """Test parameter validation for service_login_oidc (mocked)"""
    # Test registry service rejection
    with pytest.raises(ValueError, match="not supported for Registry"):
        nipyapi.security.service_login_oidc(service='registry')

    # Test invalid service assertion
    with pytest.raises(AssertionError):
        nipyapi.security.service_login_oidc(service='invalid_service')

    # Test missing parameters
    with pytest.raises(ValueError, match="requires username"):
        nipyapi.security.service_login_oidc(
            service='nifi',
            username=None,
            password='test',
            oidc_token_endpoint='http://test.com',
            client_id='test',
            client_secret='test'
        )

    with pytest.raises(ValueError, match="requires username"):
        nipyapi.security.service_login_oidc(
            service='nifi',
            username='test',
            password=None,
            oidc_token_endpoint='http://test.com',
            client_id='test',
            client_secret='test'
        )


@patch('requests.post')
def test_service_login_oidc_success_mocked(mock_post):
    """Test OIDC success path with mocked response"""
    # CRITICAL: Save the original authentication state before test
    current_config = nipyapi.config.nifi_config
    original_api_key = current_config.api_key.copy()
    original_api_key_prefix = current_config.api_key_prefix.copy()

    try:
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_access_token',
            'token_type': 'Bearer',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response

        result = nipyapi.security.service_login_oidc(
            service='nifi',
            username='test_user',
            password='test_pass',
            oidc_token_endpoint='http://localhost:8080/token',
            client_id='test_client',
            client_secret='test_secret'
        )

        assert result is True
        mock_post.assert_called_once()
        # Verify the mock token was actually set
        assert current_config.api_key.get('bearerAuth') == 'test_access_token'

    finally:
        # CRITICAL: Always restore the original authentication state
        current_config.api_key.clear()
        current_config.api_key.update(original_api_key)
        current_config.api_key_prefix.clear()
        current_config.api_key_prefix.update(original_api_key_prefix)


@patch('requests.post')
def test_service_login_oidc_return_token_info_mocked(mock_post):
    """Test OIDC return_token_info parameter with mocked response"""
    # CRITICAL: Save the original authentication state before test
    current_config = nipyapi.config.nifi_config
    original_api_key = current_config.api_key.copy()
    original_api_key_prefix = current_config.api_key_prefix.copy()

    try:
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        token_data = {
            'access_token': 'test_access_token',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': 'test_refresh_token'
        }
        mock_response.json.return_value = token_data
        mock_post.return_value = mock_response

        result = nipyapi.security.service_login_oidc(
            service='nifi',
            username='test_user',
            password='test_pass',
            oidc_token_endpoint='http://localhost:8080/token',
            client_id='test_client',
            client_secret='test_secret',
            return_token_info=True
        )

        assert result == token_data
        assert 'access_token' in result
        assert 'expires_in' in result
        # Verify the mock token was actually set
        assert current_config.api_key.get('bearerAuth') == 'test_access_token'

    finally:
        # CRITICAL: Always restore the original authentication state
        current_config.api_key.clear()
        current_config.api_key.update(original_api_key)
        current_config.api_key_prefix.clear()
        current_config.api_key_prefix.update(original_api_key_prefix)


@patch('requests.post')
def test_service_login_oidc_failure_mocked(mock_post):
    """Test OIDC failure path with mocked response"""
    # Mock failed response
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Invalid credentials"
    mock_post.return_value = mock_response

    # Test with bool_response=True
    result = nipyapi.security.service_login_oidc(
        service='nifi',
        username='bad_user',
        password='bad_pass',
        oidc_token_endpoint='http://localhost:8080/token',
        client_id='test_client',
        client_secret='test_secret',
        bool_response=True
    )

    assert result is False

    # Test with bool_response=False (should raise exception)
    with pytest.raises(ValueError, match="OIDC token acquisition failed"):
        nipyapi.security.service_login_oidc(
            service='nifi',
            username='bad_user',
            password='bad_pass',
            oidc_token_endpoint='http://localhost:8080/token',
            client_id='test_client',
            client_secret='test_secret',
            bool_response=False
        )


@patch('requests.post')
def test_service_login_oidc_exception_handling_mocked(mock_post):
    """Test OIDC exception handling with mocked failure"""
    # Mock exception
    mock_post.side_effect = Exception("Network error")

    # Test with bool_response=True
    result = nipyapi.security.service_login_oidc(
        service='nifi',
        username='test_user',
        password='test_pass',
        oidc_token_endpoint='http://localhost:8080/token',
        client_id='test_client',
        client_secret='test_secret',
        bool_response=True
    )

    assert result is False

    # Test with bool_response=False (should raise exception)
    with pytest.raises(ValueError, match="OIDC authentication error"):
        nipyapi.security.service_login_oidc(
            service='nifi',
            username='test_user',
            password='test_pass',
            oidc_token_endpoint='http://localhost:8080/token',
            client_id='test_client',
            client_secret='test_secret',
            bool_response=False
        )


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


# TODO: Add more edge case tests for policy manipulation functions
# TODO: Add tests for SSL error conditions (wrong password, etc.)
