#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configuration fixtures for pytest for `nipyapi` package."""

from __future__ import absolute_import
import pytest
from os import environ, path
import requests
from requests import ConnectionError
from collections import namedtuple
from nipyapi.canvas import *
from nipyapi.templates import *
from nipyapi.versioning import *
from nipyapi import config
from nipyapi.nifi import ProcessorConfigDTO
from time import sleep


# Test Configuration parameters
test_docker_registry_endpoint = 'http://registry:18080'
test_basename = "nipyapi_test"
test_pg_name = test_basename + "_ProcessGroup"
test_registry_client_name = test_basename + "_reg_client"
test_processor_name = test_basename + "_proc"
test_bucket_name = test_basename + "_bucket"
test_versioned_flow_name = test_basename + "_ver_flow"
test_cloned_ver_flow_name = test_basename + '_cloned_ver_flow'
test_variable_registry_entry = [
    (test_basename + '_name', test_basename + '_name' + '_value')
]
test_write_file_path = test_basename + '_fs_write_dir'
test_read_file_path = test_basename + '_fs_read_dir'
test_write_file_name = test_basename + '_fs_write_file'
test_ver_export_tmpdir = test_basename + '_ver_flow_dir'
test_ver_export_filename = test_basename + "_ver_flow_export"

test_resource_dir = 'resources'
# Test template filenames should match the template PG name
test_templates = {
    'basic': 'nipyapi_testTemplate_00',
    'complex': 'nipyapi_testTemplate_01'
}


# Determining test environment
# Can't use skiptest with parametrize for Travis
# Mostly because loading up all the environments takes too long
if "TRAVIS" in environ and environ["TRAVIS"] == "true":
    print("Running tests on TRAVIS, skipping regression suite")
    nifi_test_endpoints = [config.nifi_config.host]
    registry_test_endpoints = [config.registry_config.host]
else:
    print("Running tests on NOT TRAVIS, enabling regression suite")
    nifi_test_endpoints = [
                'http://localhost:10120/nifi-api',  # add earlier as required
                'http://localhost:10140/nifi-api',
                config.nifi_config.host  # reset to default, currently 1.5.0
            ]
    registry_test_endpoints = [config.registry_config.host]


# 'regress' generates tests against previous versions of NiFi
def pytest_generate_tests(metafunc):
    if 'regress' in metafunc.fixturenames:
        # print("Regression testing requested for ({0})."
        #       .format(metafunc.function.__name__))
        metafunc.parametrize(
            argnames='regress',
            argvalues=nifi_test_endpoints,
            indirect=True
        )


@pytest.fixture(scope="function")
def regress(request):
    # print("\nSetting nifi endpoint to ({0}).".format(request.param))
    config.nifi_config.api_client.host = request.param


# Tests that the Docker test environment is available before running test suite
@pytest.fixture(scope="session", autouse=True)
def session_setup():
    def is_endpoint_up(endpoint_url):
        try:
            response = requests.get(endpoint_url)
            if response.status_code == 200:
                return True
        except ConnectionError:
            return False

    for url in nifi_test_endpoints + registry_test_endpoints:
        target_url = url.replace('-api', '')
        if not is_endpoint_up(target_url):
            pytest.exit(
                "Expected Service endpoint ({0}) is not responding"
                    .format(target_url)
            )
    # Run cleanup at the start of the session to ensure it's clean
    cleanup()


def remove_test_templates():
    for item in test_templates.keys():
        details = get_template_by_name(test_templates[item])
        if details is not None:
            delete_template(details.id)


def remove_test_pgs():
    test_pgs = get_process_group(test_pg_name)
    try:
        # If unique, stop, then delete
        schedule_process_group(test_pgs.id, 'STOPPED')
        # This is a workaround until determistic process_group management
        # is implemented
        sleep(2)
        updated_test_pg = get_process_group(test_pgs.id, 'id')
        delete_process_group(
            updated_test_pg.id,
            updated_test_pg.revision
        )
    except AttributeError:
        if isinstance(test_pgs, list):
            for this_test_pg in test_pgs:
                schedule_process_group(this_test_pg.id, 'STOPPED')
                sleep(2)
                updated_test_pg = get_process_group(this_test_pg.id, 'id')
                delete_process_group(
                    updated_test_pg.id,
                    updated_test_pg.revision
                )


def remove_test_processors():
    target_list = [li for
                   li in list_all_processors()
                   if test_processor_name in li.status.name
                   ]
    for target in target_list:
        schedule_processor(target, 'STOPPED')
        # Workaround until deterministic processor management implemented
        sleep(2)
        delete_processor(target)


def remove_test_registry_client():
    _ = [delete_registry_client(li) for
         li in list_registry_clients().registries
         if test_registry_client_name in li.component.name
         ]


def remove_test_buckets():
    _ = [delete_registry_bucket(li) for li
         in list_registry_buckets() if
         test_bucket_name in li.name]


def cleanup():
    remove_test_templates()
    remove_test_processors()
    remove_test_pgs()
    remove_test_buckets()
    remove_test_registry_client()


@pytest.fixture(scope="class")
def template_class_wrapper(request):
    remove_test_templates()
    request.addfinalizer(cleanup)


@pytest.fixture(scope="function")
def regress(request):
    # print("\nSetting nifi endpoint to ({0}).".format(request.param))
    config.nifi_config.api_client.host = request.param


