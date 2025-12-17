"""
For interactions with the NiFi Registry Service and related functions
"""

# pylint: disable=C0302

import logging

import nipyapi

# Due to line lengths, creating shortened names for these objects
from nipyapi.nifi import VersionControlInformationDTO as VciDTO
from nipyapi.registry import VersionedFlowSnapshotMetadata as VfsMd

__all__ = [
    # Registry Client Management (works with all registry types)
    "create_registry_client",
    "list_registry_clients",
    "list_registry_client_types",
    "delete_registry_client",
    "get_registry_client",
    "ensure_registry_client",
    "update_registry_client",
    # Git-based Registry Functions (GitHub, GitLab, Bitbucket, Azure DevOps)
    "list_git_registry_buckets",
    "get_git_registry_bucket",
    "list_git_registry_flows",
    "get_git_registry_flow",
    "list_git_registry_flow_versions",
    "deploy_git_registry_flow",
    "save_git_flow_ver",
    "get_local_modifications",
    # NiFi Registry Bucket Functions
    "list_registry_buckets",
    "create_registry_bucket",
    "delete_registry_bucket",
    "get_registry_bucket",
    "ensure_registry_bucket",
    # Flow Version Management
    "save_flow_ver",
    "list_flows_in_bucket",
    "get_flow_in_bucket",
    "get_latest_flow_ver",
    "update_flow_ver",
    "get_version_info",
    "create_flow",
    "create_flow_version",
    "get_flow_version",
    "export_flow_version",
    "import_flow_version",
    "list_flow_versions",
    "deploy_flow_version",
    # Process Group Export/Import (no registry required)
    "export_process_group_definition",
    "import_process_group_definition",
]

log = logging.getLogger(__name__)


def create_registry_client(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    name, uri=None, description="", reg_type=None, properties=None, ssl_context_service=None
):
    """
    Creates a Registry Client in the NiFi Controller Services

    Args:
        name (str): The name of the new Client
        uri (str, optional): The URI for the connection. Required for NiFi Registry.
            Ignored for Git-based registries. Defaults to None.
        description (str, optional): A description for the Client. Defaults to empty string.
        reg_type (str, optional): The type of registry client to create.
            Defaults to 'org.apache.nifi.registry.flow.NifiRegistryFlowRegistryClient'.
            Other options include:
            - 'org.apache.nifi.github.GitHubFlowRegistryClient'
            - 'org.apache.nifi.gitlab.GitLabFlowRegistryClient'
            - 'org.apache.nifi.atlassian.bitbucket.BitbucketFlowRegistryClient'
            - 'org.apache.nifi.azure.devops.AzureDevOpsFlowRegistryClient'
        properties (dict, optional): Properties to configure the client. If provided,
            these are used directly. If not provided, defaults are used based on reg_type.
            For NiFi Registry, defaults to {'url': uri} if uri is provided.
            For Git-based registries, starts empty (must be configured).
        ssl_context_service (ControllerServiceEntity, optional): SSL Context Service
            (only applicable for NiFi Registry type). Defaults to None.

    Returns:
        :class:`~nipyapi.nifi.models.FlowRegistryClientEntity`: The new registry client object

    Example:
        >>> # NiFi Registry client
        >>> nifi_reg = nipyapi.versioning.create_registry_client(
        ...     name='my-registry',
        ...     uri='http://localhost:18080',
        ...     description='My NiFi Registry'
        ... )

        >>> # GitHub client with properties
        >>> github_client = nipyapi.versioning.create_registry_client(
        ...     name='github-reg',
        ...     reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        ...     description='GitHub Registry',
        ...     properties={
        ...         'Repository Owner': 'myorg',
        ...         'Repository Name': 'myrepo',
        ...         'Authentication Type': 'PERSONAL_ACCESS_TOKEN',
        ...         'Personal Access Token': 'ghp_xxx...',
        ...         'Default Branch': 'main'
        ...     }
        ... )
    """
    assert isinstance(name, str) and name is not False
    assert isinstance(description, str)

    # Determine the registry type
    client_type = reg_type or "org.apache.nifi.registry.flow.NifiRegistryFlowRegistryClient"

    # NiFi Registry uses 'url' property, Git-based registries do not
    is_nifi_registry = "NifiRegistryFlowRegistryClient" in client_type

    # Build properties based on what was provided
    if properties is not None:
        # User provided explicit properties - use them
        client_properties = properties.copy()
    elif is_nifi_registry:
        # NiFi Registry requires 'url' property
        assert (
            isinstance(uri, str) and uri is not False
        ), "uri is required for NiFi Registry clients when properties are not provided"
        client_properties = {"url": uri}
    else:
        # Git-based registries start with empty properties
        client_properties = {}

    component = {
        "name": name,
        "description": description,
        "type": client_type,
        "properties": client_properties,
    }

    with nipyapi.utils.rest_exceptions():
        controller = nipyapi.nifi.ControllerApi().create_flow_registry_client(
            body={"component": component, "revision": {"version": 0}}
        )

    # Update with SSL context if provided (only for NiFi Registry)
    if ssl_context_service and is_nifi_registry:
        update_component = dict(controller.component.to_dict())
        update_component["properties"] = {"url": uri, "ssl-context-service": ssl_context_service.id}

        with nipyapi.utils.rest_exceptions():
            controller = nipyapi.nifi.ControllerApi().update_flow_registry_client(
                id=controller.id,
                body={
                    "component": update_component,
                    "revision": {"version": controller.revision.version},
                },
            )

    return controller


def delete_registry_client(client, refresh=True):
    """
    Deletes a Registry Client from the list of NiFI Controller Services

    Args:
        client (FlowRegistryClientEntity): The client to delete
        refresh (bool): Whether to refresh the object before action

    Returns:
        (FlowRegistryClientEntity): The updated client object
    """
    assert isinstance(client, nipyapi.nifi.FlowRegistryClientEntity)
    with nipyapi.utils.rest_exceptions():
        if refresh:
            target = nipyapi.nifi.ControllerApi().get_flow_registry_client(client.id)
        else:
            target = client
        return nipyapi.nifi.ControllerApi().delete_flow_registry_client(
            id=target.id, version=target.revision.version
        )


def update_registry_client(client, properties=None, description=None, refresh=True):
    """
    Updates an existing Registry Client's configuration.

    This function merges provided properties with existing ones, allowing
    partial updates. Sensitive properties (e.g., tokens) are always applied
    if provided, since existing values cannot be inspected for comparison.

    Args:
        client (FlowRegistryClientEntity): The client to update
        properties (dict, optional): Properties to update. Merged with existing.
        description (str, optional): New description. If None, keeps existing.
        refresh (bool): Whether to refresh the object before action to get
            current revision. Defaults to True.

    Returns:
        (FlowRegistryClientEntity): The updated client object

    Example:
        >>> client = nipyapi.versioning.get_registry_client("GitHub-FlowRegistry")
        >>> updated = nipyapi.versioning.update_registry_client(
        ...     client,
        ...     properties={'Default Branch': 'feature-branch'}
        ... )
    """
    assert isinstance(client, nipyapi.nifi.FlowRegistryClientEntity)

    with nipyapi.utils.rest_exceptions():
        # Refresh to get current revision and properties
        if refresh:
            target = nipyapi.nifi.ControllerApi().get_flow_registry_client(client.id)
        else:
            target = client

        # Merge properties: existing + provided (provided wins)
        merged_properties = dict(target.component.properties or {})
        if properties:
            merged_properties.update(properties)

        # Use provided description or keep existing
        new_description = description if description is not None else target.component.description

        # Build update body
        update_dto = nipyapi.nifi.FlowRegistryClientDTO(
            id=target.id,
            name=target.component.name,
            type=target.component.type,
            description=new_description,
            properties=merged_properties,
        )

        update_entity = nipyapi.nifi.FlowRegistryClientEntity(
            component=update_dto, revision=target.revision
        )

        return nipyapi.nifi.ControllerApi().update_flow_registry_client(
            id=target.id, body=update_entity
        )


