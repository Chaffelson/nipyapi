# -*- coding: utf-8 -*-

"""
For managing flow deployments
"""

from __future__ import absolute_import
from os import access, R_OK, W_OK
from os.path import isfile, dirname
from urllib3 import PoolManager
from lxml import etree
from . import nifi
from nipyapi.nifi.rest import ApiException
from nipyapi.config import nifi_config
from nipyapi.canvas import get_process_group


__all__ = [
    "all_templates", "get_template_by_name", "deploy_template",
    "upload_template", "create_pg_snippet", "create_template",
    "delete_template", "export_template"
]


def all_templates():
    """
    Returns all Templates
    :return:
    """
    return nifi.FlowApi().get_templates()


def get_template_by_name(name):
    """
    Returns a specific template by name, if it exists
    :param name: String of the template name, exact matching
    :return TemplateEntity:
    """
    out = [
        i for i in
        all_templates().templates
        if
        name == i.template.name
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
    resp = nifi.ProcessgroupsApi().instantiate_template(
        id=pg_id,
        body=req
    )
    return resp


def create_pg_snippet(pg_id):
    """
    Creates a snippet of the targetted process group, and returns the object
    :param pg_id: ID of the process Group to snippet
    :return: Snippet Object
    """
    target_pg = get_process_group(pg_id, 'id')
    new_snippet_req = nifi.SnippetEntity(
        snippet={
            'processGroups': {
                target_pg.id: target_pg.revision
            },
            'parentGroupId':
                target_pg.nipyapi_extended.process_group_flow.parent_group_id
        }
    )
    snippet_resp = nifi.SnippetsApi().create_snippet(
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
    snippet = create_pg_snippet(pg_id)
    new_template = nifi.CreateTemplateRequestEntity(
        name=str(name),
        description=str(desc),
        snippet_id=snippet.snippet.id
    )
    resp = nifi.ProcessgroupsApi().create_template(
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
        nifi.TemplatesApi().remove_template(id=t_id)
    except ApiException as err:
        raise ValueError(err.body)


def upload_template(pg_id, template_file):
    """
    Uploads a template file (template.xml) to the given process group
    :param pg_id: The NiFi ID of the process group to target
    :param template_file: the template file (template.xml)
    :return:
    """
    # Ensure we are receiving a valid file
    assert isfile(template_file) and access(template_file, R_OK), \
        SystemError("File {0} invalid or unreadable".format(template_file))
    # Test for expected Template XML elements
    tree = etree.parse(template_file)
    root_tag = tree.getroot().tag
    if root_tag != 'template':
        raise TypeError(
            "Expected 'template' as xml root element, got ({0}) instead."
            "Are you sure this is a Template?"
                .format(root_tag)
        )
    # NiFi-1.2.0 method
    resp = nifi.ProcessgroupsApi().upload_template(
        id=pg_id,
        template=template_file
    )
    return resp


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
    if output not in valid_output_types:
        raise ValueError(
            "Output type {0} not valid for ({1})".format(
                output, valid_output_types
            )
        )
    con = PoolManager()
    url = nifi_config.host + '/templates/' + t_id + '/download'
    response = con.request('GET', url, preload_content=False)
    template_xml = etree.fromstring(response.data)
    if output == 'string':
        return etree.tostring(template_xml, encoding='utf8', method='xml')
    if output == 'file':
        assert access(dirname(file_path), W_OK), \
            "File_path {0} is inaccessible or not writable".format(file_path)
        xml_tree = etree.ElementTree(template_xml)
        xml_tree.write(file_path)
        return file_path
