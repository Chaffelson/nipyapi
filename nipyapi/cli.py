# pylint: disable=broad-exception-caught,import-outside-toplevel
"""
CLI entry point for nipyapi using Google Fire.

Provides command-line access to all nipyapi modules plus high-level CI operations.

Usage:
    nipyapi ci ensure_registry --token TOKEN --repo owner/repo
    nipyapi canvas get_process_group PG_ID
    nipyapi versioning list_registry_clients
    nipyapi layout align_pg_grid PG_ID --sort_by_name=True

    # Explicit profile selection (recommended for multi-profile setups)
    nipyapi --profile my_runtime ci get_status PG_ID
    nipyapi --profile prod_runtime system get_nifi_version_info

Global Flags:
    --version, -V       Show nipyapi version and exit
    -v                  Increase verbosity (INFO level)
    -vv                 More verbose (DEBUG level)
    --profile NAME      Select named profile from profiles file

Installation:
    pip install nipyapi[cli]

Or with uvx (no install):
    uvx --from "nipyapi[cli]" nipyapi ci ensure_registry --help

Configuration:
    The CLI auto-detects configuration using this priority:
    1. --profile argument (explicit profile selection)
    2. Environment variables (if NIFI_API_ENDPOINT is set)
    3. NIPYAPI_PROFILE env var (selects named profile from profiles file)
    4. First profile in ~/.nipyapi/profiles.yml
    5. No configuration (commands will fail with helpful error)

    Environment variables (for CI/CD):
    NIFI_API_ENDPOINT              NiFi API URL
    NIFI_BEARER_TOKEN              JWT bearer token
    NIFI_USERNAME / NIFI_PASSWORD  Basic auth (alternative to token)
    NIFI_VERIFY_SSL                SSL verification (default: true)

    User profiles file (for interactive use):
    Create ~/.nipyapi/profiles.yml with your runtime configuration.
    See nipyapi.profiles for full configuration options.

Output Formatting:
    Complex objects are serialized to JSON by default. Override with:
    NIFI_OUTPUT_FORMAT=github   GitHub Actions format (key=value, heredoc for complex)
    NIFI_OUTPUT_FORMAT=dotenv   GitLab CI format (KEY=VALUE)
    NIFI_OUTPUT_FORMAT=json     JSON format (default)

    CI environments are auto-detected via GITHUB_ACTIONS or GITLAB_CI env vars.

Log Level Control:
    NIFI_LOG_LEVEL=WARNING      Default - only warnings and errors in output
    NIFI_LOG_LEVEL=ERROR        Only errors
    NIFI_LOG_LEVEL=INFO         Normal operational info
    NIFI_LOG_LEVEL=DEBUG        Full debug output
"""

import json
import logging
import os
import sys


def _detect_output_format():
    """
    Detect the appropriate output format based on environment.

    Priority:
    1. Explicit NIFI_OUTPUT_FORMAT env var
    2. Auto-detect CI environment (GITHUB_ACTIONS, GITLAB_CI)
    3. Default to 'json' for structured output
    """
    explicit = os.environ.get("NIFI_OUTPUT_FORMAT")
    if explicit:
        return explicit.lower()

    # Auto-detect CI environments
    if os.environ.get("GITHUB_ACTIONS"):
        return "github"
    if os.environ.get("GITLAB_CI"):
        return "dotenv"

    # Default to JSON for complex objects
    return "json"


def _format_dotenv_value(key, value):
    """Format a key-value pair for dotenv output, quoting if needed."""
    # JSON-serialize lists/dicts for valid output, str() for scalars
    if isinstance(value, (list, dict)):
        v_str = json.dumps(value, default=str)
    else:
        v_str = str(value)
    # Skip multiline values (GitLab limitation)
    if "\n" in v_str or len(v_str) >= 1000:
        return None
    # Characters that require quoting for safe shell parsing
    special_chars = set(" \t|&;<>()$`\\\"'*?[]#~=!{}^")
    if any(c in v_str for c in special_chars):
        # Escape embedded double quotes
        v_escaped = v_str.replace('"', '\\"')
        return f'{key.upper()}="{v_escaped}"'
    return f"{key.upper()}={v_str}"


