"""Tests for `nipyapi.cli` module."""

import json
import os


# =============================================================================
# Helper Function Tests (no NiFi connection required)
# =============================================================================


def test_serialize_result_string():
    """Test that strings are returned as valid JSON."""
    from nipyapi.cli import _serialize_result
    result = _serialize_result("hello", "json")
    assert result == '"hello"'  # JSON-encoded string


def test_serialize_result_simple_types():
    """Test serialization of simple types as valid JSON."""
    from nipyapi.cli import _serialize_result
    assert _serialize_result(42, "json") == "42"
    assert _serialize_result(3.14, "json") == "3.14"
    assert _serialize_result(True, "json") == "true"  # JSON boolean
    assert _serialize_result(None, "json") == "null"  # JSON null


def test_serialize_result_dict_json():
    """Test JSON serialization of dict."""
    from nipyapi.cli import _serialize_result
    result = _serialize_result({"key": "value", "count": 5}, "json")
    parsed = json.loads(result)
    assert parsed["key"] == "value"
    assert parsed["count"] == 5


def test_serialize_result_dict_github():
    """Test GitHub Actions output format."""
    from nipyapi.cli import _serialize_result
    result = _serialize_result({"flow_id": "abc123", "pg_name": "test"}, "github")
    # snake_case -> kebab-case for GitHub
    assert "flow-id=abc123" in result
    assert "pg-name=test" in result


def test_serialize_result_dict_github_heredoc():
    """Test GitHub Actions heredoc format for multiline values."""
    from nipyapi.cli import _serialize_result
    multiline_value = "line1\nline2\nline3"
    result = _serialize_result({"content": multiline_value}, "github")
    # Should use heredoc syntax for multiline
    assert "content<<EOF" in result
    assert "line1\nline2\nline3" in result
    assert result.count("EOF") == 2  # Opening and closing


def test_serialize_result_dict_github_long_value():
    """Test GitHub Actions heredoc format for very long values."""
    from nipyapi.cli import _serialize_result
    long_value = "x" * 600  # Over 500 char threshold
    result = _serialize_result({"data": long_value}, "github")
    # Should use heredoc syntax for long values
    assert "data<<EOF" in result
    assert long_value in result


def test_serialize_result_dict_dotenv():
    """Test GitLab dotenv output format."""
    from nipyapi.cli import _serialize_result
    result = _serialize_result({"flow_id": "abc123", "pg_name": "test"}, "dotenv")
    # UPPER_CASE for dotenv
    assert "FLOW_ID=abc123" in result
    assert "PG_NAME=test" in result


def test_serialize_result_dict_dotenv_special_chars():
    """Test GitLab dotenv quoting for values with special characters."""
    from nipyapi.cli import _serialize_result

    # Values with special characters should be quoted
    result = _serialize_result({
        "simple": "abc123",
        "with_spaces": "hello world",
        "with_pipe": "error | warning",
        "with_brackets": "[ERROR] message",
        "with_quotes": 'value with "quotes"',
    }, "dotenv")

    # Simple value should NOT be quoted
    assert 'SIMPLE=abc123' in result

    # Values with special chars SHOULD be quoted
    assert 'WITH_SPACES="hello world"' in result
    assert 'WITH_PIPE="error | warning"' in result
    assert 'WITH_BRACKETS="[ERROR] message"' in result

    # Embedded quotes should be escaped
    assert 'WITH_QUOTES="value with \\"quotes\\""' in result


def test_serialize_result_list_json():
    """Test JSON serialization of list."""
    from nipyapi.cli import _serialize_result
    result = _serialize_result([{"a": 1}, {"b": 2}], "json")
    parsed = json.loads(result)
    assert len(parsed) == 2
    assert parsed[0]["a"] == 1


def test_serialize_result_list_non_json():
    """Test list serialization with non-JSON format returns JSONL."""
    from nipyapi.cli import _serialize_result
    result = _serialize_result([{"a": 1}, {"b": 2}], "github")
    # Should be one JSON object per line (JSONL)
    lines = result.strip().split("\n")
    assert len(lines) == 2
    assert json.loads(lines[0]) == {"a": 1}
    assert json.loads(lines[1]) == {"b": 2}


def test_serialize_result_dict_with_nested_list_github():
    """Test GitHub format properly JSON-serializes nested lists."""
    from nipyapi.cli import _serialize_result
    data = {
        "flow_count": "2",
        "flows": [{"name": "flow1", "id": "abc"}, {"name": "flow2", "id": "def"}]
    }
    result = _serialize_result(data, "github")

    # Check scalar value
    assert "flow-count=2" in result

    # The flows value should be valid JSON (double quotes, not Python repr single quotes)
    lines = result.strip().split("\n")
    flows_line = [l for l in lines if l.startswith("flows=")][0]
    flows_json = flows_line[6:]  # Remove "flows=" prefix

    # Must be parseable as JSON
    parsed = json.loads(flows_json)
    assert len(parsed) == 2
    assert parsed[0]["name"] == "flow1"
    assert parsed[1]["id"] == "def"


