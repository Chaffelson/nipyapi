# -*- coding: utf-8 -*-

"""
A convenience script for generating an interactive test environment.
"""

from __future__ import absolute_import
import logging
import nipyapi

# Note that this is the URI for NiFi to connect to Registry
# Which may be different from your localhost connection if using Docker
# Docker is likely to be http://<docker name for registry>:18080

_insecure_rc_endpoint = 'http://registry:18080'


_basename = "nipyapi_console"
_pg0 = _basename + '_process_group_0'
_proc0 = _basename + '_processor_0'
_rc0 = _basename + '_reg_client_0'
_b0 = _basename + '_bucket_0'
_b1 = _basename + '_bucket_1'
_vf0 = _basename + '_ver_flow_0'
_vf1 = _basename + '_ver_flow_1'

__all__ = ['process_group_0', 'processor_0', 'reg_client_0', 'bucket_0',
           'bucket_1', 'ver_flow_info_0', 'ver_flow_0', 'ver_flow_snapshot_0',
           'ver_flow_1', 'ver_flow_snapshot_1', 'ver_flow_json_0',
           'ver_flow_yaml_0', 'ver_flow_raw_0', 'flow_template_0']

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log.info("Setting up NiPyApi Demo Console")
log.info("Cleaning up old NiPyApi Console Process Groups")
process_group_0 = nipyapi.canvas.get_process_group(_pg0)
if process_group_0 is not None:
    nipyapi.canvas.delete_process_group(
        process_group_0,
        force=True,
        refresh=True
    )
log.info("Creating process_group_0 as an empty process group name %s", _pg0)
process_group_0 = nipyapi.canvas.create_process_group(
    nipyapi.canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id'),
    _pg0,
    location=(400.0, 400.0)
)

log.info("Cleaning up old NiPyApi Console Processors")
processor_0 = nipyapi.canvas.get_processor(_proc0)
if processor_0 is not None:
    nipyapi.canvas.delete_processor(process_group_0, True)
log.info("Creating processor_0 as a new GenerateFlowFile named %s in the "
         "previous ProcessGroup", _proc0)
processor_0 = nipyapi.canvas.create_processor(
    parent_pg=process_group_0,
    processor=nipyapi.canvas.get_processor_type('GenerateFlowFile'),
    location=(400.0, 400.0),
    name=_proc0,
    config=nipyapi.nifi.ProcessorConfigDTO(
        scheduling_period='1s',
        auto_terminated_relationships=['success']
    )
)

log.info("Creating reg_client_0 as NiFi Registry Client")
# If the secured environment demo setup has already run, then we just
# want to reuse that client for NiFi <> Registry Comms
reg_client_0 = nipyapi.versioning.get_registry_client(
    'nipyapi_secure_reg_client_0',
    'name'
)
if not reg_client_0:
    try:
        reg_client_0 = nipyapi.versioning.create_registry_client(
            name=_rc0,
            uri=_insecure_rc_endpoint,
            description='NiPyApi Demo Console'
        )
    except ValueError:
        reg_client_0 = nipyapi.versioning.get_registry_client(_rc0)

log.info("Cleaning up old NiPyApi Console Registry Buckets")
bucket_0 = nipyapi.versioning.get_registry_bucket(_b0)
if bucket_0 is not None:
    nipyapi.versioning.delete_registry_bucket(bucket_0)
bucket_1 = nipyapi.versioning.get_registry_bucket(_b1)
if bucket_1 is not None:
    nipyapi.versioning.delete_registry_bucket(bucket_1)
log.info("Creating bucket_0 as new a Registry Bucket named %s", _b0)
bucket_0 = nipyapi.versioning.create_registry_bucket(_b0)
assert isinstance(bucket_0, nipyapi.registry.Bucket)
log.info("Creating bucket_1 as new a Registry Bucket named %s", _b1)
bucket_1 = nipyapi.versioning.create_registry_bucket(_b1)
assert isinstance(bucket_1, nipyapi.registry.Bucket)

log.info("Saving %s as a new Versioned Flow named %s in Bucket %s, and saving "
         "as variable ver_flow_info_0", _pg0, _vf0, _b0)
ver_flow_info_0 = nipyapi.versioning.save_flow_ver(
    process_group=process_group_0,
    registry_client=reg_client_0,
    bucket=bucket_0,
    flow_name=_vf0,
    desc='A Versioned Flow',
    comment='A Versioned Flow'
)
log.info("Creating ver_flow_0 as a copy of the new Versioned Flow object")
ver_flow_0 = nipyapi.versioning.get_flow_in_bucket(
    bucket_0.identifier,
    ver_flow_info_0.version_control_information.flow_id,
    'id'
)
log.info("Creating ver_flow_snapshot_0 as a copy of the new Versioned Flow"
         "Snapshot")
ver_flow_snapshot_0 = nipyapi.versioning.get_latest_flow_ver(
    bucket_0.identifier, ver_flow_0.identifier
)

log.info("Creating ver_flow_1 as an empty Versioned Flow stub named %s in %s",
         _vf1, _b1)
ver_flow_1 = nipyapi.versioning.create_flow(
    bucket_id=bucket_1.identifier,
    flow_name=_vf1,
    flow_desc='A cloned Versioned NiFi-Registry Flow'
)
log.info("Creating ver_flow_snapshot_1 by cloning the first snapshot %s into "
         "the new Versioned Flow Stub %s", _vf0, _vf1)
ver_flow_snapshot_1 = nipyapi.versioning.create_flow_version(
    flow=ver_flow_1,
    flow_snapshot=ver_flow_snapshot_0
)

log.info("Creating ver_flow_raw_0 as a raw Json export of %s", _vf0)
ver_flow_raw_0 = nipyapi.versioning.get_flow_version(
    bucket_0.identifier, ver_flow_0.identifier, export=True
)
log.info("Creating ver_flow_json_0 as a sorted pretty Json export of %s", _vf0)
ver_flow_json_0 = nipyapi.versioning.export_flow_version(
    bucket_0.identifier, ver_flow_0.identifier, mode='json'
)
log.info("Creating ver_flow_yaml_0 as a sorted pretty Yaml export of %s", _vf0)
ver_flow_yaml_0 = nipyapi.versioning.export_flow_version(
    bucket_0.identifier, ver_flow_0.identifier, mode='yaml'
)

log.info("Creating flow_template_0 as a new Template from Process Group %s",
         _pg0)
flow_template_0 = nipyapi.templates.get_template_by_name(
    process_group_0.status.name
)
if flow_template_0 is not None:
    nipyapi.templates.delete_template(flow_template_0.id)
flow_template_0 = nipyapi.templates.create_template(
    process_group_0.id,
    process_group_0.status.name,
    'A Demo Template'
)
print("Demo Console deployed!")