@pytest.fixture(scope="function", name='fix_pg')
def fixture_pg(request):
    class Dummy:
        def __init__(self):
            pass

        def generate(self, parent_pg=None, suffix=''):
            if parent_pg is None:
                target_pg = get_process_group(get_root_pg_id(), 'id')
            else:
                target_pg = parent_pg
            return create_process_group(
                    target_pg,
                    test_pg_name + suffix,
                    location=(400.0, 400.0)
                )

    request.addfinalizer(cleanup)
    return Dummy()


@pytest.fixture(name='fix_reg_client')
def fixture_reg_client(request):
    request.addfinalizer(remove_test_registry_client)
    return create_registry_client(
        name=test_registry_client_name,
        uri=test_docker_registry_endpoint,
        description='NiPyApi Test Wrapper'
    )


@pytest.fixture(name='fix_proc')
def fixture_proc(request):
    class Dummy:
        def __init__(self):
            pass

        def generate(self, parent_pg=None, suffix=''):
            if parent_pg is None:
                target_pg = get_process_group(get_root_pg_id(), 'id')
            else:
                target_pg = parent_pg
            return create_processor(
                parent_pg=target_pg,
                processor=get_processor_type('GenerateFlowFile'),
                location=(400.0, 400.0),
                name=test_processor_name + suffix,
                config=ProcessorConfigDTO(
                    scheduling_period='1s',
                    auto_terminated_relationships=['success']
                )
            )

    request.addfinalizer(remove_test_processors)
    return Dummy()


@pytest.fixture(name='fix_bucket')
def fixture_bucket(request, fix_reg_client):
    request.addfinalizer(remove_test_buckets)
    FixtureBucket = namedtuple(
        'FixtureBucket', ('client', 'bucket')
    )
    return FixtureBucket(
        client=fix_reg_client,
        bucket=create_registry_bucket(test_bucket_name)
    )


@pytest.fixture(name='fix_ver_flow')
def fixture_ver_flow(fix_bucket, fix_pg, fix_proc):
    FixtureVerFlow = namedtuple(
        'FixtureVerFlow', getattr(fix_bucket, '_fields') + (
            'pg', 'proc', 'info', 'flow', 'snapshot', 'dto')
    )
    f_pg = fix_pg.generate()
    f_proc = fix_proc.generate(parent_pg=f_pg)
    f_info = save_flow_ver(
            process_group=f_pg,
            registry_client=fix_bucket.client,
            bucket=fix_bucket.bucket,
            flow_name=test_versioned_flow_name,
            comment='NiPyApi Test',
            desc='NiPyApi Test'
        )
    f_flow = get_flow_in_bucket(
            bucket_id=fix_bucket.bucket.identifier,
            identifier=f_info.version_control_information.flow_id,
            identifier_type='id'
        )
    f_snapshot = get_latest_flow_ver(
        fix_bucket.bucket.identifier,
        f_flow.identifier
    )
    # f_dto = ('nipyapi.registry.models', 'VersionedProcessGroup')
    f_dto = ('nipyapi.registry.models', 'VersionedFlowSnapshot')
    return FixtureVerFlow(
        *fix_bucket,
        pg=f_pg,
        proc=f_proc,
        info=f_info,
        flow=f_flow,
        snapshot=f_snapshot,
        dto=f_dto
    )


@pytest.fixture(name='fix_flow_serde')
def fixture_flow_serde(tmpdir, fix_ver_flow):
    FixtureFlowSerde = namedtuple(
        'FixtureFlowSerde',
        getattr(fix_ver_flow, '_fields') + ('filepath', 'json', 'yaml')
    )
    f_filepath = tmpdir.mkdir(test_ver_export_tmpdir)\
        .join(test_ver_export_filename)
    f_json = export_flow(
        flow_snapshot=fix_ver_flow.snapshot,
        file_path=str(f_filepath) + '.json',
        mode='json'
    )
    f_yaml = export_flow(
        flow_snapshot=fix_ver_flow.snapshot,
        file_path=str(f_filepath) + '.yaml',
        mode='yaml'
    )
    return FixtureFlowSerde(
        *fix_ver_flow,
        filepath=str(f_filepath),
        json=f_json,
        yaml=f_yaml
    )


@pytest.fixture(name='fix_ctv')
def fixture_complex_template_versioning(fix_ver_flow):
    FixtureCTV = namedtuple(
        'FixtureCTV', getattr(fix_ver_flow, '_fields') + (
            'template', 'info_w_template', 'snapshot_w_template'
        )
    )
    f_t_type = 'complex'
    f_t_name = test_templates[f_t_type]
    f_t_filename = f_t_name + '.xml'
    f_t_path = path.join(
        path.dirname(__file__),
        test_resource_dir,
        f_t_filename
    )
    f_template = get_template_by_name(f_t_name)
    if not f_template:
        upload_template(
            pg_id=fix_ver_flow.pg.id,
            template_file=f_t_path
        )
        f_template = get_template_by_name(f_t_name)
    _ = deploy_template(
        fix_ver_flow.pg.id,
        f_template.id
    )
    f_info_2 = save_flow_ver(
        process_group=fix_ver_flow.pg,
        registry_client=fix_ver_flow.client,
        bucket=fix_ver_flow.bucket,
        flow_id=fix_ver_flow.flow.identifier
    )
    f_snapshot_2 = get_latest_flow_ver(
        fix_ver_flow.bucket.identifier,
        fix_ver_flow.flow.identifier
    )
    return FixtureCTV(
        *fix_ver_flow,
        template=f_template,
        info_w_template=f_info_2,
        snapshot_w_template=f_snapshot_2
    )
