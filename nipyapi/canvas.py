# pylint: disable=C0302

"""
For interactions with the NiFi Canvas.
"""

import logging
import os
from collections import namedtuple

import nipyapi
from nipyapi.utils import exception_handler

# Named tuple for get_flow_components return value
FlowSubgraph = namedtuple("FlowSubgraph", ["components", "connections"])

__all__ = [
    "get_root_pg_id",
    "recurse_flow",
    "get_flow",
    "get_process_group_status",
    "get_process_group",
    "list_all_process_groups",
    "delete_process_group",
    "schedule_process_group",
    "create_process_group",
    "list_all_processors",
    "list_all_processor_types",
    "get_processor_type",
    "get_processor_docs",
    "create_processor",
    "delete_processor",
    "get_processor",
    "schedule_processor",
    "get_funnel",
    "update_processor",
    "get_variable_registry",
    "update_variable_registry",
    "purge_connection",
    "list_flowfiles",
    "get_flowfile_details",
    "get_flowfile_content",
    "peek_flowfiles",
    "purge_process_group",
    "schedule_components",
    "get_bulletins",
    "get_bulletin_board",
    "list_invalid_processors",
    "list_sensitive_processors",
    "list_all_connections",
    "get_connection",
    "update_connection",
    "create_connection",
    "delete_connection",
    "get_component_connections",
    "create_controller",
    "list_all_controllers",
    "delete_controller",
    "update_controller",
    "schedule_controller",
    "schedule_all_controllers",
    "get_controller",
    "list_all_controller_types",
    "get_controller_type",
    "get_controller_service_docs",
    "list_all_by_kind",
    "list_all_input_ports",
    "list_all_output_ports",
    "list_all_funnels",
    "list_all_remote_process_groups",
    "delete_funnel",
    "get_remote_process_group",
    "update_process_group",
    "create_funnel",
    "create_remote_process_group",
    "delete_remote_process_group",
    "set_remote_process_group_transmission",
    "get_pg_parents_ids",
    "delete_port",
    "create_port",
    "get_flow_components",
    "FlowSubgraph",
    "verify_controller",
    "verify_processor",
    "get_controller_state",
    "clear_controller_state",
    "get_processor_state",
    "clear_processor_state",
]

log = logging.getLogger(__name__)


def get_root_pg_id():
    """
    Convenience function to return the UUID of the Root Process Group

    Returns (str): The UUID of the root PG
    """
    return nipyapi.nifi.FlowApi().get_process_group_status("root").process_group_status.id


def recurse_flow(pg_id="root"):
    """
    Returns information about a Process Group and all its Child Flows.

    Recurses the child flows by appending each process group with a
    'nipyapi_extended' parameter which contains the child process groups, etc.

    Note: This previously used actual recursion which broke on large NiFi
    environments, we now use a task/list update approach.

    Args:
        pg_id (str): The Process Group UUID

    Returns:
         :class:`~nipyapi.nifi.models.ProcessGroupFlowEntity`: enriched NiFi Flow object
    """
    assert isinstance(pg_id, str), "pg_id should be a string"

    out = get_flow(pg_id)
    tasks = [(x.id, x) for x in out.process_group_flow.flow.process_groups]
    while tasks:
        this_pg_id, this_parent_obj = tasks.pop()
        this_flow = get_flow(this_pg_id)
        setattr(this_parent_obj, "nipyapi_extended", this_flow)
        tasks += [(x.id, x) for x in this_flow.process_group_flow.flow.process_groups]
    return out


def get_flow(pg_id="root"):
    """
    Returns information about a Process Group and flow.

    This surfaces the native implementation, for the recursed implementation
    see 'recurse_flow'

    Args:
        pg_id (str): id of the Process Group to retrieve, defaults to the root
            process group if not set

    Returns:
         :class:`~nipyapi.nifi.models.ProcessGroupFlowEntity`: The Process Group object
    """
    assert isinstance(pg_id, str), "pg_id should be a string"
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.FlowApi().get_flow(pg_id)


def get_process_group_status(pg_id="root", detail="names"):
    """
    Returns an entity containing the status of the Process Group.
    Optionally may be configured to return a simple dict of name:id pairings

    Note that there is also a 'process group status' command available, but it
    returns a subset of this data anyway, and this call is more useful

    Args:
        pg_id (str): The UUID of the Process Group
        detail (str): 'names' or 'all'; whether to return a simple dict of
            name:id pairings, or the full details. Defaults to 'names'

    Returns:
         :class:`~nipyapi.nifi.models.ProcessGroupEntity`: The Process Group Entity including
         the status
    """
    assert isinstance(pg_id, str), "pg_id should be a string"
    assert detail in ["names", "all"]
    raw = nipyapi.nifi.ProcessGroupsApi().get_process_group(id=pg_id)
    if detail == "names":
        out = {raw.component.name: raw.component.id}
        return out
    return raw


@exception_handler(404, None)
def get_process_group(identifier, identifier_type="name", greedy=True):
    """
    Filters the list of all process groups against a given identifier string
    occurring in a given identifier_type field.

    Args:
        identifier (str): the string to filter the list for
        identifier_type (str): the field to filter on, set in config.py
        greedy (bool): True for partial match, False for exact match

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches

    """
    assert isinstance(identifier, str)
    assert identifier_type in ["name", "id"]
    with nipyapi.utils.rest_exceptions():
        if identifier_type == "id" or identifier == "root":
            # assuming unique fetch of pg id, 'root' is special case
            # implementing separately to avoid recursing entire canvas
            out = nipyapi.nifi.ProcessGroupsApi().get_process_group(identifier)
        else:
            obj = list_all_process_groups()
            out = nipyapi.utils.filter_obj(obj, identifier, identifier_type, greedy=greedy)
    return out


# pylint: disable=R1737
def list_all_process_groups(pg_id="root"):
    """
    Returns a flattened list of all Process Groups on the canvas.
    Potentially slow if you have a large canvas.

    Note that the ProcessGroupsApi().get_process_groups(pg_id) command only
    provides the first layer of pgs, whereas this trawls the entire canvas

    Args:
        pg_id (str): The UUID of the Process Group to start from, defaults to
            the Canvas root

    Returns:
         list[ProcessGroupEntity]

    """
    assert isinstance(pg_id, str), "pg_id should be a string"

    def flatten(parent_pg):
        """
        Recursively flattens the native datatypes into a generic list.
        Note that the root is a special case as it has no parent

        Args:
            parent_pg (ProcessGroupEntity): object to flatten

        Yields:
            Generator for all ProcessGroupEntities, eventually
        """
        for child_pg in parent_pg.process_group_flow.flow.process_groups:
            for item in flatten(child_pg.nipyapi_extended):
                yield item
            yield child_pg

    # Recurse children
    root_flow = recurse_flow(pg_id)
    # Flatten list of children with extended detail
    out = list(flatten(root_flow))
    # update parent with flattened list of extended child detail
    root_entity = get_process_group(pg_id, "id")
    setattr(root_entity, "nipyapi_extended", root_flow)
    out.append(root_entity)
    return out
    #
    # if pg_id == 'root' or pg_id == get_root_pg_id():
    #     # This duplicates the nipyapi_extended structure to the root case
    #     root_entity = get_process_group('root', 'id')
    #     root_entity.__setattr__('nipyapi_extended', root_flow)
    #     out.append(root_entity)
    # return out


def list_invalid_processors(pg_id="root", summary=False):
    """
    Returns a flattened list of all Processors with Invalid Statuses

    Args:
        pg_id (str): The UUID of the Process Group to start from, defaults to
            the Canvas root
        summary (bool): True to return just the list of relevant
            properties per Processor, False for the full listing

    Returns:
        list[ProcessorEntity]
    """
    assert isinstance(pg_id, str), "pg_id should be a string"
    assert isinstance(summary, bool)
    proc_list = [x for x in list_all_processors(pg_id) if x.component.validation_errors]
    if summary:
        out = [{"id": x.id, "summary": x.component.validation_errors} for x in proc_list]
    else:
        out = proc_list
    return out


def list_sensitive_processors(pg_id="root", summary=False):
    """
    Returns a flattened list of all Processors on the canvas which have
    sensitive properties that would need to be managed during deployment

    Args:
        pg_id (str): The UUID of the Process Group to start from, defaults to
            the Canvas root
        summary (bool): True to return just the list of relevant
            properties per Processor, False for the full listing

    Returns:
        list[ProcessorEntity] or list(dict)
    """
    assert isinstance(pg_id, str), "pg_id should be a string"
    assert isinstance(summary, bool)
    cache = nipyapi.config.cache.get("list_sensitive_processors")
    if not cache:
        cache = []
    matches = []
    proc_list = list_all_processors(pg_id)
    for proc in proc_list:
        if proc.component.type in cache:
            matches.append(proc)
        else:
            sensitive_test = False
            for _, detail in proc.component.config.descriptors.items():
                if detail.sensitive is True:
                    sensitive_test = True
                    break
            if sensitive_test:
                matches.append(proc)
                cache.append(str(proc.component.type))
    if cache:
        nipyapi.config.cache["list_sensitive_processors"] = cache
    if summary:
        return [
            {x.id: [p for p, q in x.component.config.descriptors.items() if q.sensitive is True]}
            for x in matches
        ]
    return matches


def list_all_processors(pg_id="root"):
    """
    Returns a flat list of all Processors under the provided Process Group

    Args:
        pg_id (str): The UUID of the Process Group to start from, defaults to
            the Canvas root

    Returns:
         list[ProcessorEntity]
    """
    assert isinstance(pg_id, str), "pg_id should be a string"

    if nipyapi.utils.check_version("1.7.0") <= 0:
        # Case where NiFi > 1.7.0
        targets = nipyapi.nifi.ProcessGroupsApi().get_processors(
            id=pg_id, include_descendant_groups=True
        )
        return targets.processors
    # Handle older NiFi instances
    out = []
    # list of child process groups
    pg_ids = [x.id for x in list_all_process_groups(pg_id)]
    # process target list
    for this_pg_id in pg_ids:
        procs = nipyapi.nifi.ProcessGroupsApi().get_processors(this_pg_id)
        if procs.processors:
            out += procs.processors
    return out


def schedule_process_group(process_group_id, scheduled):
    """
    Start or Stop a Process Group and all components.

    Note that this doesn't guarantee that all components have started, as
    some may be in Invalid states.

    Args:
        process_group_id (str): The UUID of the target Process Group
        scheduled (bool): True to start, False to stop

    Returns:
         (bool): True of successfully scheduled, False if not

    """
    assert isinstance(process_group_id, str)
    assert isinstance(scheduled, bool)

    def _running_schedule_process_group(pg_id_):
        test_obj = nipyapi.nifi.ProcessGroupsApi().get_process_group(pg_id_)
        if test_obj.status.aggregate_snapshot.active_thread_count == 0:
            return True
        return False

    assert isinstance(get_process_group(process_group_id, "id"), nipyapi.nifi.ProcessGroupEntity)
    result = schedule_components(pg_id=process_group_id, scheduled=scheduled)
    # If target scheduled state was successfully updated
    if result:
        # If we want to stop the processor
        if not scheduled:
            # Test that the processor threads have halted
            stop_test = nipyapi.utils.wait_to_complete(
                _running_schedule_process_group, process_group_id
            )
            if stop_test:
                # Return True if we stopped the Process Group
                return result
            # Return False if we scheduled a stop, but it didn't stop
            return False
    # Return the True or False result if we were trying to start it
    return result


