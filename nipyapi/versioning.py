# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Registry Service and related functions
"""

from __future__ import absolute_import
from . import nifi, config, registry, canvas
from nipyapi.nifi.rest import ApiException as ApiExceptionN
from nipyapi.registry.rest import ApiException as ApiExceptionR

__all__ = [
    'create_registry_client', 'list_registry_clients',
    'delete_registry_client', 'get_registry_client', 'list_registry_buckets',
    'create_registry_bucket', 'delete_registry_bucket', 'get_registry_bucket',
    'save_flow_ver', 'list_flows_in_bucket', 'get_flow_in_bucket',
    'get_latest_flow_ver', 'update_flow_ver', 'get_version_info',
    'create_flow', 'create_flow_version'
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
    except ApiExceptionN as e:
        raise ValueError(e.body)


def delete_registry_client(client):
    try:
        return nifi.ControllerApi().delete_registry_client(
            id=client.id,
            version=client.revision.version
        )
    except ApiExceptionN as e:
        raise ValueError(e.body)


def list_registry_clients():
    try:
        return nifi.ControllerApi().get_registry_clients()
    except ApiExceptionN as e:
        raise ValueError(e.body)


def get_registry_client(identifier, identifier_type='name'):
    valid_id_types = ['name', 'id']
    if identifier_type not in valid_id_types:
        raise ValueError(
            "invalid identifier_type. ({0}) not in ({1})".format(
                identifier_type, valid_id_types
            )
        )
    all_rcs = list_registry_clients()
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


def list_registry_buckets():
    try:
        return registry.BucketsApi().get_buckets()
    except ApiExceptionR as e:
        raise ValueError(e.body)


def create_registry_bucket(name):
    try:
        return registry.BucketsApi().create_bucket(
            body={
                'name': name
            }
        )
    except ApiExceptionR as e:
        raise ValueError(e.body)


def delete_registry_bucket(bucket):
    try:
        return registry.BucketsApi().delete_bucket(
            bucket_id=bucket.identifier
        )
    except ApiExceptionR as e:
        raise ValueError(e.body)


def get_registry_bucket(identifier, identifier_type='name'):
    valid_id_types = ['name', 'id']
    if identifier_type not in valid_id_types:
        raise ValueError(
            "invalid identifier_type. ({0}) not in ({1})".format(
                identifier_type, valid_id_types
            )
        )
    try:
        if identifier_type == 'name':
            out = [
                li for li in list_registry_buckets()
                if identifier in li.name
            ]
            if not out:
                return None
            elif len(out) > 1:
                return out
            return out[0]
        if identifier_type == 'id':
            return registry.BucketsApi().get_bucket(identifier)
    except ApiExceptionR as e:
        raise ValueError(e.body)


def list_flows_in_bucket(bucket_id):
    try:
        return registry.BucketFlowsApi().get_flows(bucket_id)
    except ApiExceptionR as e:
        raise ValueError(e.body)


def get_flow_in_bucket(bucket_id, identifier, identifier_type='name'):
    valid_id_types = ['name', 'id']
    if identifier_type not in valid_id_types:
        raise ValueError(
            "invalid identifier_type. ({0}) not in ({1})".format(
                identifier_type, valid_id_types
            )
        )
    try:
        if identifier_type == 'id':
            return registry.BucketFlowsApi().get_flow(bucket_id, identifier)
        if identifier_type == 'name':
            out = [
                li for li in list_flows_in_bucket(bucket_id)
                if identifier in li.name
            ]
            if not out:
                return None
            elif len(out) > 1:
                return out
            return out[0]
    except ApiExceptionR as e:
        raise ValueError(e.body)


def save_flow_ver(process_group, registry_client, bucket, flow_name=None,
                  flow_id=None, comment='', desc=''):
    try:
        return nifi.VersionsApi().save_to_flow_registry(
            id=process_group.id,
            body=nifi.StartVersionControlRequestEntity(
                process_group_revision=process_group.revision,
                versioned_flow=nifi.VersionedFlowDTO(
                    bucket_id=bucket.identifier,
                    comments=comment,
                    description=desc,
                    flow_name=flow_name,
                    flow_id=flow_id,
                    registry_id=registry_client.id
                )
            )
        )
    except ApiExceptionN as e:
        raise ValueError(e.body)


def stop_flow_ver(process_group, refresh=True):
    try:
        if refresh:
            target_pg = canvas.get_process_group(process_group.id, 'id')
        else:
            target_pg = process_group
        return nifi.VersionsApi().stop_version_control(
            id=target_pg.id,
            version=target_pg.revision.version
        )
    except ApiExceptionN as e:
        raise ValueError(e.body)


def revert_flow_ver(process_group):
    # ToDo: Add handling for flows with live data
    try:
        return nifi.VersionsApi().initiate_revert_flow_version(
            id=process_group.id,
            body=nifi.VersionsApi().get_version_information(process_group.id)
        )
    except ApiExceptionN as e:
        raise ValueError(e.body)


def update_flow_ver(process_group, registry_client, flow,
                    update_children=False):
    # TODO: This needs a lot more investigation
    # This function is more complicated than expected, so leaving it for the
    # next release
    pass
    # try:
    #     return nifi.VersionsApi().update_flow_version(
    #         id=process_group.id,
    #         body=nifi.VersionedFlowSnapshotEntity(
    #             process_group_revision=process_group.revision,
    #             registry_id=registry_client.id,
    #             update_descendant_versioned_flows=update_children,
    #             versioned_flow_snapshot=get_latest_flow_ver(
    #                 bucket_id=flow.bucket_identifier,
    #                 flow_id=flow.identifier
    #             )
    #         )
    #     )
    # except ApiExceptionN as e:
    #     raise ValueError(e.body)


def get_latest_flow_ver(bucket_id, flow_id):
    try:
        return registry.BucketFlowsApi().get_latest_flow_version(
            bucket_id, flow_id
        )
    except ApiExceptionR as e:
        raise ValueError(e.body)


def get_version_info(process_group):
    try:
        return nifi.VersionsApi().get_version_information(
            process_group.id
        )
    except ApiExceptionN as e:
        raise ValueError(e.body)


def create_flow(bucket_id, flow_name, flow_desc='', flow_type='Flow'):
    try:
        return registry.BucketFlowsApi().create_flow(
            bucket_id=bucket_id,
            body=registry.VersionedFlow(
                name=flow_name,
                description=flow_desc,
                bucket_identifier=bucket_id,
                type=flow_type
            )
        )
    except ApiExceptionR as e:
        raise ValueError(e.body)


def create_flow_version(bucket_id, flow, flow_snapshot):
    try:
        return registry.BucketFlowsApi().create_flow_version(
            bucket_id=bucket_id,
            flow_id=flow.identifier,
            body=registry.VersionedFlowSnapshot(
                flow_contents=flow_snapshot.flow_contents,
                snapshot_metadata=registry.VersionedFlowSnapshotMetadata(
                    version=flow.version_count + 1
                ),
            )
        )
    except ApiExceptionR as e:
        raise ValueError(e.body)
