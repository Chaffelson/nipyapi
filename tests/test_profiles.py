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

    def test_detect_oidc_auth_password_flow(self):
        """Test OIDC Resource Owner Password flow detection and validation."""
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
        assert len(params) == 5  # All params including optional username/password

    def test_detect_oidc_auth_client_credentials_flow(self):
        """Test OIDC Client Credentials flow detection and validation."""
        config = {
            'oidc_token_endpoint': 'https://keycloak/token',
            'oidc_client_id': 'nipyapi-client',
            'oidc_client_secret': 'secret123',
            # No nifi_user/nifi_pass - client credentials flow
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.NIFI_AUTH_METHODS, 'NiFi'
        )

        assert method == 'oidc'
        assert params['oidc_token_endpoint'] == 'https://keycloak/token'
        assert params['oidc_client_id'] == 'nipyapi-client'
        assert params['oidc_client_secret'] == 'secret123'
        assert 'nifi_user' not in params  # Should not include optional params if not provided
        assert 'nifi_pass' not in params
        assert len(params) == 3  # Only required params

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
            # Missing oidc_client_secret (required for OIDC)
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

    def test_registry_unauthenticated_explicit(self):
        """Test explicit unauthenticated method specification for Registry."""
        config = {
            'registry_url': 'http://localhost:18080/nifi-registry-api',
            'registry_auth_method': 'unauthenticated'
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.REGISTRY_AUTH_METHODS, 'Registry'
        )

        assert method == 'unauthenticated'
        assert params == {}

    def test_registry_unauthenticated_fallback(self):
        """Test auto-detection falls back to unauthenticated when no credentials."""
        config = {
            'registry_url': 'http://localhost:18080/nifi-registry-api',
            'registry_user': None,
            'registry_pass': None
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.REGISTRY_AUTH_METHODS, 'Registry'
        )

        assert method == 'unauthenticated'
        assert params == {}

    def test_explicit_method_overrides_auto_detection(self):
        """Test that explicit method specification overrides auto-detection."""
        config = {
            'registry_url': 'http://localhost:18080/nifi-registry-api',
            'registry_auth_method': 'unauthenticated',
            'registry_user': 'testuser',  # These should be ignored
            'registry_pass': 'testpass'
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.REGISTRY_AUTH_METHODS, 'Registry'
        )

        assert method == 'unauthenticated'
        assert params == {}  # Credentials ignored when explicit method specified

    def test_registry_method_resolution_order_mtls_beats_unauthenticated(self):
        """Test mTLS is detected over unauthenticated when both could apply."""
        config = {
            'registry_url': 'https://localhost:18443/nifi-registry-api',
            'client_cert': '/path/to/cert.pem',
            'client_key': '/path/to/key.pem',
            # No registry_user/registry_pass, so unauthenticated could also match
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.REGISTRY_AUTH_METHODS, 'Registry'
        )

        # mTLS should win over unauthenticated
        assert method == 'mtls'
        assert 'client_cert' in params

    def test_registry_method_resolution_order_basic_beats_unauthenticated(self):
        """Test basic auth is detected over unauthenticated when both could apply."""
        config = {
            'registry_url': 'https://localhost:18443/nifi-registry-api',
            'registry_user': 'testuser',
            'registry_pass': 'testpass',
            # No client certs, so unauthenticated could also match
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.REGISTRY_AUTH_METHODS, 'Registry'
        )

        # Basic should win over unauthenticated
        assert method == 'basic'
        assert 'registry_user' in params

    def test_registry_method_resolution_order_mtls_beats_basic(self):
        """Test that when both mTLS and basic credentials are present, mTLS wins."""
        config = {
            'registry_url': 'https://localhost:18443/nifi-registry-api',
            'client_cert': '/path/to/cert.pem',
            'client_key': '/path/to/key.pem',
            'registry_user': 'testuser',
            'registry_pass': 'testpass'
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.REGISTRY_AUTH_METHODS, 'Registry'
        )

        # mTLS should win when both are present (depends on dictionary iteration order)
        assert method == 'mtls'
        assert 'client_cert' in params
        assert 'registry_user' not in params

    def test_unauthenticated_only_when_no_other_method_matches(self):
        """Test unauthenticated is only selected when no other method can be detected."""
        config = {
            'registry_url': 'http://localhost:18080/nifi-registry-api',
            # Deliberately incomplete credentials that don't match any method
            'registry_user': 'testuser',  # Missing registry_pass
            'client_cert': '/path/to/cert.pem',  # Missing client_key
        }

        method, params = nipyapi.profiles._detect_and_validate_auth(
            config, nipyapi.profiles.REGISTRY_AUTH_METHODS, 'Registry'
        )

        # Should fall back to unauthenticated since other methods can't be fully detected
        assert method == 'unauthenticated'
        assert params == {}


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
        """Test OIDC method has correct required and optional parameters."""
        oidc_method = nipyapi.profiles.NIFI_AUTH_METHODS['oidc']

        required = oidc_method['required_keys']
        optional = oidc_method['optional_keys']

        # Required for both flows
        assert 'oidc_token_endpoint' in required
        assert 'oidc_client_id' in required
        assert 'oidc_client_secret' in required

        # Optional - enables Resource Owner Password flow
        assert 'nifi_user' in optional
        assert 'nifi_pass' in optional

    def test_mtls_requirements(self):
        """Test mTLS method has correct required/optional parameters."""
        mtls_method = nipyapi.profiles.NIFI_AUTH_METHODS['mtls']

        required = mtls_method['required_keys']
        optional = mtls_method['optional_keys']

        assert 'client_cert' in required
        assert 'client_key' in required
        assert 'client_key_password' in optional


