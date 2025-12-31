"""
detach_flow - remove version control from a flow (for forking).
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def detach_flow(
    process_group_id: Optional[str] = None,
) -> dict:
    """
    Detach a flow from version control.

    Removes version control from a process group, allowing it to be
    re-versioned to a different registry. This is the first step in
    forking a read-only flow to your own repository.

    After detaching, use commit_flow to save the flow to your own
    registry client and bucket.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID

    Returns:
        dict with:
          - detached: True if successfully detached
          - process_group_name: Name of the process group
          - previous_registry: Name of the previous registry (if available)
          - previous_flow_id: Previous flow identifier

    Raises:
        ValueError: Missing required parameters or not under version control

    Example::

        # Fork workflow: detach from read-only registry, save to your own
        nipyapi ci detach_flow --process_group_id PG_ID
        nipyapi ci commit_flow --process_group_id PG_ID --registry_client MyRepo --bucket flows
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    log.info("Detaching flow from version control: %s", process_group_id)

    # Get the process group
    pg = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not pg:
        raise ValueError(f"Process group not found: {process_group_id}")

    # Check if under version control
    vci = pg.component.version_control_information
    if not vci:
        raise ValueError(f"Process group '{pg.component.name}' is not under version control")

    # Capture info before detaching
    previous_registry_id = vci.registry_id
    previous_flow_id = vci.flow_id
    previous_bucket = vci.bucket_id

    log.debug(
        "Current version control: registry=%s, flow=%s, bucket=%s",
        previous_registry_id,
        previous_flow_id,
        previous_bucket,
    )

    # Try to get registry name for better output
    previous_registry_name = None
    try:
        reg = nipyapi.versioning.get_registry_client(previous_registry_id)
        if reg:
            previous_registry_name = reg.component.name
    except Exception:  # pylint: disable=broad-exception-caught
        pass

    # Stop version control
    nipyapi.versioning.stop_flow_ver(pg)

    log.info(
        "Detached '%s' from version control (was: %s/%s)",
        pg.component.name,
        previous_registry_name or previous_registry_id,
        previous_flow_id,
    )

    return {
        "detached": True,
        "process_group_name": pg.component.name,
        "previous_registry": previous_registry_name or previous_registry_id,
        "previous_flow_id": previous_flow_id,
        "previous_bucket": previous_bucket,
    }
