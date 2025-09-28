"""
For Managing NiFi Parameter Contexts
"""

import logging

import nipyapi
from nipyapi.nifi import ParameterContextDTO, ParameterContextEntity, ParameterDTO, ParameterEntity
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
