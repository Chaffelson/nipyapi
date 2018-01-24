#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configuration fixtures for pytest for `nipyapi` package."""

import pytest
from os import environ
from nipyapi.canvas import create_process_group, get_process_group
from nipyapi.canvas import delete_process_group, get_root_pg_id
from nipyapi.canvas import list_all_process_groups, create_processor
from nipyapi.canvas import delete_processor, list_all_processors
from nipyapi.canvas import get_processor_type
from nipyapi.templates import get_template_by_name, delete_template
from nipyapi.versioning import create_registry_client, delete_registry_client
from nipyapi.versioning import list_all_registry_clients
from nipyapi import config



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
        def generate(self):
            return create_process_group(
                    get_process_group(get_root_pg_id(), 'id'),
                    config.test_pg_name,
                    location=(400.0, 400.0)
                )

    def cleanup_test_pgs():
        test_pgs = get_process_group(config.test_pg_name)
        try:
            # If unique, then delete
            delete_process_group(
                test_pgs.id,
                test_pgs.revision
            )
        except AttributeError:
            if isinstance(test_pgs, list):
                for this_test_pg in test_pgs:
                    delete_process_group(
                        this_test_pg.id,
                        this_test_pg.revision
                    )

    request.addfinalizer(cleanup_test_pgs)
    return Dummy()


@pytest.fixture()
def fixture_reg_client(request):
    def cleanup_test_registry_clients():
        _ = [delete_registry_client(li) for
         li in list_all_registry_clients().registries
         if config.test_registry_client_name in li.component.name
        ]

    cleanup_test_registry_clients()
    create_registry_client(
        name=config.test_registry_client_name,
        uri=config.test_docker_registry_endpoint,
        description='NiPyApi Test Wrapper'
    )

    request.addfinalizer(cleanup_test_registry_clients)


@pytest.fixture()
def fixture_processor(request):
    class Dummy:
        def generate(self):
            return create_processor(
                parent_pg=get_process_group(get_root_pg_id(), 'id'),
                processor=get_processor_type('ListenSyslog'),
                location=(400.0, 400.0),
                name=config.test_processor_name
            )

    def cleanup_test_processors():
        _ = [delete_processor(li) for
         li in list_all_processors()
         if config.test_processor_name in li.status.name
         ]

    request.addfinalizer(cleanup_test_processors)
    return Dummy()
