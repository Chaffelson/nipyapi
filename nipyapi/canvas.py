# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
STATUS: Work in Progress to determine pythonic datamodel
"""

from __future__ import absolute_import
import nipyapi

__all__ = [
    "get_root_pg_id", "recurse_flow", "get_flow", "get_process_group_status",
    "get_process_group", "list_all_process_groups", "delete_process_group",
    "schedule_process_group", "create_process_group", "list_all_processors",
    "list_all_processor_types", "get_processor_type", 'create_processor',
    'delete_processor', 'get_processor', 'schedule_processor',
    'update_processor', 'get_variable_registry', 'update_variable_registry',
    'get_connections', 'purge_connection'
]


def get_root_pg_id():
    """Simple Example function for wrapper demonstration"""
    con = nipyapi.nifi.FlowApi()
    pg_root = con.get_process_group_status('root')
    return pg_root.process_group_status.id


def recurse_flow(pg_id='root'):
    """
    Returns information about a Process Group and all its Child Flows
    :param pg_id: id of a Process Group to use as the root for recursion
    , defaults to root if none supplied
    :returns ProcessGroupFlowEntity: Nested Process Group information
    """

    def _walk_flow(node):
        """This recursively extends the ProcessGroupEntity to contain the
        ProcessGroupFlowEntity of each of it's child process groups.
        So you can have the entire canvas in a single object
        """
        if isinstance(node, nipyapi.nifi.ProcessGroupFlowEntity):
            for pg in node.process_group_flow.flow.process_groups:
                pg.__setattr__(
                    'nipyapi_extended',
                    recurse_flow(pg.id)
                )
            return node

    return _walk_flow(get_flow(pg_id))


def get_flow(pg_id='root'):
    """
    Returns information about a Process Group and flow
    This surfaces the native implementation, for the recursed implementation
    see 'recurse_flow'
    :param pg_id: id of the Process Group to retrieve, defaults to the root
    process group if not set
    :return ProcessGroupFlowEntity: the Process Group object
    """
    try:
        return nipyapi.nifi.FlowApi().get_flow(pg_id)
    except nipyapi.nifi.rest.ApiException as err:
        raise ValueError(err.body)


def get_process_group_status(pg_id='root', detail='names'):
    """
    Returns the full record of a Process Group
    Note that there is also a 'process group status' command available, but it
    returns a subset of this data anyway, and this call is more useful
    :param pg_id: NiFi ID of the Process Group to retrieve
    :param detail: Level of detail to respond with
    :return:
    """
    valid_details = ['names', 'all']
    if detail not in valid_details:
        raise ValueError(
            'detail requested ({0}) not in valid list ({1})'
            .format(detail, valid_details)
        )
    raw = nipyapi.nifi.ProcessgroupsApi().get_process_group(id=pg_id)
    if detail == 'names':
        out = {
            raw.component.name: raw.component.id
        }
        return out
    elif detail == 'all':
        return raw


def get_process_group(identifier, identifier_type='name'):
    """
    Returns a process group, if it exists. Returns a list for duplicates
    :param identifier: String of the name or id of the process group
    :param identifier_type: 'name' or 'id'
    :return: ProcessGroupEntity if unique, None if not found, List if duplicate
    """
    try:
        obj = list_all_process_groups()
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
    return nipyapi.utils.filter_obj(obj, identifier, identifier_type)


def list_all_process_groups():
    """
    Returns a flattened list of all Process Groups.
    :return list: list of ProcessGroupEntity objects
    """

    # TODO: Check if get_process_groups is fixed in newer versions
    def flatten(parent_pg):
        """
        Recursively flattens the native datatypes into a generic list.
        Note that the root is a special case as it has no parent
        :param parent_pg: ProcessGroupEntity to flatten
        :return yield: generator for all ProcessGroupEntities, eventually
        """
        for child_pg in parent_pg.process_group_flow.flow.process_groups:
            for sub in flatten(child_pg.nipyapi_extended):
                yield sub
            yield child_pg

    root_flow = recurse_flow('root')
    out = list(flatten(root_flow))
    # This duplicates the nipyapi_extended structure to the root case
    root_entity = nipyapi.nifi.ProcessgroupsApi().get_process_group('root')
    root_entity.__setattr__('nipyapi_extended', root_flow)
    out.append(root_entity)
    return out


def list_all_processors():
    """
    Returns a flat list of all Processors anywhere on the canvas
    :return: list of ProcessorEntity's
    """

    def flattener():
        """
        Memory efficient flattener, sort of.
        :return: yield's a ProcessEntity
        """
        for pg in list_all_process_groups():
            for proc in pg.nipyapi_extended.process_group_flow.flow.processors:
                yield proc

    return list(flattener())


def schedule_process_group(process_group_id, scheduled):
    """
    Start or Stop a Process Group and all components.
    Note that this doesn't guarantee that all components have started, as
    some may be in Invalid states.
    :param process_group_id: ID of the Process Group
    :param scheduled: Bool; True to Start, False to Stop
    :return: Bool, Success or not
    """
    def _waiting_for_godot(pg_id_):
        test_obj = nipyapi.nifi.ProcessgroupsApi().get_process_group(pg_id_)
        if test_obj.status.aggregate_snapshot.active_thread_count == 0:
            return True
        return False
    assert isinstance(
        get_process_group(process_group_id, 'id'),
        nipyapi.nifi.ProcessGroupEntity
    )
    assert isinstance(scheduled, bool)
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
                _waiting_for_godot,
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
    deletes a specific process group
    :param process_group: ProcessGroupEntity of the process group to be removed
    :param force: Bool; will attempt to clean down the PG before removal.
    Use with caution!
    :param refresh: Boolean, whether to refresh the PG status before action
    :return ProcessGroupEntity: the updated entity object for the deleted PG
    :raises: AssertionError for bad params, ValueError for bad API calls
    """
    assert isinstance(process_group, nipyapi.nifi.ProcessGroupEntity)
    assert isinstance(force, bool)
    assert isinstance(refresh, bool)
    if refresh or force:
        target = nipyapi.nifi.ProcessgroupsApi().get_process_group(
            process_group.id
        )
    else:
        target = process_group
    if force:
        # Stop everything
        schedule_process_group(target.id, scheduled=False)
        # Remove data from queues
        for con in get_connections(target.id).connections:
            purge_connection(con.id)
        # Remove templates
        for template in nipyapi.templates.list_all_templates().templates:
            if target.id == template.template.group_id:
                nipyapi.templates.delete_template(template.id)
    try:
        return nipyapi.nifi.ProcessgroupsApi().remove_process_group(
            id=target.id,
            version=target.revision.version,
            client_id=target.revision.client_id
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def create_process_group(parent_pg, new_pg_name, location):
    """
    Creates a new PG with a given name under the provided parent PG
    :param parent_pg: ProcessGroupEntity object of the parent PG
    :param new_pg_name: String to name the new PG
    :param location: Tuple of (x,y) coordinates to place the new PG
    :return: ProcessGroupEntity of the new PG
    """
    try:
        return nipyapi.nifi.ProcessgroupsApi().create_process_group(
            id=parent_pg.id,
            body=nipyapi.nifi.ProcessGroupEntity(
                revision=parent_pg.revision,
                component=nipyapi.nifi.ProcessGroupDTO(
                    name=new_pg_name,
                    position=nipyapi.nifi.PositionDTO(
                        x=float(location[0]),
                        y=float(location[1])
                    )
                )
            )
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise e


def list_all_processor_types():
    """
    Produces the list of all available processor types in the NiFi instance
    :return ProcessorTypesEntity: Native Datatype containing list
    """
    try:
        return nipyapi.nifi.FlowApi().get_processor_types()
    except nipyapi.nifi.rest.ApiException as e:
        raise e


def get_processor_type(identifier, identifier_type='name'):
    """
    Gets the abstract object describing a Processor, or list thereof
    :param identifier: String to search for
    :param identifier_type: Processor descriptor to search: bundle, name or tag
    :return: DocumentedTypeDTO if unique, None if not found, List if duplicate
    """
    try:
        obj = list_all_processor_types().processor_types
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
    return nipyapi.utils.filter_obj(obj, identifier, identifier_type)


def create_processor(parent_pg, processor, location, name=None, config=None):
    """
    Instantiates a given processon the canvas
    :param parent_pg: Process Group to instantiate the Processor in
    :param processor: Processor Type object
    :param location: (x,y) coordinates to instantiate that processor at
    :param name: String name of the processor
    :param config: Processor Config object of parameters
    :return: ProcessorEntity
    """
    if name is None:
        processor_name = processor.type.split('.')[-1]
    else:
        processor_name = name
    if config is None:
        target_config = nipyapi.nifi.ProcessorConfigDTO()
    else:
        target_config = config
    try:
        return nipyapi.nifi.ProcessgroupsApi().create_processor(
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
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def get_processor(identifier, identifier_type='name'):
    """
    Gets a deployed Processor, or list thereof
    :param identifier: String to filter on
    :param identifier_type: 'name' or 'id' to identify field to filter on
    :return: None if 0 matches, list if > 1, single ProcessorEntity if ==1
    """
    try:
        obj = list_all_processors()
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
    return nipyapi.utils.filter_obj(obj, identifier, identifier_type)


def delete_processor(processor, refresh=True, force=False):
    """
    Remove a processor from the canvas, with prejudice if necessary
    :param processor: ProcessorEntity of the processor to target
    :param refresh: Whether to refresh the object, defaults to True
    :param force: Whether to also stop the Processor first, if it is running
    :return: Final Processor status
    :raises: AssertionError for bad params, ValueError if the API rejects you
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
            raise ("Could not prepare processor ({0}) for deletion"
                   .format(target.id))
        target = get_processor(processor.id, 'id')
        assert isinstance(target, nipyapi.nifi.ProcessorEntity)
    try:
        return nipyapi.nifi.ProcessorsApi().delete_processor(
            id=target.id,
            version=target.revision.version
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def schedule_components(pg_id, scheduled, components=None):
    """
    Changes scheduled target state of a list of Components in a Process Group
    :param pg_id: ID of the Process Group containing the components
    :param scheduled: Bool; True to Start, False to stop
    :param components: List of Component Entities to Schedule
    :return: Bool of success or not
    :raises: AssertionError for bad params, ValueError if the API rejects you
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
    try:
        result = nipyapi.nifi.FlowApi().schedule_components(
            id=pg_id,
            body=body
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
    if result.state == target_state:
        return True
    return False


def schedule_processor(processor, scheduled, refresh=True):
    """
    Start or Stop a specific processor
    :param processor: ProcessorEntity of the Processor target
    :param scheduled: Bool; True to Start, False to Stop
    :param refresh: Bool; whether to refresh the processor first
    :return: Bool of success or not
    :raises: AssertionError for bad params, ValueError if the API rejects you
    """
    assert isinstance(processor, nipyapi.nifi.ProcessorEntity)
    assert isinstance(scheduled, bool)
    assert isinstance(refresh, bool)

    def _dangleberries(processor_):
        test_obj = nipyapi.nifi.ProcessorsApi().get_processor(processor_.id)
        if test_obj.status.aggregate_snapshot.active_thread_count == 0:
            return True
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
            stop_test = nipyapi.utils.wait_to_complete(_dangleberries, target)
            if stop_test:
                # Return True if we stopped the processor
                return result
            # Return False if we scheduled a stop, but it didn't stop
            return False
    # Return the True or False result if we were trying to start the processor
    return result


def update_processor(processor, update):
    """
    EXPERIMENTAL
    Updates the configuration parameters of a stopped processor
    :param processor: Processor object to be updated
    :param update: ProcessorConfigDTO, updated configuration parameters
    :return: updated ProcessorEntity
    """
    if not isinstance(update, nipyapi.nifi.ProcessorConfigDTO):
        raise ValueError(
            "update param is not an instance of nifi.ProcessorConfigDTO"
        )
    try:
        return nipyapi.nifi.ProcessorsApi().update_processor(
            processor.id,
            body=nipyapi.nifi.ProcessorEntity(
                component=nipyapi.nifi.ProcessorDTO(
                    config=update,
                    id=processor.id
                ),
                revision=processor.revision,
            )
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def get_variable_registry(process_group, ancestors=True):
    """
    Gets the contents of the variable registry attached to a Process Group
    :param process_group: ProcessGroup object
    :param ancestors: Whether to get the variables from parent Process Groups
    :return: VariableRegistryEntity
    """
    try:
        return nipyapi.nifi.ProcessgroupsApi().get_variable_registry(
            process_group.id,
            include_ancestor_groups=ancestors
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def update_variable_registry(process_group, update):
    """
    Updates one or more key:value pairs in the variable registry
    :param process_group: ProcessGroup object to update the variables on
    :param update: (key,value) tuples of the variables to write to the registry
    :return: VariableRegistryEntity
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
    try:
        return nipyapi.nifi.ProcessgroupsApi().update_variable_registry(
            id=process_group.id,
            body=nipyapi.nifi.VariableRegistryEntity(
                process_group_revision=process_group.revision,
                variable_registry=nipyapi.nifi.VariableRegistryDTO(
                    process_group_id=process_group.id,
                    variables=var_update
                )
            )
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def get_connections(pg_id):
    """
    lists all child connections for a given ProcessGroup iD
    :param pg_id: ID of the Process Group
    :return: ConnectionsEntity, which contains a list of Connections
    """
    try:
        return nipyapi.nifi.ProcessgroupsApi().get_connections(pg_id)
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def purge_connection(con_id):
    """
    Drops all flowfiles in a given connection
    :param con_id: ID of the Connection to clear
    :return:
    """
    # TODO: Implement wait_to_finish for this function
    try:
        return nipyapi.nifi.FlowfilequeuesApi().create_drop_request(con_id)
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
