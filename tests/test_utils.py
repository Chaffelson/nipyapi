"""Tests for `nipyapi` _utils package."""

import os
import sys
import pytest
from unittest.mock import patch
from tests import conftest
import json
from deepdiff import DeepDiff
from nipyapi import utils, nifi, system, config, profiles
from nipyapi.config import default_string_encoding as DEF_ENCODING


@conftest.requires_registry
def test_dump(fix_flow_serde):
    # Testing that we don't modify or lose information in the round trip
    # Processing in memory for json
    export_obj = json.loads(fix_flow_serde.raw.decode(DEF_ENCODING))
    ss_json = utils.dump(
        obj=export_obj,
        mode='json'
    )
    assert isinstance(ss_json, str)
    round_trip_json = utils.load(ss_json)
    with pytest.raises(AssertionError):
        _ = utils.dump('', 'FakeNews')
    with pytest.raises(TypeError):
        _ = utils.dump({None}, 'json')
    # Test Yaml
    ss_yaml = utils.dump(
        obj=export_obj,
        mode='yaml'
    )
    assert isinstance(ss_yaml, str)
    round_trip_yaml = utils.load(ss_yaml)
    assert DeepDiff(
        round_trip_json,
        round_trip_yaml,
        verbose_level=2,
        ignore_order=False
    ) == {}


@conftest.requires_registry
def test_load(fix_flow_serde):
    # Validating load testing again in case we break the 'dump' test
    r1 = utils.load(
        obj=fix_flow_serde.json,
        dto=fix_flow_serde.dto
    )
    # Validate match
    assert DeepDiff(
        fix_flow_serde.snapshot.flow_contents,
        r1.flow_contents,
        verbose_level=2,
        ignore_order=True
    ) == {}
    with pytest.raises(AssertionError):
        _ = utils.load({})


def test_fs_write(tmpdir):
    f_fdir = tmpdir.mkdir(conftest.test_write_file_path)
    f_fpath = f_fdir.join(conftest.test_write_file_name)
    test_obj = conftest.test_write_file_name
    r1 = utils.fs_write(
        obj=test_obj,
        file_path=f_fpath
    )
    assert r1 == test_obj
    # Test writing to an invalid location - use a path that fails for both root and non-root
    invalid_path = '/nonexistent/directory/structure/that/cannot/exist/file.txt'
    if sys.version_info >= (3,3):
        with pytest.raises((OSError, IOError, PermissionError)):
            _ = utils.fs_write(
                obj=test_obj,
                file_path=invalid_path
            )
    else:
        with pytest.raises((OSError, IOError)):
            _ = utils.fs_write(
                obj=test_obj,
                file_path=invalid_path
            )
    # Test writing an invalid object
    with pytest.raises((TypeError,AttributeError)):
        _ = utils.fs_write(
            obj={},
            file_path=f_fpath
        )


def test_fs_read(tmpdir):
    # Create a simple test file - no need for heavy Registry fixtures
    test_content = '{"test": "data", "nested": {"value": 123}}'
    test_file = tmpdir.join("test_file.json")
    test_file.write(test_content)

    r1 = utils.fs_read(file_path=str(test_file))
    assert r1 == test_content

    # Test reading from unreachable file
    with pytest.raises((OSError, IOError, FileNotFoundError, PermissionError)):
        _ = utils.fs_read(file_path='/dev/AlmostCertainlyNotAValidReadDevice')


def test_filter_obj(fix_pg):
    f_pg = fix_pg.generate()
    t_1 = ['pie']
    with pytest.raises(ValueError):
        _ = utils.filter_obj(t_1, '', '')
    with pytest.raises(ValueError):
        _ = utils.filter_obj([f_pg], '', 'pie')
    r1 = utils.filter_obj([f_pg], conftest.test_pg_name, 'name')
    assert isinstance(r1, nifi.ProcessGroupEntity)
    r2 = utils.filter_obj([f_pg], 'FakeNews', 'name')
    assert r2 is None
    f_pg2 = fix_pg.generate(suffix='2')
    # Test greedy
    r3 = utils.filter_obj([f_pg, f_pg2], conftest.test_pg_name, 'name')
    assert isinstance(r3, list)
    # Test not greedy
    r4 = utils.filter_obj([f_pg, f_pg2], conftest.test_pg_name, 'name',
                          greedy=False)
    assert isinstance(r4, nifi.ProcessGroupEntity)
    r5 = utils.filter_obj([], '', '')
    assert r5 is None


