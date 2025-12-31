"""Import a flow definition from a local file to create a process group."""

import logging
import os
from typing import Optional, Tuple

import nipyapi
import nipyapi.layout

log = logging.getLogger(__name__)


def import_flow_definition(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    file_path: Optional[str] = None,
    flow_definition: Optional[str] = None,
    parent_id: Optional[str] = None,
    location: Optional[Tuple[int, int]] = None,
) -> dict:
    """
    Import a flow definition file as a new process group.

    Creates a new process group from a JSON or YAML flow definition file.
    This does NOT require NiFi Registry - it imports directly to the canvas.

    Args:
        file_path: Path to the flow definition file (JSON or YAML).
            Env: NIFI_FLOW_FILE_PATH
        flow_definition: Flow definition as a string (alternative to file_path).
            Env: NIFI_FLOW_DEFINITION
        parent_id: Parent process group ID to import into.
            Env: NIFI_PARENT_ID
            Defaults to root process group.
        location: (x, y) tuple for placement on canvas.
            Env: NIFI_LOCATION_X, NIFI_LOCATION_Y
            If not provided, uses smart positioning to find a non-overlapping
            location in a grid layout.

    Returns:
        dict with keys: process_group_id, process_group_name, parent_id,
        and source ("file" or "string").

    Raises:
        ValueError: Missing required parameters or invalid flow definition

    Example::

        # Import from file
        nipyapi ci import_flow_definition \\
            --file_path my-flow.json \\
            --parent_id abc123

        # Import from stdin (for piping)
        cat my-flow.json | nipyapi ci import_flow_definition --flow_definition "$(cat)"
    """
    # Get from environment if not provided
    file_path = file_path or os.environ.get("NIFI_FLOW_FILE_PATH")
    flow_definition = flow_definition or os.environ.get("NIFI_FLOW_DEFINITION")
    parent_id = parent_id or os.environ.get("NIFI_PARENT_ID")

    # Parse location from env if not provided
    if location is None:
        loc_x = os.environ.get("NIFI_LOCATION_X")
        loc_y = os.environ.get("NIFI_LOCATION_Y")
        if loc_x and loc_y:
            location = (int(loc_x), int(loc_y))

    # Validate - exactly one of file_path or flow_definition
    if file_path and flow_definition:
        raise ValueError("Provide either file_path or flow_definition, not both")
    if not file_path and not flow_definition:
        raise ValueError(
            "Either file_path or flow_definition is required "
            "(or set NIFI_FLOW_FILE_PATH or NIFI_FLOW_DEFINITION)"
        )

    # Validate file exists if using file_path
    if file_path and not os.path.exists(file_path):
        raise ValueError(f"Flow definition file not found: {file_path}")

    # Default to root if not specified
    if not parent_id:
        parent_id = nipyapi.canvas.get_root_pg_id()
        log.debug("Using root process group: %s", parent_id)

    # Get parent process group
    parent_pg = nipyapi.canvas.get_process_group(parent_id, "id")
    if not parent_pg:
        raise ValueError(f"Parent process group not found: {parent_id}")

    # Use smart positioning if location not explicitly provided
    if location is None:
        location = nipyapi.layout.suggest_pg_position(parent_id)
        log.debug("Using suggested position: %s", location)

    source = "file" if file_path else "string"
    log.info(
        "Importing flow definition from %s into: %s at %s",
        file_path if file_path else "string",
        parent_pg.component.name,
        location,
    )

    # Import the flow definition
    imported_pg = nipyapi.versioning.import_process_group_definition(
        parent_pg=parent_pg,
        flow_definition=flow_definition,
        file_path=file_path,
        position=location,
    )

    pg_name = imported_pg.component.name
    log.info("Imported process group: %s (ID: %s)", pg_name, imported_pg.id)

    return {
        "process_group_id": imported_pg.id,
        "process_group_name": pg_name,
        "parent_id": parent_id,
        "source": source,
    }