def test_serialize_result_dict_with_nested_list_dotenv():
    """Test dotenv format properly JSON-serializes nested lists."""
    from nipyapi.cli import _serialize_result
    data = {
        "version_count": "3",
        "versions": [{"version": "v1"}, {"version": "v2"}, {"version": "v3"}]
    }
    result = _serialize_result(data, "dotenv")

    # Check scalar value
    assert "VERSION_COUNT=3" in result

    # The versions value should be JSON and properly quoted
    lines = result.strip().split("\n")
    versions_line = [l for l in lines if l.startswith("VERSIONS=")][0]

    # Should be quoted because JSON contains special chars
    assert versions_line.startswith('VERSIONS="')
    assert versions_line.endswith('"')

    # Extract and parse the JSON (removing quotes and unescaping)
    versions_json = versions_line[10:-1]  # Remove 'VERSIONS="' and trailing '"'
    versions_json = versions_json.replace('\\"', '"')  # Unescape quotes
    parsed = json.loads(versions_json)
    assert len(parsed) == 3
    assert parsed[0]["version"] == "v1"


def test_serialize_result_dict_with_nested_dict_github():
    """Test GitHub format flattens nested dicts (existing behavior)."""
    from nipyapi.cli import _serialize_result
    data = {
        "name": "test",
        "metadata": {"key1": "value1", "key2": "value2"}
    }
    result = _serialize_result(data, "github")

    # Nested dicts are flattened with key paths (existing behavior)
    assert "name=test" in result
    assert "metadata-key1=value1" in result
    assert "metadata-key2=value2" in result


# =============================================================================
# Complex JSON Input Parsing Tests (no NiFi connection required)
# =============================================================================
# These tests verify that complex JSON structures are correctly parsed
# when passed as strings to CLI functions (via configure_params, etc.)


def test_json_input_embedded_quotes():
    """Test JSON with embedded double quotes in values."""
    # This is what arrives when user passes: --parameters '{"msg": "say \"hello\""}'
    json_str = '{"message": "value with \\"embedded\\" quotes"}'
    parsed = json.loads(json_str)
    assert parsed["message"] == 'value with "embedded" quotes'


def test_json_input_single_quotes_in_value():
    """Test JSON with single quotes in values (no escaping needed)."""
    json_str = '{"message": "it\'s working"}'
    parsed = json.loads(json_str)
    assert parsed["message"] == "it's working"


def test_json_input_newlines():
    """Test JSON with escaped newlines in values."""
    json_str = '{"multiline": "line1\\nline2\\nline3"}'
    parsed = json.loads(json_str)
    assert parsed["multiline"] == "line1\nline2\nline3"
    assert parsed["multiline"].count("\n") == 2


def test_json_input_tabs():
    """Test JSON with escaped tabs in values."""
    json_str = '{"tabbed": "col1\\tcol2\\tcol3"}'
    parsed = json.loads(json_str)
    assert parsed["tabbed"] == "col1\tcol2\tcol3"


def test_json_input_backslashes():
    """Test JSON with backslashes (Windows paths)."""
    json_str = '{"path": "C:\\\\Users\\\\data\\\\file.txt"}'
    parsed = json.loads(json_str)
    assert parsed["path"] == "C:\\Users\\data\\file.txt"


def test_json_input_nested_dict():
    """Test JSON with nested dict values."""
    json_str = '{"config": {"database": {"host": "localhost", "port": 5432}}}'
    parsed = json.loads(json_str)
    assert parsed["config"]["database"]["host"] == "localhost"
    assert parsed["config"]["database"]["port"] == 5432


def test_json_input_list_value():
    """Test JSON with list as value."""
    json_str = '{"items": ["apple", "banana", "cherry"]}'
    parsed = json.loads(json_str)
    assert parsed["items"] == ["apple", "banana", "cherry"]


def test_json_input_mixed_nested():
    """Test JSON with mixed nested structures."""
    json_str = '{"users": [{"name": "alice", "roles": ["admin", "user"]}, {"name": "bob", "roles": ["user"]}]}'
    parsed = json.loads(json_str)
    assert len(parsed["users"]) == 2
    assert parsed["users"][0]["name"] == "alice"
    assert "admin" in parsed["users"][0]["roles"]


def test_json_input_null_value():
    """Test JSON with null value."""
    json_str = '{"optional": null, "required": "value"}'
    parsed = json.loads(json_str)
    assert parsed["optional"] is None
    assert parsed["required"] == "value"


def test_json_input_empty_string():
    """Test JSON with empty string value."""
    json_str = '{"empty": "", "not_empty": "value"}'
    parsed = json.loads(json_str)
    assert parsed["empty"] == ""
    assert parsed["not_empty"] == "value"


def test_json_input_empty_dict():
    """Test JSON with empty dict value."""
    json_str = '{"config": {}}'
    parsed = json.loads(json_str)
    assert parsed["config"] == {}


def test_json_input_empty_list():
    """Test JSON with empty list value."""
    json_str = '{"items": []}'
    parsed = json.loads(json_str)
    assert parsed["items"] == []


def test_json_input_unicode():
    """Test JSON with Unicode characters."""
    json_str = '{"greeting": "Hello \\u4e16\\u754c", "emoji": "\\u2764"}'
    parsed = json.loads(json_str)
    assert parsed["greeting"] == "Hello \u4e16\u754c"  # "Hello World" in Chinese
    assert parsed["emoji"] == "\u2764"  # Heart emoji