def test_wait_to_complete():
    # TODO: Implement test
    pass


class TestIsUuid:
    """Tests for the is_uuid utility function."""

    def test_valid_uuid_lowercase(self):
        """Test that lowercase UUIDs are recognized."""
        assert utils.is_uuid("550e8400-e29b-41d4-a716-446655440000") is True
        assert utils.is_uuid("00000000-0000-0000-0000-000000000000") is True
        assert utils.is_uuid("ffffffff-ffff-ffff-ffff-ffffffffffff") is True

    def test_valid_uuid_uppercase(self):
        """Test that uppercase UUIDs are recognized."""
        assert utils.is_uuid("550E8400-E29B-41D4-A716-446655440000") is True
        assert utils.is_uuid("FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF") is True

    def test_valid_uuid_mixed_case(self):
        """Test that mixed case UUIDs are recognized."""
        assert utils.is_uuid("550E8400-e29b-41D4-a716-446655440000") is True

    def test_invalid_uuid_wrong_length(self):
        """Test that wrong length strings are rejected."""
        assert utils.is_uuid("550e8400-e29b-41d4-a716-44665544000") is False  # too short
        assert utils.is_uuid("550e8400-e29b-41d4-a716-4466554400000") is False  # too long
        assert utils.is_uuid("550e8400e29b41d4a716446655440000") is False  # no dashes

    def test_invalid_uuid_wrong_format(self):
        """Test that wrong format strings are rejected."""
        assert utils.is_uuid("550e8400-e29b-41d4-a716446655440000") is False  # missing dash
        assert utils.is_uuid("550e8400-e29b41d4-a716-446655440000") is False  # wrong position

    def test_invalid_uuid_non_hex(self):
        """Test that non-hex characters are rejected."""
        assert utils.is_uuid("550g8400-e29b-41d4-a716-446655440000") is False  # 'g' invalid
        assert utils.is_uuid("550e8400-xxxx-41d4-a716-446655440000") is False  # 'x' invalid

    def test_non_string_types(self):
        """Test that non-string types return False."""
        assert utils.is_uuid(None) is False
        assert utils.is_uuid(123) is False
        assert utils.is_uuid(["550e8400-e29b-41d4-a716-446655440000"]) is False
        assert utils.is_uuid({"uuid": "550e8400-e29b-41d4-a716-446655440000"}) is False

    def test_empty_string(self):
        """Test that empty string returns False."""
        assert utils.is_uuid("") is False

    def test_registry_client_name_vs_id(self):
        """Test distinguishing registry client names from IDs."""
        # These look like names, not UUIDs
        assert utils.is_uuid("my-registry-client") is False
        assert utils.is_uuid("GitHub-FlowRegistry") is False
        assert utils.is_uuid("test-action-client") is False

        # This is a UUID
        assert utils.is_uuid("59c45063-019b-1000-d14f-fc1f5a10994c") is True


def test_check_version():
    # We expect the passed version to be older than the system version, and
    # the response to therefore be -1 (older/negative, newer/positive)

    # minimum version test
    assert utils.check_version('1.1.2') <= 0
    # Check equivalence
    assert utils.check_version('1.2.3', '1.2.3') == 0
    # base is older than comp
    assert utils.check_version('1.1.3', '1.2.3') == -1
    # base is newer than comp
    assert utils.check_version('1.2.3', '0.2.3') == 1
    # Check RC
    assert utils.check_version('1.0.0-rc1', '1.0.0') == 0
    # Check that snapshots are disregarded
    assert utils.check_version('1.11.0', '1.13.0-SNAPSHOT') == -1
    assert utils.check_version('1.11.0', "1.11.0-SNAPSHOT") == 0
    assert utils.check_version('1.11.0', "1.10.0-SNAPSHOT") == 1
    # Check current version
    assert utils.check_version(
        system.get_nifi_version_info().ni_fi_version
    ) == 0
    # Check 2.0.0-M4
    assert utils.check_version('2.0.0-M4', '2', service='nifi') == 0
    assert utils.check_version('2', '2.0.0-M4') == 0
    # Check 2.x vs 1.x
    assert utils.check_version('2.0.0-M4', '1.13.0') == 1
    assert utils.check_version('1.13.0', '2.0.0-M4') == -1


