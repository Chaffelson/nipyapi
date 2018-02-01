# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
STATUS: Work in Progress to determine pythonic datamodel
"""

from __future__ import absolute_import
from nipyapi import nifi
from nipyapi.nifi.rest import ApiException

__all__ = [
    "get_root_pg_id", "recurse_flow", "get_flow", "get_process_group_status",
    "get_process_group", "list_all_process_groups", "delete_process_group",
    "schedule_process_group", "create_process_group", "list_all_processors",
    "list_all_processor_types", "get_processor_type", 'create_processor',
    'delete_processor', 'get_processor', 'schedule_processor',
    'update_processor', 'get_variable_registry', 'update_variable_registry'
]


def get_root_pg_id():
    """Simple Example function for wrapper demonstration"""
    con = nifi.FlowApi()
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
        if isinstance(node, nifi.ProcessGroupFlowEntity):
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
        return nifi.FlowApi().get_flow(pg_id)
    except ApiException as err:
        raise ValueError(err.body)


def get_process_group_status(pg_id='root', detail='names'):
    """
    Returns information about a Process Group
    :param pg_id: NiFi ID of the Process Groupt to retrieve
    :param detail: Level of detail to respond with
    :return:
    """
    valid_details = ['names', 'all']
    if detail not in valid_details:
        raise ValueError(
            'detail requested ({0}) not in valid list ({1})'
            .format(detail, valid_details)
        )
    raw = nifi.ProcessgroupsApi().get_process_group(id=pg_id)
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
    valid_id_types = ['name', 'id']
    if identifier_type not in valid_id_types:
        raise ValueError(
            "invalid identifier_type. ({0}) not in ({1})".format(
                identifier_type, valid_id_types
            )
        )
    all_pgs = list_all_process_groups()
    if identifier_type == 'name':
        out = [
            li for li in all_pgs
            if identifier in li.status.name
        ]
    elif identifier_type == 'id':
        out = [
            li for li in all_pgs
            if identifier in li.id
        ]
    else:
        out = []
    if not out:
        return None
    elif len(out) > 1:
        return out
    return out[0]


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
    root_entity = nifi.ProcessgroupsApi().get_process_group('root')
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


def delete_process_group(process_group_id, revision):
    """
    deletes a specific process group
    :param process_group_id: id of the process group to be removed
    :param revision: revision object from the parent PG to the removal target
    :return ProcessGroupEntity: the updated entity object for the deleted PG
    """
    try:
        return nifi.ProcessgroupsApi().remove_process_group(
            id=process_group_id,
            version=revision.version,
            client_id=revision.client_id
        )
    except ApiException as e:
        raise ValueError(e.body)


def schedule_process_group(process_group_id, target_state):
    """
    Start or stop a Process Group and all children
    :param process_group_id: ID of the Process Group to Target
    :param target_state: Either 'RUNNING' or 'STOPPED'
    :return: dict of resulting process group state
    """
    # ideally this should be pulled from the client definition
    valid_states = ['STOPPED', 'RUNNING']
    if target_state not in valid_states:
        raise ValueError(
            "supplied state {0} not in valid states ({1})".format(
                target_state, valid_states
            )
        )
    try:
        return nifi.FlowApi().schedule_components(
            id=process_group_id,
            body={
                'id': process_group_id,
                'state': target_state
            }
        )
    except ApiException as e:
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
        return nifi.ProcessgroupsApi().create_process_group(
            id=parent_pg.id,
            body=nifi.ProcessGroupEntity(
                revision=parent_pg.revision,
                component=nifi.ProcessGroupDTO(
                    name=new_pg_name,
                    position=nifi.PositionDTO(
                        x=float(location[0]),
                        y=float(location[1])
                    )
                )
            )
        )
    except ApiException as e:
        raise e


def list_all_processor_types():
    """
    Produces the list of all available processor types in the NiFi instance
    :return ProcessorTypesEntity: Native Datatype containing list
    """
    try:
        return nifi.FlowApi().get_processor_types()
    except ApiException as e:
        raise e


def get_processor_type(identifier, identifier_type='name'):
    """
    Gets the abstract object describing a Processor, or list thereof
    :param identifier: String to search for
    :param identifier_type: Processor descriptor to search: bundle, name or tag
    :return: DocumentedTypeDTO if unique, None if not found, List if duplicate
    """
    valid_id_types = ['bundle', 'name', 'tag']
    if identifier_type not in valid_id_types:
        raise ValueError(
            "identifier_type not in valid list ({0})".format(
                identifier_type
            )
        )
    out = []
    all_p = list_all_processor_types().processor_types
    if identifier_type == 'name':
        out = [
            i for i in all_p if
            identifier in i.type
        ]
    if identifier_type == 'bundle':
        out = [
            i for i in all_p if
            identifier in i.bundle.artifact
        ]
    if identifier_type == 'tag':
        out = [
            i for i in all_p if
            identifier in str(i.tags)
        ]
    if not out:
        return None
    elif len(out) > 1:
        return out
    return out[0]


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
        target_config = nifi.ProcessorConfigDTO()
    else:
        target_config = config
    try:
        return nifi.ProcessgroupsApi().create_processor(
            id=parent_pg.id,
            body=nifi.ProcessorEntity(
                revision={'version': 0},
                component=nifi.ProcessorDTO(
                    position=nifi.PositionDTO(
                        x=float(location[0]),
                        y=float(location[1])
                    ),
                    type=processor.type,
                    name=processor_name,
                    config=target_config
                )
            )
        )
    except ApiException as e:
        raise ValueError(e.body)


def get_processor(identifier, identifier_type='name'):
    """
    Gets a deployed Processor, or list thereof
    :param identifier: String to filter on
    :param identifier_type: 'name' or 'id' to identify field to filter on
    :return:
    """
    valid_id_types = ['name', 'id']
    if identifier_type not in valid_id_types:
        raise ValueError(
            "invalid identifier_type. ({0}) not in ({1})".format(
                identifier_type, valid_id_types
            )
        )
    if identifier_type == 'name':
        out = [
            li for li in list_all_processors()
            if identifier in li.status.name
        ]
        if not out:
            return None
        elif len(out) > 1:
            return out
        return out[0]
    if identifier_type == 'id':
        return nifi.ProcessorsApi().get_processor(identifier)


def delete_processor(processor, refresh=True):
    """
    Removes a Processor from the Canvas
    :param processor: Processor Object to be removed
    :param refresh: True|False, whether to refresh the object state
    :return: ProcessorEntity with updated status etc.
    """
    try:
        if refresh:
            target_proc = get_processor(processor.id, 'id')
        else:
            target_proc = processor
        return nifi.ProcessorsApi().delete_processor(
            id=target_proc.id,
            version=target_proc.revision.version
        )
    except ApiException as e:
        raise ValueError(e.body)


def schedule_processor(processor, target_state, refresh=True):
    """
    Starts or Stops a given Processor.
    WARNING: Limited functionality and many uncontrolled edgecases!
    :param processor: Processor object to Schedule
    :param target_state: 'STOPPED' or 'RUNNING'
    :param refresh: True|False, whether to refresh the processor state
    :return: Updated ProcessorEntity
    """
    valid_states = ['STOPPED', 'RUNNING']
    if target_state not in valid_states:
        raise ValueError(
            "supplied state {0} not in valid states ({1})".format(
                target_state, valid_states
            )
        )
    try:
        if refresh:
            target_proc = get_processor(processor.id, 'id')
        else:
            target_proc = processor
        return nifi.ProcessorsApi().update_processor(
            id=target_proc.id,
            body=nifi.ProcessorEntity(
                revision=target_proc.revision,
                component=nifi.ProcessorDTO(
                    state=target_state,
                    id=target_proc.id
                ),
            )
        )
    except ApiException as e:
        raise ValueError(e.body)


def update_processor(processor, update):
    """
    Updates the configuration parameters of a stopped processor
    :param processor: Processor object to be updated
    :param update: ProcessorConfigDTO, updated configuration parameters
    :return: updated ProcessorEntity
    """
    if not isinstance(update, nifi.ProcessorConfigDTO):
        raise ValueError(
            "update param is not an instance of nifi.ProcessorConfigDTO"
        )
    try:
        return nifi.ProcessorsApi().update_processor(
            processor.id,
            body=nifi.ProcessorEntity(
                component=nifi.ProcessorDTO(
                    config=update,
                    id=processor.id
                ),
                revision=processor.revision,
            )
        )
    except ApiException as e:
        raise ValueError(e.body)


def get_variable_registry(process_group, ancestors=True):
    """
    Gets the contents of the variable registry attached to a Process Group
    :param process_group: ProcessGroup object
    :param ancestors: Whether to get the variables from parent Process Groups
    :return: VariableRegistryEntity
    """
    try:
        return nifi.ProcessgroupsApi().get_variable_registry(
            process_group.id,
            include_ancestor_groups=ancestors
        )
    except ApiException as e:
        raise ValueError(e.body)


def update_variable_registry(process_group, update):
    """
    Updates one or more key:value pairs in the variable registry
    :param process_group: ProcessGroup object to update the variables on
    :param update: (key,value) tuples of the variables to write to the registry
    :return: VariableRegistryEntity
    """
    if not isinstance(process_group, nifi.ProcessGroupEntity):
        raise ValueError(
            'param process_group is not a valid nifi.ProcessGroupEntity'
        )
    if not isinstance(update, list):
        raise ValueError(
            'param update is not a valid list of (key,value) tuples'
        )
    # Parse variable update into the datatype
    var_update = [
        nifi.VariableEntity(
            nifi.VariableDTO(
                name=li[0],
                value=li[1],
                process_group_id=process_group.id
            )
        ) for li in update
    ]
    try:
        return nifi.ProcessgroupsApi().update_variable_registry(
            id=process_group.id,
            body=nifi.VariableRegistryEntity(
                process_group_revision=process_group.revision,
                variable_registry=nifi.VariableRegistryDTO(
                    process_group_id=process_group.id,
                    variables=var_update
                )
            )
        )
    except ApiException as e:
        raise ValueError(e.body)
