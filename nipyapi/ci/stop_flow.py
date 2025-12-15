# pylint: disable=duplicate-code
"""
stop_flow - stop a running process group.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def _env_bool(name, default=False):
    """Parse a boolean from environment variable."""
    value = os.environ.get(name, "").lower()
    if value in ("true", "1", "yes"):
        return True
    if value in ("false", "0", "no"):
        return False
    return default


def stop_flow(
    process_group_id: Optional[str] = None,
    disable_controllers: Optional[bool] = None,
) -> dict:
    """
    Stop a process group (stop processors).

    By default, this function only stops processors. Controller services
    remain enabled so the flow can be quickly restarted.

    Use --disable_controllers if you need to delete the process group
    afterward (deletion requires disabled controllers and purged queues).

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID
        disable_controllers: Also disable controller services.
            Env: NIFI_DISABLE_CONTROLLERS (default: false)
            Only needed before deletion.

    Returns:
        dict with stopped, process_group_name, controllers_disabled

    Raises:
        ValueError: Missing required parameters
        Exception: NiFi API errors

    Examples:
        # Simple stop (processors only, controllers stay enabled)
        nipyapi ci stop_flow --process_group_id PG_ID

        # Stop for deletion (also disable controllers)
        nipyapi ci stop_flow --process_group_id PG_ID --disable_controllers
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    if disable_controllers is None:
        disable_controllers = _env_bool("NIFI_DISABLE_CONTROLLERS", default=False)

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    log.info("Stopping process group: %s", process_group_id)

    # Get process group
    process_group = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not process_group:
        raise ValueError(f"Process group not found: {process_group_id}")

    pg_name = process_group.component.name
    log.debug("Found process group: %s", pg_name)

    # Stop processors
    log.debug("Stopping processors...")
    nipyapi.canvas.schedule_process_group(process_group_id, scheduled=False)

    # Disable controllers only if explicitly requested
    if disable_controllers:
        log.debug("Disabling controller services...")
        nipyapi.canvas.schedule_all_controllers(process_group_id, scheduled=False)
        log.info("Stopped %s (controllers disabled)", pg_name)
    else:
        log.info("Stopped %s (controllers still enabled)", pg_name)

    return {
        "stopped": "true",
        "process_group_name": pg_name,
        "controllers_disabled": str(disable_controllers).lower(),
    }
