#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for nipyapi security module."""

from os import path
import pytest
from tests import conftest
import nipyapi
from nipyapi import security


def test_create_service_user():
    pass
    # ~ nifi_user = security.create_service_user(
        # ~ identity='testuser',
        # ~ service='nifi'
    # ~ )
    # ~ assert isinstance(nifi_user, nipyapi.nifi.UserEntity)


def test_service_login():
    pass


def test_set_service_auth_token():
    pass


def test_service_logout():
    pass


def test_get_service_access_status():
    pass


def test_add_user_to_access_policy():
    pass


def test_add_user_group_to_access_policy():
    pass


def test_update_access_policy():
    pass


def test_get_access_policy_for_resource(regress_nifi):
    pass


def test_create_access_policy():
    pass


def test_list_service_users():
    pass


def test_get_service_user():
    pass


def test_set_service_ssl_context():
    pass


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
