#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configuration fixtures for pytest for `nipyapi` package."""

import pytest
from os import environ
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


# Fixture to ensure test environment is available before running
@pytest.fixture(scope="session", autouse=True)
def test_environment_setup():
    pass


# This wraps the template tests to ensure things are cleaned up.
@pytest.fixture(scope="class")
def template_class_wrapper(request):
    def remove_test_templates():
        test_templates = ['nipyapi_testTemplate_00', 'nipyapi_testTemplate_01']
        for item in test_templates:
            details = get_template_by_name(item)
            if details is not None:
                delete_template(details.id)

    def remove_test_pgs():
        pg_list = list_all_process_groups()
        test_pgs = [
            item for item in pg_list
            if 'nipyapi_test' in item.status.name
        ]
        for pg in test_pgs:
            delete_process_group(
                pg.id,
                pg.revision
        )

    remove_test_templates()

    def cleanup():
        remove_test_templates()
        remove_test_pgs()
    request.addfinalizer(cleanup)


@pytest.fixture(scope="function")
def fixture_pg(request):
    class Dummy:
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

    def cleanup_test_pgs():
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
                    updated_test_pg = get_process_group(this_test_pg.id, 'id')
                    delete_process_group(
                        updated_test_pg.id,
                        updated_test_pg.revision
                    )

    request.addfinalizer(cleanup_test_pgs)
    return Dummy()


@pytest.fixture()
def fixture_reg_client(request):
    def cleanup_test_registry_client():
        _ = [delete_registry_client(li) for
             li in list_registry_clients().registries
             if test_registry_client_name in li.component.name
            ]

    cleanup_test_registry_client()
    request.addfinalizer(cleanup_test_registry_client)
    return create_registry_client(
        name=test_registry_client_name,
        uri=test_docker_registry_endpoint,
        description='NiPyApi Test Wrapper'
    )


@pytest.fixture()
def fixture_processor(request):
    class Dummy:
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

    def cleanup_test_processors():
        target_list = [li for
             li in list_all_processors()
             if test_processor_name in li.status.name
             ]
        for target in target_list:
            schedule_processor(target, 'STOPPED')
            # Workaround until deterministic processor management implemented
            sleep(2)
            delete_processor(target)

    request.addfinalizer(cleanup_test_processors)
    return Dummy()


@pytest.fixture()
def fixture_registry_bucket(request, fixture_reg_client):
    class Dummy:
        def generate(self, suffix=''):
            return (
                create_registry_bucket(test_bucket_name + suffix),
                fixture_reg_client
            )

    def cleanup_test_buckets():
        _ = [delete_registry_bucket(li) for li
             in list_registry_buckets() if
             test_bucket_name in li.name]

    cleanup_test_buckets()
    request.addfinalizer(cleanup_test_buckets)
    return Dummy()


@pytest.fixture()
def fixture_versioned_flow(fixture_registry_bucket, fixture_pg,
                           fixture_processor):
    fix_rb, fix_rc = fixture_registry_bucket.generate()
    fix_pg = fixture_pg.generate()
    fix_p = fixture_processor.generate(parent_pg=fix_pg)
    fix_vf_info = save_flow_ver(
        process_group=fix_pg,
        registry_client=fix_rc,
        bucket=fix_rb,
        flow_name=test_versioned_flow_name,
        comment='NiPyApi Test',
        desc='NiPyApi Test'
    )
    return (
        fix_rc, fix_rb, fix_pg, fix_p, fix_vf_info
    )

