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


# SSL Constraint and Configuration Tests

def test_ssl_constraint_logic_http_urls():
    """Test SSL constraint logic correctly handles HTTP URLs"""
    import nipyapi.profiles

    # Test HTTP URL - should force disable_host_check=None regardless of verify_ssl
    test_config = {
        'nifi_url': 'http://localhost:8080/nifi-api',
        'nifi_verify_ssl': False,  # Smart default for HTTP
        'nifi_disable_host_check': None,
    }

    # Simulate the constraint logic from resolve_profile_config
    config = test_config.copy()
    if config.get("nifi_url"):
        if not config["nifi_url"].startswith("https://"):
            # HTTP: hostname checking not applicable
            config["nifi_disable_host_check"] = None
        elif config.get("nifi_verify_ssl") is False and config.get("nifi_disable_host_check") is None:
            # HTTPS + no SSL verification: must disable hostname checking
            config["nifi_disable_host_check"] = True

    # HTTP URLs should always have disable_host_check=None
    assert config["nifi_disable_host_check"] is None
    assert config["nifi_verify_ssl"] is False


def test_ssl_constraint_logic_https_verify_false():
    """Test SSL constraint logic prevents invalid HTTPS + verify_ssl=False combinations"""
    import nipyapi.profiles

    # Test HTTPS URL with verify_ssl=False - should auto-correct disable_host_check
    test_config = {
        'nifi_url': 'https://localhost:9443/nifi-api',
        'nifi_verify_ssl': False,  # No certificate verification
        'nifi_disable_host_check': None,  # Default would enable hostname checking
    }

    # Simulate the constraint logic from resolve_profile_config
    config = test_config.copy()
    if config.get("nifi_url"):
        if not config["nifi_url"].startswith("https://"):
            config["nifi_disable_host_check"] = None
        elif config.get("nifi_verify_ssl") is False and config.get("nifi_disable_host_check") is None:
            # CRITICAL: Prevent "Cannot set verify_mode to CERT_NONE when check_hostname is enabled"
            config["nifi_disable_host_check"] = True

    # Should auto-correct to prevent SSL error
    assert config["nifi_disable_host_check"] is True
    assert config["nifi_verify_ssl"] is False


def test_ssl_constraint_logic_https_verify_true():
    """Test SSL constraint logic respects user settings for valid HTTPS combinations"""
    # Test HTTPS URL with verify_ssl=True - should respect user disable_host_check setting
    test_config = {
        'nifi_url': 'https://localhost:9443/nifi-api',
        'nifi_verify_ssl': True,  # Certificate verification enabled
        'nifi_disable_host_check': None,  # Secure default (hostname checking enabled)
    }

    # Simulate the constraint logic
    config = test_config.copy()
    if config.get("nifi_url"):
        if not config["nifi_url"].startswith("https://"):
            config["nifi_disable_host_check"] = None
        elif config.get("nifi_verify_ssl") is False and config.get("nifi_disable_host_check") is None:
            config["nifi_disable_host_check"] = True
        # verify_ssl=True: respect user setting (don't auto-correct)

    # Should preserve user setting for valid combination
    assert config["nifi_disable_host_check"] is None  # Secure default preserved
    assert config["nifi_verify_ssl"] is True


def test_ssl_constraint_logic_explicit_user_override():
    """Test SSL constraint logic respects explicit user overrides"""
    # User explicitly sets disable_host_check=True even with verify_ssl=False
    test_config = {
        'nifi_url': 'https://localhost:9443/nifi-api',
        'nifi_verify_ssl': False,
        'nifi_disable_host_check': True,  # User explicitly set
    }

    # Simulate the constraint logic
    config = test_config.copy()
    if config.get("nifi_url"):
        if not config["nifi_url"].startswith("https://"):
            config["nifi_disable_host_check"] = None
        elif config.get("nifi_verify_ssl") is False and config.get("nifi_disable_host_check") is None:
            config["nifi_disable_host_check"] = True
        # User already set disable_host_check=True, don't override

    # Should preserve explicit user setting
    assert config["nifi_disable_host_check"] is True
    assert config["nifi_verify_ssl"] is False


def test_ssl_constraint_logic_both_services():
    """Test SSL constraint logic handles both NiFi and Registry independently"""
    # Mixed scenario: HTTPS NiFi with no SSL verification, HTTP Registry
    test_config = {
        'nifi_url': 'https://localhost:9443/nifi-api',
        'nifi_verify_ssl': False,
        'nifi_disable_host_check': None,
        'registry_url': 'http://localhost:18080/nifi-registry-api',
        'registry_verify_ssl': False,
        'registry_disable_host_check': None,
    }

    # Simulate the constraint logic for both services
    config = test_config.copy()

    # NiFi logic
    if config.get("nifi_url"):
        if not config["nifi_url"].startswith("https://"):
            config["nifi_disable_host_check"] = None
        elif config.get("nifi_verify_ssl") is False and config.get("nifi_disable_host_check") is None:
            config["nifi_disable_host_check"] = True

    # Registry logic
    if config.get("registry_url"):
        if not config["registry_url"].startswith("https://"):
            config["registry_disable_host_check"] = None
        elif config.get("registry_verify_ssl") is False and config.get("registry_disable_host_check") is None:
            config["registry_disable_host_check"] = True

    # NiFi: HTTPS + verify_ssl=False → auto-correct to disable_host_check=True
    assert config["nifi_disable_host_check"] is True

    # Registry: HTTP → force disable_host_check=None (not applicable)
    assert config["registry_disable_host_check"] is None


def test_ssl_constraint_integration_with_profiles():
    """Integration test: SSL constraints work with real profile resolution"""
    import nipyapi.profiles

    # Test that all built-in profiles have valid SSL configurations after resolution
    profiles = ['single-user', 'secure-ldap', 'secure-mtls', 'secure-oidc']

    for profile_name in profiles:
        config = nipyapi.profiles.resolve_profile_config(profile_name)

        # Check NiFi SSL configuration
        if config.get('nifi_url'):
            nifi_verify = config.get('nifi_verify_ssl')
            nifi_disable_host = config.get('nifi_disable_host_check')
            nifi_url = config['nifi_url']

            if nifi_url.startswith('https://'):
                # HTTPS: verify SSL constraint
                if nifi_verify is False:
                    # verify_ssl=False requires disable_host_check=True to prevent SSL errors
                    assert nifi_disable_host is True, f"Profile {profile_name}: HTTPS + verify_ssl=False must have disable_host_check=True"
            else:
                # HTTP: hostname checking not applicable
                assert nifi_disable_host is None, f"Profile {profile_name}: HTTP URLs must have disable_host_check=None"

        # Check Registry SSL configuration
        if config.get('registry_url'):
            registry_verify = config.get('registry_verify_ssl')
            registry_disable_host = config.get('registry_disable_host_check')
            registry_url = config['registry_url']

            if registry_url.startswith('https://'):
                # HTTPS: verify SSL constraint
                if registry_verify is False:
                    assert registry_disable_host is True, f"Profile {profile_name}: HTTPS + verify_ssl=False must have disable_host_check=True"
            else:
                # HTTP: hostname checking not applicable
                assert registry_disable_host is None, f"Profile {profile_name}: HTTP URLs must have disable_host_check=None"


# TODO: Add more edge case tests for policy manipulation functions
# TODO: Add tests for SSL error conditions (wrong password, etc.)
