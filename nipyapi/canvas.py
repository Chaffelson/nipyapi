# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
STATUS: Work in Progress to determine pythonic datamodel
"""

from __future__ import absolute_import
from swagger_client import ProcessGroupFlowEntity, FlowDTO
from swagger_client import ProcessGroupEntity, LabelEntity
from swagger_client import FunnelEntity, FlowApi
from swagger_client import ProcessgroupsApi


def get_root_pg_id():
    """Simple Example function for wrapper demonstration"""
    con = FlowApi()
    pg_root = con.get_process_group_status('root')
    return pg_root.process_group_status.id


def flow(pg_id='root'):
    """
    Returns information about a Process Group and its Flow
    :param pg_id: id of a Process Group, defaults to root if none supplied
    :returns: dict of the Process Group information
    """
    return _recurse_flows(pg_id)


def process_group_status(pg_id='root', detail='names'):
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
    raw = ProcessgroupsApi().get_process_group(id=pg_id)
    if detail == 'names':
        out = {
            raw.component.name: raw.component.id
        }
        return out
    elif detail == 'all':
        return raw


def _recurse_flows(process_group_id='root'):
    """
    Returns a nested dict of the names and ids of all components
    :param process_group_id: ID of process group to treat as root of
        recursive fetch, or 'root' to fetch root
    :return:
    """
    def _walk_flow(node):
        # This recursively unpacks the data models
        if isinstance(node, ProcessGroupFlowEntity):
            pg_detail = {
                'name': node.process_group_flow.breadcrumb.breadcrumb.name,
                'id': node.process_group_flow.breadcrumb.breadcrumb.id,
                'uri': node.process_group_flow.uri,
                'parent_group_id': node.process_group_flow.parent_group_id
            }
            # there doesn't appear to be a command to fetch everything
            # so we have to recurse down the chain of process_groups
            pg_detail.update(_walk_flow(node.process_group_flow.flow))
            return pg_detail
        elif isinstance(node, FlowDTO):
            # We have to use getattr here to retain the custom data type
            # Each category (k) is a list of dicts
            return {
                k: [
                    _walk_flow(li) for li in getattr(node, k)
                ] for k in
                node.to_dict().keys()
            }
        elif isinstance(node, ProcessGroupEntity):
            # The Revision information is needed for creating snippets
            # it's only available from the parent process group flow info
            out = {
                'revision': node.revision
            }
            # recurse into the nested process group
            out.update(
                _walk_flow(FlowApi().get_flow(node.id))
            )
            return out
        elif isinstance(node, (LabelEntity, FunnelEntity)):
            return {
                k: v for
                k, v in
                node.component.to_dict().items() if
                k in ['id', 'label']
            }
        return {
            k: v for
            k, v in
            node.status.to_dict().items() if
            k in ['id', 'name']
        }

    return _walk_flow(FlowApi().get_flow(process_group_id))


def get_process_group_by_name(pg_name):
    """
    Retrieves a specific process group by name, if it exists
    """
    out = [
        li for li in list_all_process_groups()
        if li['name'] == pg_name
    ]
    if len(out) is 1:
        return out[0]
    return None


def list_all_process_groups():
    """
    Returns a flattened list of all Process groups as {id:name} dicts
    :return:
    """
    def _pg_list(pg_flow):
        out = []
        for item in pg_flow['process_groups']:
            out.append({
                'id': item['id'],
                'name': item['name'],
                'revision': item['revision']
            })
            # Not using += here due to bug in pylint
            # https://github.com/PyCQA/pylint/issues/1462
            out = out + _pg_list(item)
        return out
    return _pg_list(flow())


def delete_process_group(process_group_id, revision):
    """
    deletes a specific process group
    :param process_group_id:
    :param revision:
    :return None:
    """
    ProcessgroupsApi().remove_process_group(
        id=process_group_id,
        version=revision.version,
        client_id=revision.client_id
    )
