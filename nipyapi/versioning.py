# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Registry Service and related functions
"""

from __future__ import absolute_import
import six
import nipyapi
# Due to line lengths, creating shortened names for these objects
from nipyapi.nifi import VersionControlInformationDTO as VciDTO
from nipyapi.registry import VersionedFlowSnapshotMetadata as VfsMd

__all__ = [
    'create_registry_client', 'list_registry_clients',
    'delete_registry_client', 'get_registry_client', 'list_registry_buckets',
    'create_registry_bucket', 'delete_registry_bucket', 'get_registry_bucket',
    'save_flow_ver', 'list_flows_in_bucket', 'get_flow_in_bucket',
    'get_latest_flow_ver', 'update_flow_ver', 'get_version_info',
    'create_flow', 'create_flow_version', 'get_flow_version',
    'export_flow_version', 'import_flow_version', 'list_flow_versions'
]


def create_registry_client(name, uri, description):
    """
    Creates a Registry Client in the NiFi Controller Services

    Args:
        name (str): The name of the new Client
        uri (str): The URI for the connection, such as 'http://registry:18080'
        description (str): A description for the Client

    Returns:
        (RegistryClientEntity): The new registry client object
    """
    try:
        return nipyapi.nifi.ControllerApi().create_registry_client(
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
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def delete_registry_client(client):
    """
    Deletes a Registry Client from the list of NiFI Controller Services

    Args:
        client (RegistryClientEntity): The client to delete

    Returns:
        (RegistryClientEntity): The updated client object
    """
    try:
        return nipyapi.nifi.ControllerApi().delete_registry_client(
            id=client.id,
            version=client.revision.version
        )
    except (nipyapi.nifi.rest.ApiException, AttributeError) as e:
        raise ValueError(e)


def list_registry_clients():
    """
    Lists the available Registry Clients in the NiFi Controller Services

    Returns:
        (list[RegistryClientEntity]) objects
    """
    try:
        return nipyapi.nifi.ControllerApi().get_registry_clients()
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def get_registry_client(identifier, identifier_type='name'):
    """
    Filters the Registry clients to a particular identifier

    Args:
        identifier (str): the filter string
        identifier_type (str): the parameter to filter on

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches
    """
    try:
        obj = list_registry_clients().registries
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)
    return nipyapi.utils.filter_obj(obj, identifier, identifier_type)


def list_registry_buckets():
    """
    Lists all available Buckets in the NiFi Registry

    Returns:
        (list[Bucket]) objects
    """
    try:
        return nipyapi.registry.BucketsApi().get_buckets()
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)


def create_registry_bucket(name):
    """
    Creates a new Registry Bucket

    Args:
        name (str): name for the bucket, must be unique in the Registry

    Returns:
        (Bucket): The new Bucket object
    """
    try:
        return nipyapi.registry.BucketsApi().create_bucket(
            body={
                'name': name
            }
        )
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)


def delete_registry_bucket(bucket):
    """
    Removes a bucket from the NiFi Registry

    Args:
        bucket (Bucket): the Bucket object to remove

    Returns:
        (Bucket): The updated Bucket object
    """
    try:
        return nipyapi.registry.BucketsApi().delete_bucket(
            bucket_id=bucket.identifier
        )
    except (nipyapi.registry.rest.ApiException, AttributeError) as e:
        raise ValueError(e)


def get_registry_bucket(identifier, identifier_type='name'):
    """
    Filters the Bucket list to a particular identifier

    Args:
        identifier (str): the filter string
        identifier_type (str): the param to filter on

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches
    """
    try:
        obj = list_registry_buckets()
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)
    return nipyapi.utils.filter_obj(obj, identifier, identifier_type)


def list_flows_in_bucket(bucket_id):
    """
    List of all Flows in a given NiFi Registry Bucket

    Args:
        bucket_id (str): The UUID of the Bucket to fetch from

    Returns:
        (list[VersionedFlow]) objects
    """
    try:
        return nipyapi.registry.BucketFlowsApi().get_flows(bucket_id)
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)


def get_flow_in_bucket(bucket_id, identifier, identifier_type='name'):
    """
    Filters the Flows in a Bucket against a particular identifier

    Args:
        bucket_id (str): UUID of the Bucket to filter against
        identifier (str): The string to filter on
        identifier_type (str): The param to check

    Returns:
        None for no matches, Single Object for unique match,
        list(Objects) for multiple matches
    """
    try:
        obj = list_flows_in_bucket(bucket_id)
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)
    return nipyapi.utils.filter_obj(obj, identifier, identifier_type)


def save_flow_ver(process_group, registry_client, bucket, flow_name=None,
                  flow_id=None, comment='', desc='', refresh=True):
    """
    Adds a Process Group into NiFi Registry Version Control, or saves a new
    version to an existing VersionedFlow with a new version

    Args:
        process_group (ProcessGroupEntity): the ProcessGroup object to save
            as a new Flow Version
        registry_client (RegistryClient): The Client linked to the Registry
            which contains the Bucket to save to
        bucket (Bucket): the Bucket on the NiFi Registry to save to
            Note you need either a name for a new VersionedFlow, or the ID of
            an existing one to save a new version
        flow_name (str): A name for the VersionedFlow in the Bucket
        flow_id (Optional [str]): Identifier of an existing VersionedFlow in
            the bucket, if saving a new version to an existing flow
        comment (str): A comment for the version commit
        desc (str): A description of the VersionedFlow
        refresh (bool): whether to refresh the object revisions before action

    Returns:
        (VersionControlInformationEntity)
    """
    if refresh:
        target_pg = nipyapi.canvas.get_process_group(process_group.id, 'id')
    else:
        target_pg = process_group
    try:
        return nipyapi.nifi.VersionsApi().save_to_flow_registry(
            id=target_pg.id,
            body=nipyapi.nifi.StartVersionControlRequestEntity(
                process_group_revision=target_pg.revision,
                versioned_flow=nipyapi.nifi.VersionedFlowDTO(
                    bucket_id=bucket.identifier,
                    comments=comment,
                    description=desc,
                    flow_name=flow_name,
                    flow_id=flow_id,
                    registry_id=registry_client.id
                )
            )
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def stop_flow_ver(process_group, refresh=True):
    """
    Removes a Process Group from Version Control

    Args:
        process_group (ProcessGroupEntity): the ProcessGroup to work with
        refresh (bool): Whether to refresh the object status before actioning

    Returns:
        (VersionControlInformationEntity)
    """
    try:
        if refresh:
            target_pg = nipyapi.canvas.get_process_group(
                process_group.id, 'id'
            )
        else:
            target_pg = process_group
        return nipyapi.nifi.VersionsApi().stop_version_control(
            id=target_pg.id,
            version=target_pg.revision.version
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def revert_flow_ver(process_group):
    """
    Attempts to roll back uncommitted changes to a Process Group to the last
    committed version

    Args:
        process_group (ProcessGroupEntity): the ProcessGroup to work with

    Returns:
        (VersionedFlowUpdateRequestEntity)
    """
    # ToDo: Add handling for flows with live data
    try:
        return nipyapi.nifi.VersionsApi().initiate_revert_flow_version(
            id=process_group.id,
            body=nipyapi.nifi.VersionsApi().get_version_information(
                process_group.id
            )
        )
    except (nipyapi.nifi.rest.ApiException, AttributeError) as e:
        raise ValueError(e)


def list_flow_versions(bucket_id, flow_id):
    """
    EXPERIMENTAL
    List all the versions of a given Flow in a given Bucket

    Args:
        bucket_id (str): UUID of the bucket holding the flow to be enumerated
        flow_id (str): UUID of the flow in the bucket to be enumerated

    Returns:
        list(VersionedFlowSnapshotMetadata)
    """
    try:
        return nipyapi.registry.BucketFlowsApi().get_flow_versions(
            bucket_id=bucket_id,
            flow_id=flow_id
        )
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)


def update_flow_ver(process_group, target_version=None):
    """
    Changes a versioned flow to the specified version, or the latest version

    Args:
        process_group (ProcessGroupEntity): ProcessGroupEntity under version
            control to change
        target_version (Optional [None, Int]): Either None to move to the
        latest available version, or Int of the version number to move to

    Returns:
        (bool): True if successful, False if not
    """
    def _running_update_flow_version():
        """
        Tests for completion of the operation

        Returns:
            (bool) Boolean of operation success
        """
        status = nipyapi.nifi.VersionsApi().get_update_request(
            u_init.request.request_id
        )
        if not status.request.complete:
            return False
        else:
            if status.request.failure_reason is None:
                return True
            else:
                raise ValueError(
                    "Flow Version Update did not complete successfully. "
                    "Error text {0}".format(status.request.failure_reason)
                )
    try:
        vci = get_version_info(process_group)
        assert isinstance(vci, nipyapi.nifi.VersionControlInformationEntity)
        flow_vers = list_flow_versions(
            vci.version_control_information.bucket_id,
            vci.version_control_information.flow_id
        )
        if target_version is None:
            # the first version is always the latest available
            ver = flow_vers[0].version
        else:
            # otherwise the version must be an int
            if not isinstance(target_version, int):
                raise ValueError("target_version must be a positive Integer to"
                                 " pick a specific available version, or None"
                                 " for the latest version to be fetched")
            ver = target_version
        u_init = nipyapi.nifi.VersionsApi().initiate_version_control_update(
            id=process_group.id,
            body=nipyapi.nifi.VersionControlInformationEntity(
                process_group_revision=vci.process_group_revision,
                version_control_information=VciDTO(
                    bucket_id=vci.version_control_information.bucket_id,
                    flow_id=vci.version_control_information.flow_id,
                    group_id=vci.version_control_information.group_id,
                    registry_id=vci.version_control_information.registry_id,
                    version=ver
                )
            )
        )
        nipyapi.utils.wait_to_complete(_running_update_flow_version)
        return nipyapi.nifi.VersionsApi().get_update_request(
            u_init.request.request_id
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def get_latest_flow_ver(bucket_id, flow_id):
    """
    Gets the most recent version of a VersionedFlowSnapshot from a bucket

    Args:
        bucket_id (str): the UUID of the Bucket containing the flow
        flow_id (str): the UUID of the VersionedFlow to be retrieved

    Returns:
        (VersionedFlowSnapshot)
    """
    try:
        return get_flow_version(
            bucket_id, flow_id, version=None
        )
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)


def get_version_info(process_group):
    """
    Gets the Version Control information for a particular Process Group

    Args:
        process_group (ProcessGroupEntity): the ProcessGroup to work with

    Returns:
        (VersionControlInformationEntity)
    """
    try:
        return nipyapi.nifi.VersionsApi().get_version_information(
            process_group.id
        )
    except (nipyapi.nifi.rest.ApiException, AttributeError) as e:
        raise ValueError(e)


def create_flow(bucket_id, flow_name, flow_desc='', flow_type='Flow'):
    """
    Creates a new VersionedFlow stub in NiFi Registry.
    Can be used to write VersionedFlow information to without using a NiFi
    Process Group directly

    Args:
        bucket_id (str): UUID of the Bucket to write to
        flow_name (str): Name for the new VersionedFlow object
        flow_desc (Optional [str]): Description for the new VersionedFlow
            object
        flow_type (Optional [str]): Type of the VersionedFlow, should be 'Flow'

    Returns:
        (VersionedFlow)
    """
    try:
        return nipyapi.registry.BucketFlowsApi().create_flow(
            bucket_id=bucket_id,
            body=nipyapi.registry.VersionedFlow(
                name=flow_name,
                description=flow_desc,
                bucket_identifier=bucket_id,
                type=flow_type,
                version_count=0
            )
        )
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)


def create_flow_version(flow, flow_snapshot, refresh=True):
    """
    EXPERIMENTAL

    Writes a FlowSnapshot into a VersionedFlow as a new version update

    Note that this differs from save_flow_ver which creates a new Flow Version
    containing the snapshot. This function writes a snapshot to an existing
    Flow Version. Useful in migrating Flow Versions between environments.

    Args:
        bucket_id (str): Deprecated, now pulled from the flow parameter
        flow (VersionedFlowObject): the VersionedFlow object to write to
        flow_snapshot (VersionedFlowSnapshot): the Snapshot to write into the
            VersionedFlow
        refresh (bool): Whether to refresh the object status before actioning
        raw_snapshot (bool): Deprecated, as not using a full snapshot resulted
            in inconsistent behavior

    Returns:
        The new (VersionedFlowSnapshot)
    """
    if not isinstance(flow_snapshot, nipyapi.registry.VersionedFlowSnapshot):
        raise ValueError("flow_snapshot must be an instance of a "
                         "registry.VersionedFlowSnapshot object, not an {0}"
                         .format(type(flow_snapshot)))
    try:
        if refresh:
            target_flow = get_flow_in_bucket(
                bucket_id=flow.bucket_identifier,
                identifier=flow.identifier,
                identifier_type='id'
            )
        else:
            target_flow = flow
        target_bucket = get_registry_bucket(
            target_flow.bucket_identifier, 'id'
        )
        # The current version of NiFi doesn't ignore link objects passed to it
        bad_params = ['link']
        for obj in [target_bucket, target_flow]:
            for p in bad_params:
                obj.__setattr__(p, None)
        return nipyapi.registry.BucketFlowsApi().create_flow_version(
            bucket_id=target_bucket.identifier,
            flow_id=target_flow.identifier,
            body=nipyapi.registry.VersionedFlowSnapshot(
                flow=target_flow,
                bucket=target_bucket,
                flow_contents=flow_snapshot.flow_contents,
                snapshot_metadata=VfsMd(
                    version=target_flow.version_count + 1,
                    comments=flow_snapshot.snapshot_metadata.comments,
                    bucket_identifier=target_flow.bucket_identifier,
                    flow_identifier=target_flow.identifier
                ),
            )
        )
    except nipyapi.registry.rest.ApiException as e:
        raise ValueError(e.body)


def get_flow_version(bucket_id, flow_id, version=None, export=False):
    """
    Retrieves the latest, or a specific, version of a Flow

    Args:
        bucket_id (str): the UUID of the bucket containing the Flow
        flow_id (str): the UUID of the Flow to be retrieved from the Bucket
        version (Optional [None, str]): 'None' to retrieve the latest version,
            or a version number as a string to get that version
        export (bool): True to get the raw json object from the server for
            export, False to get the native DataType

    Returns:
        (VersionedFlowSnapshot): If export=False, or the raw json otherwise

    WARNING: This call is impacted by
    https://issues.apache.org/jira/browse/NIFIREG-135
    Which means you can't trust the version count
    """
    assert isinstance(bucket_id, six.string_types)
    assert isinstance(flow_id, six.string_types)
    assert version is None or isinstance(version, six.string_types)
    assert isinstance(export, bool)
    if version:
        try:
            out = nipyapi.registry.BucketFlowsApi().get_flow_version(
                bucket_id=bucket_id,
                flow_id=flow_id,
                version_number=version,
                _preload_content=not export
            )
        except nipyapi.registry.rest.ApiException as e:
            raise ValueError(e.body)
    else:
        try:
            out = nipyapi.registry.BucketFlowsApi().get_latest_flow_version(
                bucket_id,
                flow_id,
                _preload_content=not export
            )
        except ValueError as e:
            raise e
    if export:
        return out.data
    return out


def export_flow_version(bucket_id, flow_id, version=None, file_path=None,
                        mode='json'):
    """
    Convenience method to export the identified VersionedFlowSnapshot in the
    provided format mode.

    Args:
        bucket_id (str): the UUID of the bucket containing the Flow
        flow_id (str): the UUID of the Flow to be retrieved from the Bucket
        version (Optional [None, Str]): 'None' to retrieve the latest version,
            or a version number as a string to get that version
        file_path (str): The path and filename to write to. Defaults to None
            which returns the serialised obj
        mode (str): 'json' or 'yaml' to specific the encoding format

    Returns:
        (str) of the encoded Snapshot
    """
    assert isinstance(bucket_id, six.string_types)
    assert isinstance(flow_id, six.string_types)
    assert file_path is None or isinstance(file_path, six.string_types)
    assert version is None or isinstance(version, six.string_types)
    assert mode in ['yaml', 'json']
    raw_obj = get_flow_version(bucket_id, flow_id, version, export=True)
    export_obj = nipyapi.utils.dump(nipyapi.utils.load(raw_obj), mode)
    if file_path:
        return nipyapi.utils.fs_write(
            obj=export_obj,
            file_path=file_path,
        )
    return export_obj


def import_flow_version(bucket_id, encoded_flow=None, file_path=None,
                        flow_name=None, flow_id=None):
    """
    Imports a given encoded_flow version into the bucket and flow described,
    may optionally be passed a file to read the encoded flow_contents from.

    Note that only one of encoded_flow or file_path, and only one of flow_name
    or flow_id should be specified.

    Args:
        bucket_id (str): UUID of the bucket to write the encoded_flow version
        encoded_flow (Optional [str]): The encoded flow to import; if not
            specified file_path is read from.
        file_path (Optional [str]): The file path to read the encoded flow from
            , if not specified encoded_flow is read from.
        flow_name (Optional [str]): If this is to be the first version in a new
            flow object, then this is the String name for the flow object.
        flow_id (Optional [str]): If this is a new version for an existing flow
            object, then this is the ID of that object.

    Returns:
        The new (VersionedFlowSnapshot)
    """
    # First, decode the flow snapshot contents
    dto = ('registry', 'VersionedFlowSnapshot')
    if file_path is None and encoded_flow is not None:
        try:
            imported_flow = nipyapi.utils.load(
                encoded_flow,
                dto=dto
            )
        except ValueError as e:
            raise e
    elif file_path is not None and encoded_flow is None:
        try:
            file_in = nipyapi.utils.fs_read(
                file_path=file_path
            )
            assert isinstance(file_in, (six.string_types, bytes))
            imported_flow = nipyapi.utils.load(
                obj=file_in,
                dto=dto
            )
            assert isinstance(
                imported_flow,
                nipyapi.registry.VersionedFlowSnapshot
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
        ver_flow = create_flow(
            bucket_id=bucket_id,
            flow_name=flow_name
        )
    elif flow_name is None and flow_id is not None:
        # Case: New version in existing flow
        ver_flow = get_flow_in_bucket(
            bucket_id=bucket_id,
            identifier=flow_id,
            identifier_type='id'
        )
    else:
        raise ValueError("Either flow_id must be the identifier of a flow to"
                         " add this version to, or flow_name must be a unique "
                         "name for a flow in this bucket, but not both")
    # Now write the new version
    return create_flow_version(
        flow=ver_flow,
        flow_snapshot=imported_flow,
    )