def list_registry_clients():
    """
    Lists the available Registry Clients in the NiFi Controller Services

    Returns:
        list[:class:`~nipyapi.nifi.models.FlowRegistryClientEntity`]: objects
    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ControllerApi().get_flow_registry_clients()


def list_registry_client_types():
    """
    Lists all available Flow Registry Client types in the NiFi instance.

    This includes built-in registry types like:
    - NiFi Registry (org.apache.nifi.registry.flow.NifiRegistryFlowRegistryClient)
    - GitHub (org.apache.nifi.github.GitHubFlowRegistryClient)
    - GitLab (org.apache.nifi.gitlab.GitLabFlowRegistryClient)
    - Bitbucket (org.apache.nifi.atlassian.bitbucket.BitbucketFlowRegistryClient)
    - Azure DevOps (org.apache.nifi.azure.devops.AzureDevOpsFlowRegistryClient)

    Returns:
        list[:class:`~nipyapi.nifi.models.DocumentedTypeDTO`]: List of available
            registry client types with their properties and descriptions

    Example:
        >>> types = nipyapi.versioning.list_registry_client_types()
        >>> github_type = [t for t in types if 'GitHub' in t.type][0]
        >>> print(github_type.type)
        org.apache.nifi.github.GitHubFlowRegistryClient
    """
    with nipyapi.utils.rest_exceptions():
        result = nipyapi.nifi.ControllerApi().get_registry_client_types()
        return result.flow_registry_client_types


def get_registry_client(identifier, identifier_type="name"):
    """
    Filters the Registry clients to a particular identifier

    Args:
        identifier (str): the filter string
        identifier_type (str): the parameter to filter on

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches
    """
    with nipyapi.utils.rest_exceptions():
        obj = list_registry_clients().registries
    return nipyapi.utils.filter_obj(obj, identifier, identifier_type)


def ensure_registry_client(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    name, uri=None, description="", reg_type=None, properties=None, ssl_context_service=None
):
    """
    Ensures a Registry Client exists with the desired configuration.

    This is a convenience function that implements the common pattern of:
    1. Try to get existing client by name
    2. If found and properties provided, update the client
    3. If not found, create it
    4. Handle race conditions gracefully

    For Git-based registries (GitHub, GitLab, etc.), if properties are provided
    and client exists, the client will be updated. This supports CI/CD workflows
    where branch or credentials may change between deployments. Sensitive
    properties (like tokens) are always applied if provided since existing
    values cannot be inspected.

    Args:
        name (str): The name of the Client
        uri (str, optional): The URI for the connection. Required for NiFi Registry.
            Ignored for Git-based registries. Defaults to None.
        description (str, optional): A description for the Client. Defaults to empty string.
        reg_type (str, optional): The type of registry client to create.
            Defaults to 'org.apache.nifi.registry.flow.NifiRegistryFlowRegistryClient'
        properties (dict, optional): Properties to configure the client. If provided
            and client exists, will update the existing client with these properties.
        ssl_context_service (ControllerServiceEntity, optional): SSL Context Service

    Returns:
        (FlowRegistryClientEntity): The registry client object (existing, updated, or new)

    Note:
        For NiFi Registry clients, URI mismatch triggers recreation.
        For Git-based clients, properties trigger an update (not recreation).
    """
    # Determine if this is a NiFi Registry or Git-based registry
    client_type = reg_type or "org.apache.nifi.registry.flow.NifiRegistryFlowRegistryClient"
    is_nifi_registry = "NifiRegistryFlowRegistryClient" in client_type

    # Try to get existing client first
    try:
        existing = get_registry_client(name)
        if existing:
            # Handle both single object and list of objects
            if isinstance(existing, list):
                # Multiple matches - use the first one
                log.warning(
                    "Multiple registry clients found with name '%s', using first match", name
                )
                existing = existing[0]

            # For NiFi Registry, check if URI matches
            if is_nifi_registry and uri:
                existing_uri = existing.component.properties.get("url", "")
                if existing_uri == uri:
                    log.debug("Found existing registry client with matching URI: %s", name)
                    return existing

                # URI mismatch - delete existing and create new one
                log.debug(
                    "Registry client %s URI mismatch (existing: %s, desired: %s) - recreating",
                    name,
                    existing_uri,
                    uri,
                )
                delete_registry_client(existing)
            else:
                # For Git-based registries: update if properties provided, else return existing
                if properties:
                    log.debug("Updating existing registry client with new properties: %s", name)
                    return update_registry_client(
                        existing, properties=properties, description=description
                    )
                log.debug("Found existing registry client: %s", name)
                return existing
    except ValueError:
        # Client doesn't exist, we'll create it below
        pass

    # Try to create new client
    try:
        client = create_registry_client(
            name, uri, description, reg_type, properties, ssl_context_service
        )
        log.debug("Created new registry client: %s", name)
        return client
    except Exception as e:
        # Handle race condition where client was created between check and creation
        error_msg = str(e).lower()
        if "already exists" in error_msg or "duplicate" in error_msg:
            try:
                existing = get_registry_client(name)
                if existing:
                    # Handle both single object and list of objects
                    if isinstance(existing, list):
                        log.warning(
                            "Multiple registry clients found with name '%s' "
                            "after race condition, using first match",
                            name,
                        )
                        existing = existing[0]
                    log.debug("Found existing registry client after race condition: %s", name)
                    return existing
            except ValueError:
                # If we still can't find it, something else is wrong
                pass
        # Re-raise the original exception if we can't handle it
        raise e


# =============================================================================
# Git-based Registry Functions (GitHub, GitLab, Bitbucket, Azure DevOps)
# =============================================================================
# These functions work with Git-based Flow Registry Clients via the NiFi FlowApi.
# They are separate from the NiFi Registry functions which use the Registry API.


def list_git_registry_buckets(registry_client_id, branch=None):
    """
    List buckets (folders) from a Git-based registry client.

    This function queries a Git-based Flow Registry Client (GitHub, GitLab,
    Bitbucket, or Azure DevOps) via the NiFi FlowApi to list available buckets.
    In Git-based registries, buckets correspond to folders in the repository.

    Args:
        registry_client_id (str): The ID of the Git-based registry client.
        branch (str, optional): The branch to query. If None, uses the
            registry client's configured default branch.

    Returns:
        :class:`~nipyapi.nifi.models.FlowRegistryBucketsEntity`

    Example:
        >>> client = nipyapi.versioning.get_registry_client('my-github-client')
        >>> buckets = nipyapi.versioning.list_git_registry_buckets(client.id)
        >>> for b in buckets.buckets:
        ...     print(f"{b.id}: {b.bucket.name}")
    """
    assert isinstance(registry_client_id, str), "registry_client_id must be a string"

    with nipyapi.utils.rest_exceptions():
        if branch is not None:
            return nipyapi.nifi.FlowApi().get_buckets(registry_client_id, branch=branch)
        return nipyapi.nifi.FlowApi().get_buckets(registry_client_id)


def get_git_registry_bucket(registry_client_id, identifier, greedy=True, branch=None):
    """
    Filters the bucket list from a Git-based registry client.

    Args:
        registry_client_id (str): The ID of the Git-based registry client.
        identifier (str): The bucket name (folder name in the repository).
        greedy (bool): False for exact match, True for greedy/partial match.
        branch (str, optional): The branch to query. If None, uses the
            registry client's configured default branch.

    Returns:
        None for no matches, single object for unique match,
        list of objects for multiple matches.

    Example:
        >>> client = nipyapi.versioning.get_registry_client('my-github-client')
        >>> bucket = nipyapi.versioning.get_git_registry_bucket(
        ...     client.id, 'flows', greedy=False
        ... )
    """
    buckets_entity = list_git_registry_buckets(registry_client_id, branch=branch)
    obj = buckets_entity.buckets if buckets_entity.buckets else []
    return nipyapi.utils.filter_obj(obj, identifier, "name", greedy=greedy)


def list_git_registry_flows(registry_client_id, bucket_id, branch=None):
    """
    List flows in a bucket from a Git-based registry client.

    This function queries a Git-based Flow Registry Client to list available
    flows within a specific bucket. In Git-based registries, flows are JSON
    files within the bucket folder (e.g., `flows/my-flow.json`).

    Args:
        registry_client_id (str): The ID of the Git-based registry client.
        bucket_id (str): The bucket ID (folder name) to list flows from.
        branch (str, optional): The branch to query. If None, uses the
            registry client's configured default branch.

    Returns:
        :class:`~nipyapi.nifi.models.VersionedFlowsEntity`

    Example:
        >>> client = nipyapi.versioning.get_registry_client('my-github-client')
        >>> flows = nipyapi.versioning.list_git_registry_flows(client.id, 'flows')
        >>> for f in flows.versioned_flows:
        ...     print(f.versioned_flow.flow_id)
    """
    assert isinstance(registry_client_id, str), "registry_client_id must be a string"
    assert isinstance(bucket_id, str), "bucket_id must be a string"

    with nipyapi.utils.rest_exceptions():
        if branch is not None:
            return nipyapi.nifi.FlowApi().get_flows(registry_client_id, bucket_id, branch=branch)
        return nipyapi.nifi.FlowApi().get_flows(registry_client_id, bucket_id)


def get_git_registry_flow(registry_client_id, bucket_id, identifier, greedy=True, branch=None):
    """
    Filters the flow list in a bucket from a Git-based registry client.

    Args:
        registry_client_id (str): The ID of the Git-based registry client.
        bucket_id (str): The bucket name (folder name) containing the flows.
        identifier (str): The flow name (filename without .json).
        greedy (bool): False for exact match, True for greedy/partial match.
        branch (str, optional): The branch to query. If None, uses the
            registry client's configured default branch.

    Returns:
        None for no matches, single object for unique match,
        list of objects for multiple matches.

    Example:
        >>> client = nipyapi.versioning.get_registry_client('my-github-client')
        >>> flow = nipyapi.versioning.get_git_registry_flow(
        ...     client.id, 'flows', 'http-responder', greedy=False
        ... )
    """
    flows_entity = list_git_registry_flows(registry_client_id, bucket_id, branch=branch)
    obj = flows_entity.versioned_flows if flows_entity.versioned_flows else []

    # The flows are wrapped in versioned_flow objects, so we filter on the inner object
    if obj:
        inner_flows = [item.versioned_flow for item in obj]
        filtered = nipyapi.utils.filter_obj(inner_flows, identifier, "flow_name", greedy=greedy)
        if filtered is None:
            return None
        if isinstance(filtered, list):
            return [item for item in obj if item.versioned_flow in filtered]
        # Single match - find the wrapper
        for item in obj:
            if item.versioned_flow == filtered:
                return item
        return filtered

    return None


def list_git_registry_flow_versions(registry_client_id, bucket_id, flow_id, branch=None):
    """
    List all versions of a flow from a Git-based registry client.

    Args:
        registry_client_id (str): The ID of the Git-based registry client.
        bucket_id (str): The bucket name (folder name) containing the flow.
        flow_id (str): The flow name (filename without .json) to list versions.
        branch (str, optional): The branch to query. If None, uses the
            registry client's configured default branch.

    Returns:
        :class:`~nipyapi.nifi.models.VersionedFlowSnapshotMetadataSetEntity`

    Example:
        >>> client = nipyapi.versioning.get_registry_client('my-github-client')
        >>> versions = nipyapi.versioning.list_git_registry_flow_versions(
        ...     client.id, 'flows', 'http-responder'
        ... )
    """
    with nipyapi.utils.rest_exceptions():
        if branch is not None:
            return nipyapi.nifi.FlowApi().get_versions(
                registry_id=registry_client_id, bucket_id=bucket_id, flow_id=flow_id, branch=branch
            )
        return nipyapi.nifi.FlowApi().get_versions(
            registry_id=registry_client_id, bucket_id=bucket_id, flow_id=flow_id
        )


def deploy_git_registry_flow(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    registry_client_id, bucket_id, flow_id, parent_id, location=None, version=None, branch=None
):
    """
    Deploy a flow from a Git-based registry to the NiFi canvas.

    Creates a new Process Group under the specified parent, linked to version
    control from the Git-based registry. The deployed flow will track the
    specified version (or latest) from the repository.

    Args:
        registry_client_id (str): The ID of the Git-based registry client.
        bucket_id (str): The bucket name (folder name) containing the flow.
        flow_id (str): The flow name (filename without .json).
        parent_id (str): The ID of the parent Process Group to deploy into.
        location (tuple, optional): (x, y) coordinates for placement.
            Defaults to (0, 0).
        version (str, optional): Specific version (commit hash) to deploy.
            If None, deploys the latest version.
        branch (str, optional): The branch to deploy from. If None, uses
            the registry client's configured default branch.

    Returns:
        :class:`~nipyapi.nifi.models.ProcessGroupEntity`: The newly deployed
            Process Group.

    Example:
        >>> client = nipyapi.versioning.get_registry_client('my-github-client')
        >>> root_id = nipyapi.canvas.get_root_pg_id()
        >>> pg = nipyapi.versioning.deploy_git_registry_flow(
        ...     client.id, 'flows', 'http-responder', root_id
        ... )
    """
    location = location or (0, 0)
    assert isinstance(location, tuple), "location must be a tuple of (x, y)"

    # Get available versions
    flow_versions = list_git_registry_flow_versions(
        registry_client_id, bucket_id, flow_id, branch=branch
    )

    if not flow_versions or not flow_versions.versioned_flow_snapshot_metadata_set:
        raise ValueError(
            f"Could not find flow '{flow_id}' in bucket '{bucket_id}' "
            f"on registry client '{registry_client_id}'"
        )

    # Select version to deploy
    if version is None:
        # Deploy latest version - sort by timestamp descending to get most recent
        sorted_versions = sorted(
            flow_versions.versioned_flow_snapshot_metadata_set,
            key=lambda x: x.versioned_flow_snapshot_metadata.timestamp or 0,
            reverse=True,
        )
        target_flow = sorted_versions[0]
    else:
        # Find specific version
        matches = [
            v
            for v in flow_versions.versioned_flow_snapshot_metadata_set
            if str(v.versioned_flow_snapshot_metadata.version) == str(version)
        ]
        if not matches:
            available = [
                str(v.versioned_flow_snapshot_metadata.version)[:12]
                for v in flow_versions.versioned_flow_snapshot_metadata_set
            ]
            raise ValueError(
                f"Version '{version}' not found for flow '{flow_id}'. "
                f"Available versions: {', '.join(available[:5])}"
            )
        target_flow = matches[0]

    target_metadata = target_flow.versioned_flow_snapshot_metadata

    # Use branch from metadata if not explicitly provided
    deploy_branch = branch if branch is not None else target_metadata.branch

    # Deploy the flow
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_process_group(
            id=parent_id,
            body=nipyapi.nifi.ProcessGroupEntity(
                revision=nipyapi.nifi.RevisionDTO(version=0),
                component=nipyapi.nifi.ProcessGroupDTO(
                    position=nipyapi.nifi.PositionDTO(x=float(location[0]), y=float(location[1])),
                    version_control_information=VciDTO(
                        registry_id=registry_client_id,
                        bucket_id=target_metadata.bucket_identifier,
                        flow_id=target_metadata.flow_identifier,
                        version=target_metadata.version,
                        branch=deploy_branch,
                    ),
                ),
            ),
        )


def update_git_flow_ver(process_group, target_version=None, branch=None):
    """
    Changes a Git-registry versioned flow to the specified version.

    This function works with Git-based Flow Registry Clients (GitHub, GitLab, etc.)
    where versions are identified by commit SHAs rather than integer version numbers.

    Args:
        process_group (ProcessGroupEntity): ProcessGroupEntity under Git-based
            version control to change.
        target_version (str, optional): The commit SHA to change to. If None,
            changes to the latest available version.
        branch (str, optional): The branch to use when finding versions. If None,
            uses the branch from the current version control information.

    Returns:
        VersionedFlowUpdateRequestEntity: The completed update request with
            status information.

    Raises:
        ValueError: If the process group is not under version control, if the
            target version is not found, or if the update fails.

    Example:
        >>> pg = nipyapi.canvas.get_process_group('my-flow', 'name')
        >>> # Change to a specific commit
        >>> result = nipyapi.versioning.update_git_flow_ver(pg, 'abc123def456')
        >>> # Change to latest version
        >>> result = nipyapi.versioning.update_git_flow_ver(pg)
    """

    def _running_update_flow_version():
        """Tests for completion of the version update operation."""
        status = nipyapi.nifi.VersionsApi().get_update_request(u_init.request.request_id)
        if not status.request.complete:
            return False
        if status.request.failure_reason is None:
            return True
        raise ValueError(
            "Flow Version Update did not complete successfully. "
            "Error: {0}".format(status.request.failure_reason)
        )

    with nipyapi.utils.rest_exceptions():
        # Get current version control info
        vci = get_version_info(process_group)
        if vci is None or vci.version_control_information is None:
            raise ValueError(
                "Process group is not under version control. "
                "Cannot change version of an unversioned process group."
            )

        current_vci = vci.version_control_information

        # Determine branch to use
        use_branch = branch if branch is not None else current_vci.branch

        # Get available versions from the git registry
        flow_versions = list_git_registry_flow_versions(
            current_vci.registry_id, current_vci.bucket_id, current_vci.flow_id, branch=use_branch
        )

        if not flow_versions or not flow_versions.versioned_flow_snapshot_metadata_set:
            raise ValueError(
                f"Could not find any versions for flow '{current_vci.flow_id}' "
                f"in bucket '{current_vci.bucket_id}'"
            )

        # Select target version
        if target_version is None:
            # Get latest version - sort by timestamp descending
            sorted_versions = sorted(
                flow_versions.versioned_flow_snapshot_metadata_set,
                key=lambda x: x.versioned_flow_snapshot_metadata.timestamp or 0,
                reverse=True,
            )
            ver = sorted_versions[0].versioned_flow_snapshot_metadata.version
        else:
            # Find specific version by SHA
            matches = [
                v
                for v in flow_versions.versioned_flow_snapshot_metadata_set
                if str(v.versioned_flow_snapshot_metadata.version) == str(target_version)
            ]
            if not matches:
                available = [
                    str(v.versioned_flow_snapshot_metadata.version)[:12]
                    for v in flow_versions.versioned_flow_snapshot_metadata_set
                ]
                raise ValueError(
                    f"Version '{target_version}' not found. "
                    f"Available versions: {', '.join(available[:5])}"
                )
            ver = target_version

        # Check if already at target version
        if current_vci.version == ver:
            # Return a mock response indicating no change needed
            # We still return the current state for consistency
            return nipyapi.nifi.VersionsApi().get_version_information(process_group.id)

        # Initiate the version update
        u_init = nipyapi.nifi.VersionsApi().initiate_version_control_update(
            id=process_group.id,
            body=nipyapi.nifi.VersionControlInformationEntity(
                process_group_revision=vci.process_group_revision,
                version_control_information=VciDTO(
                    bucket_id=current_vci.bucket_id,
                    flow_id=current_vci.flow_id,
                    group_id=current_vci.group_id,
                    registry_id=current_vci.registry_id,
                    version=ver,
                    branch=use_branch,
                ),
            ),
        )

        # Wait for completion
        nipyapi.utils.wait_to_complete(_running_update_flow_version)
        return nipyapi.nifi.VersionsApi().get_update_request(u_init.request.request_id)


# pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
# pylint: disable=too-many-branches
def save_git_flow_ver(
    process_group,
    registry_client=None,
    bucket=None,
    flow_name=None,
    comment="",
    desc="",
    force=False,
    refresh=True,
):
    """
    Saves a process group to a Git-based Flow Registry.

    This function works with Git-based Flow Registry Clients (GitHub, GitLab, etc.)
    and handles both:
    - Initial commits: Starting version control for a process group
    - Subsequent commits: Saving a new version to an already versioned flow

    For initial commits, registry_client and bucket are required.
    For subsequent commits, the existing version control information is used.

    Args:
        process_group (ProcessGroupEntity or str): The ProcessGroup to save,
            or its ID as a string.
        registry_client (FlowRegistryClientEntity or str, optional): The Git
            registry client, or its name/ID. Required for initial commit.
        bucket (str, optional): The bucket/folder name in the Git registry.
            Required for initial commit.
        flow_name (str, optional): Name for the flow in the registry. Defaults
            to the process group name. Only used for initial commit.
        comment (str): Commit message for this version.
        desc (str): Description for the flow (initial commit only).
        force (bool): If True, use FORCE_COMMIT to ignore merge conflicts.
        refresh (bool): Whether to refresh the process group before saving.

    Returns:
        VersionControlInformationEntity: The version control information
            after the commit.

    Raises:
        ValueError: If required parameters are missing or objects not found.

    Example:
        >>> pg = nipyapi.canvas.get_process_group('my-flow', 'name')
        >>> # Initial commit - start version control
        >>> result = nipyapi.versioning.save_git_flow_ver(
        ...     pg, registry_client='MyGitHubClient', bucket='flows',
        ...     comment='Initial commit'
        ... )
        >>> # Subsequent commit - save new version
        >>> result = nipyapi.versioning.save_git_flow_ver(pg, comment='Fixed bug')
    """
    # Resolve process group if string ID provided
    if isinstance(process_group, str):
        target_pg = nipyapi.canvas.get_process_group(process_group, "id")
        if not target_pg:
            raise ValueError(f"Process group not found: {process_group}")
    elif refresh:
        target_pg = nipyapi.canvas.get_process_group(process_group.id, "id")
    else:
        target_pg = process_group

    # Check if already under version control
    vci = target_pg.component.version_control_information
    initial_commit = vci is None

    if initial_commit:
        # Initial commit - registry_client and bucket required
        if not registry_client:
            raise ValueError(
                "registry_client is required for initial commit "
                "(process group not under version control)"
            )
        if not bucket:
            raise ValueError(
                "bucket is required for initial commit (process group not under version control)"
            )

        # Resolve registry client
        if isinstance(registry_client, str):
            reg = get_registry_client(registry_client)
            if not reg:
                raise ValueError(f"Registry client not found: {registry_client}")
        else:
            reg = registry_client

        # Get Git bucket
        git_bucket = get_git_registry_bucket(reg.id, bucket)
        if not git_bucket:
            raise ValueError(f"Bucket not found in registry: {bucket}")

        # Use the bucket ID from the git bucket object
        bucket_id = git_bucket.id
        registry_id = reg.id
        resolved_flow_name = flow_name or target_pg.component.name
        flow_id = None  # None for initial commit

        log.info(
            "Starting Git version control for '%s' in %s/%s",
            resolved_flow_name,
            reg.component.name,
            bucket,
        )
    else:
        # Subsequent commit - use existing version control info
        if vci.state == "UP_TO_DATE":
            log.warning("Flow has no local modifications - nothing to commit")
            return nipyapi.nifi.VersionsApi().get_version_information(target_pg.id)

        bucket_id = vci.bucket_id
        registry_id = vci.registry_id
        resolved_flow_name = vci.flow_id
        flow_id = vci.flow_id

        log.info(
            "Saving new version of '%s' (state: %s)",
            target_pg.component.name,
            vci.state,
        )

    # Build the VersionedFlowDTO with Git-specific action field
    action = "FORCE_COMMIT" if force else "COMMIT"
    flow_dto = nipyapi.nifi.VersionedFlowDTO(
        bucket_id=bucket_id,
        comments=comment,
        description=desc or f"Flow: {resolved_flow_name}",
        flow_name=resolved_flow_name,
        flow_id=flow_id,
        registry_id=registry_id,
        action=action,
    )

    log.debug("Committing with action: %s", action)

    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.VersionsApi().save_to_flow_registry(
            id=target_pg.id,
            body=nipyapi.nifi.StartVersionControlRequestEntity(
                process_group_revision=target_pg.revision,
                versioned_flow=flow_dto,
            ),
        )


def get_local_modifications(process_group):
    """
    Get local modifications to a versioned process group.

    Returns structured information about all local changes made to a
    version-controlled process group since the last commit/sync.

    This is useful for:
    - Reviewing changes before committing
    - Capturing modifications before an upgrade to re-apply afterward
    - Auditing what has changed in a flow

    Args:
        process_group (ProcessGroupEntity or str): The versioned ProcessGroup,
            or its ID as a string.

    Returns:
        FlowComparisonEntity: The comparison result containing:
            - component_differences: List of ComponentDifferenceDTO objects
              with component_id, component_name, component_type, and
              differences (list of DifferenceDTO with difference_type and
              difference description)

    Raises:
        ValueError: If the process group is not found or not under version control.

    Example:
        >>> pg = nipyapi.canvas.get_process_group('my-flow', 'name')
        >>> diff = nipyapi.versioning.get_local_modifications(pg)
        >>> for component in diff.component_differences:
        ...     print(f"{component.component_name}: {len(component.differences)} changes")
    """
    # Resolve process group if string ID provided
    if isinstance(process_group, str):
        target_pg = nipyapi.canvas.get_process_group(process_group, "id")
        if not target_pg:
            raise ValueError(f"Process group not found: {process_group}")
        pg_id = process_group
    else:
        target_pg = process_group
        pg_id = process_group.id

    # Check if under version control
    vci = target_pg.component.version_control_information
    if not vci:
        raise ValueError(f"Process group '{target_pg.component.name}' is not under version control")

    log.info(
        "Getting local modifications for '%s' (state: %s)",
        target_pg.component.name,
        vci.state,
    )

    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().get_local_modifications(pg_id)


def list_registry_buckets():
    """
    Lists all available Buckets in the NiFi Registry

    Returns:
        list[:class:`~nipyapi.registry.models.Bucket`]: objects
    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.registry.BucketsApi().get_buckets()