def delete_process_group(process_group, force=False, refresh=True):
    """
    Deletes a given Process Group, with optional prejudice.

    Args:
        process_group (ProcessGroupEntity): The target Process Group
        force (bool): Stop, purge and clean the target Process Group before
            deletion. Experimental.
        refresh (bool): Whether to refresh the state first

    Returns:
         (ProcessGroupEntity: The updated object state

    """
    assert isinstance(process_group, nipyapi.nifi.ProcessGroupEntity)
    assert isinstance(force, bool)
    assert isinstance(refresh, bool)
    pg_id = process_group.id
    if refresh or force:
        target = nipyapi.nifi.ProcessGroupsApi().get_process_group(pg_id)
    else:
        target = process_group
    try:
        return nipyapi.nifi.ProcessGroupsApi().remove_process_group(
            id=target.id, version=target.revision.version, client_id=target.revision.client_id
        )
    except nipyapi.nifi.rest.ApiException as e:
        if force:
            # Retrieve parent process group
            parent_pg_id = nipyapi.canvas.get_process_group(pg_id, "id").component.parent_group_id
            # Stop, drop, and roll.
            purge_process_group(target, stop=True)
            # Remove inbound connections
            for con in list_all_connections(parent_pg_id):
                if pg_id in [con.destination_group_id, con.source_group_id]:
                    delete_connection(con)
            # Disable all Controller Services inside the PG
            schedule_all_controllers(pg_id, scheduled=False)

            # Templates are not supported in NiFi 2.x
            if nipyapi.utils.check_version("2", service="nifi") == 1:
                for template in nipyapi.templates.list_all_templates(native=False):
                    if target.id == template.template.group_id:
                        nipyapi.templates.delete_template(template.id)
            # have to refresh revision after changes
            target = nipyapi.nifi.ProcessGroupsApi().get_process_group(pg_id)
            return nipyapi.nifi.ProcessGroupsApi().remove_process_group(
                id=target.id, version=target.revision.version, client_id=target.revision.client_id
            )
        raise ValueError(e.body) from e


def create_process_group(parent_pg, new_pg_name, location, comment=""):
    """
    Creates a new Process Group with the given name under the provided parent
    Process Group at the given Location

    Args:
        parent_pg (str or ProcessGroupEntity): The parent Process Group ID
            (as a string) or ProcessGroupEntity object to create the new
            process group in. Use "root" for the root canvas.
        new_pg_name (str): The name of the new Process Group
        location (tuple[x, y]): the x,y coordinates to place the new Process
            Group under the parent
        comment (str): Entry for the Comments field

    Returns:
         :class:`~nipyapi.nifi.models.ProcessGroupEntity`: The new Process Group

    """
    # Accept either a string ID or ProcessGroupEntity
    if isinstance(parent_pg, str):
        parent_id = parent_pg
    elif isinstance(parent_pg, nipyapi.nifi.ProcessGroupEntity):
        parent_id = parent_pg.id
    else:
        raise TypeError(
            f"parent_pg must be a string ID or ProcessGroupEntity, got {type(parent_pg).__name__}"
        )
    assert isinstance(new_pg_name, str)
    assert isinstance(location, tuple)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_process_group(
            id=parent_id,
            body=nipyapi.nifi.ProcessGroupEntity(
                revision={"version": 0},
                component=nipyapi.nifi.ProcessGroupDTO(
                    name=new_pg_name,
                    position=nipyapi.nifi.PositionDTO(x=float(location[0]), y=float(location[1])),
                    comments=comment,
                ),
            ),
        )


