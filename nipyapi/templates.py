# -*- coding: utf-8 -*-

"""
For managing flow deployments
"""

from __future__ import absolute_import
from os import access, R_OK, W_OK
from os.path import isfile, dirname
import logging
import six
from lxml import etree
import nipyapi

log = logging.getLogger(__name__)

__all__ = [
    "list_all_templates", "get_template_by_name", "deploy_template",
    "upload_template", "create_pg_snippet", "create_template",
    "delete_template", "export_template", 'get_template'
]


def get_template_by_name(name):
    """
    DEPRECATED
    Returns a specific template by name, if it exists.

    Note: This function is replaced by get_template

    Args:
        name (str): The Name of the template, exact match required

    Returns:
        (TemplateEntity)

    """
    out = [
        i for i in
        list_all_templates().templates
        if
        name == i.template.name
    ]
    if len(out) is 1:
        return out[0]
    return None


def get_template(identifier, identifier_type='name'):
    """
    Filters the list of all Templates for a given string in a given field.
    Note that filters are configured in config.py

    Args:
        identifier (str): The string to filter on
        identifier_type (str): The identifier of the field to filter on

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches

    """
    assert isinstance(identifier, six.string_types)
    assert identifier_type in ['name', 'id']
    try:
        obj = nipyapi.templates.list_all_templates().templates
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
    if obj:
        return nipyapi.utils.filter_obj(obj, identifier, identifier_type)
    return obj


def deploy_template(pg_id, template_id, loc_x=0, loc_y=0):
    """
    Instantiates a given template request in a given process group

    Args:
        pg_id (str): The UUID of the Process Group to deploy into
        template_id (str): The UUID of the Template to deploy. Note that the
            Template must already be uploaded and available to the target
            Process Group
        loc_x (int): The X coordinate to deploy the Template at. Default(0)
        loc_y (int): The X coordinate to deploy the Template at. Default(0)

    Returns:
        (FlowEntity): The FlowEntity of the Process Group with the deployed
            template

    """
    try:
        return nipyapi.nifi.ProcessgroupsApi().instantiate_template(
            id=pg_id,
            body=nipyapi.nifi.InstantiateTemplateRequestEntity(
                origin_x=loc_x,
                origin_y=loc_y,
                template_id=template_id
            )
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def create_pg_snippet(pg_id):
    """
    Creates a snippet of the targeted process group, and returns the object
    ready to be turned into a Template

    Args:
        pg_id: UUID of the process Group to snippet

    Returns:
        (SnippetEntity): The Snippet Object
    """
    target_pg = nipyapi.canvas.get_process_group(pg_id, 'id')
    new_snippet_req = nipyapi.nifi.SnippetEntity(
        snippet={
            'processGroups': {
                target_pg.id: target_pg.revision
            },
            'parentGroupId':
                target_pg.component.parent_group_id
        }
    )
    snippet_resp = nipyapi.nifi.SnippetsApi().create_snippet(
        new_snippet_req
    )
    return snippet_resp


def create_template(pg_id, name, desc=''):
    """
    Creates a Template from a Process Group

    Args:
        pg_id (str): The UUID of the target Process Group
        name (str): The name for the new Template. Must be unique
        desc (optional[str]): The description for the new Template

    Returns:
        (TemplateEntity): The newly created Template

    """
    snippet = create_pg_snippet(pg_id)
    new_template = nipyapi.nifi.CreateTemplateRequestEntity(
        name=str(name),
        description=str(desc),
        snippet_id=snippet.snippet.id
    )
    return nipyapi.nifi.ProcessgroupsApi().create_template(
        id=snippet.snippet.parent_group_id,
        body=new_template
    )


def delete_template(t_id):
    """
    Deletes a Template

    Args:
        t_id (str): UUID of the Template to be deleted

    Returns:
        The updated Template object
    """
    try:
        return nipyapi.nifi.TemplatesApi().remove_template(id=t_id)
    except nipyapi.nifi.rest.ApiException as err:
        raise ValueError(err.body)


def upload_template(pg_id, template_file):
    """
    Uploads a given template xml from from the file system to the given
    Process Group

    Args:
        pg_id (str): The UUID of the Process Group to upload to
        template_file (str): The path including filename to the template file

    Returns:
        (TemplateEntity): The new Template object

    """
    # TODO: Consider reworking to allow import from string by using tmpfile
    log.info("Called upload_template against endpoint %s with args %s",
             nipyapi.config.nifi_config.api_client.host, locals())
    # Ensure we are receiving a valid file
    assert isfile(template_file) and access(template_file, R_OK), \
        SystemError("File {0} invalid or unreadable".format(template_file))
    # Test for expected Template XML elements
    tree = etree.parse(template_file)
    root_tag = tree.getroot().tag
    if root_tag != 'template':
        raise TypeError(
            "Expected 'template' as xml root element, got {0} instead."
            "Are you sure this is a Template?"
            .format(root_tag)
        )
    t_name = tree.find('name').text
    try:
        this_pg = nipyapi.canvas.get_process_group(pg_id, 'id')
        assert isinstance(this_pg, nipyapi.nifi.ProcessGroupEntity)
        # For some reason identical code that produces the duplicate error
        # in later versions is going through OK for NiFi-1.1.2
        # The error occurs as normal in Postman, so not sure what's going on
        # Will force this error for consistency until it can be investigated
        if nipyapi.templates.get_template(t_name):
            raise ValueError('A template named {} already exists.'
                             .format(t_name))
        nipyapi.nifi.ProcessgroupsApi().upload_template(
            id=this_pg.id,
            template=template_file
        )
        return nipyapi.templates.get_template(
            tree.find('name').text
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def export_template(t_id, output='string', file_path=None):
    """
    Exports a given Template as either a string or a file.

    Note that to reimport the Template it must be a file

    Args:
        t_id (str): The UUID of the Template to export
        output (str): 'string' or 'file' to set the export action
        file_path (Optional [str]): The full path including filename to write
            the Template export to

    Returns:
        (str): A String representation of the exported Template XML. Note
            that this may not be utf-8 encoded.

    """
    assert output in ['string', 'file']
    assert file_path is None or isinstance(file_path, six.string_types)
    template = nipyapi.templates.get_template(t_id, 'id')
    assert isinstance(template, nipyapi.nifi.TemplateEntity)
    obj = nipyapi.nifi.TemplatesApi().export_template(t_id)
    assert isinstance(obj, six.string_types)
    assert obj[0] == '<'
    if output == 'string':
        return obj
    if output == 'file':
        assert access(dirname(file_path), W_OK), \
            "File_path {0} is inaccessible or not writable".format(file_path)
        nipyapi.utils.fs_write(obj, file_path)
        return obj


def list_all_templates():
    """
    Gets a list of all templates on the canvas

    Returns:
        (list[TemplateEntity]): A list of TemplateEntity's
    """
    try:
        return nipyapi.nifi.FlowApi().get_templates()
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)
