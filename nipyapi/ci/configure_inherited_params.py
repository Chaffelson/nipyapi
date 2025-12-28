"""Configure parameters across inherited parameter contexts."""

import json
import logging
import os
from typing import Any, Dict, Optional, Union

import nipyapi

log = logging.getLogger(__name__)


# pylint: disable=too-many-locals,too-many-branches,too-many-statements
def configure_inherited_params(
    process_group_id: Optional[str] = None,
    parameters: Optional[Union[str, Dict[str, Any]]] = None,
    parameters_file: Optional[str] = None,
    dry_run: bool = False,
    allow_override: bool = False,
) -> dict:
    """
    Configure parameters in their owning contexts within an inheritance hierarchy.

    This function determines which parameter context owns each parameter and
    updates it in the correct context, preventing accidental shadowing.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID
        parameters: JSON string or dict of parameter name -> value pairs.
                   Env: NIFI_PARAMETERS
        parameters_file: Path to JSON or YAML file with parameter name -> value pairs.
                        Env: NIFI_PARAMETERS_FILE
        dry_run: If True, return the plan without making changes.
                Env: NIFI_DRY_RUN (default: false)
        allow_override: If True, create parameters at top level even if they
                       exist in inherited contexts. Env: NIFI_ALLOW_OVERRIDE (default: false)

    Returns:
        dict with:
            - dry_run: "true" or "false"
            - plan: Summary of planned/executed updates
            - parameters_updated: Count of parameters updated
            - contexts_modified: Count of contexts modified
            - warnings: Any warnings (e.g., asset replacement)
            - errors: Any errors (e.g., parameter not found)

    Raises:
        ValueError: Missing required parameters or invalid JSON

    Example:
        # From inline JSON
        nipyapi ci configure_inherited_params \\
            --process_group_id abc123 \\
            --parameters '{"PostgreSQL Username": "myuser"}'

        # From file
        nipyapi ci configure_inherited_params \\
            --process_group_id abc123 \\
            --parameters_file params.yaml

        # Dry run
        nipyapi ci configure_inherited_params \\
            --process_group_id abc123 \\
            --parameters_file params.json \\
            --dry_run
    """
    # Get from environment if not provided
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    parameters = parameters or os.environ.get("NIFI_PARAMETERS")
    parameters_file = parameters_file or os.environ.get("NIFI_PARAMETERS_FILE")

    # Parse boolean env vars
    if isinstance(dry_run, str):
        dry_run = dry_run.lower() in ("true", "1", "yes")
    if os.environ.get("NIFI_DRY_RUN", "").lower() in ("true", "1", "yes"):
        dry_run = True

    if isinstance(allow_override, str):
        allow_override = allow_override.lower() in ("true", "1", "yes")
    if os.environ.get("NIFI_ALLOW_OVERRIDE", "").lower() in ("true", "1", "yes"):
        allow_override = True

    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    # Handle parameters from file or direct input
    if parameters_file and parameters:
        raise ValueError("Provide either parameters or parameters_file, not both")

    if parameters_file:
        if not os.path.exists(parameters_file):
            raise ValueError(f"Parameters file not found: {parameters_file}")
        log.info("Loading parameters from file: %s", parameters_file)
        content = nipyapi.utils.fs_read(parameters_file)
        parameters = nipyapi.utils.load(content) or {}
    elif not parameters:
        raise ValueError(
            "parameters or parameters_file is required "
            "(or set NIFI_PARAMETERS or NIFI_PARAMETERS_FILE)"
        )

    # Parse JSON string if provided
    if isinstance(parameters, str):
        try:
            parameters = json.loads(parameters)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in parameters: {e}") from e

    if not isinstance(parameters, dict):
        raise ValueError("parameters must be a JSON object with key-value pairs")

    log.info(
        "Configuring %d parameter(s) on %s (dry_run=%s)",
        len(parameters),
        process_group_id,
        dry_run,
    )

    # Get process group and its parameter context
    pg = nipyapi.canvas.get_process_group(process_group_id, identifier_type="id")
    if pg is None:
        raise ValueError(f"Process group not found: {process_group_id}")

    if not pg.component.parameter_context:
        raise ValueError(
            f"Process group '{pg.component.name}' has no parameter context. "
            "Attach a parameter context before configuring parameters."
        )

    ctx_id = pg.component.parameter_context.id
    ctx_name = pg.component.parameter_context.component.name

    # Build ownership map
    ownership = nipyapi.parameters.get_parameter_ownership_map(ctx_id)

    # Plan the updates
    plan = []
    warnings = []
    errors = []
    updates_by_context = {}  # context_id -> list of (param_name, value, sensitive)

    for param_name, param_value in parameters.items():
        if param_name not in ownership:
            if allow_override:
                # Create at top level
                plan.append(
                    {
                        "parameter": param_name,
                        "context": ctx_name,
                        "context_id": ctx_id,
                        "sensitive": "false",
                        "action": "CREATE (override)",
                        "new_value": _mask_value(param_value),
                    }
                )
                if ctx_id not in updates_by_context:
                    updates_by_context[ctx_id] = []
                updates_by_context[ctx_id].append((param_name, param_value, False))
            else:
                errors.append(
                    f"Parameter '{param_name}' not found in any context. "
                    f"Use --allow_override to create it."
                )
            continue

        owner = ownership[param_name]

        # Check for asset warning
        if owner["has_asset"]:
            warnings.append(
                f"Parameter '{param_name}' currently has asset '{owner['asset_name']}' mapped. "
                f"Setting a value will replace the asset reference."
            )

        plan.append(
            {
                "parameter": param_name,
                "context": owner["context_name"],
                "context_id": owner["context_id"],
                "sensitive": str(owner["sensitive"]).lower(),
                "action": "UPDATE",
                "new_value": "********" if owner["sensitive"] else _mask_value(param_value),
            }
        )

        if owner["context_id"] not in updates_by_context:
            updates_by_context[owner["context_id"]] = []
        updates_by_context[owner["context_id"]].append(
            (param_name, param_value, owner["sensitive"])
        )

    # Execute if not dry run
    if not dry_run and not errors:
        for target_ctx_id, param_updates in updates_by_context.items():
            for param_name, param_value, _sensitive in param_updates:
                log.info("Updating %s in context %s", param_name, target_ctx_id)
                nipyapi.parameters.update_parameter_in_context(
                    context_id=target_ctx_id,
                    param_name=param_name,
                    value=param_value,
                    create_if_missing=allow_override,
                )

    # Build result
    result = {
        "dry_run": str(dry_run).lower(),
        "parameters_updated": str(len(plan) - len(errors)) if not dry_run else "0",
        "contexts_modified": str(len(updates_by_context)) if not dry_run else "0",
        "plan": " | ".join(f"{p['parameter']}→{p['context']}" for p in plan),
    }

    if warnings:
        result["warnings"] = " | ".join(warnings)
    if errors:
        result["errors"] = " | ".join(errors)

    return result


def _mask_value(value: str, max_len: int = 20) -> str:
    """Mask long values for display."""
    if value is None:
        return "<empty>"
    value_str = str(value)
    if len(value_str) > max_len:
        return value_str[:max_len] + "..."
    return value_str