def _serialize_result(obj, output_format="json"):  # pylint: disable=too-many-return-statements
    """
    Serialize an object for CLI output.

    Handles nipyapi model objects by converting to dict via swagger's to_dict().
    """
    # Already a string - return as-is
    if isinstance(obj, str):
        return obj

    # Simple types - return string representation
    if isinstance(obj, (int, float, bool, type(None))):
        return str(obj)

    # Lists - serialize each item
    if isinstance(obj, list):
        items = [_to_dict(item) for item in obj]
        if output_format == "json":
            return json.dumps(items, indent=2, default=str)
        return "\n".join(json.dumps(item, default=str) for item in items)

    # Convert to dict
    data = _to_dict(obj)

    if output_format == "github":
        # GitHub Actions format: key=value, or heredoc for complex values
        # Convert snake_case keys to kebab-case (GitHub convention)
        lines = []
        for k, v in _flatten_dict(data).items():
            # Convert snake_case to kebab-case for GitHub Actions
            key = k.replace("_", "-")
            # JSON-serialize lists/dicts for valid output, str() for scalars
            if isinstance(v, (list, dict)):
                v_str = json.dumps(v, default=str)
            else:
                v_str = str(v)
            # Use heredoc syntax for multiline or very long values
            if "\n" in v_str or len(v_str) > 500:
                lines.append(f"{key}<<EOF")
                lines.append(v_str)
                lines.append("EOF")
            else:
                lines.append(f"{key}={v_str}")
        return "\n".join(lines)
    if output_format == "dotenv":
        # GitLab dotenv format: KEY=VALUE (quoted if special chars)
        lines = [_format_dotenv_value(k, v) for k, v in _flatten_dict(data).items()]
        return "\n".join(line for line in lines if line is not None)
    # JSON format (default)
    return json.dumps(data, indent=2, default=str)


def _to_dict(obj):
    """Convert an object to a dictionary."""
    # Has swagger's to_dict method
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    # Already a dict
    if isinstance(obj, dict):
        return obj
    # Fallback - use __dict__ or str
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return {"value": str(obj)}


def _flatten_dict(d, parent_key="", sep="_"):
    """Flatten nested dict for key=value output formats."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def _get_log_level():
    """
    Get the configured log level from environment.

    Default is None (no logs in output for success, all logs for errors).
    Users can set NIFI_LOG_LEVEL to ERROR, WARNING, INFO, or DEBUG to
    always include logs at that level.
    """
    level_name = os.environ.get("NIFI_LOG_LEVEL", "").upper()
    if not level_name:
        return None  # No logs by default for success
    return getattr(logging, level_name, logging.WARNING)


def _get_log_on_error():
    """
    Check if logs should be included on error.

    Default is True (include logs on error for debugging).
    Set NIFI_LOG_ON_ERROR=false to suppress logs even on errors.
    """
    value = os.environ.get("NIFI_LOG_ON_ERROR", "true").lower()
    return value not in ("false", "0", "no", "off")


class LogCapture(logging.Handler):
    """
    Handler that captures log records to a list.

    Captures all logs at DEBUG level, but provides filtered access
    based on the configured log level.
    """

    def __init__(self):
        super().__init__()
        self.records = []
        self.all_records = []  # Keep all records for error output

    def emit(self, record):
        formatted = self.format(record)
        self.all_records.append(formatted)
        # Also keep track of level for filtering
        self.records.append((record.levelno, formatted))

    def get_logs(self, min_level=None):
        """
        Return captured log records at or above the specified level.

        Args:
            min_level: Minimum log level (default: None = return all)
        """
        if min_level is None:
            return [msg for _, msg in self.records]
        return [msg for level, msg in self.records if level >= min_level]

    def get_all_logs(self):
        """Return all captured log records (for error output)."""
        return [msg for _, msg in self.records]

    def clear(self):
        """Clear captured log records."""
        self.records = []
        self.all_records = []


def _custom_serializer(obj):
    """
    Custom serializer for Fire output.

    Converts complex nipyapi objects to formatted strings instead of showing
    Fire's default object exploration mode.
    """
    output_format = _detect_output_format()
    return _serialize_result(obj, output_format)


class SafeModule:
    """
    Wrapper that catches exceptions and returns structured error responses.

    This makes all nipyapi modules LLM-friendly by ensuring errors are returned
    as parseable JSON rather than exceptions/stack traces. Also captures logs.
    """

    def __init__(self, module):
        self._module = module

    def __getattr__(self, name):
        attr = getattr(self._module, name)
        if callable(attr):
            return self._wrap_callable(attr, name)
        return attr

    def _wrap_callable(self, func, name):
        """Wrap a callable to catch exceptions and return structured errors."""

        def wrapper(*args, **kwargs):
            # Set up log capture on nipyapi logger only (avoids duplicates)
            log_capture = LogCapture()
            log_capture.setLevel(logging.DEBUG)
            log_capture.setFormatter(logging.Formatter("%(name)s: %(message)s"))

            nipyapi_logger = logging.getLogger("nipyapi")
            original_level = nipyapi_logger.level
            nipyapi_logger.addHandler(log_capture)
            nipyapi_logger.setLevel(logging.DEBUG)

            try:
                result = func(*args, **kwargs)

                # Get configured log level (None = no logs for success)
                log_level = _get_log_level()

                # If result is a dict, optionally add logs
                if isinstance(result, dict):
                    if log_level is not None:
                        # User explicitly requested logs at this level
                        logs = log_capture.get_logs(min_level=log_level)
                        if logs:
                            result["logs"] = logs
                    # else: no logs for clean output on success
                    return result
                # For non-dict results, return as-is
                return result

            except Exception as e:
                output_format = _detect_output_format()
                # Include logs on error unless explicitly disabled
                error_result = {
                    "success": False,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "command": name,
                }
                if _get_log_on_error():
                    error_result["logs"] = log_capture.get_all_logs()
                # Print error and exit with non-zero code
                print(_serialize_result(error_result, output_format))
                sys.exit(1)

            finally:
                # Clean up handler
                nipyapi_logger.removeHandler(log_capture)
                nipyapi_logger.setLevel(original_level)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    def __dir__(self):
        """Expose module's attributes for Fire introspection."""
        return dir(self._module)


