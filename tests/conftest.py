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



# Determining test environment
# Can't use skiptest with parametrize for Travis
# Mostly because loading up all the environments takes too long
if "TRAVIS" in environ and environ["TRAVIS"] == "true":
    print("Running tests on TRAVIS, skipping regression suite")
    test_endpoints = [config.nifi_config.host]
else:
    print("Running tests on NOT TRAVIS, enabling regression suite")
    test_endpoints = [
                'http://localhost:10120/nifi-api',  # add earlier as required
                'http://localhost:10140/nifi-api',
                config.nifi_config.host  # reset to default, currently 1.5.0
            ]


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


# 'regress' generates tests against previous versions of NiFi
def pytest_generate_tests(metafunc):
    if 'regress' in metafunc.fixturenames:
        # print("Regression testing requested for ({0})."
        #       .format(metafunc.function.__name__))
        metafunc.parametrize(
            argnames='regress',
            argvalues=test_endpoints,
            indirect=True
        )


@pytest.fixture(scope="function")
def regress(request):
    # print("\nSetting nifi endpoint to ({0}).".format(request.param))
    config.nifi_config.api_client.host = request.param


@pytest.fixture(scope="function")
def fixture_pg(request):
    class Dummy:
        def generate(self, parent_pg=None):
            if parent_pg is None:
                target_pg = get_process_group(get_root_pg_id(), 'id')
            else:
                target_pg = parent_pg
            return create_process_group(
                    target_pg,
                    config.test_pg_name,
                    location=(400.0, 400.0)
                )

    def cleanup_test_pgs():
        test_pgs = get_process_group(config.test_pg_name)
        try:
            # If unique, stop, then delete
            schedule_process_group(test_pgs.id, 'STOPPED')
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
             if config.test_registry_client_name in li.component.name
            ]

    cleanup_test_registry_client()
    create_registry_client(
        name=config.test_registry_client_name,
        uri=config.test_docker_registry_endpoint,
        description='NiPyApi Test Wrapper'
    )
    request.addfinalizer(cleanup_test_registry_client)


@pytest.fixture()
def fixture_processor(request):
    class Dummy:
        def generate(self, parent_pg=None):
            if parent_pg is None:
                target_pg = get_process_group(get_root_pg_id(), 'id')
            else:
                target_pg = parent_pg
            return create_processor(
                parent_pg=target_pg,
                processor=get_processor_type('GenerateFlowFile'),
                location=(400.0, 400.0),
                name=config.test_processor_name,
                config=ProcessorConfigDTO(
                    scheduling_period='1s',
                    auto_terminated_relationships=['success']
                )
            )

    def cleanup_test_processors():
        target_list = [li for
             li in list_all_processors()
             if config.test_processor_name in li.status.name
             ]
        for target in target_list:
            schedule_processor(target, 'STOPPED')
            delete_processor(target)

    request.addfinalizer(cleanup_test_processors)
    return Dummy()


@pytest.fixture()
def fixture_registry_bucket(request):
    def cleanup_test_bucket():
        _ = [delete_registry_bucket(li) for li
             in list_registry_buckets() if
             config.test_bucket_name in li.name]

    cleanup_test_bucket()
    create_registry_bucket(config.test_bucket_name)
    request.addfinalizer(cleanup_test_bucket)
