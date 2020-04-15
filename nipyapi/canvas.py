# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas.
"""

from __future__ import absolute_import
import logging
import six
import nipyapi

__all__ = [
    "get_root_pg_id", "recurse_flow", "get_flow", "get_process_group_status",
    "get_process_group", "list_all_process_groups", "delete_process_group",
    "schedule_process_group", "create_process_group", "list_all_processors",
    "list_all_processor_types", "get_processor_type", 'create_processor',
    'delete_processor', 'get_processor', 'schedule_processor', 'get_funnel',
    'update_processor', 'get_variable_registry', 'update_variable_registry',
    'purge_connection', 'purge_process_group', 'schedule_components',
    'get_bulletins', 'get_bulletin_board', 'list_invalid_processors',
    'list_sensitive_processors', 'list_all_connections', 'create_connection',
    'delete_connection', 'get_component_connections', 'create_controller',
    'list_all_controllers', 'delete_controller', 'update_controller',
    'schedule_controller', 'get_controller', 'list_all_controller_types',
    'list_all_by_kind', 'list_all_input_ports', 'list_all_output_ports',
    'list_all_funnels', 'list_all_remote_process_groups', 'delete_funnel',
    'get_remote_process_group', 'update_process_group', 'create_funnel',
    'create_remote_process_group', 'delete_remote_process_group',
    'set_remote_process_group_transmission', 'get_pg_parents_ids'
]

log = logging.getLogger(__name__)


def get_root_pg_id():
    """
    Convenience function to return the UUID of the Root Process Group

    Returns (str): The UUID of the root PG
    """
    return nipyapi.nifi.FlowApi().get_process_group_status('root') \
        .process_group_status.id


def recurse_flow(pg_id='root'):
    """
    Returns information about a Process Group and all its Child Flows.
    Recurses the child flows by appending each process group with a
    'nipyapi_extended' parameter which contains the child process groups, etc.
    Note: This previously used actual recursion which broke on large NiFi
        environments, we now use a task/list update approach

    Args:
        pg_id (str): The Process Group UUID

    Returns:
         (ProcessGroupFlowEntity): enriched NiFi Flow object
    """
    assert isinstance(pg_id, six.string_types), "pg_id should be a string"

    out = get_flow(pg_id)
    tasks = [(x.id, x) for x in out.process_group_flow.flow.process_groups]
    while tasks:
        this_pg_id, this_parent_obj = tasks.pop()
        this_flow = get_flow(this_pg_id)
        this_parent_obj.__setattr__(
            'nipyapi_extended',
            this_flow
        )
        tasks += [(x.id, x) for x in
                  this_flow.process_group_flow.flow.process_groups]
    return out


def get_flow(pg_id='root'):
    """
    Returns information about a Process Group and flow.

    This surfaces the native implementation, for the recursed implementation
    see 'recurse_flow'

    Args:
        pg_id (str): id of the Process Group to retrieve, defaults to the root
            process group if not set

    Returns:
         (ProcessGroupFlowEntity): The Process Group object
    """
    assert isinstance(pg_id, six.string_types), "pg_id should be a string"
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.FlowApi().get_flow(pg_id)


def get_process_group_status(pg_id='root', detail='names'):
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
         (ProcessGroupEntity): The Process Group Entity including the status
    """
    assert isinstance(pg_id, six.string_types), "pg_id should be a string"
    assert detail in ['names', 'all']
    raw = nipyapi.nifi.ProcessGroupsApi().get_process_group(id=pg_id)
    if detail == 'names':
        out = {
            raw.component.name: raw.component.id
        }
        return out
    return raw


def get_process_group(identifier, identifier_type='name', greedy=True):
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
    assert isinstance(identifier, six.string_types)
    assert identifier_type in ['name', 'id']
    with nipyapi.utils.rest_exceptions():
        if identifier_type == 'id' or identifier == 'root':
            # assuming unique fetch of pg id, 'root' is special case
            # implementing separately to avoid recursing entire canvas
            out = nipyapi.nifi.ProcessGroupsApi().get_process_group(identifier)
        else:
            obj = list_all_process_groups()
            out = nipyapi.utils.filter_obj(
                obj, identifier, identifier_type, greedy=greedy)
    return out


def list_all_process_groups(pg_id='root'):
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
    assert isinstance(pg_id, six.string_types), "pg_id should be a string"

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
            for sub in flatten(child_pg.nipyapi_extended):
                yield sub
            yield child_pg

    # Recurse children
    root_flow = recurse_flow(pg_id)
    # Flatten list of children with extended detail
    out = list(flatten(root_flow))
    # update parent with flattened list of extended child detail
    root_entity = get_process_group(pg_id, 'id')
    root_entity.__setattr__('nipyapi_extended', root_flow)
    out.append(root_entity)
    return out
    #
    # if pg_id == 'root' or pg_id == get_root_pg_id():
    #     # This duplicates the nipyapi_extended structure to the root case
    #     root_entity = get_process_group('root', 'id')
    #     root_entity.__setattr__('nipyapi_extended', root_flow)
    #     out.append(root_entity)
    # return out


