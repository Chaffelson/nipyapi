# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Registry Service and related functions
"""

from __future__ import absolute_import
from nipyapi import nifi, registry, canvas, _utils
from nipyapi.nifi.rest import ApiException as ApiExceptionN
from nipyapi.registry.rest import ApiException as ApiExceptionR

__all__ = [
    'create_registry_client', 'list_registry_clients',
    'delete_registry_client', 'get_registry_client', 'list_registry_buckets',
    'create_registry_bucket', 'delete_registry_bucket', 'get_registry_bucket',
    'save_flow_ver', 'list_flows_in_bucket', 'get_flow_in_bucket',
    'get_latest_flow_ver', 'update_flow_ver', 'get_version_info',
    'create_flow', 'create_flow_version', 'get_flow_version', 'export_flow',
    'import_flow'
]


def create_registry_client(name, uri, description):
    """
    Creates a Registry Client in the NiFi Controller Services
    :param name: String, name of the client
    :param uri: String, URI such as 'http://registry:18080'
    :param description: String, Describe your client
    :return: RegistryClientEntity
    """
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
    """
    Deletes a Registry Client from the list of NiFI Controller Services
    :param client: RegistryClientEntity to be deleted
    :return: updated RegistryClientEntity
    """
    try:
        return nifi.ControllerApi().delete_registry_client(
            id=client.id,
            version=client.revision.version
        )
    except (ApiExceptionN, AttributeError) as e:
        raise ValueError(e)


def list_registry_clients():
    """
    Lists available Registry Clients in the NiFi Controller Services
    :return: list of RegistryClientEntity objects
    """
    try:
        return nifi.ControllerApi().get_registry_clients()
    except ApiExceptionN as e:
        raise ValueError(e.body)


def get_registry_client(identifier, identifier_type='name'):
    """
    Filters the Registry clients to a particular identifier
    :param identifier: String, the filter string
    :param identifier_type: String, the parameter to filter on, 'name' or 'id'
    :return: None if 0 matches, list if > 1, RegistryClientEntity if ==1
    """
    try:
        obj = list_registry_clients().registries
    except ApiExceptionR as e:
        raise ValueError(e.body)
    return _utils.filter_obj(obj, identifier, identifier_type)


def list_registry_buckets():
    """
    Lists all available Buckets in the NiFi Registry
    :return: list of Bucket objects
    """
    try:
        return registry.BucketsApi().get_buckets()
    except ApiExceptionR as e:
        raise ValueError(e.body)


def create_registry_bucket(name):
    """
    Creates a new Registry Bucket
    :param name: String, names the bucket, must be unique in the Registry
    :return: Bucket object
    """
    try:
        return registry.BucketsApi().create_bucket(
            body={
                'name': name
            }
        )
    except ApiExceptionR as e:
        raise ValueError(e.body)


def delete_registry_bucket(bucket):
    """
    Removes a bucket from the NiFi Registry
    :param bucket: the Bucket object to remove
    :return: updated Bucket object
    """
    try:
        return registry.BucketsApi().delete_bucket(
            bucket_id=bucket.identifier
        )
    except (ApiExceptionR, AttributeError) as e:
        raise ValueError(e)


def get_registry_bucket(identifier, identifier_type='name'):
    """
    Filters the Bucket list to a particular identifier
    :param identifier: String, the filter string
    :param identifier_type: String, the param to filter on, 'name' or 'id
    :return: None if 0 matches, list if > 1, single Bucket entity if ==1
    """
    try:
        obj = list_registry_buckets()
    except ApiExceptionR as e:
        raise ValueError(e.body)
    return _utils.filter_obj(obj, identifier, identifier_type)


def list_flows_in_bucket(bucket_id):
    """
    List of all Flows in a given NiFi Registry Bucket
    :param bucket_id: The identifier of the Bucket to fetch from
    :return: list of VersionedFlow objects
    """
    try:
        return registry.BucketFlowsApi().get_flows(bucket_id)
    except ApiExceptionR as e:
        raise ValueError(e.body)


def get_flow_in_bucket(bucket_id, identifier, identifier_type='name'):
    """
    Filters the Flows in a Bucket against a particular identifier
    :param bucket_id: identifier of the Bucket to filter against
    :param identifier: String, the string to filter on
    :param identifier_type: String, the param to check, 'name' or 'id'
    :return: None if 0 matches, list if > 1, single VersionedFlow entity if ==1
    """
    try:
        obj = list_flows_in_bucket(bucket_id)
    except ApiExceptionR as e:
        raise ValueError(e.body)
    return _utils.filter_obj(obj, identifier, identifier_type)


def save_flow_ver(process_group, registry_client, bucket, flow_name=None,
                  flow_id=None, comment='', desc='', refresh=True):
    """
    Adds a Process Group into NiFi Registry Version Control, or saves a new
    version to an existing VersionedFlow
    With a new version
    :param process_group: the ProcessGroup object to work with
    :param registry_client: the RegistryClient to save to
    :param bucket: the Bucket on the NiFi Registry to save to
    Note you need either a name for a new VersionedFlow, or the ID of an
    existing one to save a new version
    :param flow_name: String, a name for the VersionedFlow in the Bucket
    :param flow_id: String, identifier of an existing VersionedFlow in the
    bucket
    :param comment: String, a comment for the version commit
    :param desc: String, a description of the VersionedFlow
    :param refresh: whether to refresh the object revisions before executing
    :return: VersionControlInformationEntity
    """
    if refresh:
        target_pg = canvas.get_process_group(process_group.id, 'id')
    else:
        target_pg = process_group
    try:
        return nifi.VersionsApi().save_to_flow_registry(
            id=target_pg.id,
            body=nifi.StartVersionControlRequestEntity(
                process_group_revision=target_pg.revision,
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
    """
    Removes a Process Group from Version Control
    :param process_group: the ProcessGroup to work with
    :param refresh: Bool, whether to refresh the objet status before actioning
    :return: VersionControlInformationEntity
    """
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
    """
    Attempts to roll back uncommited changes to a Process Group to the last
    committed version
    :param process_group: the ProcessGroup to work with
    :return: VersionedFlowUpdateRequestEntity
    """
    # ToDo: Add handling for flows with live data
    try:
        return nifi.VersionsApi().initiate_revert_flow_version(
            id=process_group.id,
            body=nifi.VersionsApi().get_version_information(process_group.id)
        )
    except (ApiExceptionN, AttributeError) as e:
        raise ValueError(e)


def update_flow_ver(process_group, registry_client, flow,
                    update_children=False):
    """
    Don't use this it's not ready yet
    :param process_group:
    :param registry_client:
    :param flow:
    :param update_children:
    :return:
    """
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
    """
    Gets the most recent version of a VersionedFlowSnapshot from a bucket
    :param bucket_id: the identifier of the Bucket containing the flow
    :param flow_id: the identifier of the VersionedFlow to be retrieved
    :return: VersionedFlowSnapshot
    """
    try:
        return registry.BucketFlowsApi().get_latest_flow_version(
            bucket_id, flow_id
        )
    except ApiExceptionR as e:
        raise ValueError(e.body)


def get_version_info(process_group):
    """
    Gets the Version Control information on a particular Process Group
    :param process_group: the ProcessGroup to work with
    :return: VersionControlInformationEntity
    """
    try:
        return nifi.VersionsApi().get_version_information(
            process_group.id
        )
    except (ApiExceptionN, AttributeError) as e:
        raise ValueError(e)


def create_flow(bucket_id, flow_name, flow_desc='', flow_type='Flow'):
    """
    Creates a new VersionedFlow stub in NiFi Registry. Can be used to write
    VersionedFlow information to without using a NiFi Process Group directly
    :param bucket_id: identifier of the Bucket to write to
    :param flow_name: String, name of the VersionedFlow object
    :param flow_desc: String, description of the VersionedFlow object
    :param flow_type: String, Type of the VersionedFlow, should be 'Flow'
    :return: VersionedFlow
    """
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


def create_flow_version(flow, flow_snapshot, bucket_id=None,
                        raw_snapshot=True):
    """
    Writes a FlowSnapshot into a VersionedFlow as a new version update
    :param bucket_id: Deprecated, now pulled from the flow parameter
    :param flow: the VersionedFlow object to write to
    :param flow_snapshot: the VersionedFlowSnapshot to write into the
    VersionedFlow
    :param raw_snapshot: True if a raw VersionedFlowSnapshot, False if just
    the flow_contents (usually from a VersionedSnapShot or import)
    :return: the new VersionedFlowSnapshot
    """
    if raw_snapshot:
        flow_contents = flow_snapshot.flow_contents
    else:
        flow_contents = flow_snapshot
    try:
        return registry.BucketFlowsApi().create_flow_version(
            bucket_id=flow.bucket_identifier,
            flow_id=flow.identifier,
            body=registry.VersionedFlowSnapshot(
                flow_contents=flow_contents,
                snapshot_metadata=registry.VersionedFlowSnapshotMetadata(
                    version=flow.version_count + 1
                ),
            )
        )
    except ApiExceptionR as e:
        raise ValueError(e.body)


def get_flow_version(bucket_id, flow_id, version=None):
    """
    Retrieves the latest, or a specific, version of a Flow
    :param bucket_id: the id of the bucket containing the Flow
    :param flow_id: the id of the Flow to be retrieved from the Bucket
    :param version: 'None' to retrieve the latest version, or a version
    number as a string to get that version
    :return: an updated VersionedFlowSnapshot
    WARNING: This call is impacted by
    https://issues.apache.org/jira/browse/NIFIREG-135
    """
    if version is not None:
        try:
            return registry.BucketFlowsApi().get_flow_version(
                bucket_id=bucket_id,
                flow_id=flow_id,
                version_number=version
            )
        except ApiExceptionR as e:
            raise ValueError(e.body)
    try:
        return get_latest_flow_ver(bucket_id, flow_id)
    except ValueError as e:
        raise e


def export_flow(flow_snapshot, file_path=None, mode='json'):
    """
    Exports the flow_contents of a given VersionedFlowSnapshot in the provided
    format mode
    :param flow_snapshot: The VersionedFlowSnapshot to export
    :param file_path: Optional; String for the file to be written. No file will
    be written if left blank, the encoded object is still returned
    :param mode: String 'json' or 'yaml' to specific the encoding format
    :return: String of the encoded Snapshot
    """
    if not isinstance(flow_snapshot, registry.VersionedFlowSnapshot):
        raise TypeError("flow_snapshot must be a VersionedFlowSnapshot object")
    export_obj = flow_snapshot.flow_contents.to_dict()
    try:
        out = _utils.dump(
            obj=export_obj,
            mode=mode
        )
    except ValueError as e:
        raise e
    if file_path is None:
        return out
    elif file_path is not None:
        return _utils.fs_write(
            obj=_utils.dump(
                obj=export_obj,
                mode=mode),
            file_path=file_path,
        )
    else:
        raise ValueError("file_path must either be a valid String pointing"
                         " to the file to be written or None to return"
                         "the flow_snapshot in export format")


def import_flow(bucket_id, encoded_flow=None, file_path=None, flow_name=None,
                flow_id=None):
    """
    Imports a given encoded_flow version into the bucket and flow described,
    may optionally be passed a file to read the encoded flow_contents from.
    Note that only one of encoded_flow or file_path, and only one of flow_name
    or flow_id should be specified.
    :param bucket_id: ID of the bucket to write the encoded_flow version to
    :param encoded_flow: Optional; String of the encoded flow to import; if
    not specified file_path is read from. EXOR file_path
    :param file_path: Optional; String of the file path to read the encoded
    flow from, if not specified encoded_flow is read from. EXOR encoded_flow
    :param flow_name: Optional; If this is to be the first version in a new
    flow object, then this is the String name for the flow object. EXOR flow_id
    :param flow_id: Optional; If this is a new version for an existing flow
    object, then this is the ID of that object. EXOR flow_name
    :return: the new VersionedFlowSnapshot
    """
    # First, decode the flow snapshot contents
    if file_path is None and encoded_flow is not None:
        try:
            flow_contents = _utils.load(
                encoded_flow
            )
        except ValueError as e:
            raise e
    elif file_path is not None and encoded_flow is None:
        try:
            flow_contents = _utils.load(
                obj=_utils.fs_read(
                    file_path=file_path
                )
            )
        except ValueError as e:
            raise e
    else:
        raise ValueError("Either file_path must point to a file for import, or"
                         " flow_snapshot must be an importable object, but"
                         "not both")
    # Now handle determining which Versioned Item to write to
    if flow_id is None and flow_name is not None:
        # Case: New flow
        # create the Bucket item
        # TODO: invetisgate bringing description over
        ver_flow = create_flow(
            bucket_id=bucket_id,
            flow_name=flow_name
        )
    elif flow_name is None and flow_id is not None:
        # Case: New version in existing flow
        ver_flow = get_latest_flow_ver(
            bucket_id=bucket_id,
            flow_id=flow_id,
        )
    else:
        raise ValueError("Either flow_id must be the identifier of a flow to"
                         " add this version to, or flow_name must be a unique "
                         "name for a flow in this bucket, but not both")
    # Now write the new version
    return create_flow_version(
        flow=ver_flow.flow,
        flow_snapshot=flow_contents,
        raw_snapshot=False
    )
