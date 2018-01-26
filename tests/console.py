# -*- coding: utf-8 -*-

"""
A convenience script for generating an interactive test environment.
Note that running the main test suite will also clean up this console environment as they share namespace.
"""

from __future__ import absolute_import
from nipyapi import config
from nipyapi.canvas import *
from nipyapi.templates import *
from nipyapi.versioning import *
from nipyapi.nifi import ProcessorConfigDTO


pg = get_process_group(config.test_pg_name)
if pg is None:
    pg = create_process_group(
        get_process_group(get_root_pg_id(), 'id'),
        config.test_pg_name,
        location=(400.0, 400.0)
    )

p = get_processor(config.test_processor_name)
if p is None:
    p = create_processor(
        parent_pg=pg,
        processor=get_processor_type('GenerateFlowFile'),
        location=(400.0, 400.0),
        name=config.test_processor_name,
        config=ProcessorConfigDTO(
            scheduling_period='1s',
            auto_terminated_relationships=['success']
        )
    )

try:
    rc = create_registry_client(
        config.test_registry_client_name,
        config.test_docker_registry_endpoint,
        'NiPyApi Test'
    )
except ValueError:
    rc = get_registry_client(config.test_registry_client_name)

rb = get_registry_bucket(config.test_bucket_name)
if rb is None:
    rb = create_registry_bucket(config.test_bucket_name)


try:
    fv = save_flow_ver(pg, rc, rb, flow_name=config.test_versioned_flow_name)
    fl = get_flow_in_bucket(rb.identifier,
                            fv.version_control_information.flow_id, 'id')
    fss = get_latest_flow_ver(rb.identifier, fl.identifier)
except ValueError:
    fl = get_flow_in_bucket(rb.identifier, config.test_versioned_flow_name)
    fv = get_version_info(pg)
    fss = get_latest_flow_ver(rb.identifier, fl.identifier)

