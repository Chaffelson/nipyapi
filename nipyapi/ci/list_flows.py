# pylint: disable=broad-exception-caught
"""
list_flows - list flows (process groups) with their version control state.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def list_flows(  # pylint: disable=too-many-locals
    process_group_id: Optional[str] = None,
    descendants: Optional[bool] = None,
) -> dict:
    """
    List flows (process groups) with their version control state.

    Lists flows under the specified parent (or root) with their
    version control state, making it easy to see which flows need updates.

    Args:
        process_group_id: Parent process group ID to start from.
                         Env: NIFI_PROCESS_GROUP_ID.
                         If not provided, defaults to root process group.
        descendants: If True, include all nested process groups recursively.
                    If False (default), only show immediate children.
                    Env: NIFI_INCLUDE_DESCENDANTS.

    Returns:
        dict with:
        - parent_id: The parent process group ID searched from
        - parent_name: The parent process group name
        - total_count: Total number of process groups found
        - versioned_count: Number of version-controlled process groups
        - stale_count: Number of process groups with available updates
        - modified_count: Number of locally modified process groups
        - process_groups: List of dicts with version info for each PG

    Each process_group entry contains:
        - id, name: Process group identification
        - versioned: Whether under version control
        - current_version: Current version (or empty)
        - state: Version state (UP_TO_DATE, STALE, LOCALLY_MODIFIED, etc.)
        - modified: Whether local changes exist
        - flow_name, bucket_name: Registry flow info

    Examples:
        # List immediate child process groups from root
        nipyapi ci list_flows

        # List all process groups recursively
        nipyapi ci list_flows --descendants

        # List process groups under a specific parent
        nipyapi ci list_flows --process_group_id PG_ID
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")

    # Handle descendants flag from env var if not explicitly set
    if descendants is None:
        descendants = nipyapi.utils.getenv_bool("NIFI_INCLUDE_DESCENDANTS", False)

    # Default to root process group if not specified
    if not process_group_id:
        process_group_id = nipyapi.canvas.get_root_pg_id()
        log.info("No process_group_id specified, using root process group")

    log.info("Getting version info for process groups under: %s", process_group_id)

    # Get parent info
    parent_pg = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not parent_pg:
        raise ValueError(f"Process group not found: {process_group_id}")

    parent_name = parent_pg.component.name

    # Get child process groups
    if descendants:
        # Recursive: get all nested process groups
        all_pgs = nipyapi.canvas.list_all_process_groups(process_group_id)
        # Remove the parent from the list (it gets included)
        all_pgs = [pg for pg in all_pgs if pg.id != process_group_id]
        log.debug("Including all descendants")
    else:
        # Immediate children only
        flow = nipyapi.canvas.get_flow(process_group_id)
        all_pgs = flow.process_group_flow.flow.process_groups or []
        log.debug("Immediate children only")
    log.debug("Found %d process groups", len(all_pgs))

    process_groups = []
    versioned_count = 0
    stale_count = 0
    modified_count = 0

    for pg in all_pgs:
        pg_id = pg.id
        pg_name = pg.component.name if pg.component else "Unknown"

        entry = {
            "id": pg_id,
            "name": pg_name,
            "versioned": "false",
            "current_version": "",
            "state": "",
            "modified": "false",
            "flow_name": "",
            "bucket_name": "",
        }

        # Check version control info
        try:
            vci = pg.component.version_control_information if pg.component else None
            if vci:
                versioned_count += 1
                entry["versioned"] = "true"
                entry["current_version"] = str(vci.version) if vci.version else ""
                entry["state"] = vci.state or ""
                entry["flow_name"] = vci.flow_name or ""
                entry["bucket_name"] = vci.bucket_name or ""

                # Check if modified or stale
                if vci.state in ("LOCALLY_MODIFIED", "LOCALLY_MODIFIED_AND_STALE"):
                    entry["modified"] = "true"
                    modified_count += 1
                if vci.state in ("STALE", "LOCALLY_MODIFIED_AND_STALE"):
                    stale_count += 1

                log.debug("  %s: v%s (%s)", pg_name, entry["current_version"], entry["state"])
        except Exception as e:
            log.debug("Could not get version info for %s: %s", pg_name, e)

        process_groups.append(entry)

    # Sort by name for consistent output
    process_groups.sort(key=lambda x: x["name"].lower())

    log.info(
        "Found %d process groups: %d versioned, %d stale, %d modified",
        len(process_groups),
        versioned_count,
        stale_count,
        modified_count,
    )

    return {
        "parent_id": process_group_id,
        "parent_name": parent_name,
        "total_count": str(len(process_groups)),
        "versioned_count": str(versioned_count),
        "stale_count": str(stale_count),
        "modified_count": str(modified_count),
        "process_groups": process_groups,
    }
