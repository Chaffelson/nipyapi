# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas.
"""

from __future__ import absolute_import
import six
import nipyapi

__all__ = [
    "get_root_pg_id", "recurse_flow", "get_flow", "get_process_group_status",
    "get_process_group", "list_all_process_groups", "delete_process_group",
    "schedule_process_group", "create_process_group", "list_all_processors",
    "list_all_processor_types", "get_processor_type", 'create_processor',
    'delete_processor', 'get_processor', 'schedule_processor',
    'update_processor', 'get_variable_registry', 'update_variable_registry',
    'get_connections', 'purge_connection', 'purge_process_group',
    'get_bulletins', 'get_bulletin_board'
]


def get_root_pg_id():
    """
    Convenience function to return the UUID of the Root Process Group

    Returns (str): The UUID of the root PG
    """
    return nipyapi.nifi.FlowApi().get_process_group_status('root')\
        .process_group_status.id


def recurse_flow(pg_id='root'):
    """
    Returns information about a Process Group and all its Child Flows.
    Recurses the child flows by appending each process group with a
    'nipyapi_extended' parameter which contains the child process groups, etc.

    Args:
        pg_id (str): The Process Group UUID

    Returns:
         (ProcessGroupFlowEntity): enriched NiFi Flow object
    """
    assert isinstance(pg_id, six.string_types), "pg_id should be a string"

    def _walk_flow(node):
        """This recursively extends the ProcessGroupEntity to contain the
        ProcessGroupFlowEntity of each of it's child process groups.
        So you can have the entire canvas in a single object.
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
    try:
        return nipyapi.nifi.FlowApi().get_flow(pg_id)
    except nipyapi.nifi.rest.ApiException as err:
        raise ValueError(err.body)


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
    assert detail in ['names', 'all'], "detail should be either 'names' or " \
                                       "'all'"
    raw = nipyapi.nifi.ProcessgroupsApi().get_process_group(id=pg_id)
    if detail == 'names':
        out = {
            raw.component.name: raw.component.id
        }
        return out
    return raw


def get_process_group(identifier, identifier_type='name'):
    """
    Filters the list of all process groups against a given identifier string
    occuring in a given identifier_type field.

    Args:
        identifier (str): the string to filter the list for
        identifier_type (str): the field to filter on, set in config.py

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches

    """
    assert isinstance(identifier, six.string_types)
    assert identifier_type in ['name', 'id']
    try:
        if identifier_type == 'id':
            # assuming unique fetch of pg id
            # implementing separately to avoid recursing entire canvas
            out = nipyapi.nifi.ProcessgroupsApi().get_process_group(identifier)
        else:
            obj = list_all_process_groups()
            out = nipyapi.utils.filter_obj(obj, identifier, identifier_type)
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
    return out


def list_all_process_groups():
    """
    Returns a flattened list of all Process Groups on the canvas.
    Potentially slow if you have a large canvas.

    Note that the ProcessGroupsApi().get_process_groups(pg_id) command only
    provides the first layer of pgs, whereas this trawls the entire canvas

    Returns:
         list[ProcessGroupEntity]

    """
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

    Returns:
         list[ProcessorEntity]
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

    Args:
        process_group_id (str): The UUID of the target Process Group
        scheduled (bool): True to start, False to stop

    Returns:
         (bool): True of successfully scheduled, False if not

    """
    assert isinstance(process_group_id, six.string_types)
    assert isinstance(scheduled, bool)

    def _running_schedule_process_group(pg_id_):
        test_obj = nipyapi.nifi.ProcessgroupsApi().get_process_group(pg_id_)
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
    if refresh or force:
        target = nipyapi.nifi.ProcessgroupsApi().get_process_group(
            process_group.id
        )
    else:
        target = process_group
    if force:
        # Stop, drop, and roll.
        purge_process_group(target, stop=True)
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
    Creates a new Process Group with the given name under the provided parent
    Process Group at the given Location

    Args:
        parent_pg (ProcessGroupEntity): The parent Process Group to create the
            new process group in
        new_pg_name (str): The name of the new Process Group
        location (tuple[x, y]): the x,y coordinates to place the new Process
            Group under the parent

    Returns:
         (ProcessGroupEntity): The new Process Group

    """
    assert isinstance(parent_pg, nipyapi.nifi.ProcessGroupEntity)
    assert isinstance(new_pg_name, six.string_types)
    assert isinstance(location, tuple)
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

    Returns:
         list(ProcessorTypesEntity): A native datatype containing the
         processors list

    """
    try:
        return nipyapi.nifi.FlowApi().get_processor_types()
    except nipyapi.nifi.rest.ApiException as e:
        raise e


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
    try:
        obj = list_all_processor_types().processor_types
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
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
    Filters the list of all Processors against the given identifier string in
    the given identifier_type field

    Args:
        identifier (str): The String to filter against
        identifier_type (str): The field to apply the filter to. Set in
            config.py

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches
    """
    assert isinstance(identifier, six.string_types)
    assert identifier_type in ['name', 'id']
    try:
        if identifier_type == 'id':
            out = nipyapi.nifi.ProcessorsApi().get_processor(identifier)
        else:
            obj = list_all_processors()
            out = nipyapi.utils.filter_obj(obj, identifier, identifier_type)
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
    return out