def test_json_input_unicode_direct():
    """Test JSON with direct Unicode characters (no escaping)."""
    json_str = '{"greeting": "Hej verden", "symbol": "cafe"}'
    parsed = json.loads(json_str)
    assert parsed["greeting"] == "Hej verden"
    assert parsed["symbol"] == "cafe"


def test_json_input_numeric_values():
    """Test JSON with various numeric types."""
    json_str = '{"integer": 42, "float": 3.14159, "negative": -17, "scientific": 1.5e10}'
    parsed = json.loads(json_str)
    assert parsed["integer"] == 42
    assert abs(parsed["float"] - 3.14159) < 0.0001
    assert parsed["negative"] == -17
    assert parsed["scientific"] == 1.5e10


def test_json_input_boolean_values():
    """Test JSON with boolean values."""
    json_str = '{"enabled": true, "disabled": false}'
    parsed = json.loads(json_str)
    assert parsed["enabled"] is True
    assert parsed["disabled"] is False


def test_json_input_special_chars_in_keys():
    """Test JSON with special characters in keys."""
    json_str = '{"my-key": "value1", "my.key": "value2", "my_key": "value3"}'
    parsed = json.loads(json_str)
    assert parsed["my-key"] == "value1"
    assert parsed["my.key"] == "value2"
    assert parsed["my_key"] == "value3"


def test_json_input_long_value():
    """Test JSON with very long string value."""
    long_value = "x" * 10000
    json_str = json.dumps({"long_param": long_value})
    parsed = json.loads(json_str)
    assert len(parsed["long_param"]) == 10000


def test_json_input_deep_nesting():
    """Test JSON with deeply nested structure."""
    json_str = '{"a": {"b": {"c": {"d": {"e": "deep"}}}}}'
    parsed = json.loads(json_str)
    assert parsed["a"]["b"]["c"]["d"]["e"] == "deep"


# =============================================================================
# Roundtrip Tests (serialize -> parse)
# =============================================================================


def test_roundtrip_nested_dict_json():
    """Test nested dict survives JSON roundtrip."""
    from nipyapi.cli import _serialize_result
    original = {"config": {"nested": {"value": 123, "list": [1, 2, 3]}}}
    serialized = _serialize_result(original, "json")
    parsed = json.loads(serialized)
    assert parsed == original


def test_roundtrip_special_chars_json():
    """Test special characters survive JSON roundtrip."""
    from nipyapi.cli import _serialize_result
    original = {
        "quoted": 'value with "quotes"',
        "newline": "line1\nline2",
        "path": "C:\\Users\\data",
    }
    serialized = _serialize_result(original, "json")
    parsed = json.loads(serialized)
    assert parsed == original


def test_roundtrip_unicode_json():
    """Test Unicode survives JSON roundtrip."""
    from nipyapi.cli import _serialize_result
    original = {"greeting": "Hello World", "symbol": "cafe"}
    serialized = _serialize_result(original, "json")
    parsed = json.loads(serialized)
    assert parsed == original


def test_roundtrip_mixed_types_json():
    """Test mixed types survive JSON roundtrip."""
    from nipyapi.cli import _serialize_result
    original = {
        "string": "text",
        "integer": 42,
        "float": 3.14,
        "boolean": True,
        "null": None,
        "list": [1, "two", 3.0],
        "dict": {"nested": "value"},
    }
    serialized = _serialize_result(original, "json")
    parsed = json.loads(serialized)
    assert parsed == original


# =============================================================================
# Dict Flattening Tests
# =============================================================================


def test_flatten_dict_simple():
    """Test flattening a simple nested dict."""
    from nipyapi.cli import _flatten_dict
    flat = _flatten_dict({"a": 1, "b": 2})
    assert flat == {"a": 1, "b": 2}


def test_flatten_dict_nested():
    """Test flattening a nested dict."""
    from nipyapi.cli import _flatten_dict
    flat = _flatten_dict({"outer": {"inner": "value"}})
    assert flat == {"outer_inner": "value"}


def test_flatten_dict_deeply_nested():
    """Test flattening a deeply nested dict."""
    from nipyapi.cli import _flatten_dict
    flat = _flatten_dict({"a": {"b": {"c": 42}}})
    assert flat == {"a_b_c": 42}


def test_to_dict_with_dict():
    """Test _to_dict with a dict input."""
    from nipyapi.cli import _to_dict
    result = _to_dict({"key": "value"})
    assert result == {"key": "value"}


def test_to_dict_with_object():
    """Test _to_dict with an object that has __dict__."""
    from nipyapi.cli import _to_dict

    class SimpleObj:
        def __init__(self):
            self.name = "test"
            self.value = 123
            self._private = "hidden"

    result = _to_dict(SimpleObj())
    assert result["name"] == "test"
    assert result["value"] == 123
    assert "_private" not in result  # Private attrs excluded


def test_to_dict_with_to_dict_method():
    """Test _to_dict with an object that has a to_dict() method (swagger-style)."""
    from nipyapi.cli import _to_dict

    class SwaggerObj:
        def to_dict(self):
            return {"id": "abc123", "name": "swagger_obj"}

    result = _to_dict(SwaggerObj())
    assert result == {"id": "abc123", "name": "swagger_obj"}