class TestNiFiCliPropertiesIntegration:
    """Test NiFi CLI properties file integration functionality.

    Note: These tests are unit tests that don't require live NiFi infrastructure.
    They test the properties file parsing and profile integration logic in isolation.
    """

    def test_load_basic_properties_file(self):
        """Test loading basic NiFi CLI properties file."""
        properties_content = """# NiFi CLI Properties
baseUrl=https://localhost/runtime-cluster
oidcTokenUrl=https://localhost/keycloak/realms/test/protocol/openid-connect/token
oidcClientId=runtime
oidcClientSecret=password123
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content)
            properties_path = f.name

        try:
            config = nipyapi.profiles._load_nifi_cli_properties(properties_path)

            assert config['nifi_url'] == 'https://localhost/runtime-cluster/nifi-api'
            assert config['oidc_token_endpoint'] == 'https://localhost/keycloak/realms/test/protocol/openid-connect/token'
            assert config['oidc_client_id'] == 'runtime'
            assert config['oidc_client_secret'] == 'password123'
        finally:
            os.unlink(properties_path)

    def test_load_properties_file_with_comments_and_empty_lines(self):
        """Test properties file parsing handles comments and empty lines correctly."""
        properties_content = """# This is a comment
# Another comment

baseUrl=https://localhost/runtime-cluster

# OIDC Configuration
oidcTokenUrl=https://localhost/keycloak/token
oidcClientId=runtime
! This is also a comment
oidcClientSecret=password123

# End of file
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content)
            properties_path = f.name

        try:
            config = nipyapi.profiles._load_nifi_cli_properties(properties_path)

            assert len(config) == 4  # Only non-comment, non-empty lines
            assert config['nifi_url'] == 'https://localhost/runtime-cluster/nifi-api'
            assert config['oidc_client_id'] == 'runtime'
        finally:
            os.unlink(properties_path)

    def test_load_properties_file_with_equals_in_values(self):
        """Test properties file parsing handles equals signs in values."""
        properties_content = """baseUrl=https://localhost/runtime-cluster
oidcTokenUrl=https://localhost/keycloak/realms/test/protocol/openid-connect/token?param=value
complexValue=key=value&another=key
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content)
            properties_path = f.name

        try:
            config = nipyapi.profiles._load_nifi_cli_properties(properties_path)

            assert config['nifi_url'] == 'https://localhost/runtime-cluster/nifi-api'
            assert config['oidc_token_endpoint'] == 'https://localhost/keycloak/realms/test/protocol/openid-connect/token?param=value'
            # complexValue should not be mapped since it's not in NIFI_CLI_PROPERTY_MAPPINGS
            assert 'complexValue' not in config
        finally:
            os.unlink(properties_path)

    def test_load_properties_file_missing_file(self):
        """Test loading nonexistent properties file returns empty dict."""
        config = nipyapi.profiles._load_nifi_cli_properties('/nonexistent/path.properties')
        assert config == {}

    def test_load_properties_file_empty_path(self):
        """Test loading with empty path returns empty dict."""
        config = nipyapi.profiles._load_nifi_cli_properties(None)
        assert config == {}

        config = nipyapi.profiles._load_nifi_cli_properties('')
        assert config == {}

    def test_properties_integration_with_profile_resolution(self):
        """Test properties file integration with complete profile resolution."""
        # Create properties file
        properties_content = """baseUrl=https://localhost/runtime-cluster
