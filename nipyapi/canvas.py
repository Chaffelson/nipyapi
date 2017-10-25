# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
STATUS: Work in Progress to determine pythonic datamodel
"""

from __future__ import absolute_import

from nipyapi import swagger_client


class Canvas:
    """
    Class to contain Wrapper methods for Canvas interaction
    """
    def __init__(self, host=None):
        """
        Constructor
        :param host: The NiFi host base url to talk to
        """
        if host is None:
            self.host = swagger_client.configuration.host
        else:
            self.host = host
            swagger_client.configuration.host = self.host

    @staticmethod
    def get_root_pg_id():
        """Simple Example function for wrapper demonstration"""
        con = swagger_client.FlowApi()
        pg_root = con.get_process_group_status('root')
        return pg_root.process_group_status.id

    @staticmethod
    def flow(pg_id='root'):
        """
        Returns information about a Process Group and its Flow
        :param pg_id: id of a Process Group, defaults to root if none supplied
        :returns: dict of the Process Group information
        """
        return Canvas._recurse_flows(pg_id)

    @staticmethod
    def process_group_status(pg_id='root', detail='names'):
        """
        Returns information about a Process Group
        :param pg_id: NiFi ID of the Process Groupt to retrieve
        :param detail: Level of detail to respond with, defaults to just names and NiFi IDs
        :return:
        """
        valid_details = ['names', 'all']
        if detail not in valid_details:
            raise ValueError(
                'detail requested ({0}) not in list of valid detail requests ({1})'.format(detail, valid_details)
            )
        raw = swagger_client.ProcessgroupsApi().get_process_group(id=pg_id)
        if detail is 'names':
            out = {
                raw.component.name: raw.component.id
            }
            return out
        elif detail is 'all':
            return raw

    @staticmethod
    def _recurse_flows(process_group_id='root'):
        """
        Returns a nested dict of the names and ids of all components
        :param process_group_id: ID of process group to treat as root of recursive fetch, or 'root' to fetch root
        :return:
        """
        from nipyapi.swagger_client import ProcessGroupFlowEntity, FlowDTO
        from nipyapi.swagger_client import ProcessGroupEntity, LabelEntity, FunnelEntity

        def _walk_flow(node):
            # This recursively unpacks the data models
            if isinstance(node, ProcessGroupFlowEntity):
                pg_detail = {
                    'name': node.process_group_flow.breadcrumb.breadcrumb.name,
                    'id': node.process_group_flow.breadcrumb.breadcrumb.id,
                    'uri': node.process_group_flow.uri,
                    'parent_group_id': node.process_group_flow.parent_group_id
                }
                # there doesn't appear to be a command to fetch everything at once
                # so we have to recurse down the chain of process_groups
                pg_detail.update(_walk_flow(node.process_group_flow.flow))
                return pg_detail
            elif isinstance(node, FlowDTO):
                # We have to use getattr here to retain the custom data type
                # Each category (k) is a list of dicts, thus the complex comprehension
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
                out.update(_walk_flow(swagger_client.FlowApi().get_flow(node.id)))
                return out
            elif isinstance(node, LabelEntity) or isinstance(node, FunnelEntity):
                return {k: v for k, v in node.component.to_dict().items() if k in ['id', 'label']}
            else:
                # otherwise parse out the name/id of the various components
                return {k: v for k, v in node.status.to_dict().items() if k in ['id', 'name']}

        return _walk_flow(swagger_client.FlowApi().get_flow(process_group_id))

    @staticmethod
    def get_process_group_by_name(pg_name):
        """
        Retrieves a specific process group by name, if it exists
        """
        out = [
            li for li in Canvas.list_all_process_groups()
            if li['name'] == pg_name
        ]
        if len(out) is 1:
            return out[0]
        else:
            return None

    @staticmethod
    def list_all_process_groups():
        """
        Returns a flattened list of all Process groups as {id:name} dicts
        :return:
        """
        def _pg_list(pg_flow):
            r = []
            for li in pg_flow['process_groups']:
                r.append(
                    {
                        'id': li['id'],
                        'name': li['name']
                     }
                )
                r += _pg_list(li)
            return r
        return _pg_list(Canvas.flow())