def test_validate_parameters_versioning_support_noop():
    # Should be a no-op; legacy warnings removed due to 2.x floor
    assert utils.validate_parameters_versioning_support() is None


@conftest.requires_registry
def test_get_registry_version_info_string():
    ver = system.get_registry_version_info()
    assert isinstance(ver, str) and len(ver) > 0


def test_platform_minimum_versions():
    # Both services should be 2.x or newer in supported environments
    assert utils.check_version('2', service='nifi') <= 0
    assert utils.check_version('2', service='registry') <= 0


class TestResolveRelativePaths:
    """Test path resolution utility function."""

    def test_resolve_relative_path(self):
        """Test resolving relative path to absolute."""
        result = utils.resolve_relative_paths('certs/ca.pem')

        # Should be absolute path
        assert os.path.isabs(result)
        # Should end with our relative path
        assert result.endswith('certs/ca.pem')

    def test_preserve_absolute_path(self):
        """Test that absolute paths are preserved unchanged."""
        absolute_path = '/etc/ssl/certs/ca.pem'
        result = utils.resolve_relative_paths(absolute_path)

        assert result == absolute_path

    def test_handle_none_input(self):
        """Test that None input returns None."""
        result = utils.resolve_relative_paths(None)
        assert result is None

    def test_handle_empty_string(self):
        """Test that empty string input returns empty string."""
        result = utils.resolve_relative_paths('')
        assert result == ''

    def test_handle_whitespace_only(self):
        """Test that whitespace-only string returns unchanged."""
        whitespace_path = '   '
        result = utils.resolve_relative_paths(whitespace_path)
        assert result == whitespace_path

    def test_custom_root_path(self):
        """Test using custom root path."""
        custom_root = '/custom/root'
        result = utils.resolve_relative_paths('certs/ca.pem', custom_root)

        expected = os.path.join(custom_root, 'certs/ca.pem')
        assert result == expected

    def test_custom_root_preserves_absolute(self):
        """Test that custom root doesn't affect absolute paths."""
        absolute_path = '/etc/ssl/certs/ca.pem'
        custom_root = '/custom/root'
        result = utils.resolve_relative_paths(absolute_path, custom_root)

        assert result == absolute_path

    @pytest.mark.skipif(sys.platform == "win32", reason="Unix path tests")
    def test_unix_path_resolution(self):
        """Test Unix-style path resolution."""
        result = utils.resolve_relative_paths('resources/certs/ca.pem')

        # Should be absolute Unix path
        assert result.startswith('/')
        assert 'resources/certs/ca.pem' in result

    def test_project_root_default(self):
        """Test that default root uses PROJECT_ROOT_DIR parent."""
        import nipyapi.config

        result = utils.resolve_relative_paths('test/path')
        expected_root = os.path.dirname(nipyapi.config.PROJECT_ROOT_DIR)
        expected = os.path.join(expected_root, 'test/path')

        assert result == expected


