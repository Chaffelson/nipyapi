#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from nipyapi import canvas
from swagger_client import ProcessGroupFlowEntity, ProcessGroupEntity


def test_get_root_pg_id():
    r = canvas.get_root_pg_id()
    assert isinstance(r, str)


def test_process_group_status():
    r = canvas.get_process_group_status(pg_id='root', detail='names')
    assert isinstance(r, dict)
    r = canvas.get_process_group_status('root', 'all')
    assert isinstance(r, ProcessGroupEntity)
    with pytest.raises(ValueError):
        _ = canvas.get_process_group_status('root','invalid')


def test_get_flow():
    r = canvas.get_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'
    with pytest.raises(ValueError):
        _ = canvas.get_flow('definitelyNotAPG')


def test_recurse_flow():
    r = canvas.recurse_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'


def test_list_all_process_groups():
    r = canvas.list_all_process_groups()
    assert isinstance(r, list)


def test_create_process_group():
    test_pg_name = "nipyapi_testProcessGroup_00"
    r = canvas.create_process_group(
        canvas.get_process_group('NiFi Flow'),
        test_pg_name,
        location=(400.0,400.0)
    )
    assert r.component.name == test_pg_name
    assert r.position.x == r.position.y == 400
    assert r.component.parent_group_id == canvas.get_root_pg_id()


def test_get_process_group():
    with pytest.raises(ValueError):
        _ = canvas.get_process_group('nipyapi_test', 'invalid')
    # # TODO create function to deploy a pair of groups with the same name
    # # TODO create function to deploy a single process group for testing
    # r = canvas.get_process_group('nipyapi_test', 'name')
    # assert isinstance(r, ProcessGroupEntity)


def test_delete_process_group():
    # TODO write test
    pass


def test_schedule_process_group():
    # TODO write test
    pass
