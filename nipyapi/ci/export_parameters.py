"""Export parameter values from a parameter context hierarchy."""

import json
import logging
import os
from typing import Optional

import yaml

import nipyapi

log = logging.getLogger(__name__)


# pylint: disable=duplicate-code,too-many-branches
def export_parameters(
    context_id: Optional[str] = None,
    process_group_id: Optional[str] = None,
    file_path: Optional[str] = None,
    mode: str = "json",
    include_hierarchy: Optional[bool] = None,
) -> dict:
    """
    Export parameters from a parameter context hierarchy.

    By default, exports a flat {name: value} dict suitable for import via
    configure_inherited_params. Optionally includes the full hierarchy structure.

    Note: Sensitive parameter values cannot be exported (NiFi returns null),
    but their keys are included so users know what needs to be recreated.

    Args:
        context_id: ID of the parameter context. Env: NIFI_PARAMETER_CONTEXT_ID
        process_group_id: Optional. Resolve context from this PG instead.
                         Env: NIFI_PROCESS_GROUP_ID
        file_path: Optional path to write the export. Env: NIFI_PARAMETERS_FILE
                   If not provided, returns parameters in the result dict.
        mode: Output format: 'json' or 'yaml'. Env: NIFI_EXPORT_MODE (default: json)
        include_hierarchy: If True, include full hierarchy structure showing which
                          context owns each parameter. Env: NIFI_INCLUDE_HIERARCHY

    Returns:
        dict with keys: context_id, context_name, file_path, format,
        parameter_count, and parameters (if file_path not provided).

    Raises:
        ValueError: Missing required parameters or context not found

    Example::

        # Export by context ID
        nipyapi ci export_parameters --context_id abc123

        # Export from process group's context
        nipyapi ci export_parameters --process_group_id xyz789

        # Export to file
        nipyapi ci export_parameters --context_id abc123 \\
            --file_path params.yaml --mode yaml
    """
    # Get from environment if not provided
    context_id = context_id or os.environ.get("NIFI_PARAMETER_CONTEXT_ID")
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    file_path = file_path or os.environ.get("NIFI_PARAMETERS_FILE")
    mode = mode or os.environ.get("NIFI_EXPORT_MODE", "json")
    if include_hierarchy is None:
        include_hierarchy = nipyapi.utils.getenv_bool("NIFI_INCLUDE_HIERARCHY", False)

    # Resolve context_id from process_group_id if needed
    if not context_id and process_group_id:
        pg = nipyapi.canvas.get_process_group(process_group_id, identifier_type="id")
        if pg is None:
            raise ValueError(f"Process group not found: {process_group_id}")
        if not pg.component.parameter_context:
            raise ValueError(f"Process group '{pg.component.name}' has no parameter context.")
        context_id = pg.component.parameter_context.id

    if not context_id:
        raise ValueError(
            "context_id or process_group_id is required "
            "(or set NIFI_PARAMETER_CONTEXT_ID or NIFI_PROCESS_GROUP_ID)"
        )
    if mode not in ("json", "yaml"):
        raise ValueError("mode must be 'json' or 'yaml'")

    log.info("Exporting parameters from context %s", context_id)

    # Get context
    ctx = nipyapi.parameters.get_parameter_context(context_id, identifier_type="id")
    if ctx is None:
        raise ValueError(f"Parameter context not found: {context_id}")

    ctx_name = ctx.component.name
    log.debug("Found parameter context: %s (%s)", ctx_name, context_id)

    if include_hierarchy:
        hierarchy = nipyapi.parameters.get_parameter_context_hierarchy(context_id)
        export_data = _format_hierarchy(hierarchy)
    else:
        ownership = nipyapi.parameters.get_parameter_ownership_map(context_id)
        export_data = _build_flat_export(ownership)

    # Serialize
    if mode == "yaml":
        output = yaml.safe_dump(export_data, default_flow_style=False, sort_keys=False)
    else:
        output = json.dumps(export_data, indent=2)

    # Build result
    result = {
        "context_id": context_id,
        "context_name": ctx_name,
        "format": mode,
        "parameter_count": str(len(export_data)),
    }

    if file_path:
        log.info("Writing parameters to %s", file_path)
        nipyapi.utils.fs_write(output, file_path)
        result["file_path"] = file_path
    else:
        result["file_path"] = "stdout"
        result["parameters"] = output

    return result


def _build_flat_export(ownership: dict) -> dict:
    """Build flat {name: value} export from ownership map.

    Includes all parameters. Sensitive parameter values will be null
    (as returned by NiFi) but keys are preserved for migration purposes.
    """
    return {param_name: info["current_value"] for param_name, info in ownership.items()}


def _format_hierarchy(hierarchy: dict) -> dict:
    """Format hierarchy structure for export.

    Creates a structure showing each context and its parameters.
    Sensitive parameter values will be null but keys are preserved.
    """
    result = {
        "context": hierarchy["name"],
        "context_id": hierarchy["id"],
        "parameters": {},
    }

    if "parameters" in hierarchy:
        for param in hierarchy["parameters"]:
            result["parameters"][param["name"]] = param.get("value")

    if hierarchy.get("inherited"):
        result["inherited"] = [_format_hierarchy(child) for child in hierarchy["inherited"]]

    return result