oidcTokenUrl=https://localhost/keycloak/token
oidcClientId=runtime
oidcClientSecret=password123
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content)
            properties_path = f.name

        # Create profile that references properties file
        yaml_content = f"""
test-cli-profile:
  nifi_cli_properties_file: {properties_path}
  nifi_ca_path: /path/to/ca.pem
  nifi_verify_ssl: false
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            config = nipyapi.profiles.resolve_profile_config('test-cli-profile', yaml_path)

            # Properties from CLI file should be merged
            assert config['nifi_url'] == 'https://localhost/runtime-cluster/nifi-api'
            assert config['oidc_token_endpoint'] == 'https://localhost/keycloak/token'
            assert config['oidc_client_id'] == 'runtime'
            assert config['oidc_client_secret'] == 'password123'

            # Profile values should also be present
            assert config['nifi_ca_path'] == '/path/to/ca.pem'
            assert config['nifi_verify_ssl'] is False
            assert config['profile'] == 'test-cli-profile'
        finally:
            os.unlink(properties_path)
            os.unlink(yaml_path)

    def test_properties_precedence_with_environment_variables(self):
        """Test that environment variables override properties file values."""
        # Create properties file
        properties_content = """baseUrl=https://localhost/runtime-cluster
oidcClientId=runtime
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content)
            properties_path = f.name

        # Create profile that references properties file
        yaml_content = f"""
test-cli-profile:
  nifi_cli_properties_file: {properties_path}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            # Set environment variable that should override properties file
            old_url = os.environ.get('NIFI_API_ENDPOINT')
            old_client_id = os.environ.get('OIDC_CLIENT_ID')
            os.environ['NIFI_API_ENDPOINT'] = 'https://override:9443/nifi-api'
            os.environ['OIDC_CLIENT_ID'] = 'override_client'

            config = nipyapi.profiles.resolve_profile_config('test-cli-profile', yaml_path)

            # Environment variables should override properties file values
            assert config['nifi_url'] == 'https://override:9443/nifi-api'
            assert config['oidc_client_id'] == 'override_client'
        finally:
            # Clean up environment
            if old_url is not None:
                os.environ['NIFI_API_ENDPOINT'] = old_url
            else:
                os.environ.pop('NIFI_API_ENDPOINT', None)
            if old_client_id is not None:
                os.environ['OIDC_CLIENT_ID'] = old_client_id
            else:
                os.environ.pop('OIDC_CLIENT_ID', None)
            os.unlink(properties_path)
            os.unlink(yaml_path)

    def test_properties_file_path_resolution(self):
        """Test that properties file path is resolved relative to current directory."""
        # Create properties file in a subdirectory
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            subdir = os.path.join(temp_dir, 'config')
            os.makedirs(subdir)

            properties_content = """baseUrl=https://localhost/runtime-cluster
oidcClientId=runtime
"""
            properties_path = os.path.join(subdir, 'nifi-cli.properties')
            with open(properties_path, 'w') as f:
                f.write(properties_content)

            # Test relative path resolution
            relative_path = os.path.relpath(properties_path)
            config = nipyapi.profiles._load_nifi_cli_properties(relative_path)

            assert config['nifi_url'] == 'https://localhost/runtime-cluster/nifi-api'
            assert config['oidc_client_id'] == 'runtime'

    def test_env_var_nifi_cli_properties_file(self):
        """Test NIPYAPI_NIFI_CLI_PROPERTIES_FILE environment variable support."""
        # Create properties file
        properties_content = """baseUrl=https://env-test/nifi-api