def list_all_processor_types():
    """
    Produces the list of all available processor types in the NiFi instance

    Returns:
         list(ProcessorTypesEntity): A native datatype containing the
         processors list

    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.FlowApi().get_processor_types()


def get_processor_type(identifier, identifier_type="name", greedy=True):
    """
    Gets the abstract object describing a Processor, or list thereof

    Args:
        identifier (str): the string to filter the list for
        identifier_type (str): the field to filter on, set in config.py
        greedy (bool): False for exact match, True for greedy match

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches

    """
    with nipyapi.utils.rest_exceptions():
        obj = list_all_processor_types().processor_types
    if obj:
        return nipyapi.utils.filter_obj(obj, identifier, identifier_type, greedy=greedy)
    return obj


def get_processor_docs(processor):
    """
    Get detailed documentation for a processor, including properties, use cases, and tags.

    This function retrieves the full ProcessorDefinition from NiFi, which contains
    comprehensive documentation useful for understanding processor capabilities
    and configuration options.

    Args:
        processor (ProcessorEntity or DocumentedTypeDTO or str): An existing processor,
            a processor type from get_processor_type(), or a type name string
            (e.g., "GenerateFlowFile" or full qualified name).

    Returns:
        :class:`~nipyapi.nifi.models.ProcessorDefinition`: Processor documentation
            including property_descriptors, tags, supported_relationships,
            multi_processor_use_cases, dynamic_properties, and more.
        None: If processor type not found.

    Example::

        # From existing processor
        proc = nipyapi.canvas.get_processor("MyProcessor")
        docs = nipyapi.canvas.get_processor_docs(proc)
        print(docs.tags)  # ['record', 'update', 'json', ...]
        print(docs.property_descriptors.keys())

        # From processor type
        proc_type = nipyapi.canvas.get_processor_type("UpdateRecord")
        docs = nipyapi.canvas.get_processor_docs(proc_type)

        # From type name string
        docs = nipyapi.canvas.get_processor_docs("GenerateFlowFile")

    """
    # Extract bundle info based on input type
    if isinstance(processor, nipyapi.nifi.ProcessorEntity):
        bundle = processor.component.bundle
        proc_type = processor.component.type
    elif isinstance(processor, nipyapi.nifi.DocumentedTypeDTO):
        bundle = processor.bundle
        proc_type = processor.type
    elif isinstance(processor, str):
        # Look up processor type by name
        proc_type_obj = get_processor_type(processor, identifier_type="name", greedy=False)
        if proc_type_obj is None:
            # Try greedy match
            proc_type_obj = get_processor_type(processor, identifier_type="name", greedy=True)
        if proc_type_obj is None:
            return None
        if isinstance(proc_type_obj, list):
            proc_type_obj = proc_type_obj[0]  # Take first match
        bundle = proc_type_obj.bundle
        proc_type = proc_type_obj.type
    else:
        raise ValueError(
            f"processor must be ProcessorEntity, DocumentedTypeDTO, or str, "
            f"got: {type(processor).__name__}"
        )

    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.FlowApi().get_processor_definition(
            group=bundle.group,
            artifact=bundle.artifact,
            version=bundle.version,
            type=proc_type,
        )


def create_processor(parent_pg, processor, location, name=None, config=None):
    """
    Instantiates a given processor on the canvas

    Args:
        parent_pg (str or ProcessGroupEntity): The parent Process Group ID
            (as a string) or ProcessGroupEntity object
        processor (DocumentedTypeDTO): The abstract processor type object to be
            instantiated
        location (tuple[x, y]): The location coordinates
        name (Optional [str]):  The name for the new Processor
        config (Optional [ProcessorConfigDTO]): A configuration object for the
            new processor

    Returns:
         :class:`~nipyapi.nifi.models.ProcessorEntity`: The new Processor

    """
    # Accept either a string ID or ProcessGroupEntity
    if isinstance(parent_pg, str):
        parent_id = parent_pg
    elif isinstance(parent_pg, nipyapi.nifi.ProcessGroupEntity):
        parent_id = parent_pg.id
    else:
        raise TypeError(
            f"parent_pg must be a string ID or ProcessGroupEntity, got {type(parent_pg).__name__}"
        )
    assert isinstance(processor, nipyapi.nifi.DocumentedTypeDTO)
    if name is None:
        processor_name = processor.type.split(".")[-1]
    else:
        processor_name = name
    if config is None:
        target_config = nipyapi.nifi.ProcessorConfigDTO()
    else:
        target_config = config
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_processor(
            id=parent_id,
            body=nipyapi.nifi.ProcessorEntity(
                revision={"version": 0},
                component=nipyapi.nifi.ProcessorDTO(
                    position=nipyapi.nifi.PositionDTO(x=float(location[0]), y=float(location[1])),
                    type=processor.type,
                    bundle=processor.bundle,
                    name=processor_name,
                    config=target_config,
                ),
            ),
        )


@exception_handler(404, None)
def get_processor(identifier, identifier_type="name", greedy=True):
    """
    Filters the list of all Processors against the given identifier string in
    the given identifier_type field

    Args:
        identifier (str): The String to filter against
        identifier_type (str): The field to apply the filter to. Set in
            config.py
        greedy (bool): Whether to exact match (False) or partial match (True)

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches
    """
    assert isinstance(identifier, str)
    assert identifier_type in ["name", "id"]
    if identifier_type == "id":
        out = nipyapi.nifi.ProcessorsApi().get_processor(identifier)
    else:
        obj = list_all_processors()
        out = nipyapi.utils.filter_obj(obj, identifier, identifier_type, greedy=greedy)
    return out


def delete_processor(processor, refresh=True, force=False):
    """
    Deletes a Processor from the canvas, with optional prejudice.

    Args:
        processor (ProcessorEntity): The processor to delete
        refresh (bool): Whether to refresh the Processor state before action
        force (bool): Whether to stop, purge and remove connections to the
            Processor before deletion. Behavior may change in future releases.

    Returns:
         :class:`~nipyapi.nifi.models.ProcessorEntity`: The updated ProcessorEntity

    """
    assert isinstance(processor, nipyapi.nifi.ProcessorEntity)
    assert isinstance(refresh, bool)
    assert isinstance(force, bool)
    if refresh or force:
        target = get_processor(processor.id, "id")
        if target is None:
            return None  # Processor does not exist
        assert isinstance(target, nipyapi.nifi.ProcessorEntity)
    else:
        target = processor
    if force:
        if not schedule_processor(target, False):
            raise ValueError("Could not prepare processor {0} for deletion".format(target.id))
        inbound_cons = [
            x for x in get_component_connections(processor) if processor.id == x.destination_id
        ]
        for con in inbound_cons:
            delete_connection(con, purge=True)
        # refresh state before trying delete
        target = get_processor(processor.id, "id")
        assert isinstance(target, nipyapi.nifi.ProcessorEntity)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessorsApi().delete_processor(
            id=target.id, version=target.revision.version
        )


def schedule_components(pg_id, scheduled, components=None):
    """
    Change the scheduled target state of a list of components within a Process Group.

    Note that this does not guarantee that components will be Started or
    Stopped afterwards, merely that they will have their scheduling updated.

    This function only supports RUNNING and STOPPED states. For RUN_ONCE,
    use :func:`schedule_processor` on individual processors.

    Args:
        pg_id (str): The UUID of the parent Process Group
        scheduled (bool): True to start (RUNNING), False to stop (STOPPED)
        components (list[ComponentType]): The list of Component Entities to
            schedule, e.g. ProcessorEntity's. If None, schedules all
            components in the Process Group.

    Returns:
        bool: True for success, False for failure

    """
    assert isinstance(get_process_group(pg_id, "id"), nipyapi.nifi.ProcessGroupEntity)
    assert isinstance(scheduled, bool)
    assert components is None or isinstance(components, list)
    target_state = "RUNNING" if scheduled else "STOPPED"
    body = nipyapi.nifi.ScheduleComponentsEntity(id=pg_id, state=target_state)
    if components:
        body.components = {i.id: i.revision for i in components}
    with nipyapi.utils.rest_exceptions():
        result = nipyapi.nifi.FlowApi().schedule_components(id=pg_id, body=body)
    if result.state == target_state:
        return True
    return False


def schedule_processor(processor, scheduled, refresh=True):
    """
    Set a Processor to Start, Stop, Disable, or Run Once.

    Note that this doesn't guarantee that it will change state, merely that
    it will be instructed to try. Some effort is made to wait and see if the
    processor reaches the target state.

    Args:
        processor (str or ProcessorEntity): The Processor ID or ProcessorEntity object.
        scheduled (bool or str): True/False for RUNNING/STOPPED, or one of
            "RUNNING", "STOPPED", "DISABLED", "RUN_ONCE".
        refresh (bool): Whether to refresh the object before action.

    Returns:
        bool: True for success, False for failure.

    Example::

        # Start a processor by ID
        nipyapi.canvas.schedule_processor("<processor-id>", True)

        # Start a processor object (backwards compatible)
        nipyapi.canvas.schedule_processor(proc, True)

        # Stop a processor
        nipyapi.canvas.schedule_processor(proc, False)

        # Disable a processor (prevents starting, useful for maintenance)
        nipyapi.canvas.schedule_processor(proc, "DISABLED")

        # Run once - executes one scheduling cycle then stops
        nipyapi.canvas.schedule_processor(proc, "RUN_ONCE")
    """
    # Accept ID or entity
    if isinstance(processor, str):
        processor_id = processor
        processor = get_processor(processor_id, "id")
        if processor is None:
            raise ValueError(f"Processor not found: {processor_id}")
    assert isinstance(processor, nipyapi.nifi.ProcessorEntity)
    assert isinstance(refresh, bool)

    # Normalize scheduled to a state string
    valid_states = ("RUNNING", "STOPPED", "DISABLED", "RUN_ONCE")
    if isinstance(scheduled, bool):
        target_state = "RUNNING" if scheduled else "STOPPED"
    elif isinstance(scheduled, str) and scheduled.upper() in valid_states:
        target_state = scheduled.upper()
    else:
        raise ValueError(f"scheduled must be bool or one of {valid_states}, got: {scheduled!r}")

    def _processor_stopped(processor_):
        test_obj = nipyapi.canvas.get_processor(processor_.id, "id")
        if test_obj.status.aggregate_snapshot.active_thread_count == 0:
            return True
        log.info(
            "Processor not stopped, active thread count %s",
            test_obj.status.aggregate_snapshot.active_thread_count,
        )
        return False

    def _processor_running(processor_):
        test_obj = nipyapi.canvas.get_processor(processor_.id, "id")
        if test_obj.component.state == "RUNNING":
            return True
        log.info("Processor not started, run_status %s", test_obj.component.state)
        return False

    def _processor_run_once_complete(processor_):
        """Check if RUN_ONCE has completed (processor returns to STOPPED)."""
        test_obj = nipyapi.canvas.get_processor(processor_.id, "id")
        # RUN_ONCE completes when state returns to STOPPED and no active threads
        if (
            test_obj.component.state == "STOPPED"
            and test_obj.status.aggregate_snapshot.active_thread_count == 0
        ):
            return True
        log.info(
            "RUN_ONCE not complete, state=%s threads=%s",
            test_obj.component.state,
            test_obj.status.aggregate_snapshot.active_thread_count,
        )
        return False

    def _processor_disabled(processor_):
        """Check if processor has reached DISABLED state."""
        test_obj = nipyapi.canvas.get_processor(processor_.id, "id")
        if test_obj.component.state == "DISABLED":
            return True
        log.info("Processor not disabled, state=%s", test_obj.component.state)
        return False

    if refresh:
        target = nipyapi.canvas.get_processor(processor.id, "id")
        assert isinstance(target, nipyapi.nifi.ProcessorEntity)
    else:
        target = processor

    # Use direct processor API for all state changes (handles all transitions
    # including from DISABLED state, which schedule_components cannot handle)
    body = nipyapi.nifi.ProcessorRunStatusEntity(revision=target.revision, state=target_state)
    with nipyapi.utils.rest_exceptions():
        nipyapi.nifi.ProcessorsApi().update_run_status4(body=body, id=target.id)

    # Wait for target state
    if target_state == "RUN_ONCE":
        return nipyapi.utils.wait_to_complete(_processor_run_once_complete, target)
    if target_state == "DISABLED":
        return nipyapi.utils.wait_to_complete(_processor_disabled, target)
    if target_state == "STOPPED":
        return nipyapi.utils.wait_to_complete(_processor_stopped, target)
    # RUNNING
    return nipyapi.utils.wait_to_complete(_processor_running, target)


def update_process_group(pg, update, refresh=True):
    """
    Updates a given Process Group.

    Args:
        pg (ProcessGroupEntity): The Process Group to
          target for update
        update (dict): key:value pairs to update
        refresh (bool): Whether to refresh the Process Group before
          applying the update

    Returns:
        :class:`~nipyapi.nifi.models.ProcessGroupEntity`: The updated ProcessorEntity

    """
    assert isinstance(pg, nipyapi.nifi.ProcessGroupEntity)
    with nipyapi.utils.rest_exceptions():
        if refresh:
            pg = get_process_group(pg.id, "id")
        return nipyapi.nifi.ProcessGroupsApi().update_process_group(
            id=pg.id,
            body=nipyapi.nifi.ProcessGroupEntity(
                component=nipyapi.nifi.ProcessGroupDTO(id=pg.id, **update),
                id=pg.id,
                revision=pg.revision,
            ),
        )


def update_processor(processor, update=None, name=None, refresh=True, auto_stop=False):
    """
    Updates a Processor's configuration and/or name.

    For configuration changes, pass a ProcessorConfigDTO:
        nifi.ProcessorConfigDTO(scheduling_period='3s')

    For renaming, pass the new name. Both can be provided together.

    Processors must be stopped for certain updates (including renaming).
    If auto_stop is True (default), the processor will be stopped before
    updating and restarted afterward if it was originally running.

    Args:
        processor (ProcessorEntity): The Processor to target for update
        update (ProcessorConfigDTO, optional): Configuration parameters to update
        name (str, optional): New name for the processor
        refresh (bool): Whether to refresh the Processor object state
            before applying the update. Default True.
        auto_stop (bool): If True, automatically stop the processor before
            updating and restart afterward if it was running. Default False.

    Returns:
        :class:`~nipyapi.nifi.models.ProcessorEntity`: The updated ProcessorEntity

    Raises:
        ValueError: If neither update nor name is provided, or if update is not
            a ProcessorConfigDTO, or if processor is running and auto_stop=False.
    """
    if update is None and name is None:
        raise ValueError("Must provide 'update' (ProcessorConfigDTO) and/or 'name'")
    if update is not None and not isinstance(update, nipyapi.nifi.ProcessorConfigDTO):
        raise ValueError("update param is not an instance of nifi.ProcessorConfigDTO")

    with nipyapi.utils.rest_exceptions():
        if refresh:
            processor = get_processor(processor.id, "id")

        was_running = processor.component.state == "RUNNING"

        if was_running and not auto_stop:
            raise ValueError(
                f"Processor '{processor.component.name}' is running. "
                "Stop it first or set auto_stop=True."
            )

        # Stop if running
        if was_running:
            schedule_processor(processor, scheduled=False, refresh=True)
            processor = get_processor(processor.id, "id")

        # Build the update DTO with whatever fields are provided
        dto_kwargs = {"id": processor.component.id}
        if name is not None:
            dto_kwargs["name"] = name
        if update is not None:
            dto_kwargs["config"] = update

        result = nipyapi.nifi.ProcessorsApi().update_processor(
            id=processor.id,
            body=nipyapi.nifi.ProcessorEntity(
                id=processor.id,
                revision=processor.revision,
                component=nipyapi.nifi.ProcessorDTO(**dto_kwargs),
            ),
        )

        # Restart if it was running
        if was_running:
            schedule_processor(result, scheduled=True, refresh=True)
            result = get_processor(result.id, "id")

        return result


def get_variable_registry(process_group, ancestors=True):
    """
    Gets the contents of the variable registry attached to a Process Group

    Args:
        process_group (ProcessGroupEntity): The Process Group to retrieve the
            Variable Registry from
        ancestors (bool): Whether to include the Variable Registries from child
            Process Groups

    Returns:
        :class:`~nipyapi.nifi.models.VariableRegistryEntity`: The Variable Registry

    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().get_variable_registry(
            process_group.id, include_ancestor_groups=ancestors
        )


def update_variable_registry(process_group, update, refresh=True):
    """
    Updates one or more key:value pairs in the variable registry

    Args:
        process_group (:class:`~nipyapi.nifi.models.ProcessGroupEntity`): The Process Group which
            has the Variable Registry to be updated
        update (list[tuple]): The variables to write to the registry
        refresh (bool): Whether to refresh the object revision before updating

    Returns:
        :class:`~nipyapi.nifi.models.VariableRegistryEntity`: The created or updated Variable
            Registry Entries

    """
    if not isinstance(process_group, nipyapi.nifi.ProcessGroupEntity):
        raise ValueError("param process_group is not a valid nifi.ProcessGroupEntity")
    if not isinstance(update, list):
        raise ValueError("param update is not a valid list of (key,value) tuples")
    # Parse variable update into the datatype
    var_update = [
        nipyapi.nifi.VariableEntity(
            nipyapi.nifi.VariableDTO(name=li[0], value=li[1], process_group_id=process_group.id)
        )
        for li in update
    ]
    with nipyapi.utils.rest_exceptions():
        if refresh:
            process_group = get_process_group(process_group.id, "id")
        return nipyapi.nifi.ProcessGroupsApi().update_variable_registry(
            id=process_group.id,
            body=nipyapi.nifi.VariableRegistryEntity(
                process_group_revision=process_group.revision,
                variable_registry=nipyapi.nifi.VariableRegistryDTO(
                    process_group_id=process_group.id, variables=var_update
                ),
            ),
        )


