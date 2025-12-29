# pylint: disable=broad-exception-caught
"""
get_status - get comprehensive status for a process group.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def get_status(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    process_group_id: Optional[str] = None,
) -> dict:
    """
    Get comprehensive status information for a process group.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID.
                         If not provided, defaults to root process group.

    Returns:
        dict with status information including:
        - process_group_id, process_group_name, state, is_root
        - Processor counts (total, running, stopped, invalid, disabled)
        - Controller counts (total, enabled, disabled)
        - Version control info (versioned, version_id, version_state, etc.)
        - Parameter context info

    Example::

        # Get status of specific process group
        nipyapi ci get_status --process_group_id PG_ID

        # Get status of entire canvas (root process group)
        nipyapi ci get_status
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")

    # Default to root process group if not specified (safe for read-only operation)
    is_root = False
    if not process_group_id:
        process_group_id = nipyapi.canvas.get_root_pg_id()
        is_root = True
        log.info("No process_group_id specified, using root process group")

    log.info("Getting status for: %s", process_group_id)

    # Get process group with full status
    pg = nipyapi.canvas.get_process_group_status(process_group_id, detail="all")
    if not pg:
        raise ValueError(f"Process group not found: {process_group_id}")

    pg_name = pg.component.name
    log.debug("Found process group: %s", pg_name)

    result = {
        "process_group_id": process_group_id,
        "process_group_name": pg_name,
        "is_root": str(is_root).lower(),
    }

    # Processor counts
    running = pg.running_count or 0
    stopped = pg.stopped_count or 0
    invalid = pg.invalid_count or 0
    disabled = pg.disabled_count or 0

    if running > 0:
        state = "RUNNING"
    elif stopped > 0:
        state = "STOPPED"
    else:
        state = "EMPTY"

    result["state"] = state
    result["total_processors"] = str(running + stopped + invalid + disabled)
    result["running_processors"] = str(running)
    result["stopped_processors"] = str(stopped)
    result["invalid_processors"] = str(invalid)
    result["disabled_processors"] = str(disabled)

    log.debug("State: %s (%d running, %d stopped)", state, running, stopped)

    # Queue stats and active threads
    if pg.status and pg.status.aggregate_snapshot:
        agg = pg.status.aggregate_snapshot
        result["queued_flowfiles"] = str(agg.flow_files_queued or 0)
        result["queued_bytes"] = str(agg.bytes_queued or 0)
        result["active_threads"] = str(agg.active_thread_count or 0)

    # Controller services
    controllers = nipyapi.canvas.list_all_controllers(process_group_id, descendants=True)
    if controllers:
        enabled = sum(1 for c in controllers if c.component.state == "ENABLED")
        disabled_ctrl = sum(1 for c in controllers if c.component.state == "DISABLED")
        result["total_controllers"] = str(len(controllers))
        result["enabled_controllers"] = str(enabled)
        result["disabled_controllers"] = str(disabled_ctrl)
    else:
        result["total_controllers"] = "0"
        result["enabled_controllers"] = "0"
        result["disabled_controllers"] = "0"

    # Version control info
    vci = pg.component.version_control_information
    if vci:
        result["versioned"] = "true"
        result["version_id"] = vci.version or ""
        result["flow_id"] = vci.flow_id or ""
        result["flow_name"] = vci.flow_name or ""
        result["bucket_id"] = vci.bucket_id or ""
        result["bucket_name"] = vci.bucket_name or ""
        result["registry_id"] = vci.registry_id or ""
        result["version_state"] = vci.state or ""
        result["modified"] = str(vci.state not in ["UP_TO_DATE", "SYNC_FAILURE"]).lower()
        log.debug("Version: %s (%s)", vci.version, vci.state)
    else:
        result["versioned"] = "false"
        result["modified"] = "false"

    # Parameter context
    pc_ref = pg.component.parameter_context
    if pc_ref and pc_ref.id:
        result["has_parameter_context"] = "true"
        result["parameter_context_id"] = pc_ref.id
        pc_name = pc_ref.component.name if pc_ref.component else ""
        result["parameter_context_name"] = pc_name
        try:
            pc = nipyapi.parameters.get_parameter_context(pc_ref.id)
            result["parameter_count"] = str(len(pc.component.parameters or []))
        except Exception:
            result["parameter_count"] = "0"
    else:
        result["has_parameter_context"] = "false"
        result["parameter_count"] = "0"

    # Bulletins (warnings/errors)
    # Use get_bulletin_board for comprehensive bulletins including controller services
    # The pg_entity.bulletins field only shows bulletins attached to the PG itself,
    # missing controller service and some component bulletins
    try:
        bulletins = nipyapi.bulletins.get_bulletin_board(pg_id=process_group_id)
        if bulletins:
            warning_count = sum(1 for b in bulletins if b.level == "WARNING")
            error_count = sum(1 for b in bulletins if b.level == "ERROR")
            result["bulletin_warnings"] = str(warning_count)
            result["bulletin_errors"] = str(error_count)
            # Include first few bulletin messages for quick diagnosis
            if warning_count > 0 or error_count > 0:
                messages = []
                for b in bulletins[:3]:  # Limit to first 3
                    messages.append(f"[{b.level}] {b.source_name}: {b.message[:100]}")
                result["bulletin_messages"] = " | ".join(messages)
                log.warning("Found %d warnings, %d errors", warning_count, error_count)
        else:
            result["bulletin_warnings"] = "0"
            result["bulletin_errors"] = "0"
    except Exception as e:
        log.debug("Could not fetch bulletins: %s", e)
        result["bulletin_warnings"] = "0"
        result["bulletin_errors"] = "0"

    log.info("Status retrieved for %s: %s", pg_name, state)
    return result
