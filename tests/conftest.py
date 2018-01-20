#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configuration fixtures for pytest for `nipyapi` package."""

import pytest
from os import environ
from nipyapi.canvas import create_process_group, get_process_group
from nipyapi.canvas import delete_process_group, get_root_pg_id
from nipyapi.config import swagger_config

test_header = 'nipyapi_test'
test_pg_name = test_header + "_ProcessGroup"

# Determining test environment
# Can't use skiptest with parametrize for Travis
if "TRAVIS" in environ and environ["TRAVIS"] == "true":
    print("Running tests on TRAVIS, skipping regression suite")
    test_endpoints = [swagger_config.host]
else:
    print("Running tests on NOT TRAVIS, enabling regression suite")
    test_endpoints = [
                'http://localhost:10120/nifi-api',  # add earlier as required
                'http://localhost:10140/nifi-api',
                swagger_config.host  # reset to default, currently 1.5.0
            ]


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
    swagger_config.api_client.host = request.param


@pytest.fixture(scope="function")
def test_pg(request):
    class Dummy:
        def generate(self):
            return create_process_group(
                    get_process_group(get_root_pg_id(), 'id'),
                    test_pg_name,
                    location=(400.0, 400.0)
                )

    def cleanup_test_pgs():
        test_pgs = get_process_group(test_pg_name)
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
