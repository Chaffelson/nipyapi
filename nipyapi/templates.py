# -*- coding: utf-8 -*-

"""
For managing flow deployments
"""

from __future__ import absolute_import
from os import access, R_OK, W_OK
from os.path import isfile, dirname
from urllib3 import PoolManager
from lxml.etree import tostring, fromstring, ElementTree
from swagger_client import FlowApi, ProcessgroupsApi, SnippetEntity
from swagger_client import SnippetsApi, TemplatesApi
from swagger_client import CreateTemplateRequestEntity
from swagger_client import configuration
from swagger_client.rest import ApiException
from nipyapi import canvas


def all_templates():
    """
    Returns all Templates
    :return:
    """
    return FlowApi().get_templates()


def get_template_by_name(name):
    """
    Returns a specific template by name, if it exists
    :param name:
    :return:
    """
    out = [
        i for i in
        all_templates().to_dict()['templates']
        if
        name == i['template']['name']
    ]
    if len(out) is 1:
        return out[0]
    return None


def deploy_template(pg_id, template_id, loc_x=0, loc_y=0):
    """
    Instantiates a given template request in a given process group
    :param pg_id: ID of the process group to be parent
    :param template_id: ID of the template to be deployed
    :param loc_x: x-axis location of the template
    :param loc_y: y-axis location of the template
    :return: dict of the server response
    """
    from swagger_client import InstantiateTemplateRequestEntity
    req = InstantiateTemplateRequestEntity(
        origin_x=loc_x,
        origin_y=loc_y,
        template_id=template_id
    )
    resp = ProcessgroupsApi().instantiate_template(
        id=pg_id,
        body=req
    )
    return resp


def upload_template(pg_id, template_file):
    """
    Uploads a template file (template.xml) to the given process group
    :param pg_id: The NiFi ID of the process group to target
    :param template_file: the template file (template.xml)
    :return:
    """
    assert isfile(template_file) and access(template_file, R_OK), \
        SystemError("File {0} invalid or unreadable".format(template_file))
    resp = ProcessgroupsApi().upload_template(
        id=pg_id,
        template=template_file
    )
    return resp


def make_pg_snippet(pg_id):
    """
    Creates a snippet of the targetted process group, and returns the object
    :param pg_id: ID of the process Group to snippet
    :return: Snippet Object
    """
    # Get the targeted process group
    target_pg = canvas.get_flow(pg_id)
    # get it's parent process group so we get the revision information
    parent_pg = canvas.get_flow(target_pg['parent_group_id'])
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
    snippet_resp = SnippetsApi().create_snippet(
        new_snippet_req
    )
    return snippet_resp


def create_template(pg_id, name, desc=''):
    """
    Turns a process group into a Template
    :param pg_id: NiFi ID of the Process Group to Template
    :param name: Unique Name of the Template
    :param desc: Description of the Template
    :return: dict of Template information
    """
    snippet = make_pg_snippet(pg_id)
    new_template = CreateTemplateRequestEntity(
        name=str(name),
        description=str(desc),
        snippet_id=snippet.snippet.id
    )
    resp = ProcessgroupsApi().create_template(
        id=snippet.snippet.parent_group_id,
        body=new_template
    )
    return resp


def delete_template(t_id):
    """
    Deletes a Template
    :param t_id: ID of the Template to be deleted
    :return:
    """
    try:
        TemplatesApi().remove_template(id=t_id)
    except ApiException as err:
        raise ValueError(err.body)


def export_template(t_id, output='string', file_path=None):
    """
    Exports a template as a string of xml
    :param t_id: ID of the template to export
    :param output: string of return type of template, 'str' or 'file'
    :param file_path: if file output type, the path and filename to write to
    :return: basestring of the xml template or file path written
    """
    # TemplatesAPI.export template is broken in swagger definition of NiFi1.2
    # return TemplateDTO is replaced by return string in a later version
    valid_output_types = ['file', 'string']
    con = PoolManager()
    url = configuration.host + '/templates/' + t_id + '/download'
    response = con.request('GET', url, preload_content=False)
    template_xml = fromstring(response.data)
    if output == 'string':
        return tostring(template_xml, encoding='utf8', method='xml')
    elif output == 'file':
        assert access(dirname(file_path), W_OK), \
            "File_path {0} is inaccessible or not writable".format(file_path)
        xml_tree = ElementTree(template_xml)
        xml_tree.write(file_path)
        return file_path
    else:
        raise ValueError(
            "Output type {0} not part of valid list ({1})".format(
                output, valid_output_types
            )
        )
