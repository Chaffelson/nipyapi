# pylint: disable=broad-exception-caught
"""
purge_flowfiles - drop all queued flow files from a process group.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def purge_flowfiles(
    process_group_id: Optional[str] = None,
    stop: bool = True,
) -> dict:
    """
    Purge all queued flow files from a process group.

    This drops all FlowFiles from all connections within the process group.
    Useful for clearing stuck data or recovering from failed states.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID
        stop: Stop the process group before purging (recommended).
            Default: True

    Returns:
        dict with purge results

    Raises:
        ValueError: Missing required parameters

    Examples:
        # Purge with stop (safest)
        nipyapi ci purge_flowfiles --process_group_id PG_ID

        # Purge without stopping (use with caution)
        nipyapi ci purge_flowfiles --process_group_id PG_ID --stop false
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    nipyapi.profiles.switch()

    log.info("Purging flow files from process group: %s", process_group_id)

    # Get process group
    try:
        process_group = nipyapi.canvas.get_process_group(process_group_id, "id")
    except nipyapi.nifi.rest.ApiException as e:
        if e.status == 404:
            raise ValueError(f"Process group not found: {process_group_id}") from e
        raise

    if not process_group:
        raise ValueError(f"Process group not found: {process_group_id}")

    pg_name = process_group.component.name
    log.debug("Found process group: %s", pg_name)

    # Get queued count before purge
    status = nipyapi.canvas.get_process_group_status(process_group_id)
    queued_before = 0
    if status and status.aggregate_snapshot:
        queued_before = status.aggregate_snapshot.flow_files_queued or 0

    # Purge the process group
    try:
        results = nipyapi.canvas.purge_process_group(process_group, stop=stop)
        connections_purged = len(results)
        log.info("Purged %d connections in: %s", connections_purged, pg_name)
    except Exception as e:
        log.error("Failed to purge: %s", e)
        return {
            "process_group_id": process_group_id,
            "process_group_name": pg_name,
            "purged": "false",
            "error": str(e),
        }

    # Get queued count after purge
    status = nipyapi.canvas.get_process_group_status(process_group_id)
    queued_after = 0
    if status and status.aggregate_snapshot:
        queued_after = status.aggregate_snapshot.flow_files_queued or 0

    return {
        "process_group_id": process_group_id,
        "process_group_name": pg_name,
        "purged": "true",
        "stopped": str(stop).lower(),
        "connections_purged": str(connections_purged),
        "flowfiles_before": str(queued_before),
        "flowfiles_after": str(queued_after),
    }
