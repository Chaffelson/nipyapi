"""
CI convenience functions for NiFi flow management.

These functions wrap nipyapi operations with:
- Environment variable support for CI/CD platforms
- Sensible defaults
- Simplified interfaces

They return plain dicts and raise exceptions on error.
The CLI handles output formatting, logging capture, and exit codes.

Example:
    nipyapi ci ensure_registry --repo owner/repo
    nipyapi ci deploy_flow --bucket flows --flow my-flow
    nipyapi ci start_flow

Profile resolution:
    CI functions auto-detect configuration source:
    1. If NIFI_API_ENDPOINT env var is set, use environment variables
    2. Otherwise, use first profile from ~/.nipyapi/profiles.yml if it exists
    3. Fall back to development examples if neither available
"""

from .change_version import change_version
from .cleanup import cleanup
from .configure_inherited_params import configure_inherited_params
from .configure_params import configure_params
from .deploy_flow import deploy_flow
from .ensure_registry import ensure_registry
from .get_status import get_status
from .get_versions import get_versions
from .purge_flowfiles import purge_flowfiles
from .resolve_git_ref import resolve_git_ref
from .revert_flow import revert_flow
from .start_flow import start_flow
from .stop_flow import stop_flow
from .upload_asset import upload_asset

__all__ = [
    "ensure_registry",
    "deploy_flow",
    "start_flow",
    "stop_flow",
    "get_status",
    "get_versions",
    "configure_params",
    "configure_inherited_params",
    "change_version",
    "revert_flow",
    "cleanup",
    "purge_flowfiles",
    "resolve_git_ref",
    "upload_asset",
]
