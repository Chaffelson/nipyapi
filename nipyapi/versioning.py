# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Registry Service and related functions
"""

from __future__ import absolute_import
from . import nifi, config
from nipyapi.nifi.rest import ApiException

__all__ = [
    'create_registry_client', 'list_all_registry_clients',
    'delete_registry_client', 'get_registry_client'
]


def create_registry_client(name, uri, description):
    try:
        return nifi.ControllerApi().create_registry_client(
            body={
                'component': {
                    'uri': uri,
                    'name': name,
                    'description': description
                },
                'revision': {
                    'version': 0
                }
            }
        )
    except ApiException as e:
        raise ValueError(e.body)


def delete_registry_client(client):
    try:
        return nifi.ControllerApi().delete_registry_client(
            id=client.id,
            version=client.revision.version
        )
    except ApiException as e:
        raise ValueError(e.body)


def list_all_registry_clients():
    return nifi.ControllerApi().get_registry_clients()


def get_registry_client(identifier, identifier_type='name'):
    # TODO: This duplicates functionality from canvas, consider a common func
    valid_id_types = ['name', 'id']
    if identifier_type not in valid_id_types:
        raise ValueError(
            "invalid identifier_type. ({0}) not in ({1})".format(
                identifier_type, valid_id_types
            )
        )
    all_rcs = list_all_registry_clients()
    if identifier_type == 'name':
        out = [
            li for li in all_rcs.registries
            if identifier in li.component.name
        ]
    elif identifier_type == 'id':
        out = [
            li for li in all_rcs.registries
            if identifier in li.id
        ]
    else:
        out = []
    if not out:
        return None
    elif len(out) > 1:
        return out
    return out[0]