class TestIsEndpointUp:
    """Test the is_endpoint_up function with various response scenarios."""

    def test_success_status_codes(self):
        """Test that success status codes (200-399) return True."""
        import unittest.mock
        import requests

        test_cases = [200, 201, 204, 301, 302, 399]

        for status_code in test_cases:
            with unittest.mock.patch('requests.get') as mock_get:
                mock_response = unittest.mock.Mock()
                mock_response.status_code = status_code
                mock_get.return_value = mock_response

                result = utils.is_endpoint_up('http://test-url')
                assert result is True, f"Status {status_code} should return True"

    def test_auth_error_status_codes(self):
        """Test that auth error codes (401, 403) return True (service ready for auth)."""
        import unittest.mock
        import requests

        test_cases = [401, 403]

        for status_code in test_cases:
            with unittest.mock.patch('requests.get') as mock_get:
                mock_response = unittest.mock.Mock()
                mock_response.status_code = status_code
                mock_get.return_value = mock_response

                result = utils.is_endpoint_up('http://test-url')
                assert result is True, f"Auth error {status_code} should return True"

    def test_server_error_status_codes(self):
        """Test that server error codes (4xx except 401/403, 5xx) return False."""
        import unittest.mock
        import requests

        test_cases = [400, 404, 405, 500, 502, 503]

        for status_code in test_cases:
            with unittest.mock.patch('requests.get') as mock_get:
                mock_response = unittest.mock.Mock()
                mock_response.status_code = status_code
                mock_get.return_value = mock_response

                result = utils.is_endpoint_up('http://test-url')
                assert result is False, f"Error status {status_code} should return False"

    def test_ssl_cert_error_returns_true(self):
        """Test that SSL certificate errors return True (service up, cert issues)."""
        import unittest.mock
        import requests

        cert_errors = [
            "CERTIFICATE_VERIFY_FAILED",
            "certificate verify failed",
            "WRONG_VERSION_NUMBER"
        ]

        for error_msg in cert_errors:
            with unittest.mock.patch('requests.get') as mock_get:
                mock_get.side_effect = requests.exceptions.SSLError(error_msg)

                result = utils.is_endpoint_up('https://test-url')
                assert result is True, f"SSL cert error '{error_msg}' should return True"

    def test_ssl_handshake_error_returns_false(self):
        """Test that SSL handshake errors return False (service not ready)."""
        import unittest.mock
        import requests

        handshake_errors = [
            "UNEXPECTED_EOF_WHILE_READING",
            "CONNECTION_RESET_BY_PEER",
            "SSL handshake failed"
        ]

        for error_msg in handshake_errors:
            with unittest.mock.patch('requests.get') as mock_get:
                mock_get.side_effect = requests.exceptions.SSLError(error_msg)

                result = utils.is_endpoint_up('https://test-url')
                assert result is False, f"SSL handshake error '{error_msg}' should return False"

    def test_read_timeout_error_returns_false(self):
        """Test that read timeout errors return False (service not ready)."""
        import unittest.mock
        import requests

        with unittest.mock.patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ReadTimeout("Read timeout")

            result = utils.is_endpoint_up('https://test-url')
            assert result is False, "Read timeout should return False"

    def test_connection_error_returns_false(self):
        """Test that connection errors return False (service down)."""
        import unittest.mock
        import requests

        with unittest.mock.patch('requests.get') as mock_get:
            mock_get.side_effect = requests.ConnectionError("Connection failed")

            result = utils.is_endpoint_up('http://test-url')
            assert result is False, "Connection errors should return False"

    def test_empty_status_code(self):
        """Test that empty/None status codes return False."""
        import unittest.mock

        with unittest.mock.patch('requests.get') as mock_get:
            mock_response = unittest.mock.Mock()
            mock_response.status_code = None
            mock_get.return_value = mock_response

            result = utils.is_endpoint_up('http://test-url')
            assert result is False, "Empty status code should return False"