oidcClientId=env_runtime
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content)
            properties_path = f.name

        # Create profile without explicit properties file
        yaml_content = """
test-env-profile:
  nifi_ca_path: /path/to/ca.pem
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            # Set environment variable to specify properties file
            old_env = os.environ.get('NIPYAPI_NIFI_CLI_PROPERTIES_FILE')
            os.environ['NIPYAPI_NIFI_CLI_PROPERTIES_FILE'] = properties_path

            config = nipyapi.profiles.resolve_profile_config('test-env-profile', yaml_path)

            # Properties from environment-specified file should be loaded
            assert config['nifi_url'] == 'https://env-test/nifi-api'
            assert config['oidc_client_id'] == 'env_runtime'
            assert config['nifi_ca_path'] == '/path/to/ca.pem'
        finally:
            # Clean up environment
            if old_env is not None:
                os.environ['NIPYAPI_NIFI_CLI_PROPERTIES_FILE'] = old_env
            else:
                os.environ.pop('NIPYAPI_NIFI_CLI_PROPERTIES_FILE', None)
            os.unlink(properties_path)
            os.unlink(yaml_path)

    def test_properties_file_malformed_handling(self):
        """Test handling of malformed properties file."""
        # Create malformed properties file (missing equals signs)
        properties_content = """# Valid comment
baseUrl=https://localhost/nifi-api
invalid_line_without_equals
oidcClientId=runtime
another_invalid_line
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content)
            properties_path = f.name

        try:
            config = nipyapi.profiles._load_nifi_cli_properties(properties_path)

            # Should only parse valid lines
            assert config['nifi_url'] == 'https://localhost/nifi-api'
            assert config['oidc_client_id'] == 'runtime'
            # Invalid lines should be skipped
            assert len(config) == 2
        finally:
            os.unlink(properties_path)

    def test_empty_values_handling(self):
        """Test that empty values in properties file are not included."""
        properties_content = """baseUrl=https://localhost/nifi-api
oidcClientId=
oidcClientSecret=
oidcTokenUrl=https://localhost/keycloak/token
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content)
            properties_path = f.name

        try:
            config = nipyapi.profiles._load_nifi_cli_properties(properties_path)

            # Non-empty values should be included
            assert config['nifi_url'] == 'https://localhost/nifi-api'
            assert config['oidc_token_endpoint'] == 'https://localhost/keycloak/token'
            # Empty/whitespace values should not be included
            assert 'oidc_client_id' not in config
            assert 'oidc_client_secret' not in config
        finally:
            os.unlink(properties_path)

    def test_property_mappings_completeness(self):
        """Test that NIFI_CLI_PROPERTY_MAPPINGS covers expected properties."""
        mappings = nipyapi.profiles.NIFI_CLI_PROPERTY_MAPPINGS

        # Test expected mappings exist
        assert mappings['baseUrl'] == 'nifi_url'
        assert mappings['oidcTokenUrl'] == 'oidc_token_endpoint'
        assert mappings['oidcClientId'] == 'oidc_client_id'
        assert mappings['oidcClientSecret'] == 'oidc_client_secret'

        # Test all mapped values are valid profile keys
        for cli_key, profile_key in mappings.items():
            assert profile_key in nipyapi.profiles.DEFAULT_PROFILE_CONFIG, \
                f"Mapped profile key '{profile_key}' not found in DEFAULT_PROFILE_CONFIG"

    def test_base_url_nifi_api_appending(self):
        """Test that /nifi-api is automatically appended to baseUrl."""
        # Test baseUrl without /nifi-api
        properties_content = """baseUrl=https://localhost/runtime-cluster
oidcClientId=runtime
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content)
            properties_path = f.name

        try:
            config = nipyapi.profiles._load_nifi_cli_properties(properties_path)
            assert config['nifi_url'] == 'https://localhost/runtime-cluster/nifi-api'
        finally:
            os.unlink(properties_path)

        # Test baseUrl that already has /nifi-api (should not double-append)
        properties_content_with_api = """baseUrl=https://localhost/runtime-cluster/nifi-api
oidcClientId=runtime
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.properties', delete=False) as f:
            f.write(properties_content_with_api)
            properties_path = f.name

        try:
            config = nipyapi.profiles._load_nifi_cli_properties(properties_path)
            assert config['nifi_url'] == 'https://localhost/runtime-cluster/nifi-api'
        finally:
            os.unlink(properties_path)