def create_registry_bucket(name, description=None):
    """
    Creates a new Registry Bucket

    Args:
        name (str): name for the bucket, must be unique in the Registry
        description (str, optional): description for the bucket

    Returns:
        :class:`~nipyapi.registry.models.Bucket`: The new Bucket object
    """
    with nipyapi.utils.rest_exceptions():
        # Create a proper Bucket object with all supported fields
        bucket_obj = nipyapi.registry.models.Bucket(name=name, description=description)

        bucket = nipyapi.registry.BucketsApi().create_bucket(body=bucket_obj)
        log.debug(
            "Created bucket %s against registry connection at %s",
            bucket.identifier,
            nipyapi.config.registry_config.api_client.host,
        )
        return bucket


def ensure_registry_bucket(name, description=None):
    """
    Ensures a Registry Bucket exists, creating it if necessary.

    This is a convenience function that implements the common pattern of:
    1. Try to get existing bucket by name
    2. If not found, create it
    3. Handle race conditions gracefully

    Args:
        name (str): name for the bucket, must be unique in the Registry
        description (str, optional): description for the bucket (only used if creating new)

    Returns:
        (Bucket): The bucket object (existing or new)
    """
    # Try to get existing bucket first
    try:
        existing = get_registry_bucket(name)
        if existing:
            log.debug("Found existing registry bucket: %s", name)
            return existing
    except ValueError:
        # Bucket doesn't exist, we'll create it below
        pass

    # Try to create new bucket
    try:
        bucket = create_registry_bucket(name, description)
        log.debug("Created new registry bucket: %s", name)
        return bucket
    except Exception as e:
        # Handle race condition where bucket was created between check and creation
        error_msg = str(e).lower()
        if "already exists" in error_msg or "duplicate" in error_msg:
            try:
                existing = get_registry_bucket(name)
                log.debug("Found existing registry bucket after race condition: %s", name)
                return existing
            except ValueError:
                # If we still can't find it, something else is wrong
                pass
        # Re-raise the original exception if we can't handle it
        raise e


