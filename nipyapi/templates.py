# -*- coding: utf-8 -*-

"""
For managing flow deployments
"""

from __future__ import absolute_import

from nipyapi import swagger_client


def templates():
    """
    Returns all Templates
    :return:
    """
    return swagger_client.FlowApi().get_templates()


def deploy_template(pg_id, template_config):
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


def upload_template(pg_id, template_file):
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


def export_template(t_id):
    """
    Exports a given template
    :param t_id: NiFi ID of the Template
    :return:
    """
    template_file = swagger_client.TemplatesApi().export_template(
        id=t_id
    )


# TODO: Work on snippets
