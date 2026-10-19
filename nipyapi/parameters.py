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
from nipyapi.utils import exception_handler

log = logging.getLogger(__name__)

# Sentinel object to distinguish "value not provided" from "value is None"
_NOT_PROVIDED = object()

__all__ = [
    "list_all_parameter_providers",
    "get_parameter_provider",
    "list_all_parameter_provider_types",
    "get_parameter_provider_type",
    "update_parameter_provider",
    "fetch_parameter_provider",
    "apply_parameter_provider",
    "fetch_and_apply_parameter_provider",
    "set_inherited_parameter_contexts",
    "get_process_group_parameter_context",
    "connect_parameter_provider_group",
    "list_all_parameter_contexts",
    "list_orphaned_contexts",
    "create_parameter_context",
    "delete_parameter_context",
    "get_parameter_context",
    "update_parameter_context",
    "rename_parameter_context",
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


def list_all_parameter_providers():
    """List all parameter providers.

    Returns:
        list[ParameterProviderEntity]: Configured providers.
    """
    return nipyapi.nifi.FlowApi().get_parameter_providers().parameter_providers


@exception_handler(404, None)
def get_parameter_provider(identifier, identifier_type="name", greedy=True):
    """Find parameter providers by name, ID, or provider type.

    Args:
        identifier (str): Name, ID, or provider class name to match.
        identifier_type (str): One of "name", "id", or "type".
        greedy (bool): Use substring matching instead of exact matching.

    Returns:
        ParameterProviderEntity or list or None: Single match, multiple matches,
            or None when no provider matches.
    """
    assert isinstance(identifier, str)
    assert identifier_type in ["name", "id", "type"]
    if identifier_type == "id":
        return nipyapi.nifi.ParameterProvidersApi().get_parameter_provider(identifier)
    return nipyapi.utils.filter_obj(
        list_all_parameter_providers(), identifier, identifier_type, greedy=greedy
    )


def list_all_parameter_provider_types():
    """List available parameter provider types.

    Returns:
        list[DocumentedTypeDTO]: Installed provider types.
    """
    return nipyapi.nifi.FlowApi().get_parameter_provider_types().parameter_provider_types


def get_parameter_provider_type(identifier, identifier_type="name", greedy=True):
    """Find installed parameter provider types.

    Args:
        identifier (str): Class name, bundle, or tag to match.
        identifier_type (str): Registered DocumentedTypeDTO filter field.
        greedy (bool): Use substring matching instead of exact matching.

    Returns:
        DocumentedTypeDTO or list or None: Matching provider type(s).
    """
    with nipyapi.utils.rest_exceptions():
        types = list_all_parameter_provider_types()
    if types:
        return nipyapi.utils.filter_obj(types, identifier, identifier_type, greedy=greedy)
    return types


def update_parameter_provider(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    provider, properties, greedy=True, identifier_type="auto", allow_dynamic=False, refresh=True
):
    """Update provider properties, optionally refreshing the provider first.

    Args:
        provider (ParameterProviderEntity or str): Provider entity, ID, or name.
        properties (dict): Property names and values; None clears a property.
        greedy (bool): Allow partial name matching.
        identifier_type (str): "auto", "id", or "name".
        allow_dynamic (bool): Allow keys absent from static property descriptors.
        refresh (bool): Refresh the provider before updating. Defaults to True.

    Returns:
        ParameterProviderEntity: Updated provider, with sensitive properties masked by NiFi.

    Raises:
        ValueError: If lookup is ambiguous or a property name is unknown.
        TypeError: If properties is not a dictionary.
    """
    if not isinstance(properties, dict):
        raise TypeError("properties must be a dictionary")
    live = nipyapi.utils.resolve_entity(
        provider,
        get_parameter_provider,
        nipyapi.nifi.ParameterProviderEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
    if refresh:
        live = get_parameter_provider(live.id, identifier_type="id")
    # Reuse the descriptor validation shared by processor and controller configuration.
    component = nipyapi.canvas._prepare_component_config(  # pylint: disable=protected-access
        live.component.descriptors or {},
        live.component.type,
        nipyapi.nifi.ParameterProviderDTO,
        properties,
        allow_dynamic,
    )
    component.id = live.id
    return nipyapi.nifi.ParameterProvidersApi().update_parameter_provider(
        id=live.id,
        body=nipyapi.nifi.ParameterProviderEntity(
            id=live.id,
            revision=live.revision,
            component=component,
        ),
    )


def fetch_parameter_provider(provider, greedy=True, identifier_type="auto", refresh=True):
    """Fetch and stage provider parameters without applying them to contexts.

    This is a write operation. The synchronous POST response contains staged groups.

    Args:
        provider (ParameterProviderEntity or str): Provider entity, ID, or name.
        greedy (bool): Allow partial name matching.
        identifier_type (str): "auto", "id", or "name".
        refresh (bool): Refresh the provider before the operation. Defaults to True.

    Returns:
        ParameterProviderEntity: Provider with staged parameter groups.

    Raises:
        ValueError: If lookup fails.
        ApiException: If fetch fails; the original NiFi response is preserved.
    """
    live = nipyapi.utils.resolve_entity(
        provider,
        get_parameter_provider,
        nipyapi.nifi.ParameterProviderEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
    if refresh:
        live = get_parameter_provider(live.id, identifier_type="id")
    try:
        return nipyapi.nifi.ParameterProvidersApi().fetch_parameters(
            id=live.id,
            body=nipyapi.nifi.ParameterProviderParameterFetchEntity(
                id=live.id,
                revision=live.revision,
            ),
        )
    except nipyapi.nifi.rest.ApiException as exc:
        if exc.status == 500:
            log.warning(
                "Provider fetch failed (HTTP 500). Check provider configuration and source "
                "access; consider narrowing its scope before retrying."
            )
        raise


def _select_parameter_groups(provider, group_names):
    groups = provider.component.parameter_group_configurations or []
    if group_names is None:
        return groups
    if isinstance(group_names, str):
        group_names = [group_names]
    if not isinstance(group_names, (list, tuple)) or not all(
        isinstance(name, str) for name in group_names
    ):
        raise TypeError("group_names must be a name or a list of names")
    missing = set(group_names) - {group.group_name for group in groups}
    if missing:
        raise ValueError(f"Unknown parameter groups: {sorted(missing)}")
    return [group for group in groups if group.group_name in group_names]


# pylint: disable-next=too-many-arguments,too-many-positional-arguments,too-many-locals
def apply_parameter_provider(
    provider,
    group_names=None,
    sensitivity="SENSITIVE",
    sensitivities=None,
    synchronized=None,
    fetch_result=None,
    greedy=True,
    identifier_type="auto",
    refresh=True,
):
    """Apply selected staged groups and wait for the completed request.

    Args:
        provider (ParameterProviderEntity or str): Provider entity, ID, or name.
        group_names (list[str] or str): Groups to apply; None selects all staged groups.
        sensitivity (str): Default "SENSITIVE" or "NON_SENSITIVE" for unset choices.
        sensitivities (dict): Parameter name to "SENSITIVE" or "NON_SENSITIVE". Each name
            applies in every selected group and must match a staged parameter; other
            parameters retain their staged choices.
        synchronized (bool): Override whether contexts stay synchronized with their provider
            group. None (default) keeps the staged value, or True where unset; NiFi skips
            unsynchronized groups on apply, and a warning is logged when none remain.
        fetch_result (ParameterProviderEntity): Optional staged response from fetch.
        greedy (bool): Allow partial name matching.
        identifier_type (str): "auto", "id", or "name".
        refresh (bool): Refresh the provider before the operation. Defaults to True.

    Returns:
        ParameterProviderApplyParametersRequestDTO: Completed request including affected
            components. Sensitive parameter values remain masked by NiFi.

    Raises:
        ValueError: Invalid group, sensitivity, or parameter name, mismatched fetch,
            or failed request.
    """
    if sensitivity not in {"SENSITIVE", "NON_SENSITIVE"}:
        raise ValueError("sensitivity must be SENSITIVE or NON_SENSITIVE")
    if sensitivities is not None and not isinstance(sensitivities, dict):
        raise TypeError("sensitivities must be a dictionary")
    overrides = sensitivities or {}
    if any(value not in {"SENSITIVE", "NON_SENSITIVE"} for value in overrides.values()):
        raise ValueError("sensitivities must contain SENSITIVE or NON_SENSITIVE values")
    if synchronized is not None and not isinstance(synchronized, bool):
        raise TypeError("synchronized must be a boolean or None")
    live = nipyapi.utils.resolve_entity(
        provider,
        get_parameter_provider,
        nipyapi.nifi.ParameterProviderEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
    if refresh:
        live = get_parameter_provider(live.id, identifier_type="id")
    if fetch_result is not None and (
        not isinstance(fetch_result, nipyapi.nifi.ParameterProviderEntity)
        or fetch_result.id != live.id
    ):
        raise ValueError("fetch_result must belong to the selected provider")
    groups = _select_parameter_groups(
        fetch_result if fetch_result is not None else live, group_names
    )
    unknown = set(overrides).difference(*[group.parameter_sensitivities or {} for group in groups])
    if unknown:
        raise ValueError(f"Unknown parameters in sensitivities: {sorted(unknown)}")
    configurations = [
        nipyapi.nifi.ParameterGroupConfigurationEntity(
            group_name=group.group_name,
            parameter_context_name=group.parameter_context_name or group.group_name,
            parameter_sensitivities={
                name: overrides.get(name, value or sensitivity)
                for name, value in (group.parameter_sensitivities or {}).items()
            },
            synchronized=(
                synchronized if synchronized is not None else group.synchronized is not False
            ),
        )
        for group in groups
    ]
    handle = nipyapi.nifi.ParameterProvidersApi()
    submitted = handle.submit_apply_parameters(
        provider_id=live.id,
        body=nipyapi.nifi.ParameterProviderParameterApplicationEntity(
            id=live.id,
            revision=live.revision,
            parameter_group_configurations=configurations,
        ),
    )
    request_id = submitted.request.request_id
    result = nipyapi.utils.wait_for_request(
        lambda: handle.get_parameter_provider_apply_parameters_request(live.id, request_id),
        lambda: handle.delete_apply_parameters_request(live.id, request_id),
        nipyapi_delay=1,
        nipyapi_max_wait=nipyapi.config.long_max_wait,
    )
    if not any(configuration.synchronized for configuration in configurations):
        log.warning(
            "Parameter provider %s apply completed with nothing to apply: "
            "no synchronized groups were selected",
            live.id,
        )
    return result


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def fetch_and_apply_parameter_provider(
    provider,
    group_names=None,
    sensitivity="SENSITIVE",
    sensitivities=None,
    synchronized=None,
    require_parameters=True,
    greedy=True,
    identifier_type="auto",
    refresh=True,
):
    """Fetch provider parameters and apply the selected groups.

    Args:
        provider (ParameterProviderEntity or str): Provider entity, ID, or name.
        group_names (list[str] or str): Groups to apply; None selects all groups.
        sensitivity (str): Default sensitivity for previously unset choices.
        sensitivities (dict): Parameter name overrides; see apply_parameter_provider.
        synchronized (bool): Synchronized override; see apply_parameter_provider.
        require_parameters (bool): Reject missing or empty selected groups.
        greedy (bool): Allow partial name matching.
        identifier_type (str): "auto", "id", or "name".
        refresh (bool): Refresh the provider before the operation. Defaults to True.

    Returns:
        ParameterProviderApplyParametersRequestDTO: Completed apply request.

    Raises:
        ValueError: Missing/empty selected groups, or the errors raised by
            apply_parameter_provider.
    """
    fetched = fetch_parameter_provider(
        provider, greedy=greedy, identifier_type=identifier_type, refresh=refresh
    )
    groups = _select_parameter_groups(fetched, group_names)
    if require_parameters and (
        not groups or any(not group.parameter_sensitivities for group in groups)
    ):
        raise ValueError("Selected groups contain no parameters or include an empty group")
    return apply_parameter_provider(
        fetched,
        group_names=group_names,
        sensitivity=sensitivity,
        sensitivities=sensitivities,
        synchronized=synchronized,
        fetch_result=fetched,
        refresh=refresh,
    )


def list_all_parameter_contexts():
    """
    Lists all Parameter Contexts available on the Canvas

    Returns:
        list(ParameterContextEntity)
    """
    handle = nipyapi.nifi.FlowApi()
    return handle.get_parameter_contexts().parameter_contexts


def list_orphaned_contexts():
    """
    Lists Parameter Contexts that are not bound to any Process Groups.

    An orphaned context is one that exists but has no process groups
    referencing it. These may be safe to delete after cleanup operations.

    Returns:
        list(ParameterContextEntity): Contexts with no bound process groups
    """
    all_contexts = list_all_parameter_contexts()
    return [ctx for ctx in all_contexts if not ctx.component.bound_process_groups]


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
    Update an already existing Parameter Context.

    Wait for completion and delete the completed request. Request-level failures
    raise ValueError. Timeout or polling interruption does not cancel the update;
    see utils.wait_for_request for cleanup and error precedence.

    Args:
        context (ParameterContextEntity): Parameter Context updated
          to be applied

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The updated Parameter Context
    """

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
    # Use long timeout: parameter updates involve stopping processors, disabling
    # controller services, applying changes, re-enabling services, and restarting
    # processors. This can take significant time especially with many parameters
    # or slow-to-connect services.
    request_id = update_request.request.request_id
    nipyapi.utils.wait_for_request(
        lambda: handle.get_parameter_context_update(target.id, request_id),
        lambda: handle.delete_update_request(context_id=target.id, request_id=request_id),
        nipyapi_delay=1,
        nipyapi_max_wait=nipyapi.config.long_max_wait,
    )
    return get_parameter_context(context.id, identifier_type="id")


def _submit_parameter_context_update(context, component):
    handle = nipyapi.nifi.ParameterContextsApi()
    live = handle.get_parameter_context(context.id)
    submitted = handle.submit_parameter_context_update(
        context_id=live.id,
        body=ParameterContextEntity(id=live.id, revision=live.revision, component=component),
    )
    request_id = submitted.request.request_id
    return nipyapi.utils.wait_for_request(
        lambda: handle.get_parameter_context_update(live.id, request_id),
        lambda: handle.delete_update_request(live.id, request_id),
        nipyapi_delay=1,
        nipyapi_max_wait=nipyapi.config.long_max_wait,
    )


def _inherited_context_references(context, inherited, mode, greedy, identifier_type):
    if mode not in ("prepend", "replace"):
        raise ValueError("mode must be prepend or replace")
    if not isinstance(inherited, (list, tuple)):
        raise TypeError("inherited must be a list of contexts, IDs, or names")
    resolved = [
        nipyapi.utils.resolve_entity(
            item,
            get_parameter_context,
            ParameterContextEntity,
            strict=True,
            greedy=greedy,
            identifier_type=identifier_type,
        )
        for item in inherited
    ]
    if mode == "prepend":
        resolved += context.component.inherited_parameter_contexts or []
    references = []
    seen = set()
    for item in resolved:
        if item.id == context.id:
            raise ValueError("A parameter context cannot inherit itself")
        if item.id not in seen:
            seen.add(item.id)
            references.append(
                ParameterContextEntity(
                    id=item.id,
                    component=ParameterContextDTO(
                        id=item.id, name=item.component.name if item.component else None
                    ),
                )
            )
    return references


def set_inherited_parameter_contexts(
    context, inherited, mode="prepend", greedy=True, identifier_type="auto"
):
    """Prepend or replace inherited contexts without changing local parameters.

    The target is always re-read, so the update is built from its current
    inheritance rather than from a supplied entity.

    Args:
        context (ParameterContextEntity or str): Target context, ID, or name.
        inherited (list): Context entities, IDs, or names in precedence order.
        mode (str): "prepend" puts the listed contexts first, in the given order, including
            any already inherited, and keeps the others after them; "replace" removes
            the others.
        greedy (bool): Allow partial name matching.
        identifier_type (str): "auto", "id", or "name" for string identifiers.

    Returns:
        ParameterContextUpdateRequestDTO: Completed update and affected components.

    Raises:
        ValueError: Invalid mode, missing/ambiguous context, or failed update.
        ApiException: NiFi rejects the update, including inheritance conflicts (409).
    """
    live = nipyapi.utils.resolve_entity(
        context,
        get_parameter_context,
        ParameterContextEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
    live = get_parameter_context(live.id, identifier_type="id")
    references = _inherited_context_references(live, inherited, mode, greedy, identifier_type)
    return _submit_parameter_context_update(
        live,
        ParameterContextDTO(
            id=live.id,
            name=live.component.name,
            parameters=[],
            inherited_parameter_contexts=references,
        ),
    )


def get_process_group_parameter_context(process_group, greedy=True, identifier_type="auto"):
    """Get the context currently bound to a process group.

    The process group is always re-read, so a supplied entity's binding is not trusted.

    Args:
        process_group (ProcessGroupEntity or str): Process group entity, ID, or name.
        greedy (bool): Allow partial name matching.
        identifier_type (str): "auto", "id", or "name".

    Returns:
        ParameterContextEntity or None: Bound context, or None for an unbound group.

    Raises:
        ValueError: The process group cannot be uniquely resolved.
    """
    group = nipyapi.utils.resolve_entity(
        process_group,
        nipyapi.canvas.get_process_group,
        nipyapi.nifi.ProcessGroupEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
    group = nipyapi.canvas.get_process_group(group.id, "id")
    binding = group.component.parameter_context
    return get_parameter_context(binding.id, "id") if binding and binding.id else None


def _resolve_context_target(target, greedy, identifier_type):
    if isinstance(target, str):
        # Query both namespaces rather than silently preferring a colliding name.
        candidates = []
        for getter, entity_type in (
            (get_parameter_context, ParameterContextEntity),
            (nipyapi.canvas.get_process_group, nipyapi.nifi.ProcessGroupEntity),
        ):
            result = nipyapi.utils.resolve_entity(
                target,
                getter,
                entity_type,
                strict=False,
                greedy=greedy,
                identifier_type=identifier_type,
            )
            if result is not None:
                candidates.extend(result if isinstance(result, list) else [result])
        if len(candidates) != 1:
            raise ValueError("Target must identify exactly one context or process group")
        target = candidates[0]
    if isinstance(target, nipyapi.nifi.ProcessGroupEntity):
        target = get_process_group_parameter_context(target)
        if target is None:
            raise ValueError("Process group has no bound parameter context")
    return nipyapi.utils.resolve_entity(
        target,
        get_parameter_context,
        ParameterContextEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )


def _connect_inherited_references(live, source, mappings):
    """Prepend a new source; keep an inherited one in place unless it is shadowed."""
    current = live.component.inherited_parameter_contexts or []
    position = next((i for i, item in enumerate(current) if item.id == source.id), None)
    if position is None:
        return _inherited_context_references(live, [source], "prepend", False, "id")
    # The first inherited context defining a name wins, and aliases resolve against it.
    names = set(mappings.values())
    for item in current[:position]:
        higher = get_parameter_context(item.id, identifier_type="id")
        if higher is None or higher.component is None:
            raise ValueError(
                f"Cannot read higher-precedence inherited context {item.id} to check shadowing"
            )
        shadowed = sorted(
            names & {entry.parameter.name for entry in higher.component.parameters or []}
        )
        if shadowed:
            raise ValueError(
                f"Inherited context '{higher.component.name}' takes precedence and shadows "
                f"{shadowed}; reorder with set_inherited_parameter_contexts(mode='replace')"
            )
    return _inherited_context_references(live, [], "prepend", False, "id")


def connect_parameter_provider_group(
    target, group_name, mappings, identifier_type="auto", greedy=True
):
    """Inherit a provider-created context and set local sensitive parameter aliases.

    The target, and any process-group binding, is always re-read before the update.
    A context not yet inherited is placed first, because the first inherited context
    defining a name wins and aliases resolve against it. An already inherited context
    keeps its position unless a higher one defines a mapped source name; then this
    raises, so the order can be set with set_inherited_parameter_contexts.

    Args:
        target (ParameterContextEntity or ProcessGroupEntity or str): Target context
            or process group. A group must have a bound context. Ambiguous names fail.
        group_name (str): Exact name of the provider-created parameter context.
        mappings (dict): Local parameter name to source parameter name.
        identifier_type (str): "auto", "id", or "name" for target lookup.
        greedy (bool): Allow partial target name matching.

    Returns:
        ParameterContextUpdateRequestDTO: Completed update and affected components.

    Raises:
        ValueError: Missing source parameters, ambiguous/unbound target, invalid aliases,
            a mapped source name shadowed by a higher-precedence inherited context,
            a non-sensitive source parameter (NiFi would leave the sensitive alias
            unresolved), or a local non-sensitive parameter that cannot be changed
            to sensitive.
    """
    if not isinstance(mappings, dict) or not all(
        isinstance(name, str) and name and isinstance(source, str) and source
        for name, source in mappings.items()
    ):
        raise TypeError("mappings must map nonempty local names to source parameter names")
    live = _resolve_context_target(target, greedy, identifier_type)
    live = get_parameter_context(live.id, identifier_type="id")
    source = nipyapi.utils.resolve_entity(
        group_name,
        get_parameter_context,
        ParameterContextEntity,
        strict=True,
        greedy=False,
        identifier_type="name",
    )
    available = {
        item.parameter.name: item.parameter.sensitive for item in source.component.parameters or []
    }
    missing = set(mappings.values()) - set(available)
    if missing:
        raise ValueError(
            f"Missing source parameters: {sorted(missing)}; available: {sorted(available)}"
        )
    # NiFi leaves a reference unresolved when the sensitivities differ.
    missing = sorted({name for name in mappings.values() if not available[name]})
    if missing:
        raise ValueError(f"Source parameters are not sensitive: {missing}")
    if any("}" in name or "#{" in name for name in mappings.values()):
        raise ValueError(
            "Source parameter names must be representable as a single parameter reference"
        )
    existing = {
        item.parameter.name: item.parameter
        for item in live.component.parameters or []
        if not item.parameter.inherited
    }
    for name, source_name in mappings.items():
        if name in existing and not existing[name].sensitive:
            raise ValueError(
                f"Local parameter '{name}' is non-sensitive; NiFi cannot change its sensitivity"
            )
        if name == source_name:
            raise ValueError("A local alias cannot reference itself")
    references = _connect_inherited_references(live, source, mappings)
    aliases = [
        prepare_parameter(
            name,
            "#{" + source_name + "}",
            description=existing[name].description if name in existing else None,
            sensitive=True,
        )
        for name, source_name in mappings.items()
    ]
    return _submit_parameter_context_update(
        live,
        ParameterContextDTO(
            id=live.id,
            name=live.component.name,
            parameters=aliases,
            inherited_parameter_contexts=references,
        ),
    )


def rename_parameter_context(context, name, refresh=True, greedy=True, identifier_type="auto"):
    """
    Rename a Parameter Context without resubmitting parameter values.

    This is a lightweight wrapper around update_parameter_context that only
    updates the name field, avoiding the overhead of revalidating all parameters.

    Args:
        context (ParameterContextEntity or str): Parameter Context to rename,
            as a ParameterContextEntity object, context ID, or context name.
        name (str): The new name for the parameter context.
        refresh (bool): Whether to refresh the Context before renaming.
        greedy (bool): For name lookup, True for partial match, False for exact.
        identifier_type (str): How to interpret string identifier:
            "auto" (default) detects UUID vs name, "id" or "name" to force.

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The renamed Parameter Context

    Raises:
        TypeError: If context is not a string or ParameterContextEntity.
        ValueError: If parameter context not found or multiple matches found.

    Example::

        # Rename by ID
        nipyapi.parameters.rename_parameter_context('ctx-id', 'new-name')

        # Rename by name
        nipyapi.parameters.rename_parameter_context('old-name', 'new-name')
    """
    context = nipyapi.utils.resolve_entity(
        context,
        get_parameter_context,
        ParameterContextEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )

    if refresh:
        context = get_parameter_context(context.id, identifier_type="id")

    # Build entity with just the name changed, empty parameters list
    context.component.name = name
    context.component.parameters = []

    return update_parameter_context(context)


def delete_parameter_context(context, refresh=True, greedy=True, identifier_type="auto"):
    """
    Removes a Parameter Context

    Args:
        context (ParameterContextEntity or str): Parameter Context to be deleted,
            as a ParameterContextEntity object, context ID, or context name.
        refresh (bool): Whether to refresh the Context before Deletion
        greedy (bool): For name lookup, True for partial match, False for exact.
        identifier_type (str): How to interpret string identifier:
            "auto" (default) detects UUID vs name, "id" or "name" to force.

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The removed Parameter Context

    Raises:
        TypeError: If context is not a string or ParameterContextEntity.
        ValueError: If parameter context not found or multiple matches found.
    """
    context = nipyapi.utils.resolve_entity(
        context,
        get_parameter_context,
        nipyapi.nifi.ParameterContextEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
    handle = nipyapi.nifi.ParameterContextsApi()
    if refresh:
        context = handle.get_parameter_context(context.id)
    return handle.delete_parameter_context(id=context.id, version=context.revision.version)


def prepare_parameter(name, value=_NOT_PROVIDED, description=None, sensitive=False):
    """
    Parses basic inputs into a Parameter object ready for submission

    Args:
        name (str): The Name for the Parameter
        value (str, int, float, None): The Value for the Parameter.
            - Omit: Don't change existing value (useful for updating description only)
            - None: Explicitly unset/remove the value
            - "": Set to empty string
            - Other: Set to that value
        description (str): Optional Description for the Parameter
        sensitive (bool): Whether to mark the Parameter Value as sensitive

    Returns:
        :class:`~nipyapi.nifi.models.ParameterEntity`: The ParameterEntity ready for use

    Example::

        >>> # Create parameter with value
        >>> param = prepare_parameter("Username", "admin")

        >>> # Update description without changing value (e.g., for sensitive params)
        >>> param = prepare_parameter("Password", description="Database password")

        >>> # Explicitly unset/remove a parameter's value
        >>> param = prepare_parameter("OptionalSetting", value=None)
    """
    assert all(x is None or isinstance(x, str) for x in [name, description])

    if value is _NOT_PROVIDED:
        # Value omitted - don't include value in DTO (leaves existing value unchanged)
        out = ParameterEntity(
            parameter=ParameterDTO(name=name, description=description, sensitive=sensitive)
        )
    elif value is None:
        # Explicitly unset the value
        out = ParameterEntity(
            parameter=ParameterDTO(
                name=name,
                value=None,
                value_removed=True,
                description=description,
                sensitive=sensitive,
            )
        )
    else:
        # Set to provided value
        out = ParameterEntity(
            parameter=ParameterDTO(
                name=name, value=value, description=description, sensitive=sensitive
            )
        )
    return out


def delete_parameter_from_context(context, parameter_name, greedy=True, identifier_type="auto"):
    """
    Delete a specific Parameter from a Parameter Context

    Args:
        context (ParameterContextEntity or str): The Parameter Context to Update,
            as a ParameterContextEntity object, context ID, or context name.
        parameter_name (str): The Parameter to delete
        greedy (bool): For name lookup, True for partial match, False for exact.
        identifier_type (str): How to interpret string identifier:
            "auto" (default) detects UUID vs name, "id" or "name" to force.

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The updated Parameter Context

    Raises:
        TypeError: If context is not a string or ParameterContextEntity.
        ValueError: If parameter context not found or multiple matches found.
    """
    context = nipyapi.utils.resolve_entity(
        context,
        get_parameter_context,
        nipyapi.nifi.ParameterContextEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
    context.component.parameters = [ParameterEntity(parameter=ParameterDTO(name=parameter_name))]
    return update_parameter_context(context=context)


def upsert_parameter_to_context(context, parameter, greedy=True, identifier_type="auto"):
    """
    Insert or Update Parameter within a Parameter Context

    Args:
        context (ParameterContextEntity or str): The Parameter Context to Modify,
            as a ParameterContextEntity object, context ID, or context name.
        parameter (ParameterEntity): The ParameterEntity to insert or update
        greedy (bool): For name lookup, True for partial match, False for exact.
        identifier_type (str): How to interpret string identifier:
            "auto" (default) detects UUID vs name, "id" or "name" to force.

    Returns:
        :class:`~nipyapi.nifi.models.ParameterContextEntity`: The updated Parameter Context

    Raises:
        TypeError: If context is not a string or ParameterContextEntity.
        ValueError: If parameter context not found or multiple matches found.
    """
    context = nipyapi.utils.resolve_entity(
        context,
        get_parameter_context,
        nipyapi.nifi.ParameterContextEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
    context.component.parameters = [parameter]
    return update_parameter_context(context=context)


def assign_context_to_process_group(
    pg, context_id, cascade=False, greedy=True, identifier_type="auto"
):
    """
    Assigns a given Parameter Context to a specific Process Group
    Optionally cascades down to direct children Process Groups

    Args:
        pg (ProcessGroupEntity or str): The Process Group to target,
            as a ProcessGroupEntity object, process group ID, or name.
        context_id (str): The ID of the Parameter Context
        cascade (bool): Cascade Parameter Context down to child Process Groups?
        greedy (bool): For name lookup, True for partial match, False for exact.
        identifier_type (str): How to interpret string identifier:
            "auto" (default) detects UUID vs name, "id" or "name" to force.

    Returns:
        :class:`~nipyapi.nifi.models.ProcessGroupEntity`: The updated Process Group

    Raises:
        TypeError: If pg is not a string or ProcessGroupEntity.
        ValueError: If process group not found or multiple matches found.
    """
    assert isinstance(context_id, str)
    pg = nipyapi.utils.resolve_entity(
        pg,
        nipyapi.canvas.get_process_group,
        nipyapi.nifi.ProcessGroupEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
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


def remove_context_from_process_group(pg, greedy=True, identifier_type="auto"):
    """
    Clears any Parameter Context from the given Process Group

    Args:
        pg (ProcessGroupEntity or str): The Process Group to target,
            as a ProcessGroupEntity object, process group ID, or name.
        greedy (bool): For name lookup, True for partial match, False for exact.
        identifier_type (str): How to interpret string identifier:
            "auto" (default) detects UUID vs name, "id" or "name" to force.

    Returns:
        :class:`~nipyapi.nifi.models.ProcessGroupEntity`: The updated Process Group

    Raises:
        TypeError: If pg is not a string or ProcessGroupEntity.
        ValueError: If process group not found or multiple matches found.
    """
    pg = nipyapi.utils.resolve_entity(
        pg,
        nipyapi.canvas.get_process_group,
        nipyapi.nifi.ProcessGroupEntity,
        strict=True,
        greedy=greedy,
        identifier_type=identifier_type,
    )
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

    Example::

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
        dict mapping parameter names to ownership info dicts. Each ownership
        dict has: context_id, context_name, description, sensitive, has_asset,
        asset_name, and current_value (None if sensitive).

    Example::

        >>> ownership = get_parameter_ownership_map(context_id)
        >>> print(ownership["PostgreSQL Username"])
        {'context_id': '...', 'context_name': 'PostgreSQL Source Parameters', ...}
    """

    hierarchy = get_parameter_context_hierarchy(context_id)
    ownership_map = {}

    def _traverse(h):
        for param in h["parameters"]:
            ownership_map[param["name"]] = {
                "context_id": h["id"],
                "context_name": h["name"],
                "description": param["description"],
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

    Example::

        >>> # Safe update - only if param exists in this context
        >>> update_parameter_in_context(ctx_id, "Username", "newuser")

        >>> # Create if missing (use with caution - may shadow inherited params)
        >>> update_parameter_in_context(ctx_id, "NewParam", "value", create_if_missing=True)
    """

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

    Example::

        >>> assets = list_assets(context_id)
        >>> for asset in assets:
        ...     print(f"{asset['name']} ({asset['id']})")
    """

    handle = nipyapi.nifi.ParameterContextsApi()
    # get_assets1: NiFi 2.10 ConnectorsApi collision suffixed the original
    response = handle.get_assets1(context_id)

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

    Example::

        >>> # Upload from file path
        >>> asset = upload_asset(context_id, file_path="/path/to/driver.jar")

        >>> # Upload from bytes with explicit filename
        >>> asset = upload_asset(context_id, file_bytes=data, filename="driver.jar")
    """

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
    # create_asset1: NiFi 2.10 ConnectorsApi collision suffixed the original
    result = handle.create_asset1(body=file_bytes, context_id=context_id, filename=filename)

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

    Example::

        >>> result = delete_asset(context_id, asset_id)
        >>> print(f"Deleted: {result['name']}")
    """

    handle = nipyapi.nifi.ParameterContextsApi()
    result = handle.delete_asset(context_id=context_id, asset_id=asset_id)

    log.info("Deleted asset '%s' from context %s", result.asset.name, context_id)

    return {
        "id": result.asset.id,
        "name": result.asset.name,
    }


def prepare_parameter_with_asset(
    name, asset_id=None, asset_name=None, description=None, assets=None
):
    """
    Prepare a parameter that references one or more assets.

    Use this to update a parameter to point to uploaded asset(s).
    Provide either (asset_id + asset_name) for a single asset, or assets
    for multiple assets. These are mutually exclusive.

    Args:
        name (str): Parameter name (required)
        asset_id (str, optional): ID of a single asset. Must be provided
            together with asset_name. Cannot be used with assets.
        asset_name (str, optional): Name of a single asset. Must be provided
            together with asset_id. Cannot be used with assets.
        description (str, optional): Parameter description
        assets (list, optional): List of asset dicts, each with 'id' and
            'name' keys. Cannot be used with asset_id/asset_name.

    Returns:
        :class:`~nipyapi.nifi.models.ParameterEntity`: ParameterEntity ready for
            use with update_parameter_context or upsert_parameter_to_context

    Example (single asset)::

        >>> # Upload asset first
        >>> asset = upload_asset(context_id, file_path="/path/to/driver.jar")
        >>> # Then prepare parameter to reference it
        >>> param = prepare_parameter_with_asset(
        ...     name="JDBC Driver",
        ...     asset_id=asset['id'],
        ...     asset_name=asset['name']
        ... )
        >>> upsert_parameter_to_context(context, param)

    Example (multiple assets)::

        >>> # Upload multiple JARs
        >>> jar1 = upload_asset(context_id, file_path="/path/to/activemq-client.jar")
        >>> jar2 = upload_asset(context_id, file_path="/path/to/activemq-broker.jar")
        >>> # Reference all in one parameter
        >>> param = prepare_parameter_with_asset(
        ...     name="JMS Client Libraries",
        ...     assets=[jar1, jar2]  # Each dict has 'id' and 'name'
        ... )
        >>> upsert_parameter_to_context(context, param)
    """

    # Validate argument combinations
    has_single = asset_id is not None or asset_name is not None
    has_multiple = assets is not None

    if has_single and has_multiple:
        raise ValueError(
            "Cannot specify both asset_id/asset_name and assets. "
            "Use asset_id/asset_name for single asset, or assets for multiple."
        )

    if not has_single and not has_multiple:
        raise ValueError("Must specify either asset_id and asset_name, or assets list.")

    if has_single:
        if asset_id is None or asset_name is None:
            raise ValueError("Both asset_id and asset_name are required for single asset.")
        asset_refs = [AssetReferenceDTO(id=asset_id, name=asset_name)]
    else:
        # Validate assets list
        if not isinstance(assets, list) or len(assets) == 0:
            raise ValueError("assets must be a non-empty list of dicts with 'id' and 'name' keys.")
        asset_refs = []
        for i, asset in enumerate(assets):
            if not isinstance(asset, dict) or "id" not in asset or "name" not in asset:
                raise ValueError(
                    f"Asset at index {i} must be a dict with 'id' and 'name' keys. " f"Got: {asset}"
                )
            asset_refs.append(AssetReferenceDTO(id=asset["id"], name=asset["name"]))

    return ParameterEntity(
        parameter=ParameterDTO(name=name, description=description, referenced_assets=asset_refs)
    )
