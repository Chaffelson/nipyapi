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


def test_get_process_group(test_pg):
    with pytest.raises(ValueError):
        _ = canvas.get_process_group('nipyapi_test', 'invalid')
    single_pg = test_pg.generate()
    pg1 = canvas.get_process_group(single_pg.id, 'id')
    assert isinstance(pg1, ProcessGroupEntity)
    duplicate_pg = test_pg.generate()
    pg2 = canvas.get_process_group(duplicate_pg.id, 'id')
    assert pg2.id != pg1.id
    pg_list = canvas.get_process_group(single_pg.status.name)
    assert isinstance(pg_list, list)
    assert len(pg_list) == 2


def test_delete_process_group(test_pg):
    single_pg = test_pg.generate()
    target_pg = canvas.get_process_group(single_pg.component.name)
    r = canvas.delete_process_group(
        target_pg.id,
        target_pg.revision
    )
    assert r.id == target_pg.id
    assert r.status is None


def test_schedule_process_group():
    # TODO write test
    pass
