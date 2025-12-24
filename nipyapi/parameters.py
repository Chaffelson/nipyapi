"""
For Managing NiFi Parameter Contexts
"""

import logging

import nipyapi
from nipyapi.nifi import (
    AssetReferenceDTO,
    ParameterContextDTO,
    ParameterContextEntity,
    ParameterDTO,
    ParameterEntity,
)
from nipyapi.utils import enforce_min_ver, exception_handler

log = logging.getLogger(__name__)

__all__ = [
    "list_all_parameter_contexts",
    "create_parameter_context",
    "delete_parameter_context",
    "get_parameter_context",
    "update_parameter_context",
    "prepare_parameter",
    "delete_parameter_from_context",
    "upsert_parameter_to_context",
    "assign_context_to_process_group",
    "remove_context_from_process_group",
    # Hierarchy functions
    "get_parameter_context_hierarchy",
    "get_parameter_ownership_map",
    "update_parameter_in_context",
    # Asset functions
    "list_assets",
    "upload_asset",
    "delete_asset",
    "prepare_parameter_with_asset",
]


def list_all_parameter_contexts():
    """
    Lists all Parameter Contexts available on the Canvas

    Returns:
        list(ParameterContextEntity)
    """
    enforce_min_ver("1.10.0")
    handle = nipyapi.nifi.FlowApi()
    return handle.get_parameter_contexts().parameter_contexts


@exception_handler(404, None)
def get_parameter_context(identifier, identifier_type="name", greedy=True):
    """
    Gets one or more Parameter Contexts matching a given identifier

    Args:
        identifier (str): The Name or ID matching Parameter Context(s)
        identifier_type (str): 'name' or 'id'
        greedy (bool): False for exact match, True for string match

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches

    """
    enforce_min_ver("1.10.0")
    assert isinstance(identifier, str)
    assert identifier_type in ["name", "id"]
    if identifier_type == "id":
        handle = nipyapi.nifi.ParameterContextsApi()
        out = handle.get_parameter_context(identifier)
    else:
        obj = list_all_parameter_contexts()
        out = nipyapi.utils.filter_obj(obj, identifier, identifier_type, greedy=greedy)
    return out


def create_parameter_context(name, description=None, parameters=None, inherited_contexts=None):
    """
    Create a new Parameter Context with optional description and
        initial Parameters

    Args:
        name (str): The Name for the new Context
        description (str): An optional description
        parameters (list[ParameterEntity]): A list of prepared Parameters
        inherited_contexts (list[ParameterContextEntity]): A list of
            inherited Parameter Contexts

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The New Parameter Context

    """
    enforce_min_ver("1.10.0")
    assert isinstance(name, str)
    assert description is None or isinstance(description, str)
    handle = nipyapi.nifi.ParameterContextsApi()
    inherited = inherited_contexts if inherited_contexts else []
    out = handle.create_parameter_context(
        body=ParameterContextEntity(
            revision=nipyapi.nifi.RevisionDTO(version=0),
            component=ParameterContextDTO(
                name=name,
                description=description,
                parameters=parameters if parameters else [],
                # list() per NiFi Jira 7995
                inherited_parameter_contexts=inherited,
                # requires empty list per NiFi Jira 9470
            ),
        )
    )
    return out


def update_parameter_context(context):
    """
    Update an already existing Parameter Context

    Args:
        context (ParameterContextEntity): Parameter Context updated
          to be applied
        refresh (bool): Whether to refresh the object before Updating

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The updated Parameter Context
    """
    enforce_min_ver("1.10.0")

    def _update_complete(context_id, request_id):
        return (
            nipyapi.nifi.ParameterContextsApi()
            .get_parameter_context_update(context_id, request_id)
            .request.complete
        )

    if not isinstance(context, ParameterContextEntity):
        raise ValueError(
            "Supplied Parameter Context update should "
            "be an instance of nipyapi.nifi.ParameterContextDTO"
        )
    handle = nipyapi.nifi.ParameterContextsApi()
    target = get_parameter_context(context.id, identifier_type="id")
    update_request = handle.submit_parameter_context_update(
        context_id=target.id,
        body=ParameterContextEntity(
            id=target.id, revision=target.revision, component=context.component
        ),
    )
    nipyapi.utils.wait_to_complete(
        _update_complete,
        target.id,
        update_request.request.request_id,
        nipyapi_delay=1,
        nipyapi_max_wait=10,
    )
    _ = handle.delete_update_request(
        context_id=target.id, request_id=update_request.request.request_id
    )
    return get_parameter_context(context.id, identifier_type="id")


