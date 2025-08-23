"""Tests for `nipyapi.profiles` module."""

import os
import tempfile
import pytest
from unittest.mock import patch
import nipyapi.profiles
from tests import conftest


class TestLoadProfilesFromFile:
    """Test profile file loading functionality."""

    def test_load_yaml_profiles(self):
        """Test loading profiles from YAML file."""
        yaml_content = """
single-user:
  nifi_url: https://localhost:9444/nifi-api
  nifi_user: einstein
  nifi_pass: password1234

secure-ldap:
  nifi_url: https://localhost:9444/nifi-api
  nifi_user: einstein
  nifi_pass: password
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            profiles = nipyapi.profiles.load_profiles_from_file(yaml_path)

            assert 'single-user' in profiles
            assert 'secure-ldap' in profiles
            assert profiles['single-user']['nifi_url'] == 'https://localhost:9444/nifi-api'
            assert profiles['secure-ldap']['nifi_user'] == 'einstein'
        finally:
            os.unlink(yaml_path)

    def test_load_json_profiles(self):
        """Test loading profiles from JSON file."""
        json_content = """
{
  "single-user": {
    "nifi_url": "https://localhost:9444/nifi-api",
    "nifi_user": "einstein"
  },
  "secure-mtls": {
    "client_cert": "/path/to/cert.pem",
    "client_key": "/path/to/key.pem"
  }
}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(json_content)
            json_path = f.name

        try:
            profiles = nipyapi.profiles.load_profiles_from_file(json_path)

            assert 'single-user' in profiles
            assert 'secure-mtls' in profiles
            assert profiles['single-user']['nifi_url'] == 'https://localhost:9444/nifi-api'
            assert profiles['secure-mtls']['client_cert'] == '/path/to/cert.pem'
        finally:
            os.unlink(json_path)

    def test_load_nonexistent_file(self):
        """Test loading from nonexistent file raises appropriate error."""
        with pytest.raises(FileNotFoundError):
            nipyapi.profiles.load_profiles_from_file('/nonexistent/path.yml')


class TestDetectAndValidateAuth:
    """Test authentication method detection and validation."""

    def test_detect_oidc_auth(self):
        """Test OIDC authentication detection and validation."""
        config = {
            'oidc_token_endpoint': 'https://keycloak/token',
            'oidc_client_id': 'nipyapi-client',
            'oidc_client_secret': 'secret123',
            'nifi_user': 'einstein',
            'nifi_pass': 'password'
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.NIFI_AUTH_METHODS, 'NiFi'
        )

        assert method == 'oidc'
        assert params['oidc_token_endpoint'] == 'https://keycloak/token'
        assert params['nifi_user'] == 'einstein'
        assert len(params) == 5  # All required params

    def test_detect_mtls_auth(self):
        """Test mTLS authentication detection and validation."""
        config = {
            'client_cert': '/path/to/cert.pem',
            'client_key': '/path/to/key.pem',
            'client_key_password': 'keypass'
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.NIFI_AUTH_METHODS, 'NiFi'
        )

        assert method == 'mtls'
        assert params['client_cert'] == '/path/to/cert.pem'
        assert params['client_key'] == '/path/to/key.pem'
        assert params['client_key_password'] == 'keypass'

    def test_detect_basic_auth(self):
        """Test basic authentication detection and validation."""
        config = {
            'nifi_user': 'einstein',
            'nifi_pass': 'password1234'
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.NIFI_AUTH_METHODS, 'NiFi'
        )

        assert method == 'basic'
        assert params['nifi_user'] == 'einstein'
        assert params['nifi_pass'] == 'password1234'

    def test_oidc_validation_failure(self):
        """Test OIDC validation fails with missing required params."""
        config = {
            'oidc_token_endpoint': 'https://keycloak/token',
            'oidc_client_id': 'nipyapi-client',
            # Missing oidc_client_secret, nifi_user, nifi_pass
        }

        with pytest.raises(ValueError, match="NiFi oidc authentication requires"):
            nipyapi.profiles._detect_and_validate_auth(
                config, nipyapi.profiles.NIFI_AUTH_METHODS, 'NiFi'
            )

    def test_no_valid_auth_method(self):
        """Test error when no valid authentication method is detected."""
        config = {
            'some_random_key': 'value',
            'nifi_user': '',  # Empty string = invalid
        }

        with pytest.raises(ValueError, match="No valid NiFi authentication method detected"):
            nipyapi.profiles._detect_and_validate_auth(
                config, nipyapi.profiles.NIFI_AUTH_METHODS, 'NiFi'
            )

    def test_empty_string_handling(self):
        """Test that empty strings are treated as missing values."""
        config = {
            'oidc_token_endpoint': '',  # Empty string should not trigger OIDC
            'nifi_user': 'einstein',
            'nifi_pass': 'password'
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.NIFI_AUTH_METHODS, 'NiFi'
        )

        # Should fall back to basic auth since OIDC detection fails
        assert method == 'basic'

    def test_registry_auth_detection(self):
        """Test registry-specific authentication detection."""
        config = {
            'registry_user': 'reg_user',
            'registry_pass': 'reg_pass'
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.REGISTRY_AUTH_METHODS, 'Registry'
        )

        assert method == 'basic'
        assert params['registry_user'] == 'reg_user'
        assert params['registry_pass'] == 'reg_pass'