def delete_registry_bucket(bucket):
    """
    Removes a bucket from the NiFi Registry

    Args:
        bucket (Bucket): the Bucket object to remove

    Returns:
        (Bucket): The updated Bucket object
    """
    try:
        return nipyapi.registry.BucketsApi().delete_bucket(
            version=bucket.revision.version if bucket.revision is not None else 0,
            bucket_id=bucket.identifier,
        )
    except (nipyapi.registry.rest.ApiException, AttributeError) as e:
        raise ValueError(e) from e


def get_registry_bucket(identifier, identifier_type="name", greedy=True):
    """
    Filters the Bucket list to a particular identifier

    Args:
        identifier (str): the filter string
        identifier_type (str): the param to filter on
        greedy (bool): False for exact match, True for greedy match

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches
    """
    with nipyapi.utils.rest_exceptions():
        obj = list_registry_buckets()
    return nipyapi.utils.filter_obj(obj, identifier, identifier_type, greedy=greedy)


def list_flows_in_bucket(bucket_id):
    """
    List of all Flows in a given NiFi Registry Bucket

    Args:
        bucket_id (str): The UUID of the Bucket to fetch from

    Returns:
        (list[VersionedFlow]) objects
    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.registry.BucketFlowsApi().get_flows(bucket_id)


def get_flow_in_bucket(bucket_id, identifier, identifier_type="name", greedy=True):
    """
    Filters the Flows in a Bucket against a particular identifier

    Args:
        bucket_id (str): UUID of the Bucket to filter against
        identifier (str): The string to filter on
        identifier_type (str): The param to check
        greedy (bool): False for exact match, True for greedy match

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches
    """
    with nipyapi.utils.rest_exceptions():
        obj = list_flows_in_bucket(bucket_id)
    return nipyapi.utils.filter_obj(obj, identifier, identifier_type, greedy=greedy)


# pylint: disable=R0913,R0917
def save_flow_ver(
    process_group,
    registry_client,
    bucket,
    flow_name=None,
    flow_id=None,
    comment="",
    desc="",
    refresh=True,
    force=False,
):
    """
    Adds a Process Group into NiFi Registry Version Control, or saves a new
    version to an existing VersionedFlow with a new version

    Args:
        process_group (ProcessGroupEntity): the ProcessGroup object to save
            as a new Flow Version
        registry_client (RegistryClient): The Client linked to the Registry
            which contains the Bucket to save to
        bucket (Bucket): the Bucket on the NiFi Registry to save to
        flow_name (str): A name for the VersionedFlow in the Bucket
            Note you need either a name for a new VersionedFlow, or the ID of
            an existing one to save a new version
        flow_id (Optional [str]): Identifier of an existing VersionedFlow in
            the bucket, if saving a new version to an existing flow
        comment (str): A comment for the version commit
        desc (str): A description of the VersionedFlow
        refresh (bool): Whether to refresh the object revisions before action
        force (bool): Whether to Force Commit, or just regular Commit

    Returns:
        :class:`~nipyapi.nifi.models.VersionControlInformationEntity`
    """
    # Validate parameter types
    assert isinstance(
        registry_client, nipyapi.nifi.FlowRegistryClientEntity
    ), "registry_client must be a FlowRegistryClientEntity, got: {}".format(type(registry_client))
    assert isinstance(
        bucket, nipyapi.registry.Bucket
    ), "bucket must be a Registry Bucket, got: {}".format(type(bucket))
    assert isinstance(
        process_group, nipyapi.nifi.ProcessGroupEntity
    ), "process_group must be a ProcessGroupEntity, got: {}".format(type(process_group))

    if refresh:
        target_pg = nipyapi.canvas.get_process_group(process_group.id, "id")
    else:
        target_pg = process_group
    flow_dto = nipyapi.nifi.VersionedFlowDTO(
        bucket_id=bucket.identifier,
        comments=comment,
        description=desc,
        flow_name=flow_name,
        flow_id=flow_id,
        registry_id=registry_client.id,
    )
    if nipyapi.utils.check_version("1.10.0") <= 0:
        # no 'action' property in versions < 1.10
        flow_dto.action = "FORCE_COMMIT" if force else "COMMIT"
    with nipyapi.utils.rest_exceptions():
        nipyapi.utils.validate_parameters_versioning_support()
        return nipyapi.nifi.VersionsApi().save_to_flow_registry(
            id=target_pg.id,
            body=nipyapi.nifi.StartVersionControlRequestEntity(
                process_group_revision=target_pg.revision, versioned_flow=flow_dto
            ),
        )


def stop_flow_ver(process_group, refresh=True):
    """
    Removes a Process Group from Version Control

    Args:
        process_group (ProcessGroupEntity): the ProcessGroup to work with
        refresh (bool): Whether to refresh the object status before actioning

    Returns:
        :class:`~nipyapi.nifi.models.VersionControlInformationEntity`
    """
    with nipyapi.utils.rest_exceptions():
        if refresh:
            target_pg = nipyapi.canvas.get_process_group(process_group.id, "id")
        else:
            target_pg = process_group
        return nipyapi.nifi.VersionsApi().stop_version_control(
            id=target_pg.id, version=target_pg.revision.version
        )


def revert_flow_ver(process_group, wait=False):
    """
    Attempts to roll back uncommitted changes to a Process Group to the last
    committed version.

    Args:
        process_group (ProcessGroupEntity): the ProcessGroup to work with
        wait (bool): If True, waits for the revert operation to complete and
            returns the final VersionControlInformationEntity. If False
            (default), returns immediately with the request entity for
            backward compatibility.

    Returns:
        If wait=False: (VersionedFlowUpdateRequestEntity) - the initiated request
        If wait=True: (VersionControlInformationEntity) - the final state after
            revert completes

    Raises:
        ValueError: If wait=True and the revert operation fails or times out
    """
    assert isinstance(process_group, nipyapi.nifi.ProcessGroupEntity)

    with nipyapi.utils.rest_exceptions():
        # Get version control info - includes current process_group_revision
        vci = nipyapi.nifi.VersionsApi().get_version_information(process_group.id)

        revert_request = nipyapi.nifi.VersionsApi().initiate_revert_flow_version(
            id=process_group.id,
            body=vci,
        )

        if not wait:
            return revert_request

        # Wait for revert to complete by monitoring version control state
        # NiFi cleans up revert requests quickly, so we poll state instead
        def _revert_complete():
            vci = nipyapi.nifi.VersionsApi().get_version_information(process_group.id)
            # Revert is complete when state is no longer LOCALLY_MODIFIED
            # and not in a transitional state
            state = vci.version_control_information.state
            if state == "LOCALLY_MODIFIED":
                return False  # Still reverting or not started
            if state in ("UP_TO_DATE", "STALE", "SYNC_FAILURE"):
                return True  # Revert completed (success or failure)
            return False  # Unknown state, keep waiting

        nipyapi.utils.wait_to_complete(_revert_complete)

        # Return the final version control state
        return nipyapi.nifi.VersionsApi().get_version_information(process_group.id)


def list_flow_versions(bucket_id, flow_id, registry_id=None, service="registry"):
    """
    EXPERIMENTAL
    List all the versions of a given Flow in a given Bucket

    Args:
        bucket_id (str): UUID of the bucket holding the flow to be enumerated
        flow_id (str): UUID of the flow in the bucket to be enumerated
        registry_id (str): UUID of the registry client linking the bucket, only
            required if requesting flows via NiFi instead of directly Registry
        service (str): Accepts 'nifi' or 'registry', indicating which service
            to query

    Returns:
        list(VersionedFlowSnapshotMetadata) or
            (VersionedFlowSnapshotMetadataSetEntity)
    """
    assert service in ["nifi", "registry"]
    if service == "nifi":
        with nipyapi.utils.rest_exceptions():
            return nipyapi.nifi.FlowApi().get_versions(
                registry_id=registry_id, bucket_id=bucket_id, flow_id=flow_id
            )
    else:
        with nipyapi.utils.rest_exceptions():
            return nipyapi.registry.BucketFlowsApi().get_flow_versions(
                bucket_id=bucket_id, flow_id=flow_id
            )


def update_flow_ver(process_group, target_version=None):
    """
    Changes a versioned flow to the specified version, or the latest version

    Args:
        process_group (ProcessGroupEntity): ProcessGroupEntity under version
            control to change
        target_version (Optional [None, Int]): Either None to move to the
        latest available version, or Int of the version number to move to

    Returns:
        (bool): True if successful, False if not
    """

    def _running_update_flow_version():
        """
        Tests for completion of the operation

        Returns:
            (bool) Boolean of operation success
        """
        status = nipyapi.nifi.VersionsApi().get_update_request(u_init.request.request_id)
        if not status.request.complete:
            return False
        if status.request.failure_reason is None:
            return True
        raise ValueError(
            "Flow Version Update did not complete successfully. "
            "Error text {0}".format(status.request.failure_reason)
        )

    with nipyapi.utils.rest_exceptions():
        vci = get_version_info(process_group)
        assert isinstance(vci, nipyapi.nifi.VersionControlInformationEntity)
        flow_vers = list_flow_versions(
            vci.version_control_information.bucket_id, vci.version_control_information.flow_id
        )
        if target_version is None:
            # the first version is always the latest available
            ver = flow_vers[0].version
        else:
            # otherwise the version must be an int
            if not isinstance(target_version, int):
                raise ValueError(
                    "target_version must be a positive Integer to"
                    " pick a specific available version, or None"
                    " for the latest version to be fetched"
                )
            ver = target_version
        u_init = nipyapi.nifi.VersionsApi().initiate_version_control_update(
            id=process_group.id,
            body=nipyapi.nifi.VersionControlInformationEntity(
                process_group_revision=vci.process_group_revision,
                version_control_information=VciDTO(
                    bucket_id=vci.version_control_information.bucket_id,
                    flow_id=vci.version_control_information.flow_id,
                    group_id=vci.version_control_information.group_id,
                    registry_id=vci.version_control_information.registry_id,
                    version=ver,
                ),
            ),
        )
        nipyapi.utils.wait_to_complete(_running_update_flow_version)
        return nipyapi.nifi.VersionsApi().get_update_request(u_init.request.request_id)


def get_latest_flow_ver(bucket_id, flow_id):
    """
    Gets the most recent version of a VersionedFlowSnapshot from a bucket

    Args:
        bucket_id (str): the UUID of the Bucket containing the flow
        flow_id (str): the UUID of the VersionedFlow to be retrieved

    Returns:
        (VersionedFlowSnapshot)
    """
    with nipyapi.utils.rest_exceptions():
        return get_flow_version(bucket_id, flow_id, version=None)


def get_version_info(process_group):
    """
    Gets the Version Control information for a particular Process Group

    Args:
        process_group (ProcessGroupEntity): the ProcessGroup to work with

    Returns:
        :class:`~nipyapi.nifi.models.VersionControlInformationEntity`
    """
    assert isinstance(process_group, nipyapi.nifi.ProcessGroupEntity)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.VersionsApi().get_version_information(process_group.id)


def create_flow(bucket_id, flow_name, flow_desc="", flow_type="Flow"):
    """
    Creates a new VersionedFlow stub in NiFi Registry.
    Can be used to write VersionedFlow information to without using a NiFi
    Process Group directly

    Args:
        bucket_id (str): UUID of the Bucket to write to
        flow_name (str): Name for the new VersionedFlow object
        flow_desc (Optional [str]): Description for the new VersionedFlow
            object
        flow_type (Optional [str]): Type of the VersionedFlow, should be 'Flow'

    Returns:
        (VersionedFlow)
    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.registry.BucketFlowsApi().create_flow(
            bucket_id=bucket_id,
            body=nipyapi.registry.VersionedFlow(
                name=flow_name,
                description=flow_desc,
                bucket_identifier=bucket_id,
                type=flow_type,
                version_count=0,
            ),
        )