def delete_parameter_context(context, refresh=True):
    """
    Removes a Parameter Context

    Args:
        context (ParameterContextEntity): Parameter Context to be deleted
        refresh (bool): Whether to refresh the Context before Deletion

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The removed Parameter Context
    """
    enforce_min_ver("1.10.0")
    assert isinstance(context, nipyapi.nifi.ParameterContextEntity)
    handle = nipyapi.nifi.ParameterContextsApi()
    if refresh:
        context = handle.get_parameter_context(context.id)
    return handle.delete_parameter_context(id=context.id, version=context.revision.version)


def prepare_parameter(name, value, description=None, sensitive=False):
    """
    Parses basic inputs into a Parameter object ready for submission

    Args:
        name (str): The Name for the Parameter
        value (str, int, float): The Value for the Parameter
        description (str): Optional Description for the Parameter
        sensitive (bool): Whether to mark the Parameter Value as sensitive

    Returns:
        :class:`~nipyapi.nifi.models.ParameterEntity`: The ParameterEntity ready for use
    """
    enforce_min_ver("1.10.0")
    assert all(x is None or isinstance(x, str) for x in [name, description])
    out = ParameterEntity(
        parameter=ParameterDTO(name=name, value=value, description=description, sensitive=sensitive)
    )
    return out


def delete_parameter_from_context(context, parameter_name):
    """
    Delete a specific Parameter from a Parameter Context
    Args:
        context (ParameterContextEntity): The Parameter Context to Update
        parameter_name (str): The Parameter to delete

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The updated Parameter Context
    """
    enforce_min_ver("1.10.0")
    context.component.parameters = [ParameterEntity(parameter=ParameterDTO(name=parameter_name))]
    return update_parameter_context(context=context)


def upsert_parameter_to_context(context, parameter):
    """
    Insert or Update Parameter within a Parameter Context

    Args:
        context (ParameterContextEntity): The Parameter Context to Modify
        parameter(ParameterEntity): The ParameterEntity to insert or update

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The updated Parameter Context
    """
    enforce_min_ver("1.10.0")
    context.component.parameters = [parameter]
    return update_parameter_context(context=context)


def assign_context_to_process_group(pg, context_id, cascade=False):
    """
    Assigns a given Parameter Context to a specific Process Group
    Optionally cascades down to direct children Process Groups

    Args:
        pg (ProcessGroupEntity): The Process Group to target
        context_id (str): The ID of the Parameter Context
        cascade (bool): Cascade Parameter Context down to child Process Groups?

    Returns:
        :class:`~nipyapi.nifi.models.ProcessGroupEntity`: The updated Process Group
    """
    assert isinstance(context_id, str)
    if cascade:
        # Update the specified Process Group & all children
        child_pgs = nipyapi.canvas.list_all_process_groups(pg_id=pg.id)
        for child_pg in child_pgs:
            nipyapi.canvas.update_process_group(
                pg=child_pg, update={"parameter_context": {"id": context_id}}
            )
    return nipyapi.canvas.update_process_group(
        pg=pg, update={"parameter_context": {"id": context_id}}
    )


def remove_context_from_process_group(pg):
    """
    Clears any Parameter Context from the given Process Group

    Args:
        pg (ProcessGroupEntity): The Process Group to target

    Returns:
        :class:`~nipyapi.nifi.models.ProcessGroupEntity`: The updated Process Group
    """
    return nipyapi.canvas.update_process_group(pg=pg, update={"parameter_context": {"id": None}})