def create_connection(source, target, relationships=None, name=None, bends=None):
    """
    Creates a connection between two objects for the given relationships

    Args:
        source: Object to initiate the connection, e.g. ProcessorEntity
        target: Object to terminate the connection, e.g. FunnelEntity
        relationships (list): list of strings of relationships to connect, may
            be collected from the object 'relationships' property (optional)
        name (str): Defaults to None, String of Name for Connection (optional)
        bends (list): List of PositionDTO or (x, y) tuples for connection bends.
            For self-loop connections (source == target), bends are auto-calculated
            if not provided, to ensure the loop renders correctly in the UI.

    Returns:
        :class:`~nipyapi.nifi.models.ConnectionEntity`: for the created connection

    """
    # determine source and destination strings by class supplied
    source_type = nipyapi.utils.infer_object_label_from_class(source)
    target_type = nipyapi.utils.infer_object_label_from_class(target)
    if source_type not in ["OUTPUT_PORT", "INPUT_PORT", "FUNNEL"]:
        source_rels = [x.name for x in source.component.relationships]
        if relationships:
            assert all(i in source_rels for i in relationships), (
                "One or more relationships [{0}] not in list of valid "
                "Source Relationships [{1}]".format(str(relationships), str(source_rels))
            )
        else:
            # if no relationships supplied, we connect them all
            relationships = source_rels

    # Auto-calculate bends for self-loop connections if not provided.
    # Without bends, self-loops render incorrectly in the UI (zero-length line).
    # Bend offsets derived from empirical analysis in layout module.
    if source.id == target.id and bends is None:
        # Self-loop: create bends to the right of the processor
        # Offsets: X +477 (processor width + margin), Y +39 and +89 (bracket center)
        src_x = source.position.x
        src_y = source.position.y
        bends = [
            nipyapi.nifi.PositionDTO(x=src_x + 477, y=src_y + 39),
            nipyapi.nifi.PositionDTO(x=src_x + 477, y=src_y + 89),
        ]

    # Convert tuple bends to PositionDTO if needed
    if bends:
        bend_dtos = []
        for b in bends:
            if isinstance(b, tuple):
                # pylint: disable=unsubscriptable-object
                bend_dtos.append(nipyapi.nifi.PositionDTO(x=float(b[0]), y=float(b[1])))
            else:
                bend_dtos.append(b)
        bends = bend_dtos

    if source_type == "OUTPUT_PORT":
        # the hosting process group for an Output port connection to another
        # process group is the common parent process group
        parent_pg = get_process_group(source.component.parent_group_id, "id")
        if parent_pg.id == get_root_pg_id():
            parent_id = parent_pg.id
        else:
            parent_id = parent_pg.component.parent_group_id
    else:
        parent_id = source.component.parent_group_id
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_connection(
            id=parent_id,
            body=nipyapi.nifi.ConnectionEntity(
                revision=nipyapi.nifi.RevisionDTO(version=0),
                source_type=source_type,
                destination_type=target_type,
                component=nipyapi.nifi.ConnectionDTO(
                    source=nipyapi.nifi.ConnectableDTO(
                        id=source.id, group_id=source.component.parent_group_id, type=source_type
                    ),
                    name=name,
                    destination=nipyapi.nifi.ConnectableDTO(
                        id=target.id, group_id=target.component.parent_group_id, type=target_type
                    ),
                    selected_relationships=relationships,
                    bends=bends,
                ),
            ),
        )


def delete_connection(connection, purge=False):
    """
    Deletes a connection, optionally purges it first

    Args:
        connection (ConnectionEntity): Connection to delete
        purge (bool): True to Purge, Defaults to False

    Returns:
        :class:`~nipyapi.nifi.models.ConnectionEntity`: the modified Connection

    """
    assert isinstance(connection, nipyapi.nifi.ConnectionEntity)
    if purge:
        purge_connection(connection.id)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ConnectionsApi().delete_connection(
            id=connection.id, version=connection.revision.version
        )


def list_all_connections(pg_id="root", descendants=True):
    """
    Lists all connections for a given Process Group ID

    Args:
        pg_id (str): ID of the Process Group to retrieve Connections from
        descendants (bool): True to recurse child PGs, False to not

    Returns:
        (list): List of ConnectionEntity objects

    """
    return list_all_by_kind("connections", pg_id, descendants)


def get_connection(connection):
    """
    Get a connection by ID or refresh a ConnectionEntity.

    Args:
        connection: Either a connection UUID (str) or a ConnectionEntity object.
            If a ConnectionEntity is provided, fetches a fresh copy (useful for
            getting the latest revision before updates).

    Returns:
        ConnectionEntity: The requested connection

    Example::

        # Fetch by ID
        conn = nipyapi.canvas.get_connection("abc-123-uuid")

        # Refresh an existing entity
        fresh_conn = nipyapi.canvas.get_connection(conn)
    """
    # Accept ID string or ConnectionEntity
    if isinstance(connection, nipyapi.nifi.ConnectionEntity):
        connection = connection.id
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ConnectionsApi().get_connection(connection)


def update_connection(connection, name=None, bends=None, refresh=True):
    """
    Update a connection's configuration.

    Only parameters explicitly provided will be updated. To clear bends,
    pass an empty list.

    Args:
        connection (ConnectionEntity or str): ConnectionEntity or connection ID to update.
        name (str or None): New name for the connection, or None to leave unchanged.
        bends (list or None): Bend points as list of PositionDTO or (x, y) tuples.
            None keeps existing bends, [] clears all bends, [...] sets specific points.
        refresh (bool): Whether to refresh the connection before updating.

    Returns:
        ConnectionEntity: The updated connection

    Example::

        # Clear all bends from a connection
        updated = nipyapi.canvas.update_connection(conn, bends=[])

        # Clear bends by connection ID
        updated = nipyapi.canvas.update_connection("abc-123-uuid", bends=[])

        # Rename a connection
        updated = nipyapi.canvas.update_connection(conn, name="Primary Path")

        # Set specific bend points
        updated = nipyapi.canvas.update_connection(conn, bends=[(500, 300), (500, 400)])
    """
    # Accept ID or object
    if isinstance(connection, str):
        connection = get_connection(connection)

    assert isinstance(connection, nipyapi.nifi.ConnectionEntity)

    if refresh:
        connection = get_connection(connection.id)

    # Determine updated values (None means keep existing)
    updated_name = connection.component.name if name is None else name
    updated_bends = connection.component.bends if bends is None else bends

    # Convert tuple bends to PositionDTO if needed
    if updated_bends:
        bend_dtos = []
        for b in updated_bends:
            if isinstance(b, tuple):
                bend_dtos.append(nipyapi.nifi.PositionDTO(x=float(b[0]), y=float(b[1])))
            else:
                bend_dtos.append(b)
        updated_bends = bend_dtos

    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ConnectionsApi().update_connection(
            id=connection.id,
            body=nipyapi.nifi.ConnectionEntity(
                revision=connection.revision,
                source_type=connection.source_type,
                destination_type=connection.destination_type,
                component=nipyapi.nifi.ConnectionDTO(
                    id=connection.component.id,
                    name=updated_name,
                    source=connection.component.source,
                    destination=connection.component.destination,
                    bends=updated_bends,
                ),
            ),
        )


def get_component_connections(component):
    """
    Returns list of Connections related to a given Component, e.g. Processor

    Args:
        component: Component Object to filter by, e.g. a ProcessorEntity

    Returns:
        (list): List of ConnectionEntity Objects
    """
    assert isinstance(component, nipyapi.nifi.ProcessorEntity)
    return [
        x
        for x in list_all_connections(pg_id=component.component.parent_group_id)
        if component.id in [x.destination_id, x.source_id]
    ]


def get_flow_components(  # pylint: disable=too-many-locals,too-many-branches
    start_component, pg_id=None
):
    """
    Find all components and connections in a connected flow subgraph.

    Performs a breadth-first traversal of the connection graph to find the
    complete connected subgraph (the 'flow'). Useful for selecting an entire
    flow to move or analyze as a unit. The algorithm fetches all components
    in one API call, builds an adjacency map, then performs BFS from the
    start component to find all reachable nodes.

    Args:
        start_component: Any component entity (processor, funnel, port) to
            start the traversal from
        pg_id: Process group ID containing the flow. If None, inferred from
            start_component.component.parent_group_id

    Returns:
        FlowSubgraph named tuple with 'components' (list of component entities)
        and 'connections' (list of ConnectionEntity objects within the flow).

    Example::

        # Get the complete flow subgraph
        flow = nipyapi.canvas.get_flow_components(proc1)

        # Access components
        for c in flow.components:
            print(c.component.name)

        # Access connections (useful for transpose_flow)
        nipyapi.layout.transpose_flow(
            flow.components, offset=(400, 0), connections=flow.connections
        )
    """
    # Infer pg_id from component if not provided
    if pg_id is None:
        if hasattr(start_component, "component") and hasattr(
            start_component.component, "parent_group_id"
        ):
            pg_id = start_component.component.parent_group_id
        else:
            raise ValueError("Cannot infer pg_id from component. Please provide pg_id explicitly.")

    # Single API call to get all components and connections
    flow = get_flow(pg_id)
    fc = flow.process_group_flow.flow

    # Build lookup map: component_id -> component entity
    # This avoids fetching each component individually
    component_map = {}
    for p in fc.processors or []:
        component_map[p.id] = p
    for f in fc.funnels or []:
        component_map[f.id] = f
    for p in fc.input_ports or []:
        component_map[p.id] = p
    for p in fc.output_ports or []:
        component_map[p.id] = p

    # Build adjacency map from connections (bidirectional for graph walk)
    # adjacency[id] = set of connected component ids
    adjacency = {}
    for conn in fc.connections or []:
        src_id = conn.source_id
        dst_id = conn.destination_id
        # Initialize sets if needed
        if src_id not in adjacency:
            adjacency[src_id] = set()
        if dst_id not in adjacency:
            adjacency[dst_id] = set()
        # Bidirectional edges (we want the full connected subgraph)
        adjacency[src_id].add(dst_id)
        adjacency[dst_id].add(src_id)

    # BFS traversal from start component
    start_id = start_component.id
    visited = set()
    queue = [start_id]

    while queue:
        current_id = queue.pop(0)
        if current_id in visited:
            continue
        visited.add(current_id)
        # Add all connected neighbors to queue
        for neighbor_id in adjacency.get(current_id, []):
            if neighbor_id not in visited:
                queue.append(neighbor_id)

    # Build result: components and connections within the flow
    result_components = [component_map[cid] for cid in visited if cid in component_map]

    # Filter connections to those where at least one endpoint is in the flow
    # This includes internal connections and connections to/from the flow boundary
    flow_connections = [
        conn
        for conn in fc.connections or []
        if conn.source_id in visited or conn.destination_id in visited
    ]

    return FlowSubgraph(components=result_components, connections=flow_connections)


def purge_connection(con_id):
    """
    EXPERIMENTAL
    Drops all FlowFiles in a given connection. Waits until the action is
    complete before returning.

    Note that if upstream component isn't stopped, more data may flow into
    the connection after this action.

    Args:
        con_id (str): The UUID of the Connection to be purged

    Returns:
        :class:`~nipyapi.nifi.models.DropRequestEntity`: The status reporting object for the drop
        request.

    """

    def _autumn_leaves(con_id_, drop_request_):
        test_obj = (
            nipyapi.nifi.FlowFileQueuesApi()
            .get_drop_request(con_id_, drop_request_.drop_request.id)
            .drop_request
        )
        if not test_obj.finished:
            return False
        if test_obj.failure_reason:
            raise ValueError(
                "Unable to complete drop request{0}, error was {1}".format(
                    test_obj, test_obj.drop_request.failure_reason
                )
            )
        return True

    with nipyapi.utils.rest_exceptions():
        drop_req = nipyapi.nifi.FlowFileQueuesApi().create_drop_request(con_id)
    assert isinstance(drop_req, nipyapi.nifi.DropRequestEntity)
    return nipyapi.utils.wait_to_complete(_autumn_leaves, con_id, drop_req)


