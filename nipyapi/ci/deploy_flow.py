"""
deploy_flow - deploy a flow from Git registry to NiFi canvas.
"""

import logging
import os
from typing import Optional, Tuple

import nipyapi

log = logging.getLogger(__name__)


def deploy_flow(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
    registry_client: Optional[str] = None,
    bucket: Optional[str] = None,
    flow: Optional[str] = None,
    parent_id: Optional[str] = None,
    branch: Optional[str] = None,
    version: Optional[str] = None,
    location: Optional[Tuple[int, int]] = None,
    greedy: bool = False,
    parameter_context_handling: Optional[str] = None,
) -> dict:
    """
    Deploy a flow from a Git-based registry to NiFi.

    Args:
        registry_client: Registry client ID (UUID) or name. Auto-detects which
            based on format. Env: NIFI_REGISTRY_CLIENT_ID
        bucket: Bucket (folder) containing the flow. Env: NIFI_BUCKET
        flow: Flow name (filename without .json). Env: NIFI_FLOW
        parent_id: Parent Process Group ID. Env: NIFI_PARENT_ID (default: root)
        branch: Branch to deploy from. Env: NIFI_FLOW_BRANCH
        version: Version (commit SHA, tag, branch). Env: NIFI_TARGET_VERSION
        location: (x, y) tuple for placement on canvas
        greedy: If True, allow partial name matching for registry_client.
                Default False (exact match for safety in CI/automation).
        parameter_context_handling: How to handle existing parameter contexts
            with the same name. Valid values:
            - 'KEEP_EXISTING': Reuse existing context by name (default)
            - 'REPLACE': Create new context with numbered suffix
            Env: NIFI_PARAMETER_CONTEXT_HANDLING

    Returns:
        dict with process_group_id, process_group_name, deployed_version

    Raises:
        ValueError: Missing required parameters or registry client not found
    """
    # Resolve from env vars
    registry_client = registry_client or os.environ.get("NIFI_REGISTRY_CLIENT_ID")
    bucket = bucket or os.environ.get("NIFI_BUCKET")
    flow = flow or os.environ.get("NIFI_FLOW")
    parent_id = parent_id or os.environ.get("NIFI_PARENT_ID")
    branch = branch or os.environ.get("NIFI_FLOW_BRANCH") or None
    version = version or os.environ.get("NIFI_TARGET_VERSION") or None
    parameter_context_handling = (
        parameter_context_handling or os.environ.get("NIFI_PARAMETER_CONTEXT_HANDLING") or None
    )

    # Parse location from env if not provided
    if location is None:
        loc_x = os.environ.get("NIFI_LOCATION_X")
        loc_y = os.environ.get("NIFI_LOCATION_Y")
        if loc_x and loc_y:
            location = (int(loc_x), int(loc_y))

    # Validate required params
    if not registry_client:
        raise ValueError("registry_client is required (or set NIFI_REGISTRY_CLIENT_ID)")
    if not bucket:
        raise ValueError("bucket is required (or set NIFI_BUCKET)")
    if not flow:
        raise ValueError("flow is required (or set NIFI_FLOW)")

    # Resolve registry client (ID or name)
    identifier_type = "id" if nipyapi.utils.is_uuid(registry_client) else "name"
    client = nipyapi.versioning.get_registry_client(
        registry_client, identifier_type=identifier_type, greedy=greedy
    )
    if client is None:
        raise ValueError(f"Registry client not found: {registry_client}")
    if isinstance(client, list):
        names = [c.component.name for c in client]
        raise ValueError(
            f"Multiple registry clients match '{registry_client}': {names}. "
            "Use exact name or ID, or set greedy=True to use first match."
        )
    registry_client_id = client.id

    # Default to root if not specified
    if not parent_id:
        parent_id = nipyapi.canvas.get_root_pg_id()
        log.debug("Using root process group: %s", parent_id)

    log.info("Deploying flow '%s' from bucket '%s'", flow, bucket)
    if branch:
        log.debug("Branch: %s", branch)
    if version:
        log.debug("Version: %s", version)

    # Deploy the flow
    process_group = nipyapi.versioning.deploy_git_registry_flow(
        registry_client_id=registry_client_id,
        bucket_id=bucket,
        flow_id=flow,
        parent_id=parent_id,
        location=location,
        version=version,
        branch=branch,
        parameter_context_handling=parameter_context_handling,
    )

    # Get version info
    version_info = process_group.component.version_control_information
    deployed_version = version_info.version if version_info else "unknown"

    log.info(
        "Deployed %s (ID: %s, version: %s)",
        process_group.component.name,
        process_group.id,
        deployed_version,
    )

    return {
        "process_group_id": process_group.id,
        "process_group_name": process_group.component.name,
        "deployed_version": deployed_version,
    }
