"""Tests for `nipyapi` _utils package."""

import os
import sys
import pytest
from tests import conftest
import json
from deepdiff import DeepDiff
from nipyapi import utils, nifi, system
from nipyapi.config import default_string_encoding as DEF_ENCODING


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


def test_fs_read(fix_flow_serde):
    r1 = utils.fs_read(
        file_path=fix_flow_serde.filepath + '.json'
    )
    assert r1 == fix_flow_serde.json
    # Test reading from unreachable file
    if sys.version_info >= (3,3):
        with pytest.raises((OSError, IOError, FileNotFoundError, PermissionError)):
            _ = utils.fs_read(
                file_path='/dev/AlmostCertainlyNotAValidReadDevice'
            )
    else:
        with pytest.raises((OSError, IOError)):
            _ = utils.fs_read(
                file_path='/dev/AlmostCertainlyNotAValidReadDevice'
            )


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
