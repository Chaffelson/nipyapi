# pylint: disable=broad-exception-caught
"""
list_registry_flows - list flows available in a Git registry bucket.
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def list_registry_flows(  # pylint: disable=too-many-locals
    registry_client: Optional[str] = None,
    bucket: Optional[str] = None,
    branch: Optional[str] = None,
    detailed: bool = False,
    greedy: bool = False,
) -> dict:
    """
    List flows available in a Git registry bucket.

    This function queries a Git-based Flow Registry to list available flows
    within a bucket. Useful for discovering what flows can be deployed.

    Args:
        registry_client: Registry client ID (UUID) or name. Auto-detects which
            based on format. Env: NIFI_REGISTRY_CLIENT_ID
        bucket: Bucket (folder) containing flows. Env: NIFI_BUCKET
        branch: Branch to query. Env: NIFI_FLOW_BRANCH. If not specified,
                uses the registry client's default branch.
        detailed: If True, include description and comments for each flow.
                 Default False returns minimal info (name, flow_id).
        greedy: If True, allow partial name matching for registry_client.
                Default False (exact match for safety in CI/automation).

    Returns:
        dict with:
        - registry_client_id: The resolved registry client ID
        - registry_client_name: The registry client name
        - bucket: The bucket queried
        - branch: The branch queried (if specified)
        - flow_count: Number of flows found
        - flows: List of flow info dicts

    Raises:
        ValueError: If registry client or bucket not found, or multiple
                   registry clients match when greedy=False.

    Example::

        # List all flows in bucket
        nipyapi ci list_registry_flows --registry_client my-github --bucket flows

        # With full details
        nipyapi ci list_registry_flows --registry_client my-github --bucket flows --detailed
    """
    # Resolve from env vars
    registry_client = registry_client or os.environ.get("NIFI_REGISTRY_CLIENT_ID")
    bucket = bucket or os.environ.get("NIFI_BUCKET")
    branch = branch or os.environ.get("NIFI_FLOW_BRANCH") or None

    # Validate required params
    if not registry_client:
        raise ValueError("registry_client is required (or set NIFI_REGISTRY_CLIENT_ID)")
    if not bucket:
        raise ValueError("bucket is required (or set NIFI_BUCKET)")

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
    registry_client_name = client.component.name

    log.info(
        "Listing flows in bucket '%s' from registry '%s'",
        bucket,
        registry_client_name,
    )

    # List flows in bucket
    flows_entity = nipyapi.versioning.list_git_registry_flows(
        registry_client_id=registry_client_id,
        bucket_id=bucket,
        branch=branch,
    )

    flows_list = []
    versioned_flows = flows_entity.versioned_flows or []

    for item in versioned_flows:
        flow = item.versioned_flow
        entry = {
            "name": flow.flow_name,
            "flow_id": flow.flow_id,
        }
        if detailed:
            entry["description"] = flow.description or ""
            entry["comments"] = flow.comments or ""

        flows_list.append(entry)

    # Sort by name for consistent output
    flows_list.sort(key=lambda x: x["name"].lower())

    log.info("Found %d flow(s) in bucket '%s'", len(flows_list), bucket)

    result = {
        "registry_client_id": registry_client_id,
        "registry_client_name": registry_client_name,
        "bucket": bucket,
        "flow_count": str(len(flows_list)),
        "flows": flows_list,
    }

    if branch:
        result["branch"] = branch

    return result
