#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi.parameters` package."""

from tests import conftest
import uuid
import pytest
from nipyapi import parameters
from nipyapi.nifi import ParameterContextEntity
from nipyapi.nifi.rest import ApiException
from nipyapi.utils import check_version


def test_create_parameter_context(regress_nifi, fix_context):
    if check_version('1.10.0') >= 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate(name=conftest.test_parameter_context_name)
    assert isinstance(c1, ParameterContextEntity)
    with pytest.raises(AssertionError):
        _ = parameters.create_parameter_context(name={})
    with pytest.raises(AssertionError):
        _ = parameters.create_parameter_context(name=conftest.test_basename, description={})
    with pytest.raises(ApiException):
        # Attempt to generate duplicate Parameter Context
        _ = fix_context.generate(name=conftest.test_parameter_context_name)


def test_get_parameter_context(regress_nifi, fix_context):
    # Because regression tests are parametrized, the skip needs to be inside the function to work properly
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    r1 = parameters.get_parameter_context('fake news', 'name')
    assert r1 is None
    c2 = parameters.get_parameter_context(identifier=str(uuid.uuid4()), identifier_type='id')
    assert c2 is None
    c1 = fix_context.generate(name=conftest.test_basename + 'instance_1')
    r3 = parameters.get_parameter_context(c1.id, identifier_type='id')
    assert r3.component.name == conftest.test_basename + 'instance_1'
    c2 = fix_context.generate(name=conftest.test_basename + 'instance_2')
    r4 = parameters.get_parameter_context(conftest.test_basename + 'instance_2', identifier_type='name')
    assert r4.id == c2.id


def test_list_all_parameter_contexts(regress_nifi, fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    _ = fix_context.generate()
    r1 = parameters.list_all_parameter_contexts()
    assert isinstance(r1, list)
    for pc in r1:
        assert isinstance(pc, ParameterContextEntity)
    _ = fix_context.generate(name=conftest.test_basename + 'instance_1')
    r2 = [x for x in parameters.list_all_parameter_contexts() if conftest.test_basename in x.component.name]
    assert isinstance(r2, list)
    assert len(r2) == 2
    for pc in r2:
        assert isinstance(pc, ParameterContextEntity)


def test_delete_parameter_context(regress_nifi, fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    assert c1.revision is not None
    r1 = parameters.delete_parameter_context(c1)
    assert isinstance(r1, ParameterContextEntity)
    assert r1.revision is None
    with pytest.raises(ApiException):
        _ = parameters.delete_parameter_context(c1)


def test_update_parameter_context(regress_nifi, fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    c1.component.parameters.append(
        parameters.prepare_parameter('Black', 'Lives', 'Matter', True)
    )
    r1 = parameters.update_parameter_context(
        c1
    )
    assert isinstance(r1, ParameterContextEntity)
    assert 1 == len([x for x in r1.component.parameters if 'Black' in x.parameter.name])
    r1.component.parameters = [
        parameters.prepare_parameter('Black', 'Votes', 'Matter', True)
    ]
    r2 = parameters.update_parameter_context(
        r1
    )
    assert isinstance(r2, ParameterContextEntity)
    assert r2.component.parameters[0].parameter.description == 'Matter'


def test_delete_parameter_from_context(regress_nifi, fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    c1.component.parameters.append(
        parameters.prepare_parameter('Black', 'Lives', 'Matter', True)
    )
    _ = parameters.update_parameter_context(
        c1
    )
    r1 = parameters.delete_parameter_from_context(c1, 'Black')
    assert r1.component.parameters == []


def test_upsert_parameter_to_context(regress_nifi, fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    r1 = parameters.upsert_parameter_to_context(
        c1,
        parameters.prepare_parameter('Black', 'Lives', 'Matter', True)
    )
    assert r1.component.parameters[0].parameter.description == 'Matter'


def test_assign_context_to_process_group(regress_nifi, fix_pg, fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    pg1 = fix_pg.generate()
    r1 = parameters.assign_context_to_process_group(pg1, c1.id)
    assert r1.component.parameter_context.id == c1.id


def test_remove_context_from_process_group(regress_nifi, fix_pg, fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    pg1 = fix_pg.generate()
    r1 = parameters.assign_context_to_process_group(pg1, c1.id)
    assert r1.component.parameter_context.id == c1.id
    r2 = parameters.remove_context_from_process_group(pg1)
    assert r2.component.parameter_context is None