def get_parameter_context_hierarchy(context_id, include_bindings=False, include_parameters=True):
    """
    Get the full parameter context inheritance hierarchy.

    Traverses from the given context through all inherited contexts,
    returning a nested structure showing the full hierarchy.

    Args:
        context_id (str): The ID of the root parameter context
        include_bindings (bool): If True, include bound_process_groups for each
            context showing which process groups are using it. Useful for
            determining cleanup safety. Default: False
        include_parameters (bool): If True, include parameter details for each
            context. Set to False for a lightweight structure-only view.
            Default: True (backwards compatible)

    Returns:
        dict: Hierarchy with keys:
            - id: Context ID
            - name: Context name
            - parameters: List of parameter info dicts (if include_parameters=True)
                Each parameter dict contains: name, description, sensitive, value,
                has_asset, asset_name
            - inherited: List of child hierarchy dicts (recursive)
            - bound_process_groups: List of {id, name} dicts (if include_bindings=True)

    Example:
        >>> # Get full hierarchy with parameters
        >>> hierarchy = get_parameter_context_hierarchy(context_id)
        >>> print(hierarchy['name'])  # "PostgreSQL Ingestion Parameters"
        >>> print(hierarchy['inherited'][0]['name'])  # "PostgreSQL Destination Parameters"

        >>> # Get structure with bindings for cleanup analysis
        >>> hierarchy = get_parameter_context_hierarchy(
        ...     context_id, include_bindings=True, include_parameters=False
        ... )
        >>> for ctx in [hierarchy] + hierarchy['inherited']:
        ...     bindings = len(ctx.get('bound_process_groups', []))
        ...     print(f"{ctx['name']}: {bindings} bindings")
    """
    enforce_min_ver("1.10.0")

    ctx = get_parameter_context(context_id, identifier_type="id")
    if ctx is None:
        raise ValueError(f"Parameter context not found: {context_id}")

    result = {
        "id": ctx.id,
        "name": ctx.component.name,
        "inherited": [],
    }

    # Include parameters if requested (default: True for backwards compatibility)
    if include_parameters:
        result["parameters"] = []
        for p in ctx.component.parameters or []:
            param = p.parameter
            assets = param.referenced_assets or []
            result["parameters"].append(
                {
                    "name": param.name,
                    "description": param.description,
                    "sensitive": param.sensitive or False,
                    "value": None if param.sensitive else param.value,
                    "has_asset": bool(assets),
                    "asset_name": assets[0].name if assets else None,
                }
            )

    # Include bound process groups if requested
    if include_bindings:
        result["bound_process_groups"] = [
            {"id": pg.id, "name": pg.component.name}
            for pg in (ctx.component.bound_process_groups or [])
        ]

    # Recurse into inherited contexts with same flags
    for ipc in ctx.component.inherited_parameter_contexts or []:
        child_hierarchy = get_parameter_context_hierarchy(
            ipc.id,
            include_bindings=include_bindings,
            include_parameters=include_parameters,
        )
        result["inherited"].append(child_hierarchy)

    return result


def get_parameter_ownership_map(context_id):
    """
    Build a map of parameter names to their owning context.

    Traverses the inheritance hierarchy and returns information about
    where each parameter is defined (its "owner"), including metadata
    needed for safe updates.

    Args:
        context_id (str): The ID of the root parameter context

    Returns:
        dict: Map of parameter name to ownership info:
            {
                "param_name": {
                    "context_id": "...",
                    "context_name": "...",
                    "sensitive": bool,
                    "has_asset": bool,
                    "asset_name": str or None,
                    "current_value": str or None (None if sensitive)
                }
            }

    Example:
        >>> ownership = get_parameter_ownership_map(context_id)
        >>> print(ownership["PostgreSQL Username"])
        {'context_id': '...', 'context_name': 'PostgreSQL Source Parameters', ...}
    """
    enforce_min_ver("1.10.0")

    hierarchy = get_parameter_context_hierarchy(context_id)
    ownership_map = {}

    def _traverse(h):
        for param in h["parameters"]:
            ownership_map[param["name"]] = {
                "context_id": h["id"],
                "context_name": h["name"],
                "sensitive": param["sensitive"],
                "has_asset": param["has_asset"],
                "asset_name": param["asset_name"],
                "current_value": param["value"],
            }
        for child in h["inherited"]:
            _traverse(child)

    _traverse(hierarchy)
    return ownership_map


def update_parameter_in_context(context_id, param_name, value, create_if_missing=False):
    """
    Update a parameter in a specific context, with safety checks.

    By default, this function will only update a parameter that already
    exists in the specified context. This prevents accidental creation
    of shadowing parameters in inherited hierarchies.

    Args:
        context_id (str): The ID of the parameter context to update
        param_name (str): Name of the parameter to update
        value (str): New value for the parameter
        create_if_missing (bool): If True, create the parameter if it doesn't
            exist in this context. Default False (safe mode).

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: Updated context

    Raises:
        ValueError: If parameter not found and create_if_missing=False
        ValueError: If context not found

    Example:
        >>> # Safe update - only if param exists in this context
        >>> update_parameter_in_context(ctx_id, "Username", "newuser")

        >>> # Create if missing (use with caution - may shadow inherited params)
        >>> update_parameter_in_context(ctx_id, "NewParam", "value", create_if_missing=True)
    """
    enforce_min_ver("1.10.0")

    ctx = get_parameter_context(context_id, identifier_type="id")
    if ctx is None:
        raise ValueError(f"Parameter context not found: {context_id}")

    # Find existing parameter at THIS level
    existing_param = None
    for p in ctx.component.parameters or []:
        if p.parameter.name == param_name:
            existing_param = p
            break

    if existing_param is None and not create_if_missing:
        raise ValueError(
            f"Parameter '{param_name}' not found in context '{ctx.component.name}'. "
            f"Use create_if_missing=True to create it, or check the ownership map "
            f"to find the correct context."
        )

    # Prepare the parameter update
    sensitive = existing_param.parameter.sensitive if existing_param else False
    description = existing_param.parameter.description if existing_param else None

    new_param = prepare_parameter(
        name=param_name, value=value, description=description, sensitive=sensitive
    )

    # Update via upsert
    return upsert_parameter_to_context(ctx, new_param)


