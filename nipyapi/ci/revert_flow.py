# pylint: disable=duplicate-code
"""
revert_flow - revert uncommitted local changes to a deployed flow.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def revert_flow(process_group_id: Optional[str] = None) -> dict:
    """
    Revert uncommitted changes to a deployed flow.

    Restores the process group to match the version tracked in the registry.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID

    Returns:
        dict with reverted, version, state

    Raises:
        ValueError: Missing required parameters or not under version control
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    log.info("Reverting flow: %s", process_group_id)

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
    current_version = current_vci.version
    current_state = current_vci.state

    log.debug("Current version: %s (%s)", current_version, current_state)

    # Check if revert is needed
    if current_state == "UP_TO_DATE":
        log.info("Flow already up to date, no changes to revert")
        return {
            "reverted": "false",
            "version": current_version,
            "state": current_state,
        }

    if current_state != "LOCALLY_MODIFIED":
        log.warning("Flow state is '%s', not 'LOCALLY_MODIFIED'", current_state)

    # Revert
    log.debug("Reverting local changes...")
    revert_result = nipyapi.versioning.revert_flow_ver(process_group, wait=True)

    final_state = revert_result.version_control_information.state
    final_version = revert_result.version_control_information.version

    log.info("Reverted to %s (%s)", final_version, final_state)

    return {
        "reverted": "true",
        "version": final_version,
        "state": final_state,
    }
