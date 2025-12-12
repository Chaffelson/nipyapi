"""
configure_params - set parameter values on a process group.
"""

import json
import logging
import os
from typing import Any, Dict, Optional, Union

import nipyapi

log = logging.getLogger(__name__)


def configure_params(
    process_group_id: Optional[str] = None,
    parameters: Optional[Union[str, Dict[str, Any]]] = None,
) -> dict:
    """
    Configure parameters on a process group's parameter context.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID
        parameters: JSON string or dict of parameter name -> value pairs.
                   Env: NIFI_PARAMETERS

    Returns:
        dict with parameters_updated, parameters_count, context_name

    Raises:
        ValueError: Missing required parameters or invalid JSON
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    parameters = parameters or os.environ.get("NIFI_PARAMETERS")

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")
    if not parameters:
        raise ValueError("parameters is required (or set NIFI_PARAMETERS)")

    # Parse JSON string if provided
    if isinstance(parameters, str):
        try:
            parameters = json.loads(parameters)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in parameters: {e}") from e

    if not isinstance(parameters, dict):
        raise ValueError("parameters must be a JSON object with key-value pairs")

    nipyapi.profiles.switch()

    log.info("Configuring %d parameter(s) on %s", len(parameters), process_group_id)

    # Get process group
    pg = nipyapi.canvas.get_process_group(process_group_id, identifier_type="id")
    if not pg:
        raise ValueError(f"Process group not found: {process_group_id}")

    log.debug("Found process group: %s", pg.component.name)

    # Check for parameter context
    if not pg.component.parameter_context:
        raise ValueError(
            f"Process group '{pg.component.name}' has no parameter context. "
            "Attach a parameter context before configuring parameters."
        )

    ctx_ref = pg.component.parameter_context
    ctx_name = ctx_ref.component.name
    log.debug("Parameter context: %s", ctx_name)

    # Get full context
    ctx = nipyapi.parameters.get_parameter_context(ctx_ref.id, identifier_type="id")

    # Prepare parameters
    prepared_params = []
    for param_name, param_value in parameters.items():
        param = nipyapi.parameters.prepare_parameter(
            name=param_name,
            value=str(param_value),
            sensitive=False,
        )
        prepared_params.append(param)
        log.debug("Setting %s = %s", param_name, param_value)

    # Apply parameters
    ctx.component.parameters = prepared_params
    nipyapi.parameters.update_parameter_context(ctx)

    updated_params = list(parameters.keys())
    log.info("Updated %d parameter(s): %s", len(updated_params), ", ".join(updated_params))

    return {
        "parameters_updated": ",".join(updated_params),
        "parameters_count": str(len(updated_params)),
        "context_name": ctx_name,
    }