def list_invalid_processors(pg_id='root', summary=False):
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
    assert isinstance(pg_id, six.string_types), "pg_id should be a string"
    assert isinstance(summary, bool)
    proc_list = [x for x in list_all_processors(pg_id)
                 if x.component.validation_errors]
    if summary:
        out = [{'id': x.id, 'summary': x.component.validation_errors}
               for x in proc_list]
    else:
        out = proc_list
    return out


def list_sensitive_processors(pg_id='root', summary=False):
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
    assert isinstance(pg_id, six.string_types), "pg_id should be a string"
    assert isinstance(summary, bool)
    cache = nipyapi.config.cache.get('list_sensitive_processors')
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
        nipyapi.config.cache['list_sensitive_processors'] = cache
    if summary:
        return [
            {x.id: [
                p for p, q in x.component.config.descriptors.items()
                if q.sensitive is True]}
            for x in matches
        ]
    return matches


def list_all_processors(pg_id='root'):
    """
    Returns a flat list of all Processors under the provided Process Group

    Args:
        pg_id (str): The UUID of the Process Group to start from, defaults to
            the Canvas root

    Returns:
         list[ProcessorEntity]
    """
    assert isinstance(pg_id, six.string_types), "pg_id should be a string"

    if nipyapi.utils.check_version('1.7.0') <= 0:
        # Case where NiFi > 1.7.0
        targets = nipyapi.nifi.ProcessGroupsApi().get_processors(
            id=pg_id,
            include_descendant_groups=True
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
    assert isinstance(process_group_id, six.string_types)
    assert isinstance(scheduled, bool)

    def _running_schedule_process_group(pg_id_):
        test_obj = nipyapi.nifi.ProcessGroupsApi().get_process_group(pg_id_)
        if test_obj.status.aggregate_snapshot.active_thread_count == 0:
            return True
        return False

    assert isinstance(
        get_process_group(process_group_id, 'id'),
        nipyapi.nifi.ProcessGroupEntity
    )
    result = schedule_components(
        pg_id=process_group_id,
        scheduled=scheduled
    )
    # If target scheduled state was successfully updated
    if result:
        # If we want to stop the processor
        if not scheduled:
            # Test that the processor threads have halted
            stop_test = nipyapi.utils.wait_to_complete(
                _running_schedule_process_group,
                process_group_id
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
            id=target.id,
            version=target.revision.version,
            client_id=target.revision.client_id
        )
    except nipyapi.nifi.rest.ApiException as e:
        if force:
            # Retrieve parent process group
            parent_pg_id = nipyapi.canvas.get_process_group(pg_id, 'id')\
                .component.parent_group_id
            # Stop, drop, and roll.
            purge_process_group(target, stop=True)
            # Remove inbound connections
            for con in list_all_connections(parent_pg_id):
                if pg_id in [con.destination_group_id, con.source_group_id]:
                    delete_connection(con)
            # Stop all Controller Services ONLY inside the PG
            controllers_list = list_all_controllers(pg_id)
            removed_controllers_id = []
            parent_pgs_id = get_pg_parents_ids(pg_id)
            for x in controllers_list:
                if x.component.id not in removed_controllers_id:
                    if x.component.parent_group_id not in parent_pgs_id:
                        delete_controller(x, True)
                        removed_controllers_id.append(x.component.id)

            # Remove templates
            for template in nipyapi.templates.list_all_templates(native=False):
                if target.id == template.template.group_id:
                    nipyapi.templates.delete_template(template.id)
            # have to refresh revision after changes
            target = nipyapi.nifi.ProcessGroupsApi().get_process_group(pg_id)
            return nipyapi.nifi.ProcessGroupsApi().remove_process_group(
                id=target.id,
                version=target.revision.version,
                client_id=target.revision.client_id
            )
        raise ValueError(e.body)


def create_process_group(parent_pg, new_pg_name, location, comment=''):
    """
    Creates a new Process Group with the given name under the provided parent
    Process Group at the given Location

    Args:
        parent_pg (ProcessGroupEntity): The parent Process Group to create the
            new process group in
        new_pg_name (str): The name of the new Process Group
        location (tuple[x, y]): the x,y coordinates to place the new Process
            Group under the parent
        comment (str): Entry for the Comments field

    Returns:
         (ProcessGroupEntity): The new Process Group

    """
    assert isinstance(parent_pg, nipyapi.nifi.ProcessGroupEntity)
    assert isinstance(new_pg_name, six.string_types)
    assert isinstance(location, tuple)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_process_group(
            id=parent_pg.id,
            body=nipyapi.nifi.ProcessGroupEntity(
                revision={'version': 0},
                component=nipyapi.nifi.ProcessGroupDTO(
                    name=new_pg_name,
                    position=nipyapi.nifi.PositionDTO(
                        x=float(location[0]),
                        y=float(location[1])
                    ),
                    comments=comment
                )
            )
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


def get_processor_type(identifier, identifier_type='name'):
    """
    Gets the abstract object describing a Processor, or list thereof

    Args:
        identifier (str): the string to filter the list for
        identifier_type (str): the field to filter on, set in config.py

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches

    """
    with nipyapi.utils.rest_exceptions():
        obj = list_all_processor_types().processor_types
    if obj:
        return nipyapi.utils.filter_obj(obj, identifier, identifier_type)
    return obj


def create_processor(parent_pg, processor, location, name=None, config=None):
    """
    Instantiates a given processor on the canvas

    Args:
        parent_pg (ProcessGroupEntity): The parent Process Group
        processor (DocumentedTypeDTO): The abstract processor type object to be
            instantiated
        location (tuple[x, y]): The location coordinates
        name (Optional [str]):  The name for the new Processor
        config (Optional [ProcessorConfigDTO]): A configuration object for the
            new processor

    Returns:
         (ProcessorEntity): The new Processor

    """
    if name is None:
        processor_name = processor.type.split('.')[-1]
    else:
        processor_name = name
    if config is None:
        target_config = nipyapi.nifi.ProcessorConfigDTO()
    else:
        target_config = config
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_processor(
            id=parent_pg.id,
            body=nipyapi.nifi.ProcessorEntity(
                revision={'version': 0},
                component=nipyapi.nifi.ProcessorDTO(
                    position=nipyapi.nifi.PositionDTO(
                        x=float(location[0]),
                        y=float(location[1])
                    ),
                    type=processor.type,
                    name=processor_name,
                    config=target_config
                )
            )
        )


def get_processor(identifier, identifier_type='name', greedy=True):
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
    assert isinstance(identifier, six.string_types)
    assert identifier_type in ['name', 'id']
    with nipyapi.utils.rest_exceptions():
        if identifier_type == 'id':
            out = nipyapi.nifi.ProcessorsApi().get_processor(identifier)
        else:
            obj = list_all_processors()
            out = nipyapi.utils.filter_obj(
                obj, identifier, identifier_type, greedy=greedy
            )
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
         (ProcessorEntity): The updated ProcessorEntity

    """
    assert isinstance(processor, nipyapi.nifi.ProcessorEntity)
    assert isinstance(refresh, bool)
    assert isinstance(force, bool)
    if refresh or force:
        target = get_processor(processor.id, 'id')
        assert isinstance(target, nipyapi.nifi.ProcessorEntity)
    else:
        target = processor
    if force:
        if not schedule_processor(target, False):
            raise ("Could not prepare processor {0} for deletion"
                   .format(target.id))
        inbound_cons = [
            x for x in get_component_connections(processor)
            if processor.id == x.destination_id
        ]
        for con in inbound_cons:
            delete_connection(con, purge=True)
        # refresh state before trying delete
        target = get_processor(processor.id, 'id')
        assert isinstance(target, nipyapi.nifi.ProcessorEntity)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessorsApi().delete_processor(
            id=target.id,
            version=target.revision.version
        )


def schedule_components(pg_id, scheduled, components=None):
    """
    Changes the scheduled target state of a list of components within a given
    Process Group.

    Note that this does not guarantee that components will be Started or
    Stopped afterwards, merely that they will have their scheduling updated.

    Args:
        pg_id (str): The UUID of the parent Process Group
        scheduled (bool): True to start, False to stop
        components (list[ComponentType]): The list of Component Entities to
            schdule, e.g. ProcessorEntity's

    Returns:
         (bool): True for success, False for not

    """
    assert isinstance(
        get_process_group(pg_id, 'id'),
        nipyapi.nifi.ProcessGroupEntity
    )
    assert isinstance(scheduled, bool)
    assert components is None or isinstance(components, list)
    target_state = 'RUNNING' if scheduled else 'STOPPED'
    body = nipyapi.nifi.ScheduleComponentsEntity(
        id=pg_id,
        state=target_state
    )
    if components:
        body.components = {i.id: i.revision for i in components}
    with nipyapi.utils.rest_exceptions():
        result = nipyapi.nifi.FlowApi().schedule_components(
            id=pg_id,
            body=body
        )
    if result.state == target_state:
        return True
    return False


def schedule_processor(processor, scheduled, refresh=True):
    """
    Set a Processor to Start or Stop.

    Note that this doesn't guarantee that it will change state, merely that
    it will be instructed to try.
    Some effort is made to wait and see if the processor starts

    Args:
        processor (ProcessorEntity): The Processor to target
        scheduled (bool): True to start, False to stop
        refresh (bool): Whether to refresh the object before action

    Returns:
        (bool): True for success, False for failure

    """
    assert isinstance(processor, nipyapi.nifi.ProcessorEntity)
    assert isinstance(scheduled, bool)
    assert isinstance(refresh, bool)

    def _running_schedule_processor(processor_):
        test_obj = nipyapi.canvas.get_processor(processor_.id, 'id')
        if test_obj.status.aggregate_snapshot.active_thread_count == 0:
            return True
        log.info("Processor not stopped, active thread count %s",
                 test_obj.status.aggregate_snapshot.active_thread_count)
        return False

    def _starting_schedule_processor(processor_):
        test_obj = nipyapi.canvas.get_processor(processor_.id, 'id')
        if test_obj.component.state == 'RUNNING':
            return True
        log.info("Processor not started, run_status %s",
                 test_obj.component.state)
        return False

    assert isinstance(scheduled, bool)
    if refresh:
        target = nipyapi.canvas.get_processor(processor.id, 'id')
        assert isinstance(target, nipyapi.nifi.ProcessorEntity)
    else:
        target = processor
    result = schedule_components(
        pg_id=target.status.group_id,
        scheduled=scheduled,
        components=[target]
    )
    # If target scheduled state was successfully updated
    if result:
        # If we want to stop the processor
        if not scheduled:
            # Test that the processor threads have halted
            stop_test = nipyapi.utils.wait_to_complete(
                _running_schedule_processor, target
            )
            if stop_test:
                # Return True if we stopped the processor
                return result
            # Return False if we scheduled a stop, but it didn't stop
            return False
        # Test that the Processor started
        start_test = nipyapi.utils.wait_to_complete(
            _starting_schedule_processor, target
        )
        if start_test:
            return result
        return False


def update_process_group(pg, update):
    """
        Updates a given Process Group.

        Args:
            pg (ProcessGroupEntity): The Processor to target for update
            update (dict): key:value pairs to update

        Returns:
            (ProcessGroupEntity): The updated ProcessorEntity

        """
    assert isinstance(pg, nipyapi.nifi.ProcessGroupEntity)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().update_process_group(
            id=pg.id,
            body=nipyapi.nifi.ProcessGroupEntity(
                component=nipyapi.nifi.ProcessGroupDTO(
                    id=pg.id,
                    **update
                ),
                id=pg.id,
                revision=pg.revision
            )
        )


def update_processor(processor, update):
    """
    Updates configuration parameters for a given Processor.

    An example update would be:
    nifi.ProcessorConfigDTO(scheduling_period='3s')

    Args:
        processor (ProcessorEntity): The Processor to target for update
        update (ProcessorConfigDTO): The new configuration parameters

    Returns:
        (ProcessorEntity): The updated ProcessorEntity

    """
    if not isinstance(update, nipyapi.nifi.ProcessorConfigDTO):
        raise ValueError(
            "update param is not an instance of nifi.ProcessorConfigDTO"
        )
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessorsApi().update_processor(
            id=processor.id,
            body=nipyapi.nifi.ProcessorEntity(
                component=nipyapi.nifi.ProcessorDTO(
                    config=update,
                    id=processor.id
                ),
                revision=processor.revision,
            )
        )


def get_variable_registry(process_group, ancestors=True):
    """
    Gets the contents of the variable registry attached to a Process Group

    Args:
        process_group (ProcessGroupEntity): The Process Group to retrieve the
            Variable Registry from
        ancestors (bool): Whether to include the Variable Registries from child
            Process Groups

    Returns:
        (VariableRegistryEntity): The Variable Registry

    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().get_variable_registry(
            process_group.id,
            include_ancestor_groups=ancestors
        )


def update_variable_registry(process_group, update, refresh=True):
    """
    Updates one or more key:value pairs in the variable registry

    Args:
        process_group (ProcessGroupEntity): The Process Group which has the
        Variable Registry to be updated
        update (list[tuple]): The variables to write to the registry
        refresh (bool): Whether to refresh the object revision before updating

    Returns:
        (VariableRegistryEntity): The created or updated Variable Registry
        Entries

    """
    if not isinstance(process_group, nipyapi.nifi.ProcessGroupEntity):
        raise ValueError(
            'param process_group is not a valid nifi.ProcessGroupEntity'
        )
    if not isinstance(update, list):
        raise ValueError(
            'param update is not a valid list of (key,value) tuples'
        )
    # Parse variable update into the datatype
    var_update = [
        nipyapi.nifi.VariableEntity(
            nipyapi.nifi.VariableDTO(
                name=li[0],
                value=li[1],
                process_group_id=process_group.id
            )
        ) for li in update
    ]
    with nipyapi.utils.rest_exceptions():
        if refresh:
            process_group = get_process_group(process_group.id, 'id')
        return nipyapi.nifi.ProcessGroupsApi().update_variable_registry(
            id=process_group.id,
            body=nipyapi.nifi.VariableRegistryEntity(
                process_group_revision=process_group.revision,
                variable_registry=nipyapi.nifi.VariableRegistryDTO(
                    process_group_id=process_group.id,
                    variables=var_update
                )
            )
        )


def create_connection(source, target, relationships=None, name=None):
    """
    Creates a connection between two objects for the given relationships

    Args:
        source: Object to initiate the connection, e.g. ProcessorEntity
        target: Object to terminate the connection, e.g. FunnelEntity
        relationships (list): list of strings of relationships to connect, may
            be collected from the object 'relationships' property (optional)
        name (str): Defaults to None, String of Name for Connection (optional)

    Returns:
        (ConnectionEntity): for the created connection

    """
    # determine source and destination strings by class supplied
    source_type = nipyapi.utils.infer_object_label_from_class(source)
    target_type = nipyapi.utils.infer_object_label_from_class(target)
    if source_type not in ['OUTPUT_PORT', 'INPUT_PORT', 'FUNNEL']:
        source_rels = [x.name for x in source.component.relationships]
        if relationships:
            assert all(i in source_rels for i in relationships), \
                "One or more relationships [{0}] not in list of valid " \
                "Source Relationships [{1}]" \
                .format(str(relationships), str(source_rels))
        else:
            # if no relationships supplied, we connect them all
            relationships = source_rels
    if source_type == 'OUTPUT_PORT':
        # the hosting process group for an Output port connection to another
        # process group is the common parent process group
        parent_pg = get_process_group(source.component.parent_group_id, 'id')
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
                revision=nipyapi.nifi.RevisionDTO(
                    version=0
                ),
                source_type=source_type,
                destination_type=target_type,
                component=nipyapi.nifi.ConnectionDTO(
                    source=nipyapi.nifi.ConnectableDTO(
                        id=source.id,
                        group_id=source.component.parent_group_id,
                        type=source_type
                    ),
                    name=name,
                    destination=nipyapi.nifi.ConnectableDTO(
                        id=target.id,
                        group_id=target.component.parent_group_id,
                        type=target_type
                    ),
                    selected_relationships=relationships
                )
            )
        )