class TestGetenvBool:
    """Tests for the getenv_bool utility function."""

    def setup_method(self):
        """Clean up environment variables before each test."""
        self.test_var = 'NIPYAPI_TEST_BOOL_VAR'
        if self.test_var in os.environ:
            del os.environ[self.test_var]

    def teardown_method(self):
        """Clean up environment variables after each test."""
        if self.test_var in os.environ:
            del os.environ[self.test_var]

    def test_falsy_values_return_false(self):
        """Test that standard falsy string values return False."""
        falsy_values = ['0', 'false', 'False', 'FALSE', 'no', 'No', 'NO', 'off', 'Off', 'OFF']

        for value in falsy_values:
            os.environ[self.test_var] = value
            result = utils.getenv_bool(self.test_var)
            assert result is False, f"'{value}' should return False"

    def test_empty_string_returns_false(self):
        """Test that empty string returns False."""
        os.environ[self.test_var] = ''
        result = utils.getenv_bool(self.test_var)
        assert result is False, "Empty string should return False"

    def test_truthy_values_return_true(self):
        """Test that non-falsy string values return True."""
        truthy_values = ['1', 'true', 'True', 'TRUE', 'yes', 'Yes', 'YES', 'on', 'On', 'ON', 'anything']

        for value in truthy_values:
            os.environ[self.test_var] = value
            result = utils.getenv_bool(self.test_var)
            assert result is True, f"'{value}' should return True"

    def test_unset_variable_returns_none(self):
        """Test that unset variable returns None."""
        result = utils.getenv_bool(self.test_var)
        assert result is None, "Unset variable should return None"

    def test_unset_variable_with_default_returns_default(self):
        """Test that unset variable returns default value when provided."""
        result = utils.getenv_bool(self.test_var, default=True)
        assert result is True, "Unset variable should return default True"

        result = utils.getenv_bool(self.test_var, default=False)
        assert result is False, "Unset variable should return default False"

    def test_set_variable_ignores_default(self):
        """Test that set variable ignores default value."""
        os.environ[self.test_var] = '1'
        result = utils.getenv_bool(self.test_var, default=False)
        assert result is True, "Set variable should ignore default"

        os.environ[self.test_var] = '0'
        result = utils.getenv_bool(self.test_var, default=True)
        assert result is False, "Set variable should ignore default"

    def test_case_insensitive_parsing(self):
        """Test that boolean parsing is case-insensitive."""
        test_cases = [
            ('false', False), ('FALSE', False), ('False', False),
            ('true', True), ('TRUE', True), ('True', True),
            ('no', False), ('NO', False), ('No', False),
            ('yes', True), ('YES', True), ('Yes', True),
            ('off', False), ('OFF', False), ('Off', False),
            ('on', True), ('ON', True), ('On', True),
        ]

        for value, expected in test_cases:
            os.environ[self.test_var] = value
            result = utils.getenv_bool(self.test_var)
            assert result is expected, f"'{value}' should return {expected}"

    def test_whitespace_handling(self):
        """Test that whitespace doesn't affect parsing."""
        test_cases = [
            (' 0 ', False),
            (' false ', False),
            (' 1 ', True),
            (' true ', True),
            ('   ', False),  # whitespace-only string should be False
        ]

        for value, expected in test_cases:
            os.environ[self.test_var] = value
            result = utils.getenv_bool(self.test_var)
            assert result is expected, f"'{value}' should return {expected}"

    def test_real_world_ssl_verification_examples(self):
        """Test with real-world SSL verification scenarios."""
        # Common ways to disable SSL verification
        disable_values = ['0', 'false', 'no', 'off', 'False', 'NO', 'OFF']
        for value in disable_values:
            os.environ[self.test_var] = value
            result = utils.getenv_bool(self.test_var)
            assert result is False, f"SSL verification should be disabled for '{value}'"

        # Common ways to enable SSL verification
        enable_values = ['1', 'true', 'yes', 'on', 'True', 'YES', 'ON', 'enable']
        for value in enable_values:
            os.environ[self.test_var] = value
            result = utils.getenv_bool(self.test_var)
            assert result is True, f"SSL verification should be enabled for '{value}'"