class TestResolveProfileConfig:
    """Test complete profile configuration resolution with environment variables."""

    def test_resolve_profile_basic(self):
        """Test basic profile resolution."""
        yaml_content = """
single-user:
  nifi_url: https://localhost:9444/nifi-api
  nifi_user: einstein
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            config = nipyapi.profiles.resolve_profile_config(profile_name='single-user', profiles_file_path=yaml_path)

            assert config['nifi_url'] == 'https://localhost:9444/nifi-api'
            assert config['nifi_user'] == 'einstein'
            assert config['profile'] == 'single-user'
        finally:
            os.unlink(yaml_path)

    def test_env_variable_overrides(self):
        """Test that environment variables override profile values."""
        yaml_content = """
single-user:
  nifi_url: https://localhost:9444/nifi-api
  nifi_user: einstein
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            # Set environment variables
            old_url = os.environ.get('NIFI_API_ENDPOINT')
            old_user = os.environ.get('NIFI_USERNAME')
            os.environ['NIFI_API_ENDPOINT'] = 'https://override:9443/nifi-api'
            os.environ['NIFI_USERNAME'] = 'override_user'

            config = nipyapi.profiles.resolve_profile_config(profile_name='single-user', profiles_file_path=yaml_path)

            # Environment variables should override profile values
            assert config['nifi_url'] == 'https://override:9443/nifi-api'
            assert config['nifi_user'] == 'override_user'
        finally:
            # Clean up environment
            if old_url is not None:
                os.environ['NIFI_API_ENDPOINT'] = old_url
            else:
                os.environ.pop('NIFI_API_ENDPOINT', None)
            if old_user is not None:
                os.environ['NIFI_USERNAME'] = old_user
            else:
                os.environ.pop('NIFI_USERNAME', None)
            os.unlink(yaml_path)

    def test_path_resolution(self):
        """Test that relative paths are converted to absolute paths."""
        yaml_content = """
test-profile:
  ca_path: resources/certs/ca.pem
  client_cert: ../certs/client.crt
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            config = nipyapi.profiles.resolve_profile_config(profile_name='test-profile', profiles_file_path=yaml_path)

            # Paths should be converted to absolute
            assert os.path.isabs(config['ca_path'])
            assert os.path.isabs(config['client_cert'])
            assert config['ca_path'].endswith('resources/certs/ca.pem')
        finally:
            os.unlink(yaml_path)


class TestProfileSwitch:
    """Test the main profile switching functionality."""

    def test_switch_basic_functionality(self):
        """Test that switch() function returns expected tuple format."""

        try:
            # Test with existing active profile (no actual switching to avoid corruption)
            profile_name, metadata = nipyapi.profiles.switch(conftest.ACTIVE_PROFILE, login=False)

            # Should return tuple with profile name and metadata
            assert profile_name == conftest.ACTIVE_PROFILE
            # Metadata varies by auth method, but should be None for login=False
            assert metadata is None
        finally:
            # CRITICAL: Always re-authenticate to restore session state
            # (login=False causes logout but doesn't login, leaving session unauthenticated)
            nipyapi.profiles.switch(conftest.ACTIVE_PROFILE, login=True)


    def test_switch_invalid_profile(self):
        """Test switching to nonexistent profile raises error."""
        # Test with standard profiles file - 'nonexistent' profile doesn't exist
        with pytest.raises(ValueError, match="Profile 'nonexistent' not found"):
            nipyapi.profiles.switch('nonexistent')

    def test_switch_no_services_configured(self):
        """Test error when profile has no services configured."""
        yaml_content = """
empty-profile:
  some_key: some_value
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            with pytest.raises(ValueError, match="has no nifi_url or registry_url"):
                nipyapi.profiles.switch('empty-profile', yaml_path)
        finally:
            os.unlink(yaml_path)


class TestAuthMethodDefinitions:
    """Test authentication method data structures."""

    def test_nifi_auth_methods_structure(self):
        """Test NiFi authentication methods are properly defined."""
        methods = nipyapi.profiles.NIFI_AUTH_METHODS

        assert 'oidc' in methods
        assert 'mtls' in methods
        assert 'basic' in methods

        # Each method should have required structure
        for method_name, method_def in methods.items():
            assert 'detection_keys' in method_def
            assert 'required_keys' in method_def
            assert 'optional_keys' in method_def
            assert isinstance(method_def['detection_keys'], list)
            assert isinstance(method_def['required_keys'], list)
            assert isinstance(method_def['optional_keys'], list)

    def test_registry_auth_methods_structure(self):
        """Test Registry authentication methods are properly defined."""
        methods = nipyapi.profiles.REGISTRY_AUTH_METHODS

        assert 'mtls' in methods
        assert 'basic' in methods
        # OIDC not supported for Registry
        assert 'oidc' not in methods

    def test_oidc_requirements(self):
        """Test OIDC method has all required parameters."""
        oidc_method = nipyapi.profiles.NIFI_AUTH_METHODS['oidc']

        required = oidc_method['required_keys']
        assert 'oidc_token_endpoint' in required
        assert 'oidc_client_id' in required
        assert 'oidc_client_secret' in required
        assert 'nifi_user' in required
        assert 'nifi_pass' in required

    def test_mtls_requirements(self):
        """Test mTLS method has correct required/optional parameters."""
        mtls_method = nipyapi.profiles.NIFI_AUTH_METHODS['mtls']

        required = mtls_method['required_keys']
        optional = mtls_method['optional_keys']

        assert 'client_cert' in required
        assert 'client_key' in required
        assert 'client_key_password' in optional