def delete_connection(connection, purge=False):
    """
    Deletes a connection, optionally purges it first

    Args:
        connection (ConnectionEntity): Connection to delete
        purge (bool): True to Purge, Defaults to False

    Returns:
        (ConnectionEntity): the modified Connection

    """
    assert isinstance(connection, nipyapi.nifi.ConnectionEntity)
    if purge:
        purge_connection(connection.id)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ConnectionsApi().delete_connection(
            id=connection.id,
            version=connection.revision.version
        )


def list_all_connections(pg_id='root', descendants=True):
    """
    Lists all connections for a given Process Group ID

    Args:
        pg_id (str): ID of the Process Group to retrieve Connections from
        descendants (bool): True to recurse child PGs, False to not

    Returns:
        (list): List of ConnectionEntity objects

    """
    return list_all_by_kind('connections', pg_id, descendants)


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
        x for x
        in list_all_connections(pg_id=component.component.parent_group_id)
        if component.id in [x.destination_id, x.source_id]
    ]


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
        (DropRequestEntity): The status reporting object for the drop
        request.

    """

    # TODO: Reimplement to batched instead of single threaded
    def _autumn_leaves(con_id_, drop_request_):
        test_obj = nipyapi.nifi.FlowfileQueuesApi().get_drop_request(
            con_id_,
            drop_request_.drop_request.id
        ).drop_request
        if not test_obj.finished:
            return False
        if test_obj.failure_reason:
            raise ValueError(
                "Unable to complete drop request{0}, error was {1}"
                .format(test_obj, test_obj.drop_request.failure_reason)
            )
        return True

    with nipyapi.utils.rest_exceptions():
        drop_req = nipyapi.nifi.FlowfileQueuesApi().create_drop_request(con_id)
    assert isinstance(drop_req, nipyapi.nifi.DropRequestEntity)
    return nipyapi.utils.wait_to_complete(_autumn_leaves, con_id, drop_req)


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
                "Unable to stop Process Group {0} for purging"
                .format(process_group.id)
            )
    cons = list_all_connections(process_group.id)
    result = []
    for con in cons:
        result.append({con.id: str(purge_connection(con.id))})
    return result


def get_bulletins():
    """
    Retrieves current bulletins (alerts) from the Flow Canvas

    Returns:
        (ControllerBulletinsEntity): The native datatype containing a list
    of bulletins
    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.FlowApi().get_bulletins()


