"""
get_flow_diff - fetch local changes to a versioned flow.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def get_flow_diff(
    process_group_id: Optional[str] = None,
) -> dict:
    """
    Get local modifications to a versioned flow.

    Returns structured information about all local changes made to a
    version-controlled process group since the last commit/sync.

    Use this before upgrading a flow to capture modifications that
    need to be re-applied after the upgrade.

    This function uses nipyapi.versioning.get_local_modifications for
    the underlying API call.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID

    Returns:
        dict with:
          - process_group_id: ID of the process group
          - process_group_name: Name of the process group
          - flow_id: Flow ID in registry
          - current_version: Current committed version
          - state: Version control state
          - modification_count: Number of modified components
          - modifications: List of modification details

    Raises:
        ValueError: Missing required parameters or not under version control
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    log.info("Getting local modifications for: %s", process_group_id)

    # Get the process group for metadata
    pg = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not pg:
        raise ValueError(f"Process group not found: {process_group_id}")

    vci = pg.component.version_control_information
    if not vci:
        raise ValueError(f"Process group '{pg.component.name}' is not under version control")

    # Use the versioning helper to get local modifications
    result = nipyapi.versioning.get_local_modifications(pg)

    # Format modifications for CI output
    modifications = []
    for diff in result.component_differences:
        mod = {
            "component_id": diff.component_id,
            "component_name": diff.component_name,
            "component_type": diff.component_type,
            "changes": [],
        }
        for change in diff.differences:
            mod["changes"].append(
                {
                    "type": change.difference_type,
                    "description": change.difference,
                }
            )
        modifications.append(mod)

    log.info("Found %d modified components", len(modifications))

    return {
        "process_group_id": process_group_id,
        "process_group_name": pg.component.name,
        "flow_id": vci.flow_id,
        "current_version": vci.version,
        "state": vci.state,
        "modification_count": len(modifications),
        "modifications": modifications,
    }