class TestSetEndpoint:
    """Test class for set_endpoint function."""

    def teardown_method(self):
        """Restore authentication state after each test."""
        # CRITICAL: Always restore authentication state to avoid breaking subsequent tests
        profiles.switch(conftest.ACTIVE_PROFILE)

    def test_basic_nifi_endpoint_setting(self):
        """Test basic NiFi endpoint setting functionality."""
        result = utils.set_endpoint("http://localhost:8080/nifi-api", ssl=False, login=False)
        assert result is True
        assert config.nifi_config.host == "http://localhost:8080/nifi-api"

    def test_basic_registry_endpoint_setting(self):
        """Test basic Registry endpoint setting functionality."""
        result = utils.set_endpoint("http://localhost:18080/nifi-registry-api", ssl=False, login=False)
        assert result is True
        assert config.registry_config.host == "http://localhost:18080/nifi-registry-api"

    def test_trailing_slash_removal(self):
        """Test that trailing slashes are removed from endpoints."""
        result = utils.set_endpoint("http://localhost:8080/nifi-api/", ssl=False, login=False)
        assert result is True
        assert config.nifi_config.host == "http://localhost:8080/nifi-api"

    def test_invalid_endpoint_error(self):
        """Test error handling for invalid endpoints."""
        with pytest.raises(ValueError, match="Endpoint not recognised"):
            utils.set_endpoint("http://localhost:8080/invalid-api", ssl=False, login=False)

    def test_backwards_compatibility_positional_args(self):
        """Test backwards compatibility with positional arguments."""
        result = utils.set_endpoint("http://localhost:8080/nifi-api", False, False)
        assert result is True
        assert config.nifi_config.host == "http://localhost:8080/nifi-api"

    def test_mixed_positional_and_keyword_args(self):
        """Test mixing positional and keyword arguments."""
        result = utils.set_endpoint("http://localhost:8080/nifi-api", False, login=False)
        assert result is True
        assert config.nifi_config.host == "http://localhost:8080/nifi-api"

    def test_service_detection_nifi_vs_registry(self):
        """Test that nifi vs registry endpoints are detected correctly."""
        # Test NiFi detection
        utils.set_endpoint("http://localhost:8080/nifi-api", ssl=False, login=False)
        assert config.nifi_config.host == "http://localhost:8080/nifi-api"

        # Test Registry detection
        utils.set_endpoint("http://localhost:18080/nifi-registry-api", ssl=False, login=False)
        assert config.registry_config.host == "http://localhost:18080/nifi-registry-api"

    @patch('nipyapi.utils.enforce_min_ver')
    def test_http_login_warning(self, mock_enforce_ver):
        """Test that HTTP login attempts show warnings."""
        import unittest.mock

        # Mock the version check to isolate the HTTP login warning
        mock_enforce_ver.return_value = False

        with unittest.mock.patch('nipyapi.utils.log') as mock_log:
            utils.set_endpoint(
                "http://localhost:18080/nifi-registry-api",
                ssl=False,
                login=True,
                username="test",
                password="test"
            )

            # Should log warning about HTTP login
            mock_log.warning.assert_called_once()
            warning_msg = mock_log.warning.call_args[0][0]
            assert "Consider using HTTPS" in warning_msg

    @patch('nipyapi.security.service_login')
    def test_https_ssl_login_behavior(self, mock_login):
        """Test that HTTPS + ssl=True + login=True calls service_login."""
        mock_login.return_value = True

        utils.set_endpoint(
            "https://localhost:9443/nifi-api",
            ssl=True,
            login=True,
            username="test",
            password="test"
        )

        mock_login.assert_called_once_with("nifi", username="test", password="test")

    @patch('nipyapi.security.service_login')
    def test_https_no_ssl_no_login(self, mock_login):
        """Test that HTTPS + ssl=False + login=True does not call service_login."""
        utils.set_endpoint(
            "https://localhost:9443/nifi-api",
            ssl=False,
            login=True,
            username="test",
            password="test"
        )

        # Should NOT call service_login when ssl=False
        mock_login.assert_not_called()

    @patch('nipyapi.utils.enforce_min_ver')
    def test_version_check_called(self, mock_enforce_ver):
        """Test that version enforcement is called."""
        result = utils.set_endpoint("http://localhost:8080/nifi-api", ssl=False, login=False)
        assert result is True
        mock_enforce_ver.assert_called_once_with("2", service="nifi")

    @patch('nipyapi.utils.enforce_min_ver')
    def test_version_check_failure_ignored(self, mock_enforce_ver):
        """Test that version check failures don't break set_endpoint."""
        mock_enforce_ver.side_effect = Exception("Version check failed")

        result = utils.set_endpoint("http://localhost:8080/nifi-api", ssl=False, login=False)
        assert result is True  # Should still succeed despite version check failure