def list_flowfiles(connection, limit=100):
    """
    List FlowFiles waiting in a connection's queue.

    This is a non-destructive operation - FlowFiles remain in the queue.
    Returns basic metadata for each FlowFile; use get_flowfile() to retrieve
    full details including attributes.

    Args:
        connection: Connection ID (str) or ConnectionEntity
        limit: Maximum number of FlowFiles to return (default 100)

    Returns:
        list[:class:`~nipyapi.nifi.models.FlowFileSummaryDTO`]: List of FlowFile
            summaries with uuid, filename, size, queued_duration, etc.
            Returns empty list if queue is empty.

    Example::

        # List FlowFiles in a connection
        conn = nipyapi.canvas.get_connection(connection_id)
        flowfiles = nipyapi.canvas.list_flowfiles(conn)
        for ff in flowfiles:
            print(f"{ff.uuid}: {ff.filename} ({ff.size} bytes, queued {ff.queued_duration}ms)")

        # Get first FlowFile's full details
        if flowfiles:
            details = nipyapi.canvas.get_flowfile(conn, flowfiles[0].uuid)
            print(details.attributes)

    """
    if isinstance(connection, nipyapi.nifi.ConnectionEntity):
        con_id = connection.id
    elif isinstance(connection, str):
        con_id = connection
    else:
        raise ValueError(
            f"connection must be ConnectionEntity or str, got: {type(connection).__name__}"
        )

    def _listing_complete(con_id_, listing_req_):
        test_obj = nipyapi.nifi.FlowFileQueuesApi().get_listing_request(
            con_id_, listing_req_.listing_request.id
        )
        if not test_obj.listing_request.finished:
            return False
        if test_obj.listing_request.failure_reason:
            raise ValueError(
                f"Unable to complete listing request, error: "
                f"{test_obj.listing_request.failure_reason}"
            )
        return test_obj

    with nipyapi.utils.rest_exceptions():
        listing_req = nipyapi.nifi.FlowFileQueuesApi().create_flow_file_listing(con_id)
    assert isinstance(listing_req, nipyapi.nifi.ListingRequestEntity)

    # Wait for listing to complete and get results
    result = nipyapi.utils.wait_to_complete(_listing_complete, con_id, listing_req)

    # Clean up the listing request
    try:
        nipyapi.nifi.FlowFileQueuesApi().delete_listing_request(
            con_id, listing_req.listing_request.id
        )
    except Exception:  # pylint: disable=broad-except
        pass  # Best effort cleanup

    if result and result.listing_request.flow_file_summaries:
        return result.listing_request.flow_file_summaries[:limit]
    return []


def _resolve_flowfile_cluster_node(connection_id, flowfile_uuid, cluster_node_id=None):
    """
    Resolve cluster_node_id for a FlowFile, fetching from queue listing if not provided.

    In clustered NiFi, FlowFile operations require the cluster_node_id to identify
    which node holds the FlowFile. This helper fetches it from the queue listing
    if not explicitly provided.

    Args:
        connection_id: Connection ID string
        flowfile_uuid: UUID of the FlowFile
        cluster_node_id: Optional cluster node ID. If provided, returned as-is.

    Returns:
        str: The cluster_node_id for the FlowFile

    Raises:
        ValueError: If FlowFile not found in queue listing
    """
    if cluster_node_id:
        return cluster_node_id

    summaries = list_flowfiles(connection_id, limit=100)
    matching = [s for s in summaries if s.uuid == flowfile_uuid]
    if matching:
        return matching[0].cluster_node_id

    if summaries:
        raise ValueError(
            f"FlowFile {flowfile_uuid} not found in queue. It may have been processed."
        )
    # Empty queue - return None and let API handle it (may work in standalone NiFi)
    return None


def get_flowfile_details(connection, flowfile_uuid, cluster_node_id=None):
    """
    Get full details for a specific FlowFile, including its attributes.

    This is a non-destructive operation - the FlowFile remains in the queue.

    Args:
        connection: Connection ID (str) or ConnectionEntity
        flowfile_uuid: UUID of the FlowFile to retrieve
        cluster_node_id: Node ID for clustered NiFi. If not provided, will be
            auto-resolved from queue listing (adds one API call).

    Returns:
        :class:`~nipyapi.nifi.models.FlowFileDTO`: FlowFile details including
            attributes dict, filename, size, queued_duration, etc.

    Example::

        # Get FlowFile details
        details = nipyapi.canvas.get_flowfile_details(connection_id, flowfile_uuid)
        print(f"Filename: {details.filename}")
        print(f"Size: {details.size} bytes")
        print(f"Attributes: {details.attributes}")

        # In clustered NiFi, pass the cluster_node_id from listing
        flowfiles = nipyapi.canvas.list_flowfiles(connection_id)
        if flowfiles:
            details = nipyapi.canvas.get_flowfile_details(
                connection_id,
                flowfiles[0].uuid,
                cluster_node_id=flowfiles[0].cluster_node_id
            )

    """
    if isinstance(connection, nipyapi.nifi.ConnectionEntity):
        con_id = connection.id
    elif isinstance(connection, str):
        con_id = connection
    else:
        raise ValueError(
            f"connection must be ConnectionEntity or str, got: {type(connection).__name__}"
        )

    cluster_node_id = _resolve_flowfile_cluster_node(con_id, flowfile_uuid, cluster_node_id)

    with nipyapi.utils.rest_exceptions():
        result = nipyapi.nifi.FlowFileQueuesApi().get_flow_file(
            con_id, flowfile_uuid, cluster_node_id=cluster_node_id
        )
    return result.flow_file


def get_flowfile_content(
    connection, flowfile_uuid, decode="auto", output_file=None, cluster_node_id=None
):
    """
    Download the content of a specific FlowFile.

    This is a non-destructive operation - the FlowFile remains in the queue.

    Args:
        connection (str or ConnectionEntity): Connection ID or ConnectionEntity.
        flowfile_uuid (str): UUID of the FlowFile.
        decode (str): How to decode content: "auto" (mime-based), "text" (UTF-8),
            or "bytes" (raw).
        output_file (None or bool or str): None returns content directly, True saves
            to current dir with FlowFile's filename, str saves to that path/directory.
        cluster_node_id (str or None): Node ID for clustered NiFi. If not provided,
            will be auto-resolved from queue listing (adds one API call).

    Returns:
        If output_file is None: bytes or str (depending on decode)
        If output_file is set: str path where file was saved

    Example::

        # Get content as auto-detected type
        content = nipyapi.canvas.get_flowfile_content(connection_id, flowfile_uuid)

        # Force text decoding
        text = nipyapi.canvas.get_flowfile_content(conn, uuid, decode='text')

        # Save to file using FlowFile's filename
        path = nipyapi.canvas.get_flowfile_content(conn, uuid, output_file=True)
        print(f"Saved to: {path}")

        # Save to specific directory
        path = nipyapi.canvas.get_flowfile_content(conn, uuid, output_file='/tmp/')

        # In clustered NiFi, pass the cluster_node_id from listing
        flowfiles = nipyapi.canvas.list_flowfiles(connection_id)
        if flowfiles:
            content = nipyapi.canvas.get_flowfile_content(
                connection_id,
                flowfiles[0].uuid,
                cluster_node_id=flowfiles[0].cluster_node_id
            )

    """
    if isinstance(connection, nipyapi.nifi.ConnectionEntity):
        con_id = connection.id
    elif isinstance(connection, str):
        con_id = connection
    else:
        raise ValueError(
            f"connection must be ConnectionEntity or str, got: {type(connection).__name__}"
        )

    cluster_node_id = _resolve_flowfile_cluster_node(con_id, flowfile_uuid, cluster_node_id)

    # Get FlowFile details for filename and mime_type
    flowfile = get_flowfile_details(con_id, flowfile_uuid, cluster_node_id=cluster_node_id)

    # Download raw content
    with nipyapi.utils.rest_exceptions():
        response = nipyapi.nifi.FlowFileQueuesApi().download_flow_file_content(
            con_id, flowfile_uuid, cluster_node_id=cluster_node_id, _preload_content=False
        )
    content = response.data

    # Determine if content should be decoded as text
    mime_type = flowfile.mime_type or ""
    text_mime_types = (
        "text/",
        "application/json",
        "application/xml",
        "application/javascript",
        "application/csv",
    )
    is_text = any(mime_type.startswith(t) for t in text_mime_types)

    if decode == "text" or (decode == "auto" and is_text):
        try:
            content = content.decode("utf-8")
        except UnicodeDecodeError:
            # Fall back to bytes if decode fails
            pass

    # Handle output file
    if output_file is not None:
        # Get filename from FlowFile (sanitize to basename only)
        filename = os.path.basename(flowfile.filename) if flowfile.filename else flowfile_uuid

        if output_file is True:
            # Save to current directory
            file_path = filename
        elif os.path.isdir(output_file) or output_file.endswith(os.sep):
            # It's a directory - append filename
            file_path = os.path.join(output_file, filename)
        else:
            # It's an explicit file path
            file_path = output_file

        # Write content using utility function
        nipyapi.utils.fs_write(content, file_path, binary=isinstance(content, bytes))
        return os.path.abspath(file_path)

    return content


def peek_flowfiles(connection, limit=1):
    """
    Convenience function to list and get full details for FlowFiles at front of queue.

    Combines list_flowfiles() and get_flowfile() to return complete FlowFile
    details including attributes for the first N FlowFiles in the queue.

    Args:
        connection: Connection ID (str) or ConnectionEntity
        limit: Number of FlowFiles to retrieve details for (default 1)

    Returns:
        list[:class:`~nipyapi.nifi.models.FlowFileDTO`]: List of FlowFile details
            with full attributes. Returns empty list if queue is empty.

    Example::

        # Peek at the first FlowFile
        flowfiles = nipyapi.canvas.peek_flowfiles(connection_id)
        if flowfiles:
            ff = flowfiles[0]
            print(f"Filename: {ff.filename}")
            print(f"Attributes: {ff.attributes}")

        # Peek at first 5
        flowfiles = nipyapi.canvas.peek_flowfiles(connection_id, limit=5)

    """
    summaries = list_flowfiles(connection, limit=limit)
    if not summaries:
        return []

    # Normalize connection to ID for subsequent calls
    if isinstance(connection, nipyapi.nifi.ConnectionEntity):
        con_id = connection.id
    else:
        con_id = connection

    result = []
    for summary in summaries:
        flowfile = get_flowfile_details(
            con_id, summary.uuid, cluster_node_id=summary.cluster_node_id
        )
        # Preserve cluster_node_id from summary (FlowFileDTO returns None from API)
        flowfile.cluster_node_id = summary.cluster_node_id
        result.append(flowfile)
    return result