def create_flow_version(flow, flow_snapshot, refresh=True):
    """
    EXPERIMENTAL

    Writes a FlowSnapshot into a VersionedFlow as a new version update

    Note that this differs from save_flow_ver which creates a new Flow Version
    containing the snapshot. This function writes a snapshot to an existing
    Flow Version. Useful in migrating Flow Versions between environments.

    Args:
        flow (VersionedFlowObject): the VersionedFlow object to write to
        flow_snapshot (VersionedFlowSnapshot): the Snapshot to write into the
            VersionedFlow
        refresh (bool): Whether to refresh the object status before actioning

    Returns:
        The new (VersionedFlowSnapshot)
    """
    if not isinstance(flow_snapshot, nipyapi.registry.VersionedFlowSnapshot):
        raise ValueError(
            "flow_snapshot must be an instance of a "
            "registry.VersionedFlowSnapshot object, not an {0}".format(type(flow_snapshot))
        )
    with nipyapi.utils.rest_exceptions():
        if refresh:
            target_flow = get_flow_in_bucket(
                bucket_id=flow.bucket_identifier, identifier=flow.identifier, identifier_type="id"
            )
        else:
            target_flow = flow
        target_bucket = get_registry_bucket(target_flow.bucket_identifier, "id")
        # The current version of NiFi doesn't ignore link objects passed to it
        bad_params = ["link"]
        for obj in [target_bucket, target_flow]:
            for p in bad_params:
                setattr(obj, p, None)
        nipyapi.utils.validate_parameters_versioning_support(verify_nifi=False)
        ecs = flow_snapshot.external_controller_services
        return nipyapi.registry.BucketFlowsApi().create_flow_version(
            bucket_id=target_bucket.identifier,
            flow_id=target_flow.identifier,
            body=nipyapi.registry.VersionedFlowSnapshot(
                flow=target_flow,
                bucket=target_bucket,
                flow_contents=flow_snapshot.flow_contents,
                parameter_contexts=flow_snapshot.parameter_contexts,
                external_controller_services=ecs,
                snapshot_metadata=VfsMd(
                    version=target_flow.version_count + 1,
                    comments=flow_snapshot.snapshot_metadata.comments,
                    bucket_identifier=target_flow.bucket_identifier,
                    flow_identifier=target_flow.identifier,
                ),
            ),
        )


