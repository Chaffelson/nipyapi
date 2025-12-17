"""
commit_flow - save flow to version control (initial or subsequent commit).
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def commit_flow(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    process_group_id: Optional[str] = None,
    comment: Optional[str] = None,
    registry_client: Optional[str] = None,
    bucket: Optional[str] = None,
    flow_name: Optional[str] = None,
    force: bool = False,
) -> dict:
    """
    Commit a flow to version control.

    For flows already under version control, saves a new version with the
    provided comment. For new flows, starts version control by saving the
    initial version to the specified registry client and bucket.

    This function uses nipyapi.versioning.save_git_flow_ver for Git-based
    registries (GitHub, GitLab, etc.).

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID
        comment: Commit message describing the changes. Env: NIFI_COMMIT_COMMENT
        registry_client: Registry client name (for initial commit only).
                        Env: NIFI_REGISTRY_CLIENT
        bucket: Bucket/folder name (for initial commit only). Env: NIFI_BUCKET
        flow_name: Name for the flow in registry (for initial commit only).
                  Defaults to process group name. Env: NIFI_FLOW_NAME
        force: If True, use FORCE_COMMIT to ignore merge conflicts.

    Returns:
        dict with:
          - flow_id: Flow identifier in registry
          - version: Commit SHA of the new version
          - state: Version control state after commit
          - initial_commit: True if this was the first commit

    Raises:
        ValueError: Missing required parameters or registry not found
    """
    # Resolve from env vars
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    comment = comment or os.environ.get("NIFI_COMMIT_COMMENT") or ""
    registry_client = registry_client or os.environ.get("NIFI_REGISTRY_CLIENT")
    bucket = bucket or os.environ.get("NIFI_BUCKET")
    flow_name = flow_name or os.environ.get("NIFI_FLOW_NAME")

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    log.info("Committing flow: %s", process_group_id)

    # Get the process group to check current state
    pg = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not pg:
        raise ValueError(f"Process group not found: {process_group_id}")

    # Check if already under version control
    vci = pg.component.version_control_information
    initial_commit = vci is None

    # Check for no-op case (UP_TO_DATE with no changes)
    if not initial_commit and vci.state == "UP_TO_DATE":
        log.warning("Flow has no local modifications")
        return {
            "flow_id": vci.flow_id,
            "version": vci.version,
            "state": vci.state,
            "initial_commit": False,
            "message": "No local modifications to commit",
        }

    # Use the versioning helper for Git-based registries
    result = nipyapi.versioning.save_git_flow_ver(
        process_group=pg,
        registry_client=registry_client,
        bucket=bucket,
        flow_name=flow_name,
        comment=comment,
        force=force,
        refresh=False,  # Already fetched fresh PG above
    )

    new_vci = result.version_control_information

    log.info(
        "Committed: %s (version: %s)",
        new_vci.flow_id,
        new_vci.version[:12] if new_vci.version else "unknown",
    )

    return {
        "flow_id": new_vci.flow_id,
        "version": new_vci.version,
        "state": new_vci.state,
        "initial_commit": initial_commit,
    }
