# pylint: disable=duplicate-code
"""
start_flow - start a deployed process group.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def start_flow(
    process_group_id: Optional[str] = None,
    enable_controllers: bool = True,
) -> dict:
    """
    Start a process group (enable controllers, start processors).

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID
        enable_controllers: Enable controller services first (default: True)

    Returns:
        dict with started, process_group_name

    Raises:
        ValueError: Missing required parameters
        Exception: NiFi API errors
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    nipyapi.profiles.switch()

    log.info("Starting process group: %s", process_group_id)

    # Get process group
    process_group = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not process_group:
        raise ValueError(f"Process group not found: {process_group_id}")

    pg_name = process_group.component.name
    log.debug("Found process group: %s", pg_name)

    # Enable controllers first
    if enable_controllers:
        log.debug("Enabling controller services...")
        nipyapi.canvas.schedule_all_controllers(process_group_id, scheduled=True)

    # Start processors
    log.debug("Starting processors...")
    nipyapi.canvas.schedule_process_group(process_group_id, scheduled=True)

    log.info("Started %s", pg_name)

    return {
        "started": "true",
        "process_group_name": pg_name,
    }
