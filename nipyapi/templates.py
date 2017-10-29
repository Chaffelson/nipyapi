# -*- coding: utf-8 -*-

"""
For managing flow deployments
"""

from __future__ import absolute_import

from nipyapi import swagger_client


class Templates(object):
    """
    Class to contain Wrapper methods for Template interaction
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
    def all_templates():
        """
        Returns all Templates
        :return:
        """
        return swagger_client.FlowApi().get_templates()

    @staticmethod
    def get_template_by_name(name):
        """
        Returns a specific template by name, if it exists
        :param name:
        :return:
        """
        out = [
            i for i in
            Templates.all_templates().to_dict()['templates']
            if
            name == i['template']['name']
        ]
        if len(out) is 1:
            return out[0]
        else:
            raise ValueError("Expected exactly 1 Template named ({0}), "
                             "found ({1}) instead"
                             .format(name, len(out)))

    @staticmethod
    def deploy_template(pg_id, template_id, loc_x=0, loc_y=0):
        """
        Instantiates a given template request in a given process group
        :param pg_id: The NiFi ID of the process Group to target
        :param template_config: the template request form
        :return:
        """
        from nipyapi.swagger_client import InstantiateTemplateRequestEntity
        # TODO: Test for valid template config
        # TODO: Test response
        req = InstantiateTemplateRequestEntity(
            origin_x=loc_x,
            origin_y=loc_y,
            template_id=template_id
        )
        resp = swagger_client.ProcessgroupsApi().instantiate_template(
            id=pg_id,
            body=req
        )
        return resp

    @staticmethod
    def upload_template(pg_id, template_file):
        """
        Uploads a template file (template.xml) to the given process group
        :param pg_id: The NiFi ID of the process group to target
        :param template_file: the template file (template.xml)
        :return:
        """
        # TODO: Test for valid template.xml
        # TODO: Test response
        resp = swagger_client.ProcessgroupsApi().upload_template(
            id=pg_id,
            template=template_file
        )
        return resp

    # @staticmethod
    # def export_template(t_id):
    #     """
    #     Exports a given template
    #     :param t_id: NiFi ID of the Template
    #     :return:
    #     """
    #     template_file = swagger_client.TemplatesApi().export_template(
    #         id=t_id
    #     )
    #     return None

    @staticmethod
    def _make_pg_snippet(pg_id):
        from nipyapi import Canvas
        from nipyapi.swagger_client import SnippetEntity
        # TODO: Validate inputs
        # Get the targeted process group
        target_pg = Canvas().flow(pg_id)
        # get it's parent process group so we get the revision information
        parent_pg = Canvas().flow(target_pg['parent_group_id'])
        enriched_target_pg = [
            li for li in
            parent_pg['process_groups'] if
            li['id'] == pg_id
        ][0]
        new_snippet_req = SnippetEntity()
        new_snippet_req.snippet = {
            'processGroups': {
                enriched_target_pg['id']: enriched_target_pg['revision']
            },
            'parentGroupId': enriched_target_pg['parent_group_id']
        }
        snippet_resp = swagger_client.SnippetsApi().create_snippet(
            new_snippet_req
        )
        return snippet_resp

    @staticmethod
    def create_template(pg_id, name, desc=''):
        """
        Turns a process group into a Template
        :param pg_id: NiFi ID of the Process Group to Template
        :param name: Unique Name of the Template
        :param desc: Description of the Template
        :return: dict of Template information
        """
        from nipyapi.swagger_client import ProcessgroupsApi
        from nipyapi.swagger_client import CreateTemplateRequestEntity
        # TODO: Ensure unique Template names
        # TODO: Validate inputs
        snippet = Templates._make_pg_snippet(pg_id)
        new_template = CreateTemplateRequestEntity(
            name=name,
            description=desc,
            snippet_id=snippet.snippet.id
        )
        resp = ProcessgroupsApi().create_template(
            id=snippet.snippet.parent_group_id,
            body=new_template
        )
        return resp

    @staticmethod
    def delete_template(t_id):
        """
        Delets a Template
        :param t_id: ID of the Template to be deleted
        :return:
        """
        from nipyapi.swagger_client.rest import ApiException
        try:
            swagger_client.TemplatesApi().remove_template(id=t_id)
        except ApiException as err:
            raise ValueError(err.body)