def test_to_dict_simple_types():
    """Test _to_dict returns simple types as-is."""
    from nipyapi.cli import _to_dict

    # Simple types are returned as-is for clean CLI output
    assert _to_dict(42) == 42
    assert _to_dict(3.14) == 3.14
    assert _to_dict("hello") == "hello"
    assert _to_dict(True) is True
    assert _to_dict(None) is None


def test_detect_output_format_default():
    """Test default output format is json."""
    from nipyapi.cli import _detect_output_format
    # Clear any env vars that might affect detection
    old_format = os.environ.pop("NIFI_OUTPUT_FORMAT", None)
    old_github = os.environ.pop("GITHUB_ACTIONS", None)
    old_gitlab = os.environ.pop("GITLAB_CI", None)
    try:
        assert _detect_output_format() == "json"
    finally:
        if old_format:
            os.environ["NIFI_OUTPUT_FORMAT"] = old_format
        if old_github:
            os.environ["GITHUB_ACTIONS"] = old_github
        if old_gitlab:
            os.environ["GITLAB_CI"] = old_gitlab


def test_detect_output_format_explicit():
    """Test explicit NIFI_OUTPUT_FORMAT takes priority."""
    from nipyapi.cli import _detect_output_format
    old = os.environ.get("NIFI_OUTPUT_FORMAT")
    try:
        os.environ["NIFI_OUTPUT_FORMAT"] = "dotenv"
        assert _detect_output_format() == "dotenv"
    finally:
        if old:
            os.environ["NIFI_OUTPUT_FORMAT"] = old
        else:
            os.environ.pop("NIFI_OUTPUT_FORMAT", None)


def test_detect_output_format_github():
    """Test GitHub Actions auto-detection."""
    from nipyapi.cli import _detect_output_format
    old_format = os.environ.pop("NIFI_OUTPUT_FORMAT", None)
    old_github = os.environ.get("GITHUB_ACTIONS")
    try:
        os.environ["GITHUB_ACTIONS"] = "true"
        assert _detect_output_format() == "github"
    finally:
        if old_format:
            os.environ["NIFI_OUTPUT_FORMAT"] = old_format
        if old_github:
            os.environ["GITHUB_ACTIONS"] = old_github
        else:
            os.environ.pop("GITHUB_ACTIONS", None)


def test_detect_output_format_gitlab():
    """Test GitLab CI auto-detection."""
    from nipyapi.cli import _detect_output_format
    old_format = os.environ.pop("NIFI_OUTPUT_FORMAT", None)
    old_gitlab = os.environ.get("GITLAB_CI")
    old_github = os.environ.pop("GITHUB_ACTIONS", None)
    try:
        os.environ["GITLAB_CI"] = "true"
        assert _detect_output_format() == "dotenv"
    finally:
        if old_format:
            os.environ["NIFI_OUTPUT_FORMAT"] = old_format
        if old_gitlab:
            os.environ["GITLAB_CI"] = old_gitlab
        else:
            os.environ.pop("GITLAB_CI", None)
        if old_github:
            os.environ["GITHUB_ACTIONS"] = old_github


def test_get_log_level_default():
    """Test default log level is None (no logs)."""
    from nipyapi.cli import _get_log_level
    old = os.environ.pop("NIFI_LOG_LEVEL", None)
    try:
        assert _get_log_level() is None
    finally:
        if old:
            os.environ["NIFI_LOG_LEVEL"] = old


def test_get_log_level_explicit():
    """Test explicit log level setting."""
    import logging
    from nipyapi.cli import _get_log_level
    old = os.environ.get("NIFI_LOG_LEVEL")
    try:
        os.environ["NIFI_LOG_LEVEL"] = "DEBUG"
        assert _get_log_level() == logging.DEBUG
        os.environ["NIFI_LOG_LEVEL"] = "WARNING"
        assert _get_log_level() == logging.WARNING
    finally:
        if old:
            os.environ["NIFI_LOG_LEVEL"] = old
        else:
            os.environ.pop("NIFI_LOG_LEVEL", None)


def test_get_log_on_error_default():
    """Test default log-on-error is True."""
    from nipyapi.cli import _get_log_on_error
    old = os.environ.pop("NIFI_LOG_ON_ERROR", None)
    try:
        assert _get_log_on_error() is True
    finally:
        if old:
            os.environ["NIFI_LOG_ON_ERROR"] = old


def test_get_log_on_error_disabled():
    """Test disabling log-on-error."""
    from nipyapi.cli import _get_log_on_error
    old = os.environ.get("NIFI_LOG_ON_ERROR")
    try:
        os.environ["NIFI_LOG_ON_ERROR"] = "false"
        assert _get_log_on_error() is False
        os.environ["NIFI_LOG_ON_ERROR"] = "0"
        assert _get_log_on_error() is False
    finally:
        if old:
            os.environ["NIFI_LOG_ON_ERROR"] = old
        else:
            os.environ.pop("NIFI_LOG_ON_ERROR", None)


# =============================================================================
# CLI Flag Parsing Tests
# =============================================================================


