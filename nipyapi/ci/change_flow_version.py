"""
change_flow_version - change the version of a deployed flow.
"""

import logging
import os
from typing import Optional

import nipyapi

from .resolve_git_ref import resolve_git_ref

log = logging.getLogger(__name__)


def change_flow_version(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    process_group_id: Optional[str] = None,
    target_version: Optional[str] = None,
    branch: Optional[str] = None,
    token: Optional[str] = None,
    repo: Optional[str] = None,
    provider: Optional[str] = None,
) -> dict:
    """
    Change the version of a deployed flow.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID
        target_version: Version to change to (commit SHA, tag, or branch name).
                       Env: NIFI_TARGET_VERSION. If None, changes to latest.
        branch: Branch to use. Env: NIFI_FLOW_BRANCH
        token: Git token for resolving tags. Env: GH_REGISTRY_TOKEN or GL_REGISTRY_TOKEN
        repo: Repository in owner/repo format. Env: NIFI_REGISTRY_REPO
        provider: Git provider (github/gitlab). Env: NIFI_REGISTRY_PROVIDER

    Returns:
        dict with previous_version, new_version, version_state

    Raises:
        ValueError: Missing required parameters or not under version control
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    target_version = target_version or os.environ.get("NIFI_TARGET_VERSION") or None
    branch = branch or os.environ.get("NIFI_FLOW_BRANCH") or None
    provider = provider or os.environ.get("NIFI_REGISTRY_PROVIDER", "github")
    repo = repo or os.environ.get("NIFI_REGISTRY_REPO")

    # Get token based on provider
    if not token:
        if provider == "gitlab":
            token = os.environ.get("GL_REGISTRY_TOKEN")
        else:
            token = os.environ.get("GH_REGISTRY_TOKEN")

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    log.info("Changing version for: %s", process_group_id)

    # Get process group
    process_group = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not process_group:
        raise ValueError(f"Process group not found: {process_group_id}")

    # Get current version info
    version_info = nipyapi.versioning.get_version_info(process_group)
    if not version_info or not version_info.version_control_information:
        raise ValueError(
            f"Process group '{process_group.component.name}' is not under version control"
        )

    current_vci = version_info.version_control_information
    previous_version = current_vci.version

    log.debug("Current version: %s (%s)", previous_version, current_vci.state)

    # Resolve target version (tag/branch) to SHA if needed
    resolved_version = resolve_git_ref(target_version, repo, token, provider)

    if resolved_version:
        log.info("Target version: %s (resolved to %s)", target_version, resolved_version[:12])
    else:
        log.info("Target version: latest")

    # Change version
    nipyapi.versioning.update_git_flow_ver(
        process_group=process_group,
        target_version=resolved_version,
        branch=branch,
    )

    # Get updated version info
    updated_pg = nipyapi.canvas.get_process_group(process_group_id, "id")
    updated_vci = nipyapi.versioning.get_version_info(updated_pg)
    new_version = updated_vci.version_control_information.version
    new_state = updated_vci.version_control_information.state

    log.info("Changed from %s to %s (%s)", previous_version[:12], new_version[:12], new_state)

    return {
        "previous_version": previous_version,
        "new_version": new_version,
        "version_state": new_state,
    }
