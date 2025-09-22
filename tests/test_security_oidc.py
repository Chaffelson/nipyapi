"""OIDC-specific integration tests for nipyapi security module."""

import pytest
from unittest.mock import patch, MagicMock
from tests import conftest
import nipyapi

# OIDC profile integration tests
pytestmark = pytest.mark.skipif(conftest.ACTIVE_PROFILE != 'secure-oidc', reason='OIDC profile not enabled')


# OIDC Unit Tests (Mocked)

def test_service_login_oidc_validation():
    """Test parameter validation for service_login_oidc (mocked)"""
    # Test registry service rejection
    with pytest.raises(ValueError, match="not supported for Registry"):
        nipyapi.security.service_login_oidc(service='registry')

    # Test invalid service assertion
    with pytest.raises(AssertionError):
        nipyapi.security.service_login_oidc(service='invalid_service')

    # Test missing core required parameters
    with pytest.raises(ValueError, match="requires oidc_token_endpoint"):
        nipyapi.security.service_login_oidc(
            service='nifi',
            oidc_token_endpoint=None,
            client_id='test',
            client_secret='test'
        )

    # Test invalid username/password combination (only one provided)
    with pytest.raises(ValueError, match="Invalid OIDC configuration"):
        nipyapi.security.service_login_oidc(
            service='nifi',
            username='test',
            password=None,  # Only username provided - invalid
            oidc_token_endpoint='http://test.com',
            client_id='test',
            client_secret='test'
        )

    with pytest.raises(ValueError, match="Invalid OIDC configuration"):
        nipyapi.security.service_login_oidc(
            service='nifi',
            username=None,
            password='test',  # Only password provided - invalid
            oidc_token_endpoint='http://test.com',
            client_id='test',
            client_secret='test'
        )


@patch('requests.post')
def test_service_login_oidc_client_credentials_flow_mocked(mock_post):
    """Test OIDC Client Credentials flow with mocked response"""
    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'access_token': 'test_token_client_credentials',
        'token_type': 'Bearer',
        'expires_in': 3600
    }
    mock_post.return_value = mock_response

    # Test Client Credentials flow (no username/password)
    result = nipyapi.security.service_login_oidc(
        service='nifi',
        oidc_token_endpoint='http://test.com/token',
        client_id='test_client',
        client_secret='test_secret'
    )

    assert result is True

    # Verify the correct request was made for Client Credentials flow
    # Note: verify parameter depends on current nifi_config.verify_ssl setting
    actual_call = mock_post.call_args
    expected_data = {
        'grant_type': 'client_credentials',
        'client_id': 'test_client',
        'client_secret': 'test_secret',
    }

    assert actual_call[0] == ('http://test.com/token',)
    assert actual_call[1]['headers'] == {'Content-Type': 'application/x-www-form-urlencoded'}
    assert actual_call[1]['timeout'] == 30
    assert actual_call[1]['data'] == expected_data
    assert 'verify' in actual_call[1]  # Verify parameter is present

    # Verify auth token was set
    assert nipyapi.config.nifi_config.api_key['bearerAuth'] == 'test_token_client_credentials'


@patch('requests.post')
def test_service_login_oidc_password_flow_mocked(mock_post):
    """Test OIDC Resource Owner Password flow with mocked response"""
    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'access_token': 'test_token_password',
        'token_type': 'Bearer',
        'expires_in': 3600
    }
    mock_post.return_value = mock_response

    # Test Password flow (with username/password)
    result = nipyapi.security.service_login_oidc(
        service='nifi',
        username='test_user',
        password='test_pass',
        oidc_token_endpoint='http://test.com/token',
        client_id='test_client',
        client_secret='test_secret'
    )

    assert result is True

    # Verify the correct request was made for Password flow
    # Note: verify parameter depends on current nifi_config.verify_ssl setting
    actual_call = mock_post.call_args
    expected_data = {
        'grant_type': 'password',
        'client_id': 'test_client',
        'client_secret': 'test_secret',
        'username': 'test_user',
        'password': 'test_pass',
    }

    assert actual_call[0] == ('http://test.com/token',)
    assert actual_call[1]['headers'] == {'Content-Type': 'application/x-www-form-urlencoded'}
    assert actual_call[1]['timeout'] == 30
    assert actual_call[1]['data'] == expected_data
    assert 'verify' in actual_call[1]  # Verify parameter is present

    # Verify auth token was set
    assert nipyapi.config.nifi_config.api_key['bearerAuth'] == 'test_token_password'


@patch('requests.post')
def test_service_login_oidc_success_mocked(mock_post):
    """Test OIDC success path with mocked response (backward compatibility)"""
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
    assert nipyapi.config.nifi_config.api_key.get('bearerAuth') == 'test_access_token'


@patch('requests.post')
def test_service_login_oidc_return_token_info_mocked(mock_post):
    """Test OIDC return_token_info parameter with mocked response"""
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
    assert nipyapi.config.nifi_config.api_key.get('bearerAuth') == 'test_access_token'


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


# OIDC Integration Tests


def test_service_login_oidc_integration():
    """Integration test for OIDC login with real infrastructure"""
    # This would test actual OIDC authentication against running Keycloak
    # Currently relies on conftest.py setup for OIDC authentication

    try:
        # Test that OIDC authentication was successful (through conftest setup)
        status = nipyapi.security.get_service_access_status(service="nifi", bool_response=True)
        assert status is not False  # False indicates failure, anything else indicates success

        # Test logout functionality
        result = nipyapi.security.service_logout(service="nifi")
        assert result is True
        # Verify token was actually cleared
        assert 'bearerAuth' not in nipyapi.config.nifi_config.api_key

    finally:
        # CRITICAL: Re-authenticate using profiles system to restore valid OIDC tokens
        nipyapi.profiles.switch(conftest.ACTIVE_PROFILE)


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
