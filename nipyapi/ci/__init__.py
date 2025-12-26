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

from .change_flow_version import change_flow_version
from .cleanup import cleanup
from .commit_flow import commit_flow
from .configure_inherited_params import configure_inherited_params
from .configure_params import configure_params
from .delete_nar import delete_nar
from .deploy_flow import deploy_flow
from .detach_flow import detach_flow
from .ensure_registry import ensure_registry
from .export_flow_definition import export_flow_definition
from .get_flow_diff import get_flow_diff
from .get_flow_versions import get_flow_versions
from .get_status import get_status
from .import_flow_definition import import_flow_definition
from .list_flows import list_flows
from .list_nars import list_nars
from .list_registry_flows import list_registry_flows
from .purge_flowfiles import purge_flowfiles
from .resolve_git_ref import resolve_git_ref
from .revert_flow import revert_flow
from .start_flow import start_flow
from .stop_flow import stop_flow
from .upload_asset import upload_asset
from .upload_nar import upload_nar
from .verify_config import verify_config

__all__ = [
    "ensure_registry",
    "deploy_flow",
    "start_flow",
    "stop_flow",
    "get_status",
    "list_flows",
    "list_registry_flows",
    "get_flow_versions",
    "get_flow_diff",
    "commit_flow",
    "detach_flow",
    "configure_params",
    "configure_inherited_params",
    "change_flow_version",
    "revert_flow",
    "cleanup",
    "purge_flowfiles",
    "resolve_git_ref",
    "upload_asset",
    "export_flow_definition",
    "import_flow_definition",
    "list_nars",
    "upload_nar",
    "delete_nar",
    "verify_config",
]
