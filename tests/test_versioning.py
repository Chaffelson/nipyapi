#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from nipyapi import registry, config, nifi, versioning


def test_create_registry_client():
    # First remove any leftover test client connections
    [versioning.delete_registry_client(li) for
     li in versioning.list_all_registry_clients().registries
     if config.test_registry_client_name in li.component.name
     ]
    r = versioning.create_registry_client(
        name=config.test_registry_client_name,
        uri=config.test_docker_registry_endpoint,
        description='a test connection'
    )
    assert isinstance(r, nifi.RegistryClientEntity)
    # test duplicate catch result
    with pytest.raises(ValueError):
        _ = versioning.create_registry_client(
            name=config.test_registry_client_name,
            uri=config.test_docker_registry_endpoint,
            description='who cares?'
        )


def test_list_all_registry_clients(fixture_reg_client):
    r = versioning.list_all_registry_clients()
    assert isinstance(r, nifi.RegistryClientsEntity)


def test_delete_registry_client(fixture_reg_client):
    client = versioning.get_registry_client(config.test_registry_client_name)
    r = versioning.delete_registry_client(client)
    assert isinstance(r, nifi.RegistryClientEntity)
    assert r.uri is None
    assert r.component.name == config.test_registry_client_name


def test_get_registry_client(fixture_reg_client):
    r1 = versioning.get_registry_client(config.test_registry_client_name)
    assert isinstance(r1, nifi.RegistryClientEntity)
    assert r1.component.name == config.test_registry_client_name
    r2 = versioning.get_registry_client(r1.id, 'id')
    assert r2.id == r1.id
