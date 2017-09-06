# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
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

    @staticmethod
    def get_root_pg_id():
        """Simple Example function for wrapper demonstration"""
        con = swagger_client.FlowApi()
        pg_root = con.get_process_group_status('root')
        return pg_root.process_group_status.id

    @staticmethod
    def flow(pg='root'):
        """
        Returns information about a Process Group and its Flow
        :param pg: string of name or id of a Process Group, defaults to root if none supplied
        :returns: dict of the Process Group information
        """
        return swagger_client.FlowApi().get_flow(pg)

    @staticmethod
    def templates():
        """
        Returns all Templates
        :return:
        """
        return swagger_client.FlowApi().get_templates()

    @staticmethod
    def process_group(nid='root'):
        """
        Returns information about a Process Group
        :return:
        """
        return swagger_client.ProcessgroupsApi().get_process_group(id=nid)

    def deploy_template(self, pg_id, template_config):
        """
        Instantiates a given template request in a given process group
        :param pg_id: The NiFi ID of the process Group to target for the template
        :param template_config: the template request form
        :return:
        """
        # TODO: Test for valid template config
        # TODO: Test response
        _ = swagger_client.ProcessgroupsApi().instantiate_template(
            id=pg_id,
            body=template_config
        )

    def upload_template(self, pg_id, template_file):
        """
        Uploads a template file (template.xml) to the given process group
        :param pg_id: The NiFi ID of the process group to target for the template
        :param template_file: the template file (template.xml)
        :return:
        """
        # TODO: Test for valid template.xml
        # TODO: Test response
        _ = swagger_client.ProcessgroupsApi().upload_template(
            id=pg_id,
            template=template_file
        )

    def export_template(self, t_id):
        """
        Exports a given template
        :param t_id: NiFi ID of the Template
        :return:
        """
        template_file = swagger_client.TemplatesApi().export_template(
            id=t_id
        )