def get_bulletin_board():
    """
    Retrieves the bulletin board object

    Returns:
        (BulletinBoardEntity): The native datatype BulletinBoard object
    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.FlowApi().get_bulletin_board()


def create_controller(parent_pg, controller, name=None):
    """
    Creates a new Controller Service in a given Process Group of the given
        Controller type, with the given Name

    Args:
        parent_pg (ProcessGroupEntity): Target Parent PG
        controller (DocumentedTypeDTO): Type of Controller to create, found
            via the list_all_controller_types method
        name (str[Optional]): Name for the new Controller as a String

    Returns:
        (ControllerServiceEntity)

    """
    assert isinstance(controller, nipyapi.nifi.DocumentedTypeDTO)
    assert isinstance(parent_pg, nipyapi.nifi.ProcessGroupEntity)
    assert name is None or isinstance(name, six.string_types)
    with nipyapi.utils.rest_exceptions():
        out = nipyapi.nifi.ProcessGroupsApi().create_controller_service(
            id=parent_pg.id,
            body=nipyapi.nifi.ControllerServiceEntity(
                revision={'version': 0},
                component=nipyapi.nifi.ControllerServiceDTO(
                    bundle=controller.bundle,
                    type=controller.type
                )
            ),
        )
        if name:
            update_controller(
                out,
                nipyapi.nifi.ControllerServiceDTO(
                    name=name
                )
            )
    return out


def list_all_controllers(pg_id='root', descendants=True):
    """
    Lists all controllers under a given Process Group, defaults to Root
        Optionally recurses all child Process Groups as well
    Args:
        pg_id (str): String of the ID of the Process Group to list from
        descendants (bool): True to recurse child PGs, False to not

    Returns:
        None, ControllerServiceEntity, or list(ControllerServiceEntity)

    """
    assert isinstance(pg_id, six.string_types)
    assert isinstance(descendants, bool)
    handle = nipyapi.nifi.FlowApi()
    # Testing shows that descendant doesn't work on NiFi-1.1.2
    # Or 1.2.0, despite the descendants option being available
    if nipyapi.utils.check_version('1.2.0') >= 0:
        # Case where NiFi <= 1.2.0
        out = []
        if descendants:
            pgs = list_all_process_groups(pg_id)
        else:
            pgs = [get_process_group(pg_id, 'id')]
        for pg in pgs:
            new_conts = handle.get_controller_services_from_group(
                pg.id).controller_services
            # trim duplicates from inheritance
            out += [
                x for x in new_conts
                if x.id not in [y.id for y in out]
            ]
    else:
        # Case where NiFi > 1.2.0
        # duplicate trim already handled by server
        out = handle.get_controller_services_from_group(
            pg_id,
            include_descendant_groups=descendants
        ).controller_services
    return out


def delete_controller(controller, force=False):
    """
    Delete a Controller service, with optional prejudice

    Args:
        controller (ControllerServiceEntity): Target Controller to delete
        force (bool): True to attempt Disable the Controller before deletion

    Returns:
        (ControllerServiceEntity)

    """
    assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)
    assert isinstance(force, bool)

    def _del_cont(cont_id):
        if not get_controller(cont_id, 'id', bool_response=True):
            return True
        return False

    handle = nipyapi.nifi.ControllerServicesApi()
    if force:
        # Stop and refresh
        controller = schedule_controller(controller, False, True)
    with nipyapi.utils.rest_exceptions():
        result = handle.remove_controller_service(
            id=controller.id,
            version=controller.revision.version
        )
    del_test = nipyapi.utils.wait_to_complete(
        _del_cont,
        controller.id,
        nipyapi_max_wait=15,
        nipyapi_delay=1
    )
    if not del_test:
        raise ValueError("Timed out waiting for Controller Deletion")
    return result


def update_controller(controller, update, refresh=True):
    """
    Updates the Configuration of a Controller Service

    Args:
        controller (ControllerServiceEntity): Target Controller to update
        update (ControllerServiceDTO): Controller Service configuration object
            containing the new config params and properties
        refresh (bool): True to refresh before applying

    Returns:
        (ControllerServiceEntity)

    """
    assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)
    assert isinstance(update, nipyapi.nifi.ControllerServiceDTO)
    # Insert the ID into the update
    if refresh:
        controller = get_controller(controller.id, 'id')
    update.id = controller.id
    return nipyapi.nifi.ControllerServicesApi().update_controller_service(
        id=controller.id,
        body=nipyapi.nifi.ControllerServiceEntity(
            component=update,
            revision=controller.revision,
            id=controller.id
        )
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
        test_obj = get_controller(cont_id, 'id')
        if test_obj.component.state == tgt_state:
            return True
        return False

    handle = nipyapi.nifi.ControllerServicesApi()
    target_state = 'ENABLED' if scheduled else 'DISABLED'
    if refresh:
        controller = nipyapi.canvas.get_controller(controller.id, 'id')
        assert isinstance(controller, nipyapi.nifi.ControllerServiceEntity)
    if nipyapi.utils.check_version('1.2.0') >= 0:
        # Case where NiFi <= 1.2.0
        result = update_controller(
            controller=controller,
            update=nipyapi.nifi.ControllerServiceDTO(
                state=target_state
            )
        )
    else:
        # Case where NiFi > 1.2.0
        result = handle.update_run_status(
            id=controller.id,
            body=nipyapi.nifi.ControllerServiceRunStatusEntity(
                revision=controller.revision,
                state=target_state
            )
        )
    if not result:
        raise ValueError("Scheduling request failed")
    state_test = nipyapi.utils.wait_to_complete(
        _schedule_controller_state,
        controller.id,
        target_state,
        nipyapi_delay=nipyapi.config.long_retry_delay,
        nipyapi_max_wait=nipyapi.config.long_max_wait
    )
    if state_test:
        return get_controller(controller.id, 'id')
    raise ValueError("Scheduling request timed out")


def get_controller(identifier, identifier_type='name',
                   bool_response=False, greedy=True):
    """
    Retrieve a given Controller

    Args:
        identifier (str): ID or Name of a Controller to find
        identifier_type (str): 'id' or 'name', defaults to name
        bool_response (bool): If True, will return False if the Controller is
            not found - useful when testing for deletion completion
        greedy (bool): True for partial match, False for exact match

    Returns:

    """
    assert isinstance(identifier, six.string_types)
    assert identifier_type in ['name', 'id']
    handle = nipyapi.nifi.ControllerServicesApi()
    try:
        if identifier_type == 'id':
            out = handle.get_controller_service(identifier)
        else:
            obj = list_all_controllers()
            out = nipyapi.utils.filter_obj(
                obj, identifier, identifier_type, greedy=greedy)
    except nipyapi.nifi.rest.ApiException as e:
        if bool_response:
            return False
        raise ValueError(e.body)
    return out


def list_all_controller_types():
    """
    Lists all Controller Service types available on the environment

    Returns:
        list(DocumentedTypeDTO)
    """
    handle = nipyapi.nifi.FlowApi()
    return handle.get_controller_service_types().controller_service_types


def list_all_by_kind(kind, pg_id='root', descendants=True):
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
        'input_ports', 'output_ports', 'funnels', 'controllers', 'connections',
        'remote_process_groups'
    ]
    if kind == 'controllers':
        return list_all_controllers(pg_id, descendants)
    handle = nipyapi.nifi.ProcessGroupsApi()
    call_function = getattr(handle, 'get_' + kind)
    out = []
    if descendants:
        pgs = list_all_process_groups(pg_id)
    else:
        pgs = [get_process_group(pg_id, 'id')]
    for pg in pgs:
        out += call_function(pg.id).__getattribute__(kind)
    return out


def list_all_input_ports(pg_id='root', descendants=True):
    """Convenience wrapper for list_all_by_kind for input ports"""
    return list_all_by_kind('input_ports', pg_id, descendants)


def list_all_output_ports(pg_id='root', descendants=True):
    """Convenience wrapper for list_all_by_kind for output ports"""
    return list_all_by_kind('output_ports', pg_id, descendants)


def list_all_funnels(pg_id='root', descendants=True):
    """Convenience wrapper for list_all_by_kind for funnels"""
    return list_all_by_kind('funnels', pg_id, descendants)


def list_all_remote_process_groups(pg_id='root', descendants=True):
    """Convenience wrapper for list_all_by_kind for remote process groups"""
    return list_all_by_kind('remote_process_groups', pg_id, descendants)


def get_remote_process_group(rpg_id, summary=False):
    """
    Fetch a remote process group object, with optional summary of just ports
    """
    rpg = nipyapi.nifi.RemoteProcessGroupsApi().get_remote_process_group(
        rpg_id
    )
    if not summary:
        out = rpg
    else:
        out = {
            'id': rpg.id,
            'input_ports': rpg.component.contents.input_ports,
            'output_ports': rpg.component.contents.output_ports
        }
    return out


def create_remote_process_group(target_uris, transport='RAW', pg_id='root',
                                position=None):
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
    assert transport in ['RAW', 'HTTP']
    assert isinstance(pg_id, str)
    pg_id = pg_id if not 'root' else get_root_pg_id()
    position = position if position else (400, 400)
    assert isinstance(position, tuple)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_remote_process_group(
            id=pg_id,
            body=nipyapi.nifi.RemoteProcessGroupEntity(
                component=nipyapi.nifi.RemoteProcessGroupDTO(
                    position=nipyapi.nifi.PositionDTO(
                        x=float(position[0]),
                        y=float(position[1])
                    ),
                    target_uris=target_uris,
                    transport_protocol=transport
                ),
                revision=nipyapi.nifi.RevisionDTO(version=0),
            )
        )


def delete_remote_process_group(rpg, refresh=True):
    """
    Deletes a given remote process group

    Args:
        rpg (RemoteProcessGroupEntity): Remote Process Group to remove
        refresh (bool): Whether to refresh the object before action

    Returns:
        (RemoteProcessGroupEntity)
    """
    assert isinstance(rpg, nipyapi.nifi.RemoteProcessGroupEntity)
    if refresh:
        rpg = get_remote_process_group(rpg.id)
    handle = nipyapi.nifi.RemoteProcessGroupsApi()
    with nipyapi.utils.rest_exceptions():
        return handle.remove_remote_process_group(
            id=rpg.id,
            version=rpg.revision.version
        )


def set_remote_process_group_transmission(rpg, enable=True, refresh=True):
    """
    Enable or Disable Transmission for an RPG

    Args:
        rpg (RemoteProcessGroupEntity): The ID of the remote process group
          to modify
        enable (bool): True to enable, False to disable
        refresh (bool): Whether to refresh the object before action

    Returns:

    """
    assert isinstance(rpg, nipyapi.nifi.RemoteProcessGroupEntity)
    assert isinstance(enable, bool)
    if refresh:
        rpg = get_remote_process_group(rpg.id)
    handle = nipyapi.nifi.RemoteProcessGroupsApi()
    with nipyapi.utils.rest_exceptions():
        return handle.update_remote_process_group_run_status(
            id=rpg.id,
            body=nipyapi.nifi.RemotePortRunStatusEntity(
                state='TRANSMITTING' if enable else 'STOPPED',
                revision=rpg.revision
            )
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
    assert isinstance(pg_id, six.string_types)
    position = position if position else (400, 400)
    assert isinstance(position, tuple)
    handle = nipyapi.nifi.ProcessGroupsApi()
    port_generator = getattr(handle, 'create_' + port_type.lower())
    with nipyapi.utils.rest_exceptions():
        return port_generator(
            id=pg_id,
            body=nipyapi.nifi.PortEntity(
                revision=nipyapi.nifi.RevisionDTO(version=0),
                component=nipyapi.nifi.PortDTO(
                    parent_group_id=pg_id,
                    position=nipyapi.nifi.PositionDTO(
                        x=float(position[0]),
                        y=float(position[1])
                    ),
                    name=name
                )
            )
        )


def delete_port(port):
    """Deletes a given port from the canvas if possible"""
    assert isinstance(port, nipyapi.nifi.PortEntity)
    if 'INPUT' in port.port_type:
        with nipyapi.utils.rest_exceptions():
            return nipyapi.nifi.InputPortsApi().remove_input_port(
                id=port.id,
                version=port.revision.version)
    if 'OUTPUT' in port.port_type:
        with nipyapi.utils.rest_exceptions():
            return nipyapi.nifi.OutputPortsApi().remove_output_port(
                id=port.id,
                version=port.revision.version)


def get_funnel(funnel_id):
    """Gets a given Funnel by ID"""
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.FunnelApi().get_funnel(funnel_id)


def create_funnel(pg_id, position=None):
    """
    Creates a Funnel Object

    Args:
        pg_id (str): ID of the parent Process Group
        position (tuple[int, int]): Position on canvas

    Returns:
        (FunnelEntity) Created Funnel
    """
    position = position if position else (400, 400)
    assert isinstance(position, tuple)
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ProcessGroupsApi().create_funnel(
            id=pg_id,
            body=nipyapi.nifi.FunnelEntity(
                position=nipyapi.nifi.PositionDTO(
                    x=float(position[0]),
                    y=float(position[1])
                ),
                revision=nipyapi.nifi.RevisionDTO(version=0),
                component=nipyapi.nifi.FunnelDTO(
                    parent_group_id=pg_id
                )
            )
        )


def delete_funnel(funnel, refresh=True):
    """
    Deletes a Funnel Object

    Args:
        funnel (FunnelEntity): The Funnel to delete
        refresh (bool): Whether to refresh the object state
            before execution

    Returns:
        (FunnelEntity) Deleted FunnelEntity reference
    """
    assert isinstance(funnel, nipyapi.nifi.FunnelEntity)
    with nipyapi.utils.rest_exceptions():
        if refresh:
            funnel = get_funnel(funnel.id)
        return nipyapi.nifi.FunnelApi().remove_funnel(
            id=funnel.id,
            version=funnel.revision.version
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
        pg_id = nipyapi.canvas.get_process_group(pg_id, 'id') \
            .component.parent_group_id
        parent_groups.append(pg_id)
    # Removing the None value
    parent_groups.pop()
    return parent_groups