def get_flow_version(bucket_id, flow_id, version=None, export=False):
    """
    Retrieves the latest, or a specific, version of a Flow

    Args:
        bucket_id (str): the UUID of the bucket containing the Flow
        flow_id (str): the UUID of the Flow to be retrieved from the Bucket
        version (Optional [None, str]): 'None' to retrieve the latest version,
            or a version number as a string to get that version
        export (bool): True to get the raw json object from the server for
            export, False to get the native DataType

    Returns:
        (VersionedFlowSnapshot): If export=False, or the raw json otherwise

    WARNING: This call is impacted by
    https://issues.apache.org/jira/browse/NIFIREG-135
    Which means you sometimes can't trust the version count
    """
    assert isinstance(bucket_id, str)
    assert isinstance(flow_id, str)
    # Version needs to be coerced to str pass API client regex test
    # Even though the client specifies it as Int
    assert version is None or isinstance(version, (str, int))
    assert isinstance(export, bool)
    if version:
        with nipyapi.utils.rest_exceptions():
            out = nipyapi.registry.BucketFlowsApi().get_flow_version(
                bucket_id=bucket_id,
                flow_id=flow_id,
                version_number=str(version),  # This str coercion is intended
                _preload_content=not export,
            )
    else:
        with nipyapi.utils.rest_exceptions():
            out = nipyapi.registry.BucketFlowsApi().get_latest_flow_version(
                bucket_id, flow_id, _preload_content=not export
            )
    if export:
        return out.data
    return out


