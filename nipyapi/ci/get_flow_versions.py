"""
get_flow_versions - list version history for a versioned flow.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def get_flow_versions(
    process_group_id: Optional[str] = None,
) -> dict:
    """
    Get version history for a versioned flow.

    Lists all versions (commits) of a flow with their metadata including
    commit SHA, author, timestamp, and comments.

    Args:
        process_group_id: ID of the versioned process group.
                         Env: NIFI_PROCESS_GROUP_ID

    Returns:
        dict with:
          - flow_id: Flow identifier in registry
          - bucket_id: Bucket containing the flow
          - registry_id: Registry client ID
          - current_version: Currently deployed version
          - versions: List of version metadata

    Raises:
        ValueError: Missing required parameters or not under version control
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    log.info("Getting flow versions for: %s", process_group_id)

    # Get the process group
    pg = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not pg:
        raise ValueError(f"Process group not found: {process_group_id}")

    # Check if under version control
    vci = pg.component.version_control_information
    if not vci:
        raise ValueError(f"Process group '{pg.component.name}' is not under version control")

    log.debug(
        "Flow: %s, Registry: %s, Bucket: %s",
        vci.flow_id,
        vci.registry_id,
        vci.bucket_id,
    )

    # Get version history from registry
    versions_response = nipyapi.versioning.list_git_registry_flow_versions(
        registry_client_id=vci.registry_id,
        bucket_id=vci.bucket_id,
        flow_id=vci.flow_id,
    )

    # Format the versions
    versions = []
    for item in versions_response.versioned_flow_snapshot_metadata_set:
        meta = item.versioned_flow_snapshot_metadata
        versions.append(
            {
                "version": meta.version,
                "author": meta.author,
                "comments": meta.comments,
                "timestamp": meta.timestamp,
                "branch": meta.branch,
            }
        )

    log.info("Found %d versions", len(versions))

    return {
        "flow_id": vci.flow_id,
        "bucket_id": vci.bucket_id,
        "registry_id": vci.registry_id,
        "current_version": vci.version,
        "state": vci.state,
        "version_count": len(versions),
        "versions": versions,
    }