def test_parse_cli_flags_profile_with_space():
    """Test _parse_cli_flags with --profile value syntax."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "--profile", "myprofile", "ci", "get_status"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert profile == "myprofile"
        assert show_version is False
        assert verbosity == 0
        # --profile and value should be removed from argv
        assert "--profile" not in sys.argv
        assert "myprofile" not in sys.argv
        assert "ci" in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_cli_flags_profile_with_equals():
    """Test _parse_cli_flags with --profile=value syntax."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "--profile=prod", "system", "info"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert profile == "prod"
        assert show_version is False
        assert verbosity == 0
        assert "--profile=prod" not in sys.argv
        assert "system" in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_cli_flags_no_profile():
    """Test _parse_cli_flags when no flags are specified."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "canvas", "get_root_pg_id"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert profile is None
        assert show_version is False
        assert verbosity == 0
        assert "canvas" in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_cli_flags_version_long():
    """Test _parse_cli_flags with --version flag."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "--version"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert show_version is True
        assert verbosity == 0
        assert profile is None
        assert "--version" not in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_cli_flags_version_short():
    """Test _parse_cli_flags with -V flag."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "-V"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert show_version is True
        assert verbosity == 0
        assert profile is None
        assert "-V" not in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_cli_flags_verbosity_single():
    """Test _parse_cli_flags with -v flag (single verbosity)."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "-v", "ci", "get_status"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert show_version is False
        assert verbosity == 1
        assert profile is None
        assert "-v" not in sys.argv
        assert "ci" in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_cli_flags_verbosity_double():
    """Test _parse_cli_flags with -vv flag (double verbosity)."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "-vv", "ci", "get_status"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert show_version is False
        assert verbosity == 2
        assert profile is None
        assert "-vv" not in sys.argv
        assert "ci" in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_cli_flags_verbosity_triple():
    """Test _parse_cli_flags with -vvv flag (triple verbosity)."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "-vvv", "system", "info"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert show_version is False
        assert verbosity == 3
        assert profile is None
        assert "-vvv" not in sys.argv
        assert "system" in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_cli_flags_verbosity_multiple_flags():
    """Test _parse_cli_flags with multiple -v flags."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "-v", "-v", "ci", "get_status"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert show_version is False
        assert verbosity == 2
        assert profile is None
        assert "-v" not in sys.argv
        assert "ci" in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_cli_flags_combined():
    """Test _parse_cli_flags with multiple flags combined."""
    import sys
    from nipyapi.cli import _parse_cli_flags

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "-vv", "--profile", "prod", "ci", "deploy"]
        show_version, verbosity, profile = _parse_cli_flags()
        assert show_version is False
        assert verbosity == 2
        assert profile == "prod"
        assert "-vv" not in sys.argv
        assert "--profile" not in sys.argv
        assert "prod" not in sys.argv
        assert "ci" in sys.argv
        assert "deploy" in sys.argv
    finally:
        sys.argv = original_argv


def test_apply_verbosity_level_0():
    """Test _apply_verbosity with verbosity 0 (default, no change)."""
    from nipyapi.cli import _apply_verbosity

    old = os.environ.pop("NIFI_LOG_LEVEL", None)
    try:
        _apply_verbosity(0)
        # Should not set NIFI_LOG_LEVEL
        assert "NIFI_LOG_LEVEL" not in os.environ
    finally:
        if old:
            os.environ["NIFI_LOG_LEVEL"] = old


def test_apply_verbosity_level_1():
    """Test _apply_verbosity with verbosity 1 (INFO)."""
    from nipyapi.cli import _apply_verbosity

    old = os.environ.get("NIFI_LOG_LEVEL")
    try:
        _apply_verbosity(1)
        assert os.environ.get("NIFI_LOG_LEVEL") == "INFO"
    finally:
        if old:
            os.environ["NIFI_LOG_LEVEL"] = old
        else:
            os.environ.pop("NIFI_LOG_LEVEL", None)


def test_apply_verbosity_level_2():
    """Test _apply_verbosity with verbosity 2 (DEBUG)."""
    from nipyapi.cli import _apply_verbosity

    old = os.environ.get("NIFI_LOG_LEVEL")
    try:
        _apply_verbosity(2)
        assert os.environ.get("NIFI_LOG_LEVEL") == "DEBUG"
    finally:
        if old:
            os.environ["NIFI_LOG_LEVEL"] = old
        else:
            os.environ.pop("NIFI_LOG_LEVEL", None)


def test_apply_verbosity_level_3():
    """Test _apply_verbosity with verbosity 3+ (still DEBUG)."""
    from nipyapi.cli import _apply_verbosity

    old = os.environ.get("NIFI_LOG_LEVEL")
    try:
        _apply_verbosity(3)
        assert os.environ.get("NIFI_LOG_LEVEL") == "DEBUG"
    finally:
        if old:
            os.environ["NIFI_LOG_LEVEL"] = old
        else:
            os.environ.pop("NIFI_LOG_LEVEL", None)


def test_log_capture_handler():
    """Test LogCapture handler captures and filters logs."""
    import logging
    from nipyapi.cli import LogCapture

    handler = LogCapture()
    handler.setFormatter(logging.Formatter("%(message)s"))

    # Create a test logger
    logger = logging.getLogger("test_cli_capture")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # Emit logs at different levels
    logger.debug("debug msg")
    logger.info("info msg")
    logger.warning("warning msg")
    logger.error("error msg")

    # Get all logs
    all_logs = handler.get_all_logs()
    assert len(all_logs) == 4

    # Get logs at WARNING and above
    warning_logs = handler.get_logs(min_level=logging.WARNING)
    assert len(warning_logs) == 2
    assert "warning msg" in warning_logs[0]
    assert "error msg" in warning_logs[1]

    # Clear and verify
    handler.clear()
    assert len(handler.get_all_logs()) == 0

    # Cleanup
    logger.removeHandler(handler)


# =============================================================================
# SafeModule Wrapper Tests (requires NiFi connection)
# =============================================================================


def test_safe_module_wraps_callable():
    """Test SafeModule wraps module functions."""
    from nipyapi.cli import SafeModule
    import nipyapi

    wrapped = SafeModule(nipyapi.canvas)

    # Check that get_root_pg_id is wrapped and callable
    assert callable(wrapped.get_root_pg_id)
    # Check docstring is preserved
    assert wrapped.get_root_pg_id.__doc__ is not None


def test_safe_module_call_success():
    """Test SafeModule successfully calls wrapped function."""
    from nipyapi.cli import SafeModule
    import nipyapi

    wrapped = SafeModule(nipyapi.canvas)
    result = wrapped.get_root_pg_id()

    # Should return a string (the root PG ID)
    assert isinstance(result, str)
    assert len(result) > 0


def test_safe_module_exposes_dir():
    """Test SafeModule exposes module attributes for Fire introspection."""
    from nipyapi.cli import SafeModule
    import nipyapi

    wrapped = SafeModule(nipyapi.canvas)
    attrs = dir(wrapped)

    # Should include key canvas functions
    assert "get_root_pg_id" in attrs
    assert "get_process_group" in attrs
    assert "list_all_processors" in attrs


def test_safe_module_error_handling():
    """Test SafeModule returns structured error on exception."""
    from nipyapi.cli import SafeModule
    from types import ModuleType

    # Create a mock module with a function that raises
    mock_module = ModuleType("mock_module")

    def failing_function():
        raise ValueError("Test error message")

    mock_module.failing_function = failing_function

    wrapped = SafeModule(mock_module)

    # Call the wrapped function - it should print error JSON and call sys.exit
    # We need to catch the SystemExit
    import io
    from contextlib import redirect_stdout

    # Force JSON output format (CI environments may have GITHUB_ACTIONS set)
    old_format = os.environ.get("NIFI_OUTPUT_FORMAT")
    os.environ["NIFI_OUTPUT_FORMAT"] = "json"

    captured = io.StringIO()
    try:
        with redirect_stdout(captured):
            wrapped.failing_function()
    except SystemExit as e:
        assert e.code == 1
    finally:
        # Restore original format
        if old_format is None:
            os.environ.pop("NIFI_OUTPUT_FORMAT", None)
        else:
            os.environ["NIFI_OUTPUT_FORMAT"] = old_format

    output = captured.getvalue()
    result = json.loads(output)
    assert result["success"] is False
    assert result["error"] == "Test error message"
    assert result["error_type"] == "ValueError"
    assert result["command"] == "failing_function"


def test_safe_module_with_log_level():
    """Test SafeModule includes logs when NIFI_LOG_LEVEL is set."""
    from nipyapi.cli import SafeModule
    from types import ModuleType
    import logging

    # Create a mock module with a function that logs
    mock_module = ModuleType("mock_module")

    def logging_function():
        logger = logging.getLogger("nipyapi.test")
        logger.info("Test log message")
        return {"result": "success"}

    mock_module.logging_function = logging_function

    wrapped = SafeModule(mock_module)

    # Set log level to capture logs
    old_level = os.environ.get("NIFI_LOG_LEVEL")
    try:
        os.environ["NIFI_LOG_LEVEL"] = "INFO"
        result = wrapped.logging_function()
        assert result["result"] == "success"
        # Logs should be included when log level is set
        if "logs" in result:
            assert any("Test log message" in log for log in result["logs"])
    finally:
        if old_level:
            os.environ["NIFI_LOG_LEVEL"] = old_level
        else:
            os.environ.pop("NIFI_LOG_LEVEL", None)


def test_safe_module_error_key_exits_nonzero():
    """Test SafeModule exits with code 1 when result contains 'error' key."""
    from nipyapi.cli import SafeModule
    from types import ModuleType
    import io
    from contextlib import redirect_stdout

    mock_module = ModuleType("mock_module")

    def function_with_error():
        return {"verified": "false", "error": "Verification failed for: component1"}

    mock_module.function_with_error = function_with_error

    wrapped = SafeModule(mock_module)

    # Force JSON output format
    old_format = os.environ.get("NIFI_OUTPUT_FORMAT")
    os.environ["NIFI_OUTPUT_FORMAT"] = "json"

    captured = io.StringIO()
    try:
        with redirect_stdout(captured):
            wrapped.function_with_error()
    except SystemExit as e:
        assert e.code == 1
    finally:
        if old_format is None:
            os.environ.pop("NIFI_OUTPUT_FORMAT", None)
        else:
            os.environ["NIFI_OUTPUT_FORMAT"] = old_format

    output = captured.getvalue()
    result = json.loads(output)
    assert result["verified"] == "false"
    assert result["error"] == "Verification failed for: component1"


def test_safe_module_errors_key_exits_nonzero():
    """Test SafeModule exits with code 1 when result contains 'errors' key."""
    from nipyapi.cli import SafeModule
    from types import ModuleType
    import io
    from contextlib import redirect_stdout

    mock_module = ModuleType("mock_module")

    def function_with_errors():
        return {"parameters_updated": "0", "errors": "Parameter 'X' not found"}

    mock_module.function_with_errors = function_with_errors

    wrapped = SafeModule(mock_module)

    # Force JSON output format
    old_format = os.environ.get("NIFI_OUTPUT_FORMAT")
    os.environ["NIFI_OUTPUT_FORMAT"] = "json"

    captured = io.StringIO()
    try:
        with redirect_stdout(captured):
            wrapped.function_with_errors()
    except SystemExit as e:
        assert e.code == 1
    finally:
        if old_format is None:
            os.environ.pop("NIFI_OUTPUT_FORMAT", None)
        else:
            os.environ["NIFI_OUTPUT_FORMAT"] = old_format

    output = captured.getvalue()
    result = json.loads(output)
    assert result["parameters_updated"] == "0"
    assert result["errors"] == "Parameter 'X' not found"


def test_safe_module_no_error_exits_zero():
    """Test SafeModule returns normally when no error key present."""
    from nipyapi.cli import SafeModule
    from types import ModuleType

    mock_module = ModuleType("mock_module")

    def success_function():
        return {"verified": "true", "summary": "All 5 components passed verification"}

    mock_module.success_function = success_function

    wrapped = SafeModule(mock_module)

    # Should return result directly, no SystemExit
    result = wrapped.success_function()
    assert result["verified"] == "true"
    assert result["summary"] == "All 5 components passed verification"


# =============================================================================
# Integration Tests (subprocess, requires NiFi)
# =============================================================================


def test_cli_help_no_nifi():
    """Test CLI --help works without NiFi connection."""
    import subprocess
    result = subprocess.run(
        ["python", "-m", "nipyapi.cli", "--", "--help"],
        capture_output=True,
        text=True,
        timeout=10
    )
    # Fire shows command groups in stderr
    output = result.stdout + result.stderr
    assert "ci" in output or "canvas" in output
    # Should not error
    assert result.returncode == 0


def test_cli_layout_constants():
    """Test CLI can access layout module constants."""
    import subprocess
    result = subprocess.run(
        ["python", "-m", "nipyapi.cli", "layout", "PROCESSOR_WIDTH"],
        capture_output=True,
        text=True,
        timeout=10
    )
    # Should return the constant value (352 based on empirical measurement)
    assert result.returncode == 0
    assert "352" in result.stdout


def test_cli_version_long_flag():
    """Test CLI --version works and shows version."""
    import subprocess
    result = subprocess.run(
        ["python", "-m", "nipyapi.cli", "--version"],
        capture_output=True,
        text=True,
        timeout=10
    )
    assert result.returncode == 0
    assert "nipyapi" in result.stdout
    # Should contain a version number pattern (e.g., 0.21.0 or 0.21.0.dev123)
    import re
    assert re.search(r"\d+\.\d+", result.stdout)


def test_cli_version_short_flag():
    """Test CLI -V works and shows version."""
    import subprocess
    result = subprocess.run(
        ["python", "-m", "nipyapi.cli", "-V"],
        capture_output=True,
        text=True,
        timeout=10
    )
    assert result.returncode == 0
    assert "nipyapi" in result.stdout
    import re
    assert re.search(r"\d+\.\d+", result.stdout)


# =============================================================================
# CLI Complex JSON Argument Tests (subprocess, no NiFi required)
# =============================================================================
# These tests verify that complex JSON arguments pass through the CLI correctly.
# They expect failures from PG lookup, NOT from JSON parsing.


def test_cli_configure_params_complex_json():
    """Test CLI handles complex JSON with nested structures."""
    import subprocess
    # Complex JSON with nested dict and list
    json_arg = '{"config": {"nested": "value"}, "items": ["a", "b"]}'
    # Force JSON output format (CI environments may have GITHUB_ACTIONS set)
    env = os.environ.copy()
    env["NIFI_OUTPUT_FORMAT"] = "json"
    result = subprocess.run(
        [
            "python", "-m", "nipyapi.cli",
            "ci", "configure_params",
            "--process_group_id", "nonexistent-pg",
            "--parameters", json_arg
        ],
        capture_output=True,
        text=True,
        timeout=30,
        env=env
    )
    # Should fail (no NiFi connection or PG not found), but NOT on JSON parsing
    assert result.returncode == 1
    error_data = json.loads(result.stdout)
    assert error_data["success"] is False
    # Key assertion: error should NOT be about JSON parsing
    assert "Invalid JSON" not in error_data["error"]


def test_cli_configure_params_json_with_quotes():
    """Test CLI handles JSON with embedded quotes."""
    import subprocess
    json_arg = '{"message": "value with \\"quotes\\""}'
    # Force JSON output format (CI environments may have GITHUB_ACTIONS set)
    env = os.environ.copy()
    env["NIFI_OUTPUT_FORMAT"] = "json"
    result = subprocess.run(
        [
            "python", "-m", "nipyapi.cli",
            "ci", "configure_params",
            "--process_group_id", "nonexistent-pg",
            "--parameters", json_arg
        ],
        capture_output=True,
        text=True,
        timeout=30,
        env=env
    )
    assert result.returncode == 1
    error_data = json.loads(result.stdout)
    assert "Invalid JSON" not in error_data["error"]


def test_cli_configure_params_json_with_newlines():
    """Test CLI handles JSON with escaped newlines."""
    import subprocess
    json_arg = '{"multiline": "line1\\nline2\\nline3"}'
    # Force JSON output format (CI environments may have GITHUB_ACTIONS set)
    env = os.environ.copy()
    env["NIFI_OUTPUT_FORMAT"] = "json"
    result = subprocess.run(
        [
            "python", "-m", "nipyapi.cli",
            "ci", "configure_params",
            "--process_group_id", "nonexistent-pg",
            "--parameters", json_arg
        ],
        capture_output=True,
        text=True,
        timeout=30,
        env=env
    )
    assert result.returncode == 1
    error_data = json.loads(result.stdout)
    assert "Invalid JSON" not in error_data["error"]


def test_cli_configure_params_json_with_backslashes():
    """Test CLI handles JSON with backslashes (Windows paths)."""
    import subprocess
    json_arg = '{"path": "C:\\\\Users\\\\data\\\\file.txt"}'
    # Force JSON output format (CI environments may have GITHUB_ACTIONS set)
    env = os.environ.copy()
    env["NIFI_OUTPUT_FORMAT"] = "json"
    result = subprocess.run(
        [
            "python", "-m", "nipyapi.cli",
            "ci", "configure_params",
            "--process_group_id", "nonexistent-pg",
            "--parameters", json_arg
        ],
        capture_output=True,
        text=True,
        timeout=30,
        env=env
    )
    assert result.returncode == 1
    error_data = json.loads(result.stdout)
    assert "Invalid JSON" not in error_data["error"]


def test_cli_configure_params_json_with_unicode():
    """Test CLI handles JSON with Unicode characters."""
    import subprocess
    json_arg = '{"greeting": "Hello \\u4e16\\u754c"}'
    # Force JSON output format (CI environments may have GITHUB_ACTIONS set)
    env = os.environ.copy()
    env["NIFI_OUTPUT_FORMAT"] = "json"
    result = subprocess.run(
        [
            "python", "-m", "nipyapi.cli",
            "ci", "configure_params",
            "--process_group_id", "nonexistent-pg",
            "--parameters", json_arg
        ],
        capture_output=True,
        text=True,
        timeout=30,
        env=env
    )
    assert result.returncode == 1
    error_data = json.loads(result.stdout)
    assert "Invalid JSON" not in error_data["error"]


def test_cli_configure_params_json_mixed_types():
    """Test CLI handles JSON with mixed value types."""
    import subprocess
    json_arg = '{"str": "text", "int": 42, "float": 3.14, "bool": true, "null": null}'
    # Force JSON output format (CI environments may have GITHUB_ACTIONS set)
    env = os.environ.copy()
    env["NIFI_OUTPUT_FORMAT"] = "json"
    result = subprocess.run(
        [
            "python", "-m", "nipyapi.cli",
            "ci", "configure_params",
            "--process_group_id", "nonexistent-pg",
            "--parameters", json_arg
        ],
        capture_output=True,
        text=True,
        timeout=30,
        env=env
    )
    assert result.returncode == 1
    error_data = json.loads(result.stdout)
    assert "Invalid JSON" not in error_data["error"]


def test_cli_configure_params_json_deep_nesting():
    """Test CLI handles deeply nested JSON structures."""
    import subprocess
    json_arg = '{"a": {"b": {"c": {"d": {"e": "deep"}}}}}'
    # Force JSON output format (CI environments may have GITHUB_ACTIONS set)
    env = os.environ.copy()
    env["NIFI_OUTPUT_FORMAT"] = "json"
    result = subprocess.run(
        [
            "python", "-m", "nipyapi.cli",
            "ci", "configure_params",
            "--process_group_id", "nonexistent-pg",
            "--parameters", json_arg
        ],
        capture_output=True,
        text=True,
        timeout=30,
        env=env
    )
    assert result.returncode == 1
    error_data = json.loads(result.stdout)
    assert "Invalid JSON" not in error_data["error"]


def test_cli_configure_params_invalid_json_error():
    """Test CLI returns proper error for invalid JSON."""
    import subprocess
    # Force JSON output format (CI environments may have GITHUB_ACTIONS set)
    env = os.environ.copy()
    env["NIFI_OUTPUT_FORMAT"] = "json"
    result = subprocess.run(
        [
            "python", "-m", "nipyapi.cli",
            "ci", "configure_params",
            "--process_group_id", "any-id",
            "--parameters", "{not valid json}"
        ],
        capture_output=True,
        text=True,
        timeout=30,
        env=env
    )
    assert result.returncode == 1
    error_data = json.loads(result.stdout)
    assert error_data["success"] is False
    # This one SHOULD fail on JSON parsing
    assert "Invalid JSON" in error_data["error"]