def purge_process_group(process_group, stop=False):
    """
    EXPERIMENTAL
    Purges the connections in a given Process Group of FlowFiles, and
    optionally stops it first

    Args:
        process_group (ProcessGroupEntity): Target Process Group
        stop (Optional [bool]): Whether to stop the Process Group before action

    Returns:
        (list[dict{ID:True|False}]): Result set. A list of Dicts of
    Connection IDs mapped to True or False for success of each connection

    """
    assert isinstance(process_group, nipyapi.nifi.ProcessGroupEntity)
    assert isinstance(stop, bool)
    if stop:
        if not schedule_process_group(process_group.id, False):
            raise ValueError(
                "Unable to stop Process Group {0} for purging".format(process_group.id)
            )
    cons = list_all_connections(process_group.id)
    result = []
    for con in cons:
        result.append({con.id: str(purge_connection(con.id))})
    return result


def get_bulletins():
    """
    Retrieves current bulletins (alerts) from the Flow Canvas.

    This is an alias for :func:`nipyapi.bulletins.get_bulletins`.

    Returns:
        (ControllerBulletinsEntity): The native datatype containing a list
            of bulletins
    """
    return nipyapi.bulletins.get_bulletins()


def get_bulletin_board(pg_id=None, source_name=None, message=None, limit=None):
    """
    Retrieves bulletins from the bulletin board with optional filtering.

    This is an alias for :func:`nipyapi.bulletins.get_bulletin_board`.

    Args:
        pg_id (str, optional): Filter to bulletins from this process group ID.
            If None, returns bulletins from all groups.
        source_name (str, optional): Filter by source component name (regex pattern).
        message (str, optional): Filter by message content (regex pattern).
        limit (int, optional): Maximum number of bulletins to return.

    Returns:
        list[BulletinDTO]: List of bulletin objects matching the filters.
            Returns empty list if no bulletins match.
    """
    return nipyapi.bulletins.get_bulletin_board(
        pg_id=pg_id, source_name=source_name, message=message, limit=limit
    )


def create_controller(parent_pg, controller, name=None):
    """
    Creates a new Controller Service in a given Process Group of the given Controller type, with the
    given Name.

    Args:
        parent_pg (:class:`~nipyapi.nifi.models.ProcessGroupEntity`): Target Parent PG
        controller (:class:`~nipyapi.nifi.models.DocumentedTypeDTO`): Type of Controller to create,
            found via the list_all_controller_types method
        name (str, optional): Name for the new Controller as a String

    Returns:
        :class:`~nipyapi.nifi.models.ControllerServiceEntity`: The created controller service

    """
    assert isinstance(controller, nipyapi.nifi.DocumentedTypeDTO)
    assert isinstance(parent_pg, nipyapi.nifi.ProcessGroupEntity)
    assert name is None or isinstance(name, str)
    with nipyapi.utils.rest_exceptions():
        # NiFi 2.x creates a PG-scoped Controller Service via ProcessGroupsApi
        out = nipyapi.nifi.ProcessGroupsApi().create_controller_service1(
            id=parent_pg.id,
            body=nipyapi.nifi.ControllerServiceEntity(
                revision={"version": 0},
                component=nipyapi.nifi.ControllerServiceDTO(
                    bundle=controller.bundle, type=controller.type
                ),
            ),
        )
        if name:
            update_controller(out, nipyapi.nifi.ControllerServiceDTO(name=name))
    return out


def list_all_controllers(pg_id="root", descendants=True, include_reporting_tasks=False):
    """
    Lists all controllers under a given Process Group, defaults to Root.
    Optionally recurses all child Process Groups as well.

    Args:
        pg_id (str): String of the ID of the Process Group to list from
        descendants (bool): True to recurse child PGs, False to not
        include_reporting_tasks (bool): True to include Reporting Tasks, False to not

    Returns:
        None, ControllerServiceEntity, or list(ControllerServiceEntity)

    """
    assert isinstance(pg_id, str)
    assert isinstance(descendants, bool)
    handle = nipyapi.nifi.FlowApi()
    # Testing shows that descendant doesn't work on NiFi-1.1.2
    # Or 1.2.0, despite the descendants option being available
    if nipyapi.utils.check_version("1.2.0") >= 0:
        # Case where NiFi <= 1.2.0
        out = []
        if descendants:
            pgs = list_all_process_groups(pg_id)
        else:
            pgs = [get_process_group(pg_id, "id")]
        for pg in pgs:
            new_conts = handle.get_controller_services_from_group(pg.id).controller_services
            # trim duplicates from inheritance
            out += [x for x in new_conts if x.id not in [y.id for y in out]]
    else:
        # Case where NiFi > 1.2.0
        # duplicate trim already handled by server
        out = handle.get_controller_services_from_group(
            pg_id, include_descendant_groups=descendants
        ).controller_services
    if include_reporting_tasks:
        mgmt_handle = nipyapi.nifi.FlowApi()
        out += mgmt_handle.get_controller_services_from_controller().controller_services
    return out


def delete_controller(controller, force=False, refresh=True):
    """
    Delete a Controller service, with optional prejudice

    Args:
        controller (ControllerServiceEntity or str): Target Controller to delete,
            either as a ControllerServiceEntity object or a controller ID string
        force (bool): True to attempt Disable the Controller before deletion
        refresh (bool): Whether to refresh the controller to get latest revision
            before deletion. Defaults to True to avoid stale revision errors.

    Returns:
        (ControllerServiceEntity)

    """
    assert isinstance(force, bool)

    # Accept ID string or object
    if isinstance(controller, str):
        controller_id = controller
        controller = get_controller(controller_id, "id")
        if controller is None:
            raise ValueError(f"Controller not found: {controller_id}")
    assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)

    def _del_cont(cont_id):
        if not get_controller(cont_id, "id", bool_response=True):
            return True
        return False

    handle = nipyapi.nifi.ControllerServicesApi()
    if force:
        # Stop and optionally refresh
        controller = schedule_controller(controller, False, refresh)
    elif refresh:
        # Just refresh to get latest revision
        controller = get_controller(controller.id, "id")
    with nipyapi.utils.rest_exceptions():
        result = handle.remove_controller_service(
            id=controller.id, version=controller.revision.version
        )
    del_test = nipyapi.utils.wait_to_complete(
        _del_cont,
        controller.id,
        nipyapi_max_wait=15,
        nipyapi_delay=nipyapi.config.short_retry_delay,
    )
    if not del_test:
        raise ValueError("Timed out waiting for Controller Deletion")
    return result


def update_controller(controller, update, refresh=True):
    """
    Updates the Configuration of a Controller Service

    Args:
        controller (ControllerServiceEntity or str): Target Controller to update,
            either as a ControllerServiceEntity object or a controller ID string
        update (ControllerServiceDTO): Controller Service configuration object
            containing the new config params and properties
        refresh (bool): Whether to refresh the controller to get latest revision
            before update. Defaults to True to avoid stale revision errors.

    Returns:
        (ControllerServiceEntity)

    """
    # Accept ID string or object
    if isinstance(controller, str):
        controller = get_controller(controller, "id")
        if controller is None:
            raise ValueError(f"Controller not found: {controller}")
    assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)
    assert isinstance(update, nipyapi.nifi.ControllerServiceDTO)

    if refresh:
        controller = get_controller(controller.id, "id")

    # Insert the ID into the update
    update.id = controller.id
    return nipyapi.nifi.ControllerServicesApi().update_controller_service(
        id=controller.id,
        body=nipyapi.nifi.ControllerServiceEntity(
            component=update, revision=controller.revision, id=controller.id
        ),
    )


def schedule_controller(controller, scheduled, refresh=False):
    """
    Start/Enable or Stop/Disable a Controller Service

    Args:
        controller (ControllerServiceEntity): Target Controller to schedule
        scheduled (bool): True to start, False to stop
        refresh (bool): Whether to refresh the component revision before
          execution

    Returns:
        (ControllerServiceEntity)

    """
    assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)
    assert isinstance(scheduled, bool)

    def _schedule_controller_state(cont_id, tgt_state):
        test_obj = get_controller(cont_id, "id")
        if test_obj.component.state == tgt_state:
            return True
        return False

    handle = nipyapi.nifi.ControllerServicesApi()
    target_state = "ENABLED" if scheduled else "DISABLED"
    if refresh:
        controller = nipyapi.canvas.get_controller(controller.id, "id")
        assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)
    # NiFi 2.x: update run status via ControllerServicesApi.update_run_status1
    result = handle.update_run_status1(
        id=controller.id,
        body=nipyapi.nifi.ControllerServiceRunStatusEntity(
            revision=controller.revision, state=target_state
        ),
    )
    if not result:
        raise ValueError("Scheduling request failed")
    state_test = nipyapi.utils.wait_to_complete(
        _schedule_controller_state,
        controller.id,
        target_state,
        nipyapi_delay=nipyapi.config.short_retry_delay,
        nipyapi_max_wait=15,
    )
    if state_test:
        return get_controller(controller.id, "id")
    raise ValueError("Scheduling request timed out")


def schedule_all_controllers(pg_id, scheduled):
    """
    Enable or Disable all Controller Services in a Process Group.

    Uses NiFi's native bulk controller service activation API which handles
    all descendant controller services automatically. Waits for all controllers
    to reach the target state before returning.

    Args:
        pg_id (str): The UUID of the Process Group
        scheduled (bool): True to enable, False to disable

    Returns:
        ActivateControllerServicesEntity: The result of the operation

    """
    assert isinstance(pg_id, str)
    assert isinstance(scheduled, bool)

    target_state = "ENABLED" if scheduled else "DISABLED"

    def _all_controllers_in_state():
        controllers = list_all_controllers(pg_id)
        if not controllers:
            return True  # No controllers to wait for
        return all(c.component.state == target_state for c in controllers)

    with nipyapi.utils.rest_exceptions():
        result = nipyapi.nifi.FlowApi().activate_controller_services(
            id=pg_id,
            body=nipyapi.nifi.ActivateControllerServicesEntity(id=pg_id, state=target_state),
        )

    # Wait for all controllers to reach target state
    state_complete = nipyapi.utils.wait_to_complete(
        _all_controllers_in_state,
        nipyapi_delay=nipyapi.config.short_retry_delay,
        nipyapi_max_wait=30,
    )
    if not state_complete:
        raise ValueError(f"Timed out waiting for controllers to reach state {target_state}")
    return result


def get_controller(
    identifier, identifier_type="name", bool_response=False, include_reporting_tasks=True
):
    """
    Retrieve a given Controller

    Args:
        identifier (str): ID or Name of a Controller to find
        identifier_type (str): 'id' or 'name', defaults to name
        bool_response (bool): If True, will return False if the Controller is
            not found - useful when testing for deletion completion
        include_reporting_tasks (bool): If True, will include Reporting Tasks in the search

    Returns:

    """
    assert isinstance(identifier, str)
    assert identifier_type in ["name", "id"]
    handle = nipyapi.nifi.ControllerServicesApi()
    out = None
    try:
        if identifier_type == "id":
            out = handle.get_controller_service(identifier)
        else:
            obj = list_all_controllers(include_reporting_tasks=include_reporting_tasks)
            out = nipyapi.utils.filter_obj(obj, identifier, identifier_type)
    except nipyapi.nifi.rest.ApiException as e:
        if bool_response:
            return False
        raise ValueError(e.body) from e
    return out