def delete_processor(processor, refresh=True, force=False):
    """
    Deletes a Processor from the canvas, with optional prejudice.

    Args:
        processor (ProcessorEntity): The processor to delete
        refresh (bool): Whether to refresh the Processor state before action
        force (bool): Whether to stop the Processor before deletion. Behavior
            may change in future releases. Experimental.

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
    Set a Processor to Start or Stop.

    Note that this doesn't guarantee that it will change state, merely that
    it will be instructed to try.

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
            stop_test = nipyapi.utils.wait_to_complete(
                _running_schedule_processor, target
            )
            if stop_test:
                # Return True if we stopped the processor
                return result
            # Return False if we scheduled a stop, but it didn't stop
            return False
    # Return the True or False result if we were trying to start the processor
    return result


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

    Args:
        process_group (ProcessGroupEntity): The Process Group to retrieve the
            Variable Registry from
        ancestors (bool): Whether to include the Variable Registries from child
            Process Groups

    Returns:
        (VariableRegistryEntity): The Variable Registry

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

    Args:
        process_group (ProcessGroupEntity): The Process Group which has the
        Variable Registry to be updated
        update (tuple[key, value]): The variables to write to the registry

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
    EXPERIMENTAL
    List all child connections within a given Process Group

    Args:
        pg_id (str): The UUID of the target Process Group

    Returns:
        (ConnectionsEntity): A native datatype which contains the list of
        all Connections in the Process Group

    """
    assert isinstance(
        get_process_group(pg_id, 'id'),
        nipyapi.nifi.ProcessGroupEntity
    )
    try:
        out = nipyapi.nifi.ProcessgroupsApi().get_connections(pg_id)
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
    assert isinstance(out, nipyapi.nifi.ConnectionsEntity)
    return out


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
        test_obj = nipyapi.nifi.FlowfilequeuesApi().get_drop_request(
            con_id_,
            drop_request_.drop_request.id
        ).drop_request
        if not test_obj.finished:
            return False
        elif test_obj.finished:
            if test_obj.failure_reason:
                raise ValueError(
                    "Unable to complete drop request{0}, error was {1}"
                    .format(
                        test_obj, test_obj.drop_request.failure_reason
                    )
                )
            else:
                return True

    try:
        drop_req = nipyapi.nifi.FlowfilequeuesApi().create_drop_request(con_id)
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
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
    cons = get_connections(process_group.id)
    result = []
    for con in cons.connections:
        result.append({con.id: str(purge_connection(con.id))})
    return result


def get_bulletins():
    """
    Retrieves current bulletins (alerts) from the Flow Canvas

    Returns:
        (ControllerBulletinsEntity): The native datatype containing a list
    of bulletins
    """
    try:
        return nipyapi.nifi.FlowApi().get_bulletins()
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def get_bulletin_board():
    """
    Retrieves the bulletin board object

    Returns:
        (BulletinBoardEntity): The native datatype BulletinBoard object
    """
    try:
        return nipyapi.nifi.FlowApi().get_bulletin_board()
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