def _parse_cli_flags():
    """
    Parse global CLI flags from sys.argv before Fire processes them.

    Handles:
        --version, -V: Show version and exit
        -v, -vv, -vvv: Increase verbosity (maps to log levels)
        --profile NAME: Select named profile

    Returns:
        tuple: (show_version: bool, verbosity: int, profile: str or None)

    Side effect:
        Removes parsed flags from sys.argv so Fire doesn't see them.
    """
    show_version = False
    verbosity = 0
    profile = None
    new_argv = [sys.argv[0]]
    i = 1

    while i < len(sys.argv):
        arg = sys.argv[i]

        # Version flags
        if arg in ("--version", "-V"):
            show_version = True
            i += 1

        # Verbosity flags: -v, -vv, -vvv, or multiple -v
        elif arg == "-v":
            verbosity += 1
            i += 1
        elif arg.startswith("-v") and all(c == "v" for c in arg[1:]):
            # Handle -vv, -vvv, etc.
            verbosity += len(arg) - 1
            i += 1

        # Profile flags
        elif arg == "--profile" and i + 1 < len(sys.argv):
            profile = sys.argv[i + 1]
            i += 2  # Skip both --profile and its value
        elif arg.startswith("--profile="):
            profile = arg.split("=", 1)[1]
            i += 1

        else:
            new_argv.append(arg)
            i += 1

    sys.argv = new_argv
    return show_version, verbosity, profile


def _apply_verbosity(verbosity):
    """
    Apply verbosity level to logging configuration.

    Args:
        verbosity: 0=WARNING (default), 1=INFO, 2+=DEBUG
    """
    if verbosity >= 2:
        os.environ["NIFI_LOG_LEVEL"] = "DEBUG"
    elif verbosity == 1:
        os.environ["NIFI_LOG_LEVEL"] = "INFO"
    # verbosity 0: leave as default (WARNING or unset)


def main():
    """CLI entry point."""
    # Suppress SSL warnings early to prevent them polluting stdout in CI
    # This is safe as the warnings are informational and CLI users expect clean output
    import urllib3

    if os.environ.get("NIFI_VERIFY_SSL", "true").lower() in ("false", "0", "no"):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Parse global flags before Fire sees them
    show_version, verbosity, explicit_profile = _parse_cli_flags()

    # Import nipyapi modules
    import nipyapi
    from nipyapi import ci

    # Handle --version flag
    if show_version:
        print(f"nipyapi {nipyapi.__version__}")
        sys.exit(0)

    # Apply verbosity to logging
    if verbosity > 0:
        _apply_verbosity(verbosity)

    try:
        import fire
    except ImportError:
        print("CLI requires the 'fire' package.")
        print("Install with: pip install nipyapi[cli]")
        sys.exit(1)

    # Auto-configure NiFi connection.
    # Priority: explicit --profile arg > NIFI_API_ENDPOINT > NIPYAPI_PROFILE > first profile
    # This matches AWS CLI / gcloud pattern - just works without explicit config
    try:
        nipyapi.profiles.switch(explicit_profile)
    except ValueError:
        pass  # No configuration found - errors will surface on first API call

    # Create CLI interface with docstring that Fire will display in help
    # pylint: disable=too-many-instance-attributes,too-few-public-methods
    class CLI:
        """NiPyAPI command-line interface for Apache NiFi automation.

        Profile Selection (use --profile before any command):
            nipyapi --profile <name> <command>     Explicit profile selection
            nipyapi --profile prod ci get_status   Example with CI module

        Configuration Priority:
            1. --profile argument (explicit)
            2. NIFI_API_ENDPOINT env var (CI/CD mode)
            3. NIPYAPI_PROFILE env var (named profile)
            4. First profile in ~/.nipyapi/profiles.yml

        Quick Start:
            nipyapi system get_nifi_version_info   Test connectivity
            nipyapi ci get_status <pg_id>          Get process group status
            nipyapi --profile prod ci deploy_flow  Deploy with explicit profile

        Full documentation: https://nipyapi.readthedocs.io/
        """

        def __init__(self):
            self.ci = SafeModule(ci)
            self.canvas = SafeModule(nipyapi.canvas)
            self.versioning = SafeModule(nipyapi.versioning)
            self.parameters = SafeModule(nipyapi.parameters)
            self.security = SafeModule(nipyapi.security)
            self.system = SafeModule(nipyapi.system)
            self.layout = SafeModule(nipyapi.layout)
            self.extensions = SafeModule(nipyapi.extensions)
            self.config = nipyapi.config
            self.profiles = nipyapi.profiles
            self.utils = nipyapi.utils

    fire.Fire(CLI, serialize=_custom_serializer)


if __name__ == "__main__":
    main()
