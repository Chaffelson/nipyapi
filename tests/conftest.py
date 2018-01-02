#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configuration fixtures for pytest for `nipyapi` package."""

import pytest
from nipyapi.canvas import create_process_group, get_process_group
from nipyapi.canvas import delete_process_group

test_header = 'nipyapi_test'
test_pg_name = test_header + "_ProcessGroup"


@pytest.fixture(scope="function")
def test_pg(request):
    class Dummy:
        def generate(self):
            return create_process_group(
                    get_process_group('NiFi Flow'),
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
