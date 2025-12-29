"""Export a flow definition from a process group to a local file."""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def export_flow_definition(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    process_group_id: Optional[str] = None,
    file_path: Optional[str] = None,
    mode: Optional[str] = None,
    include_referenced_services: Optional[bool] = None,
) -> dict:
    """
    Export a process group as a flow definition file.

    Exports the current state of a process group to a JSON or YAML file.
    This does NOT require NiFi Registry - it exports the live canvas state.

    Args:
        process_group_id: ID of the process group to export.
            Env: NIFI_PROCESS_GROUP_ID
        file_path: Path to write the flow definition to.
            Env: NIFI_FLOW_FILE_PATH
            If not provided, returns the flow definition as a string in the result.
        mode: Export format - 'json' or 'yaml'. Defaults to 'json'.
            Env: NIFI_FLOW_FORMAT
        include_referenced_services: If True, include controller services from
            outside the target group that are referenced by components within.
            Env: NIFI_INCLUDE_REFERENCED_SERVICES. Defaults to False.

    Returns:
        dict with keys: process_group_id, process_group_name, file_path,
        format, and flow_definition (if file_path not provided).

    Raises:
        ValueError: Missing required parameters or process group not found

    Example::

        # Export to file
        nipyapi ci export_flow_definition \\
            --process_group_id abc123 \\
            --file_path my-flow.json

        # Export to stdout (for piping)
        nipyapi ci export_flow_definition --process_group_id abc123

        # Export with external controller services included
        nipyapi ci export_flow_definition \\
            --process_group_id abc123 \\
            --include_referenced_services
    """
    # Get from environment if not provided
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    file_path = file_path or os.environ.get("NIFI_FLOW_FILE_PATH")
    mode = mode or os.environ.get("NIFI_FLOW_FORMAT", "json")
    if include_referenced_services is None:
        include_referenced_services = nipyapi.utils.getenv_bool(
            "NIFI_INCLUDE_REFERENCED_SERVICES", False
        )

    # Validate
    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    if mode not in ("json", "yaml"):
        raise ValueError(f"mode must be 'json' or 'yaml', got: {mode}")

    log.info("Exporting flow definition for process group: %s", process_group_id)

    # Get the process group
    pg = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not pg:
        raise ValueError(f"Process group not found: {process_group_id}")

    pg_name = pg.component.name
    log.debug("Found process group: %s", pg_name)

    # Export the flow definition
    if file_path:
        nipyapi.versioning.export_process_group_definition(
            process_group=pg,
            file_path=file_path,
            mode=mode,
            include_referenced_services=include_referenced_services,
        )
        log.info("Exported flow definition to: %s", file_path)

        return {
            "process_group_id": process_group_id,
            "process_group_name": pg_name,
            "file_path": file_path,
            "format": mode,
        }

    # Return the flow definition string
    flow_def = nipyapi.versioning.export_process_group_definition(
        process_group=pg,
        file_path=None,
        mode=mode,
        include_referenced_services=include_referenced_services,
    )
    log.info("Exported flow definition (%d bytes)", len(flow_def))

    return {
        "process_group_id": process_group_id,
        "process_group_name": pg_name,
        "file_path": "stdout",
        "format": mode,
        "flow_definition": flow_def,
    }