# =============================================================================
# Asset Management Functions
# =============================================================================


def list_assets(context_id):
    """
    List all assets in a parameter context.

    Args:
        context_id (str): The parameter context ID

    Returns:
        list[dict]: List of asset info dicts with keys: id, name, digest, missing_content

    Example:
        >>> assets = list_assets(context_id)
        >>> for asset in assets:
        ...     print(f"{asset['name']} ({asset['id']})")
    """
    enforce_min_ver("1.10.0")

    handle = nipyapi.nifi.ParameterContextsApi()
    response = handle.get_assets(context_id)

    return [
        {
            "id": asset_entity.asset.id,
            "name": asset_entity.asset.name,
            "digest": asset_entity.asset.digest,
            "missing_content": asset_entity.asset.missing_content,
        }
        for asset_entity in response.assets
    ]


def upload_asset(context_id, file_path=None, file_bytes=None, filename=None):
    """
    Upload an asset to a parameter context.

    Args:
        context_id (str): The parameter context ID
        file_path (str): Path to local file to upload (alternative to file_bytes)
        file_bytes (bytes): Raw bytes to upload (alternative to file_path)
        filename (str): Name for the asset (defaults to basename of file_path)

    Returns:
        dict: Asset info with keys: id, name, digest

    Raises:
        ValueError: If neither file_path nor file_bytes provided
        ValueError: If filename not provided when using file_bytes

    Example:
        >>> # Upload from file path
        >>> asset = upload_asset(context_id, file_path="/path/to/driver.jar")

        >>> # Upload from bytes with explicit filename
        >>> asset = upload_asset(context_id, file_bytes=data, filename="driver.jar")
    """
    enforce_min_ver("1.10.0")

    import os  # pylint: disable=import-outside-toplevel

    if file_path is None and file_bytes is None:
        raise ValueError("Either file_path or file_bytes must be provided")

    if file_path is not None:
        if filename is None:
            filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_bytes = f.read()
    elif filename is None:
        raise ValueError("filename is required when using file_bytes")

    handle = nipyapi.nifi.ParameterContextsApi()
    result = handle.create_asset(body=file_bytes, context_id=context_id, filename=filename)

    log.info("Uploaded asset '%s' to context %s", filename, context_id)

    return {
        "id": result.asset.id,
        "name": result.asset.name,
        "digest": result.asset.digest,
    }


def delete_asset(context_id, asset_id):
    """
    Delete an asset from a parameter context.

    Args:
        context_id (str): The parameter context ID
        asset_id (str): The asset ID to delete

    Returns:
        dict: Deleted asset info with keys: id, name

    Raises:
        ApiException: If asset not found or delete fails

    Example:
        >>> result = delete_asset(context_id, asset_id)
        >>> print(f"Deleted: {result['name']}")
    """
    enforce_min_ver("1.10.0")

    handle = nipyapi.nifi.ParameterContextsApi()
    result = handle.delete_asset(context_id=context_id, asset_id=asset_id)

    log.info("Deleted asset '%s' from context %s", result.asset.name, context_id)

    return {
        "id": result.asset.id,
        "name": result.asset.name,
    }


def prepare_parameter_with_asset(name, asset_id, asset_name, description=None):
    """
    Prepare a parameter that references an asset.

    Use this to update a parameter to point to an uploaded asset.

    Args:
        name (str): Parameter name
        asset_id (str): ID of the asset to reference
        asset_name (str): Name of the asset
        description (str): Optional parameter description

    Returns:
        :class:`~nipyapi.nifi.models.ParameterEntity`: ParameterEntity ready for
            use with update_parameter_context or upsert_parameter_to_context

    Example:
        >>> # Upload asset first
        >>> asset = upload_asset(context_id, file_path="/path/to/driver.jar")
        >>> # Then prepare parameter to reference it
        >>> param = prepare_parameter_with_asset(
        ...     name="JDBC Driver",
        ...     asset_id=asset['id'],
        ...     asset_name=asset['name']
        ... )
        >>> # Update the parameter context
        >>> upsert_parameter_to_context(context, param)
    """
    enforce_min_ver("1.10.0")

    asset_ref = AssetReferenceDTO(id=asset_id, name=asset_name)

    return ParameterEntity(
        parameter=ParameterDTO(name=name, description=description, referenced_assets=[asset_ref])
    )
