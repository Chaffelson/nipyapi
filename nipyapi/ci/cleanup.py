# pylint: disable=broad-exception-caught
"""
cleanup - stop and delete a deployed process group.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


# pylint: disable=too-many-arguments,too-many-positional-arguments
# pylint: disable=too-many-branches,too-many-statements,too-many-locals
def cleanup(
    process_group_id: Optional[str] = None,
    stop_only: Optional[bool] = None,
    force: Optional[bool] = None,
    delete_parameter_context: Optional[bool] = None,
    delete_orphaned_contexts: Optional[bool] = None,
    disable_controllers: Optional[bool] = None,
) -> dict:
    """
    Stop and optionally delete a process group.

    By default, this function stops the process group and disables its controllers,
    but does NOT delete it or its parameter context. Use explicit flags or
    environment variables for destructive operations.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID
        stop_only: Only stop processors, don't delete anything.
            Env: NIFI_STOP_ONLY (default: false)
        force: Force deletion even with queued FlowFiles.
            Env: NIFI_FORCE_DELETE (default: false)
        delete_parameter_context: Also delete the parameter context.
            Env: NIFI_DELETE_PARAMETER_CONTEXT (default: false)
            WARNING: Only use if you're certain no other process groups share
            this context (e.g., Openflow connectors share contexts).
        delete_orphaned_contexts: After deletion, also delete any parameter
            contexts that are no longer bound to any process groups.
            Env: NIFI_DELETE_ORPHANED_CONTEXTS (default: false)
            This is safer than delete_parameter_context as it only removes
            contexts that are definitely unused.
        disable_controllers: Disable controller services after stopping.
            Env: NIFI_DISABLE_CONTROLLERS (default: true)

    Returns:
        dict with stopped/deleted status and names

    Raises:
        ValueError: Missing required parameters

    Example::

        # Just stop the flow (safest)
        nipyapi ci cleanup --process_group_id PG_ID --stop_only

        # Stop and delete process group only (safe for shared contexts)
        nipyapi ci cleanup --process_group_id PG_ID

        # Full cleanup including parameter context (CI/CD pipelines)
        nipyapi ci cleanup --process_group_id PG_ID --delete_parameter_context --force

        # Clean up orphaned contexts after deletion (safe)
        nipyapi ci cleanup --process_group_id PG_ID --delete_orphaned_contexts

        # Via environment variables (for CI/CD)
        NIFI_DELETE_PARAMETER_CONTEXT=true NIFI_FORCE_DELETE=true nipyapi ci cleanup
    """
    # Resolve from env vars with safe defaults
    # Use parse_bool for CLI parameters (fire passes --flag=false as string "false")
    # Use getenv_bool for environment variable fallbacks
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    if stop_only is None:
        stop_only = nipyapi.utils.getenv_bool("NIFI_STOP_ONLY", default=False)
    else:
        stop_only = nipyapi.utils.parse_bool(stop_only, default=False)
    if force is None:
        force = nipyapi.utils.getenv_bool("NIFI_FORCE_DELETE", default=False)
    else:
        force = nipyapi.utils.parse_bool(force, default=False)
    if delete_parameter_context is None:
        delete_parameter_context = nipyapi.utils.getenv_bool(
            "NIFI_DELETE_PARAMETER_CONTEXT", default=False
        )
    else:
        delete_parameter_context = nipyapi.utils.parse_bool(delete_parameter_context, default=False)
    if delete_orphaned_contexts is None:
        delete_orphaned_contexts = nipyapi.utils.getenv_bool(
            "NIFI_DELETE_ORPHANED_CONTEXTS", default=False
        )
    else:
        delete_orphaned_contexts = nipyapi.utils.parse_bool(delete_orphaned_contexts, default=False)
    if disable_controllers is None:
        disable_controllers = nipyapi.utils.getenv_bool("NIFI_DISABLE_CONTROLLERS", default=True)
    else:
        disable_controllers = nipyapi.utils.parse_bool(disable_controllers, default=True)

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    log.info("Cleaning up process group: %s", process_group_id)

    # Get process group
    try:
        process_group = nipyapi.canvas.get_process_group(process_group_id, "id")
    except nipyapi.nifi.rest.ApiException as e:
        if e.status == 404:
            log.info("Process group not found - may already be deleted")
            return {
                "stopped": "false",
                "deleted": "false",
                "process_group_name": "",
                "error": "Process group not found",
            }
        raise

    if not process_group:
        return {
            "stopped": "false",
            "deleted": "false",
            "process_group_name": "",
            "error": "Process group not found",
        }

    pg_name = process_group.component.name
    log.debug("Found process group: %s", pg_name)

    # Stop processors
    log.debug("Stopping processors...")
    nipyapi.canvas.schedule_process_group(process_group_id, scheduled=False)
    log.info("Stopped processors in: %s", pg_name)

    # Disable controllers if requested
    if disable_controllers:
        log.debug("Disabling controller services...")
        try:
            nipyapi.canvas.schedule_all_controllers(process_group_id, scheduled=False)
            log.info("Disabled controller services in: %s", pg_name)
        except Exception as e:
            log.warning("Could not disable all controllers: %s", e)

    # If stop_only, we're done
    if stop_only:
        return {
            "stopped": "true",
            "deleted": "false",
            "process_group_name": pg_name,
            "message": "Stopped only (no deletion)",
        }

    # Get parameter context reference before deletion
    param_ctx_id = None
    param_ctx_name = None
    if delete_parameter_context and process_group.component.parameter_context:
        param_ctx_id = process_group.component.parameter_context.id
        param_ctx_name = process_group.component.parameter_context.component.name
        log.debug("Will delete parameter context: %s", param_ctx_name)

    # Delete process group
    log.debug("Deleting process group...")
    nipyapi.canvas.delete_process_group(process_group, force=force)
    log.info("Deleted process group: %s", pg_name)

    # Delete parameter context if explicitly requested
    param_ctx_deleted = False
    if delete_parameter_context and param_ctx_id:
        try:
            log.debug("Deleting parameter context: %s", param_ctx_name)
            ctx = nipyapi.parameters.get_parameter_context(param_ctx_id, identifier_type="id")
            nipyapi.parameters.delete_parameter_context(ctx)
            log.info("Deleted parameter context: %s", param_ctx_name)
            param_ctx_deleted = True
        except Exception as e:
            log.warning("Could not delete parameter context: %s", e)

    # Delete orphaned contexts if requested (safer than delete_parameter_context)
    orphaned_deleted = []
    if delete_orphaned_contexts:
        try:
            orphaned = nipyapi.parameters.list_orphaned_contexts()
            log.debug("Found %d orphaned parameter contexts", len(orphaned))
            for ctx in orphaned:
                try:
                    ctx_name = ctx.component.name
                    log.debug("Deleting orphaned context: %s", ctx_name)
                    nipyapi.parameters.delete_parameter_context(ctx)
                    log.info("Deleted orphaned context: %s", ctx_name)
                    orphaned_deleted.append(ctx_name)
                except Exception as e:
                    log.warning("Could not delete orphaned context %s: %s", ctx.id, e)
        except Exception as e:
            log.warning("Could not list orphaned contexts: %s", e)

    return {
        "stopped": "true",
        "deleted": "true",
        "process_group_name": pg_name,
        "parameter_context_deleted": str(param_ctx_deleted).lower(),
        "orphaned_contexts_deleted": orphaned_deleted,
    }
