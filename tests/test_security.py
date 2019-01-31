#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for nipyapi security module."""

import pytest
from tests import conftest
import nipyapi
from nipyapi import security

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
        _ = security.get_access_policy_for_resource('flow', 'read')
    # Note that on a secured NiFi with no valid policy you will get the error:
    # "No applicable policies could be found"


def test_create_service_user_nifi():
    pass
    # ~ nifi_user = security.create_service_user(
        # ~ identity='testuser',
        # ~ service='nifi'
    # ~ )
    # ~ assert isinstance(nifi_user, nipyapi.nifi.UserEntity)


def test_create_service_user_registry():
    pass
    # ~ registry_user = security.create_service_user(
        # ~ identity='testuser',
        # ~ service='registry'
    # ~ )
    # ~ assert isinstance(registry_user, nipyapi.registry.User)


def test_create_service_user_group_nifi():
    pass
    # ~ nifi_user_group = security.create_service_user_group(
        # ~ identity='testusergroup',
        # ~ service='nifi'
    # ~ )
    # ~ assert isinstance(nifi_user_group, nipyapi.nifi.UserGroupEntity)


def test_create_service_user_group_registry():
    pass
    # ~ registry_user_group = security.create_service_user_group(
        # ~ identity='testusergroup',
        # ~ service='registry'
    # ~ )
    # ~ assert isinstance(registry_user_group, nipyapi.registry.UserGroup)


def test_create_service_user_group_with_users_nifi():
    pass
    # ~ nifi_user = security.create_service_user_group(
        # ~ identity='testuser',
        # ~ service='nifi'
    # ~ )
    # ~ nifi_user_group = security.create_service_user_group(
        # ~ identity='testusergroup',
        # ~ service='nifi',
        # ~ users=[nifi_user]
    # ~ )
    # ~ assert isinstance(nifi_user_group, nipyapi.nifi.UserGroupEntity)
    # ~ assert nifi_user_group.users.len() == 1


def test_create_service_user_group_with_users_registry():
    pass
    # ~ registry_user = security.create_service_user_group(
        # ~ identity='testuser',
        # ~ service='registry'
    # ~ )
    # ~ registry_user_group = security.create_service_user_group(
        # ~ identity='testusergroup',
        # ~ service='registry',
        # ~ users=[registry_user]
    # ~ )
    # ~ assert isinstance(registry_user_group, nipyapi.registry.UserGroup)
    # ~ assert nifi_user_group.users.len() == 1