def export_flow_version(bucket_id, flow_id, version=None, file_path=None, mode="json"):
    """
    Convenience method to export the identified VersionedFlowSnapshot in the
    provided format mode.

    Args:
        bucket_id (str): the UUID of the bucket containing the Flow
        flow_id (str): the UUID of the Flow to be retrieved from the Bucket
        version (Optional [None, Str]): 'None' to retrieve the latest version,
            or a version number as a string to get that version
        file_path (str): The path and filename to write to. Defaults to None
            which returns the serialised obj
        mode (str): 'json' or 'yaml' to specific the encoding format

    Returns:
        (str) of the encoded Snapshot
    """
    assert isinstance(bucket_id, str)
    assert isinstance(flow_id, str)
    assert file_path is None or isinstance(file_path, str)
    assert version is None or isinstance(version, str)
    assert mode in ["yaml", "json"]
    raw_obj = get_flow_version(bucket_id, flow_id, version, export=True)
    export_obj = nipyapi.utils.dump(nipyapi.utils.load(raw_obj), mode)
    if file_path:
        return nipyapi.utils.fs_write(
            obj=export_obj,
            file_path=file_path,
        )
    return export_obj


def import_flow_version(bucket_id, encoded_flow=None, file_path=None, flow_name=None, flow_id=None):
    """
    Imports a given encoded_flow version into the bucket and flow described,
    may optionally be passed a file to read the encoded flow_contents from.

    Note that only one of encoded_flow or file_path, and only one of flow_name
    or flow_id should be specified.

    Args:
        bucket_id (str): UUID of the bucket to write the encoded_flow version
        encoded_flow (Optional [str]): The encoded flow to import; if not
            specified file_path is read from.
        file_path (Optional [str]): The file path to read the encoded flow from
            , if not specified encoded_flow is read from.
        flow_name (Optional [str]): If this is to be the first version in a new
            flow object, then this is the String name for the flow object.
        flow_id (Optional [str]): If this is a new version for an existing flow
            object, then this is the ID of that object.

    Returns:
        The new (VersionedFlowSnapshot)
    """
    # First, decode the flow snapshot contents
    dto = ("registry", "VersionedFlowSnapshot")
    if file_path is None and encoded_flow is not None:
        with nipyapi.utils.rest_exceptions():
            imported_flow = nipyapi.utils.load(encoded_flow, dto=dto)
    elif file_path is not None and encoded_flow is None:
        with nipyapi.utils.rest_exceptions():
            file_in = nipyapi.utils.fs_read(file_path=file_path)
            assert isinstance(file_in, (str, bytes))
            imported_flow = nipyapi.utils.load(obj=file_in, dto=dto)
            assert isinstance(imported_flow, nipyapi.registry.VersionedFlowSnapshot)
    else:
        raise ValueError(
            "Either file_path must point to a file for import, or"
            " flow_snapshot must be an importable object, but"
            "not both"
        )
    # Now handle determining which Versioned Item to write to
    if flow_id is None and flow_name is not None:
        # Case: New flow
        # create the Bucket item
        ver_flow = create_flow(bucket_id=bucket_id, flow_name=flow_name)
    elif flow_name is None and flow_id is not None:
        # Case: New version in existing flow
        ver_flow = get_flow_in_bucket(bucket_id=bucket_id, identifier=flow_id, identifier_type="id")
    else:
        raise ValueError(
            "Either flow_id must be the identifier of a flow to"
            " add this version to, or flow_name must be a unique "
            "name for a flow in this bucket, but not both"
        )
    # Now write the new version
    nipyapi.utils.validate_parameters_versioning_support(verify_nifi=False)
    return create_flow_version(
        flow=ver_flow,
        flow_snapshot=imported_flow,
    )