def list_all_controller_types():
    """
    Lists all Controller Service types available on the environment

    Returns:
        list(DocumentedTypeDTO)
    """
    handle = nipyapi.nifi.FlowApi()
    return handle.get_controller_service_types().controller_service_types


def get_controller_type(identifier, identifier_type="name", greedy=True):
    """
    Gets the abstract object describing a controller, or list thereof

    Args:
        identifier (str): the string to filter the list for
        identifier_type (str): the field to filter on, set in config.py
        greedy (bool): False for exact match, True for greedy match

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches

    """
    with nipyapi.utils.rest_exceptions():
        obj = list_all_controller_types()
    if obj:
        return nipyapi.utils.filter_obj(obj, identifier, identifier_type, greedy=greedy)
    return obj


def get_controller_service_docs(controller):
    """
    Get detailed documentation for a controller service type.

    This function retrieves the full ControllerServiceDefinition from NiFi,
    which contains comprehensive documentation useful for understanding
    controller service capabilities and configuration options.

    Args:
        controller (ControllerServiceEntity or DocumentedTypeDTO or str): An existing
            controller service, a type from get_controller_type(), or a type name
            string (e.g., "JsonTreeReader" or full qualified name).

    Returns:
        :class:`~nipyapi.nifi.models.ControllerServiceDefinition`: Controller
            documentation including property_descriptors, tags, and more.
        None: If controller type not found.

    Example::

        # From existing controller service
        cs = nipyapi.canvas.get_controller("MyJsonReader")
        docs = nipyapi.canvas.get_controller_service_docs(cs)
        print(docs.tags)
        print(docs.property_descriptors.keys())

        # From controller type
        cs_type = nipyapi.canvas.get_controller_type("JsonTreeReader")
        docs = nipyapi.canvas.get_controller_service_docs(cs_type)

        # From type name string
        docs = nipyapi.canvas.get_controller_service_docs("AvroReader")

    """
    # Extract bundle info based on input type
    if isinstance(controller, nipyapi.nifi.ControllerServiceEntity):
        bundle = controller.component.bundle
        cs_type = controller.component.type
    elif isinstance(controller, nipyapi.nifi.DocumentedTypeDTO):
        bundle = controller.bundle
        cs_type = controller.type
    elif isinstance(controller, str):
        # Look up controller type by name
        cs_type_obj = get_controller_type(controller, identifier_type="name", greedy=False)
        if cs_type_obj is None:
            # Try greedy match
            cs_type_obj = get_controller_type(controller, identifier_type="name", greedy=True)
        if cs_type_obj is None:
            return None
        if isinstance(cs_type_obj, list):
            cs_type_obj = cs_type_obj[0]  # Take first match
        bundle = cs_type_obj.bundle
        cs_type = cs_type_obj.type
    else:
        raise ValueError(
            f"controller must be ControllerServiceEntity, DocumentedTypeDTO, or str, "
            f"got: {type(controller).__name__}"
        )

    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.FlowApi().get_controller_service_definition(
            group=bundle.group,
            artifact=bundle.artifact,
            version=bundle.version,
            type=cs_type,
        )


def list_all_by_kind(kind, pg_id="root", descendants=True):
    """
    Retrieves a list of all instances of a supported object type

    Args:
        kind (str):  one of input_ports, output_ports, funnels, controllers,
            connections, remote_process_groups
        pg_id (str): optional, ID of the Process Group to use as search base
        descendants (bool): optional, whether to collect child group info

    Returns:
        list of the Entity type of the kind, or single instance, or None

    """
    assert kind in [
        "input_ports",
        "output_ports",
        "funnels",
        "controllers",
        "connections",
        "remote_process_groups",
    ]
    if kind == "controllers":
        return list_all_controllers(pg_id, descendants)
    handle = nipyapi.nifi.ProcessGroupsApi()
    call_function = getattr(handle, "get_" + kind)
    out = []
    if descendants:
        pgs = list_all_process_groups(pg_id)
    else:
        pgs = [get_process_group(pg_id, "id")]
    for pg in pgs:
        out += getattr(call_function(pg.id), kind)
    return out


def list_all_input_ports(pg_id="root", descendants=True):
    """Convenience wrapper for list_all_by_kind for input ports"""
    return list_all_by_kind("input_ports", pg_id, descendants)


def list_all_output_ports(pg_id="root", descendants=True):
    """Convenience wrapper for list_all_by_kind for output ports"""
    return list_all_by_kind("output_ports", pg_id, descendants)


def list_all_funnels(pg_id="root", descendants=True):
    """Convenience wrapper for list_all_by_kind for funnels"""
    return list_all_by_kind("funnels", pg_id, descendants)


def list_all_remote_process_groups(pg_id="root", descendants=True):
    """Convenience wrapper for list_all_by_kind for remote process groups"""
    return list_all_by_kind("remote_process_groups", pg_id, descendants)


def get_remote_process_group(rpg_id, summary=False):
    """
    Fetch a remote process group object, with optional summary of just ports
    """
    rpg = nipyapi.nifi.RemoteProcessGroupsApi().get_remote_process_group(rpg_id)
    if not summary:
        out = rpg
    else:
        out = {
            "id": rpg.id,
            "input_ports": rpg.component.contents.input_ports,
            "output_ports": rpg.component.contents.output_ports,
        }
    return out


def create_remote_process_group(target_uris, transport="RAW", pg_id="root", position=None):
    """
    Creates a new Remote Process Group with given parameters

    Args:
        target_uris (str): Comma separated list of target URIs
        transport (str): optional, RAW or HTTP
        pg_id (str): optional, UUID of parent Process Group for remote
          process group
        position (tuple): optional, tuple of location ints

    Returns:
        (RemoteProcessGroupEntity)
    """
    assert isinstance(target_uris, str)
    assert transport in ["RAW", "HTTP"]
    assert isinstance(pg_id, str)
    pg_id = pg_id if not "root" else get_root_pg_id()
    position = position if position else (400, 400)
    assert isinstance(position, tuple)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_remote_process_group(
            id=pg_id,
            body=nipyapi.nifi.RemoteProcessGroupEntity(
                component=nipyapi.nifi.RemoteProcessGroupDTO(
                    position=nipyapi.nifi.PositionDTO(x=float(position[0]), y=float(position[1])),
                    target_uris=target_uris,
                    transport_protocol=transport,
                ),
                revision=nipyapi.nifi.RevisionDTO(version=0),
            ),
        )


def delete_remote_process_group(rpg, refresh=True, force=False):
    """
    Deletes a given remote process group.

    Args:
        rpg (RemoteProcessGroupEntity): Remote Process Group to remove
        refresh (bool): Whether to refresh the object before action
        force (bool): If True, stop transmission before deleting. Use this
            when the RPG may be transmitting and you want to ensure deletion.

    Returns:
        (RemoteProcessGroupEntity)
    """
    assert isinstance(rpg, nipyapi.nifi.RemoteProcessGroupEntity)
    if refresh or force:
        rpg = get_remote_process_group(rpg.id)
    if force and rpg.component.transmitting:
        set_remote_process_group_transmission(rpg, enable=False)
        rpg = get_remote_process_group(rpg.id)
    handle = nipyapi.nifi.RemoteProcessGroupsApi()
    with nipyapi.utils.rest_exceptions():
        return handle.remove_remote_process_group(id=rpg.id, version=rpg.revision.version)


def set_remote_process_group_transmission(rpg, enable=True, refresh=True):
    """
    Enable or Disable Transmission for an RPG.

    Waits for the transmission state to actually change before returning.

    Args:
        rpg (RemoteProcessGroupEntity): The remote process group to modify
        enable (bool): True to enable transmission, False to disable
        refresh (bool): Whether to refresh the object before action

    Returns:
        (RemoteProcessGroupEntity): The updated remote process group

    Raises:
        ValueError: If the state change times out
    """
    assert isinstance(rpg, nipyapi.nifi.RemoteProcessGroupEntity)
    assert isinstance(enable, bool)

    def _check_rpg_transmission_state(rpg_id, target_transmitting):
        """Check if RPG transmission state matches target."""
        test_obj = get_remote_process_group(rpg_id)
        if test_obj.component.transmitting == target_transmitting:
            return True
        return False

    if refresh:
        rpg = get_remote_process_group(rpg.id)
    handle = nipyapi.nifi.RemoteProcessGroupsApi()
    target_state = "TRANSMITTING" if enable else "STOPPED"

    with nipyapi.utils.rest_exceptions():
        handle.update_remote_process_group_run_status(
            id=rpg.id,
            body=nipyapi.nifi.RemotePortRunStatusEntity(state=target_state, revision=rpg.revision),
        )

    # Wait for the state to actually change
    state_test = nipyapi.utils.wait_to_complete(
        _check_rpg_transmission_state,
        rpg.id,
        enable,
        nipyapi_delay=nipyapi.config.long_retry_delay,
        nipyapi_max_wait=nipyapi.config.long_max_wait,
    )
    if state_test:
        return get_remote_process_group(rpg.id)
    raise ValueError(
        f"Timed out waiting for RPG {rpg.id} transmission to " f"{'start' if enable else 'stop'}"
    )


def create_port(pg_id, port_type, name, state, position=None):
    """
    Creates a new input or output port of given characteristics

    Args:
        pg_id (str): ID of the parent Process Group
        port_type (str): Either of INPUT_PORT or OUTPUT_PORT
        name (str): optional, Name to assign to the port
        state (str): One of RUNNING, STOPPED, DISABLED
        position (tuple): optional, tuple of ints like (400, 400)

    Returns:
        (PortEntity) of the created port

    """
    assert state in ["RUNNING", "STOPPED", "DISABLED"]
    assert port_type in ["INPUT_PORT", "OUTPUT_PORT"]
    assert isinstance(pg_id, str)
    position = position if position else (400, 400)
    assert isinstance(position, tuple)
    handle = nipyapi.nifi.ProcessGroupsApi()
    port_generator = getattr(handle, "create_" + port_type.lower())
    with nipyapi.utils.rest_exceptions():
        return port_generator(
            id=pg_id,
            body=nipyapi.nifi.PortEntity(
                revision=nipyapi.nifi.RevisionDTO(version=0),
                component=nipyapi.nifi.PortDTO(
                    parent_group_id=pg_id,
                    position=nipyapi.nifi.PositionDTO(x=float(position[0]), y=float(position[1])),
                    name=name,
                ),
            ),
        )


def delete_port(port):
    """Deletes a given port from the canvas if possible"""
    assert isinstance(port, nipyapi.nifi.PortEntity)
    if "INPUT" in port.port_type:
        with nipyapi.utils.rest_exceptions():
            return nipyapi.nifi.InputPortsApi().remove_input_port(
                id=port.id, version=port.revision.version
            )
    if "OUTPUT" in port.port_type:
        with nipyapi.utils.rest_exceptions():
            return nipyapi.nifi.OutputPortsApi().remove_output_port(
                id=port.id, version=port.revision.version
            )


def get_funnel(funnel_id):
    """Gets a given Funnel by ID"""
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.FunnelsApi().get_funnel(funnel_id)


