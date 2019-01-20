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


def test_add_user_to_access_policy_nifi():
    pass
    # ~ user = nipyapi.security.create_service_user(
        # ~ identity='testuser',
        # ~ service='nifi'
    # ~ )

    # ~ assert isinstance(user, nipyapi.nifi.UserEntity)
    # ~ policy = nipyapi.security.add_user_to_access_policy(
        # ~ user=user,
        # ~ service='nifi'
    # ~ )
    # ~ assert isinstance(policy, nipyapi.nifi.AccessPolicyEntity)


def test_add_user_to_access_policy_registry():
    pass
    # ~ user = nipyapi.security.create_service_user(
        # ~ identity='testuser',
        # ~ service='registry'
    # ~ )
    # ~ assert isinstance(user, nipyapi.registry.User)
    # ~ policy = nipyapi.security.add_user_to_access_policy(
        # ~ user=user,
        # ~ service='registry'
    # ~ )
    # ~ assert isinstance(policy, nipyapi.registry.AccessPolicy)


def test_add_user_group_to_access_policy_nifi():
    pass
    # ~ user_group = nipyapi.security.create_service_user_group(
        # ~ identity='testuser_group',
        # ~ service='nifi'
    # ~ )
    # ~ assert isinstance(user_group, nipyapi.nifi.UserGroupEntity)
    # ~ policy = nipyapi.security.add_user_group_to_access_policy(
        # ~ user_group=user_group,
        # ~ service='nifi'
    # ~ )
    # ~ assert isinstance(policy, nipyapi.nifi.AccessPolicyEntity)


def test_add_user_group_to_access_policy_registry():
    pass
    # ~ user_group = nipyapi.security.create_service_user_group(
        # ~ identity='testuser_group',
        # ~ service='registry'
    # ~ )
    # ~ assert isinstance(user_group, nipyapi.registry.UserGroup)
    # ~ policy = nipyapi.security.add_user_group_to_access_policy(
        # ~ user_group=user_group,
        # ~ service='registry'
    # ~ )
    # ~ assert isinstance(policy, nipyapi.registry.AccessPolicy)