# pylint: disable=R0913, R0917
def deploy_flow_version(parent_id, location, bucket_id, flow_id, reg_client_id, version=None):
    """
    Deploys a versioned flow as a new process group inside the given parent
    process group. If version is not provided, the latest version will be
    deployed.

    Args:
        parent_id (str): The ID of the parent Process Group to create the
            new process group in.
        location (tuple[x, y]): the x,y coordinates to place the new Process
            Group under the parent
        bucket_id (str): ID of the bucket containing the versioned flow to
            deploy.
        reg_client_id (str): ID of the registry client connection to use.
        flow_id (str): ID of the versioned flow to deploy.
        version (Optional [int,str]): version to deploy, if not provided latest
            version will be deployed.

    Returns:
        (ProcessGroupEntity) of the newly deployed Process Group
    """
    # Default location to (0, 0) if not provided per Issue #342
    location = location or (0, 0)
    assert isinstance(location, tuple)
    # check reg client is valid
    target_reg_client = get_registry_client(reg_client_id, "id")
    # Being pedantic about checking this as API failure errors are terse
    # Using NiFi here to keep all calls within the same API client
    flow_versions = list_flow_versions(
        bucket_id=bucket_id, flow_id=flow_id, registry_id=reg_client_id, service="nifi"
    )
    if not flow_versions:
        raise ValueError(
            "Could not find Flows matching Bucket ID [{0}] and "
            "Flow ID [{1}] on Registry Client [{2}]".format(bucket_id, flow_id, reg_client_id)
        )
    if version is None:
        target_flow = flow_versions.versioned_flow_snapshot_metadata_set
    else:
        target_flow = [
            x
            for x in flow_versions.versioned_flow_snapshot_metadata_set
            if str(x.versioned_flow_snapshot_metadata.version) == str(version)
        ]
    if not target_flow:
        available_versions = [
            str(x.versioned_flow_snapshot_metadata.version)
            for x in flow_versions.versioned_flow_snapshot_metadata_set
        ]
        raise ValueError(
            "Could not find Version [{0}] for Flow [{1}] in Bucket [{2}] on "
            "Registry Client [{3}]. Available versions are: {4}".format(
                str(version), flow_id, bucket_id, reg_client_id, ", ".join(available_versions)
            )
        )
    target_flow = sorted(
        target_flow, key=lambda x: x.versioned_flow_snapshot_metadata.version, reverse=True
    )[0].versioned_flow_snapshot_metadata
    # Issue deploy statement
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_process_group(
            id=parent_id,
            body=nipyapi.nifi.ProcessGroupEntity(
                revision=nipyapi.nifi.RevisionDTO(version=0),
                component=nipyapi.nifi.ProcessGroupDTO(
                    position=nipyapi.nifi.PositionDTO(x=float(location[0]), y=float(location[1])),
                    version_control_information=VciDTO(
                        bucket_id=target_flow.bucket_identifier,
                        flow_id=target_flow.flow_identifier,
                        registry_id=target_reg_client.id,
                        version=target_flow.version,
                    ),
                ),
            ),
        )


def export_process_group_definition(process_group, file_path=None, mode="json"):
    """
    Export a process group as a flow definition (NiFi 2.x format).
    Does NOT require NiFi Registry - exports the current state of the process group.

    Args:
        process_group (ProcessGroupEntity): The process group to export
        file_path (str, optional): Path to write the export to. If None, returns
            the serialized string
        mode (str): Export format - 'json' or 'yaml'. Defaults to 'json'

    Returns:
        str: The serialized flow definition if file_path is None, otherwise
            the path written to

    Example:
        >>> pg = nipyapi.canvas.get_process_group('my-flow')
        >>> nipyapi.versioning.export_process_group_definition(
        ...     pg, file_path='my-flow.json', mode='json'
        ... )
        'my-flow.json'
    """
    assert isinstance(
        process_group, nipyapi.nifi.ProcessGroupEntity
    ), "process_group must be a ProcessGroupEntity"
    assert file_path is None or isinstance(file_path, str), "file_path must be None or a string"
    assert mode in ["json", "yaml"], "mode must be 'json' or 'yaml'"

    with nipyapi.utils.rest_exceptions():
        # Export returns JSON string directly from NiFi API
        flow_json_str = nipyapi.nifi.ProcessGroupsApi().export_process_group(process_group.id)

        # Convert to desired format if needed
        if mode == "yaml":
            # Parse JSON and re-serialize as YAML
            flow_obj = nipyapi.utils.load(flow_json_str)
            export_str = nipyapi.utils.dump(flow_obj, mode="yaml")
        else:
            export_str = flow_json_str

        # Write to file or return string
        if file_path:
            return nipyapi.utils.fs_write(obj=export_str, file_path=file_path)
        return export_str


def import_process_group_definition(parent_pg, flow_definition=None, file_path=None, position=None):
    """
    Import a flow definition as a new process group (NiFi 2.x format).
    Does NOT require NiFi Registry - imports from flow definition JSON/YAML.

    Args:
        parent_pg (ProcessGroupEntity): Parent process group to import into
        flow_definition (str, optional): Flow definition as JSON or YAML string.
            Either this or file_path must be provided, but not both
        file_path (str, optional): Path to flow definition file to import.
            Either this or flow_definition must be provided, but not both
        position (tuple, optional): (x, y) coordinates for the new process group.
            Defaults to (0, 0)

    Returns:
        ProcessGroupEntity: The newly imported process group

    Example:
        >>> root_pg = nipyapi.canvas.get_process_group(
        ...     nipyapi.canvas.get_root_pg_id(), 'id'
        ... )
        >>> imported_pg = nipyapi.versioning.import_process_group_definition(
        ...     parent_pg=root_pg,
        ...     file_path='my-flow.json',
        ...     position=(100, 100)
        ... )
    """
    assert isinstance(
        parent_pg, nipyapi.nifi.ProcessGroupEntity
    ), "parent_pg must be a ProcessGroupEntity"
    assert (flow_definition is None) != (
        file_path is None
    ), "Exactly one of flow_definition or file_path must be provided"
    assert position is None or isinstance(
        position, tuple
    ), "position must be None or a tuple of (x, y)"

    # Default position
    position = position or (0, 0)

    # Load flow definition
    if file_path:
        flow_json_str = nipyapi.utils.fs_read(file_path)
    else:
        flow_json_str = flow_definition

    # Parse flow to get group name (utils.load handles both JSON and YAML safely)
    flow_data = (
        nipyapi.utils.load(flow_json_str)
        if isinstance(flow_json_str, (str, bytes))
        else flow_json_str
    )
    group_name = flow_data.get("flowContents", {}).get("name", "imported-flow")

    # Use the upload endpoint which accepts file data
    # This is what the NiFi UI uses for importing flows
    with nipyapi.utils.rest_exceptions():
        # Convert the flow JSON string to bytes for file upload
        flow_bytes = (
            flow_json_str.encode("utf-8") if isinstance(flow_json_str, str) else flow_json_str
        )

        result = nipyapi.nifi.ProcessGroupsApi().upload_process_group(
            id=parent_pg.id,
            file=flow_bytes,
            group_name=group_name,
            position_x=str(float(position[0])),
            position_y=str(float(position[1])),
            client_id="nipyapi-import",
        )

        return result