def create_funnel(pg_id, position=None):
    """
    Creates a Funnel Object

    Args:
        pg_id (str): ID of the parent Process Group
        position (tuple[int, int]): Position on canvas

    Returns:
        :class:`~nipyapi.nifi.models.FunnelEntity`: Created Funnel
    """
    position = position if position else (400, 400)
    assert isinstance(position, tuple)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_funnel(
            id=pg_id,
            body=nipyapi.nifi.FunnelEntity(
                revision=nipyapi.nifi.RevisionDTO(version=0),
                component=nipyapi.nifi.FunnelDTO(
                    parent_group_id=pg_id,
                    position=nipyapi.nifi.PositionDTO(x=float(position[0]), y=float(position[1])),
                ),
            ),
        )


def delete_funnel(funnel, refresh=True):
    """
    Deletes a Funnel Object

    Args:
        funnel (FunnelEntity): The Funnel to delete
        refresh (bool): Whether to refresh the object state
            before execution

    Returns:
        :class:`~nipyapi.nifi.models.FunnelEntity`: Deleted FunnelEntity reference
    """
    assert isinstance(funnel, nipyapi.nifi.FunnelEntity)
    with nipyapi.utils.rest_exceptions():
        if refresh:
            funnel = get_funnel(funnel.id)
        return nipyapi.nifi.FunnelsApi().remove_funnel(
            id=funnel.id, version=funnel.revision.version
        )


def get_pg_parents_ids(pg_id):
    """
    Retrieve the ids of the parent Process Groups.

    Args:
        pg_id (str): Process group id

    Returns:
        (list) List of ids of the input PG parents
    """
    parent_groups = []
    while pg_id:
        pg_id = nipyapi.canvas.get_process_group(pg_id, "id").component.parent_group_id
        parent_groups.append(pg_id)
    # Removing the None value
    parent_groups.pop()
    return parent_groups


def verify_controller(controller, properties=None, attributes=None):
    """
    Verify a controller service's configuration properties are valid.

    Validates that all required properties are set and property values meet
    their defined constraints. Does NOT test actual connectivity or credentials.
    Handles the async verification workflow: submit request, poll until
    complete, cleanup.

    The controller service must be DISABLED before verification.

    Args:
        controller: ControllerServiceEntity or controller service ID (str)
        properties: Optional dict of property overrides to verify
        attributes: Optional dict of FlowFile attributes for Expression Language

    Returns:
        list[ConfigVerificationResultDTO]: Verification results. Each has
        verification_step_name, outcome ("SUCCESSFUL"/"FAILED"/"SKIPPED"),
        and explanation.

    Raises:
        ValueError: Controller not found or is currently enabled
        ApiException: NiFi API errors

    Example::

        results = nipyapi.canvas.verify_controller(dbcp_service)
        for r in results:
            print(f"{r.verification_step_name}: {r.outcome}")
            if r.outcome == "FAILED":
                print(f"  Reason: {r.explanation}")
    """
    # Accept ID or entity
    if isinstance(controller, str):
        controller = get_controller(controller, "id")

    if controller is None:
        raise ValueError("Controller service not found")

    assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)

    # Verify controller is disabled
    if controller.component.state != "DISABLED":
        raise ValueError(
            f"Controller service must be DISABLED before verification. "
            f"Current state: {controller.component.state}"
        )

    # Build verification request
    body = nipyapi.nifi.VerifyConfigRequestEntity(
        request=nipyapi.nifi.VerifyConfigRequestDTO(
            component_id=controller.id,
            properties=properties or {},
            attributes=attributes or {},
        )
    )

    api = nipyapi.nifi.ControllerServicesApi()
    request_id = None

    try:
        # Submit verification request
        with nipyapi.utils.rest_exceptions():
            response = api.submit_config_verification_request(body=body, id=controller.id)
        request_id = response.request.request_id

        # Poll until complete using wait_to_complete pattern
        def _check_complete():
            status = api.get_verification_request(id=controller.id, request_id=request_id)
            if status.request.complete:
                return status
            return False

        status = nipyapi.utils.wait_to_complete(_check_complete)
        return status.request.results or []

    finally:
        # Always cleanup the verification request
        if request_id:
            try:
                api.delete_verification_request(id=controller.id, request_id=request_id)
            except Exception:  # pylint: disable=broad-except
                log.warning("Failed to cleanup verification request %s", request_id)


def verify_processor(processor, properties=None, attributes=None):
    """
    Verify a processor's configuration properties are valid.

    Validates that all required properties are set and property values meet
    their defined constraints. Does NOT test actual connectivity or external
    service availability. Handles the async verification workflow: submit
    request, poll until complete, cleanup.

    The processor must be STOPPED before verification.

    Args:
        processor: ProcessorEntity or processor ID (str)
        properties: Optional dict of property overrides to verify
        attributes: Optional dict of FlowFile attributes for Expression Language

    Returns:
        list[ConfigVerificationResultDTO]: Verification results. Each has
        verification_step_name, outcome ("SUCCESSFUL"/"FAILED"/"SKIPPED"),
        and explanation.

    Raises:
        ValueError: Processor not found or is currently running
        ApiException: NiFi API errors

    Example::

        results = nipyapi.canvas.verify_processor(my_processor)
        for r in results:
            print(f"{r.verification_step_name}: {r.outcome}")
            if r.outcome == "FAILED":
                print(f"  Reason: {r.explanation}")
    """
    # Accept ID or entity
    if isinstance(processor, str):
        processor = get_processor(processor, "id")

    if processor is None:
        raise ValueError("Processor not found")

    assert isinstance(processor, nipyapi.nifi.ProcessorEntity)

    # Verify processor is stopped
    run_status = processor.status.run_status if processor.status else None
    if run_status and run_status.upper() in ("RUNNING", "VALIDATING"):
        raise ValueError(
            f"Processor must be STOPPED before verification. " f"Current state: {run_status}"
        )

    # Build verification request
    body = nipyapi.nifi.VerifyConfigRequestEntity(
        request=nipyapi.nifi.VerifyConfigRequestDTO(
            component_id=processor.id,
            properties=properties or {},
            attributes=attributes or {},
        )
    )

    api = nipyapi.nifi.ProcessorsApi()
    request_id = None

    try:
        # Submit verification request
        with nipyapi.utils.rest_exceptions():
            response = api.submit_processor_verification_request(body=body, id=processor.id)
        request_id = response.request.request_id

        # Poll until complete
        def _check_complete():
            status = api.get_verification_request2(id=processor.id, request_id=request_id)
            if status.request.complete:
                return status
            return False

        status = nipyapi.utils.wait_to_complete(_check_complete)
        return status.request.results or []

    finally:
        # Always cleanup the verification request
        if request_id:
            try:
                api.delete_verification_request2(id=processor.id, request_id=request_id)
            except Exception:  # pylint: disable=broad-except
                log.warning("Failed to cleanup verification request %s", request_id)


def get_controller_state(controller):
    """
    Get the state for a controller service.

    Controller services can maintain internal state (e.g., cache entries,
    connection tracking, CDC table status). This function retrieves that state.

    Args:
        controller: ControllerServiceEntity or controller service ID (str)

    Returns:
        ComponentStateEntity with component_state containing component_id,
        state_description, local_state (single node), and cluster_state
        (distributed). Check whichever state map has entries. Each state
        map has scope, total_entry_count, and state (list of StateEntryDTO).

    Raises:
        ValueError: Controller not found
        ApiException: NiFi API errors

    Example::

        state = nipyapi.canvas.get_controller_state(my_controller)
        state_map = state.component_state.local_state
        if state_map and state_map.state:
            for entry in state_map.state:
                print(f"{entry.key}: {entry.value}")
    """
    # Accept ID or entity
    if isinstance(controller, str):
        controller_id = controller
    else:
        assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)
        controller_id = controller.id

    handle = nipyapi.nifi.ControllerServicesApi()
    with nipyapi.utils.rest_exceptions():
        return handle.get_state(controller_id)


def clear_controller_state(controller):
    """
    Clear all state for a controller service.

    This removes all state entries from the controller service. Use with caution
    as this may affect the controller's behavior (e.g., clearing a CDC table
    state service will cause tables to be re-snapshotted).

    Note: The controller must be DISABLED before clearing state. Attempting to
    clear state on an enabled controller will raise an error.

    Args:
        controller: ControllerServiceEntity or controller service ID (str)

    Returns:
        ComponentStateEntity: The cleared state entity (should have 0 entries)

    Raises:
        ValueError: Controller not found or controller is enabled
        ApiException: NiFi API errors

    Example::

        # Disable controller first
        nipyapi.canvas.schedule_controller(my_controller, scheduled=False)

        # Clear all state
        nipyapi.canvas.clear_controller_state(my_controller)

        # Verify cleared
        state = nipyapi.canvas.get_controller_state(my_controller)
        assert state.component_state.local_state.total_entry_count == 0
    """
    # Accept ID or entity
    if isinstance(controller, str):
        controller_id = controller
    else:
        assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)
        controller_id = controller.id

    handle = nipyapi.nifi.ControllerServicesApi()
    with nipyapi.utils.rest_exceptions():
        return handle.clear_state1(controller_id)


def get_processor_state(processor):
    """
    Get the state for a processor.

    Processors can maintain internal state (e.g., ListFile tracks listed files,
    TailFile tracks file positions). This function retrieves that state.

    Args:
        processor: ProcessorEntity or processor ID (str)

    Returns:
        ComponentStateEntity with component_state containing component_id,
        state_description, local_state (single node), and cluster_state
        (distributed). Check whichever state map has entries. Each state
        map has scope, total_entry_count, and state (list of StateEntryDTO).

    Raises:
        ValueError: Processor not found
        ApiException: NiFi API errors

    Example::

        state = nipyapi.canvas.get_processor_state(my_list_file_processor)
        state_map = state.component_state.local_state
        if state_map and state_map.state:
            for entry in state_map.state:
                print(f"{entry.key}: {entry.value}")
    """
    # Accept ID or entity
    if isinstance(processor, str):
        processor_id = processor
    else:
        assert isinstance(processor, nipyapi.nifi.ProcessorEntity)
        processor_id = processor.id

    handle = nipyapi.nifi.ProcessorsApi()
    with nipyapi.utils.rest_exceptions():
        return handle.get_state2(processor_id)


def clear_processor_state(processor):
    """
    Clear all state for a processor.

    This removes all state entries from the processor. Use with caution as this
    may affect the processor's behavior (e.g., clearing ListFile state will
    cause all files to be re-listed).

    Args:
        processor: ProcessorEntity or processor ID (str)

    Returns:
        ComponentStateEntity: The cleared state entity (should have 0 entries)

    Raises:
        ValueError: Processor not found
        ApiException: NiFi API errors

    Example::

        # Clear all state
        nipyapi.canvas.clear_processor_state(my_processor)

        # Verify cleared
        state = nipyapi.canvas.get_processor_state(my_processor)
        assert state.component_state.local_state.total_entry_count == 0
    """
    # Accept ID or entity
    if isinstance(processor, str):
        processor_id = processor
    else:
        assert isinstance(processor, nipyapi.nifi.ProcessorEntity)
        processor_id = processor.id

    handle = nipyapi.nifi.ProcessorsApi()
    with nipyapi.utils.rest_exceptions():
        return handle.clear_state3(processor_id)
