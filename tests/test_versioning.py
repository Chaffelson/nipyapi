#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from nipyapi import registry, config, nifi, versioning


def test_create_registry_client():
    # First remove any leftover test client connections
    [versioning.delete_registry_client(li) for
     li in versioning.list_registry_clients().registries
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


def test_list_registry_clients(fixture_reg_client):
    r = versioning.list_registry_clients()
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


def test_list_registry_buckets(fixture_registry_bucket, fixture_reg_client):
    r = versioning.list_registry_buckets()
    assert isinstance(r, list)
    assert len(r) >= 1


def test_create_registry_bucket(fixture_reg_client):
    r = versioning.create_registry_bucket(config.test_bucket_name)
    assert isinstance(r, registry.Bucket)
    assert r.name == config.test_bucket_name
    # Bucket names are unique
    with pytest.raises(ValueError) as v:
        _ = versioning.create_registry_bucket(config.test_bucket_name)


def test_delete_registry_bucket(fixture_registry_bucket, fixture_reg_client):
    b1 = versioning.get_registry_bucket(config.test_bucket_name)
    r = versioning.delete_registry_bucket(b1)
    assert r.identifier == b1.identifier
    with pytest.raises(ValueError):
        _ = versioning.get_registry_bucket(b1.identifier, 'id')


def test_get_registry_bucket(fixture_registry_bucket, fixture_reg_client):
    r1 = versioning.get_registry_bucket(config.test_bucket_name)
    assert r1.name == config.test_bucket_name
    r2 = versioning.get_registry_bucket(r1.identifier, 'id')
    assert r2.name == r1.name
    with pytest.raises(ValueError):
        _ = versioning.get_registry_bucket('Irrelevant', 'Invalid')
    r3 = versioning.get_registry_bucket('NonExistantProbably')
    assert r3 is None


def test_save_flow(
        fixture_registry_bucket,
        fixture_reg_client,
        fixture_pg,):
    test_pg = fixture_pg.generate()
    test_rc = versioning.get_registry_client(config.test_registry_client_name)
    test_b = versioning.get_registry_bucket(config.test_bucket_name)
    r1 = versioning.save_flow(test_pg, test_rc, test_b,
                              config.test_versioned_flow_name, 'just a test',
                              'testing regularly')
    assert isinstance(r1, nifi.VersionControlInformationEntity)
    with pytest.raises(ValueError):
        r2 = versioning.save_flow(test_pg, test_rc, test_b,
                                  config.test_versioned_flow_name,
                                  'just a test',
                                  'testing regularly')


def test_update_flow():
    pass
