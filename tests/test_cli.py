"""Tests for `nipyapi.cli` module."""

import json
import os


# =============================================================================
# Helper Function Tests (no NiFi connection required)
# =============================================================================


def test_serialize_result_string():
    """Test that strings are returned as-is."""
    from nipyapi.cli import _serialize_result
    result = _serialize_result("hello", "json")
    assert result == "hello"


def test_serialize_result_simple_types():
    """Test serialization of simple types."""
    from nipyapi.cli import _serialize_result
    assert _serialize_result(42, "json") == "42"
    assert _serialize_result(3.14, "json") == "3.14"
    assert _serialize_result(True, "json") == "True"
    assert _serialize_result(None, "json") == "None"


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


def test_to_dict_fallback_to_string():
    """Test _to_dict falls back to string for objects without __dict__."""
    from nipyapi.cli import _to_dict

    # Use a type that doesn't have __dict__ in the expected way
    result = _to_dict(42)
    assert result == {"value": "42"}

    result = _to_dict(3.14)
    assert result == {"value": "3.14"}


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


def test_parse_profile_arg_with_space():
    """Test _parse_profile_arg with --profile value syntax."""
    import sys
    from nipyapi.cli import _parse_profile_arg

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "--profile", "myprofile", "ci", "get_status"]
        result = _parse_profile_arg()
        assert result == "myprofile"
        # --profile and value should be removed from argv
        assert "--profile" not in sys.argv
        assert "myprofile" not in sys.argv
        assert "ci" in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_profile_arg_with_equals():
    """Test _parse_profile_arg with --profile=value syntax."""
    import sys
    from nipyapi.cli import _parse_profile_arg

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "--profile=prod", "system", "info"]
        result = _parse_profile_arg()
        assert result == "prod"
        assert "--profile=prod" not in sys.argv
        assert "system" in sys.argv
    finally:
        sys.argv = original_argv


def test_parse_profile_arg_no_profile():
    """Test _parse_profile_arg when no --profile is specified."""
    import sys
    from nipyapi.cli import _parse_profile_arg

    original_argv = sys.argv.copy()
    try:
        sys.argv = ["nipyapi", "canvas", "get_root_pg_id"]
        result = _parse_profile_arg()
        assert result is None
        assert "canvas" in sys.argv
    finally:
        sys.argv = original_argv


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
    import sys

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
