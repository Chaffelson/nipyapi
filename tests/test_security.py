#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for nipyapi security module."""

import pytest
from tests import conftest
import nipyapi


def test_bootstrap_secured_nifi():
    pass
    # u = nipyapi.security.get_service_user('nobel')
    # p = nipyapi.security.create_access_policy(
    #     resource='process-groups',
    #     action='write',
    #     r_id=nipyapi.canvas.get_root_pg_id(),
    #     service='nifi'
    # )
    # nipyapi.security.add_user_to_access_policy(
    #     user=u,
    #     policy=p,
    #     service='nifi'
    # )


def test_get_access_policy_for_resource(regress_nifi):
    # Test backwards compatibility issue on unsecured NiFi
    # Returns an error stating the NiFi isn't set up for this, rather than
    # the bad parameter error reported in issue #66
    with pytest.raises(ValueError, match='This NiFi is not configured'):
        _ = nipyapi.security.get_access_policy_for_resource('flow', 'read')
    # Note that on a secured NiFi with no valid policy you will get the error:
    # "No applicable policies could be found"
