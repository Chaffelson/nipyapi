#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from tests import conftest
from nipyapi import canvas, nifi
from nipyapi.nifi import ProcessGroupFlowEntity, ProcessGroupEntity
from nipyapi.nifi import ProcessorTypesEntity, DocumentedTypeDTO
from nipyapi.nifi.rest import ApiException


def test_get_root_pg_id():
    r = canvas.get_root_pg_id()
    assert isinstance(r, str)


def test_get_process_group_status(regress):
    r = canvas.get_process_group_status(pg_id='root', detail='names')
    assert isinstance(r, dict)
    r = canvas.get_process_group_status('root', 'all')
    assert isinstance(r, ProcessGroupEntity)
    # We rely on this int for testing if a PG is running or not
    assert isinstance(r.running_count, int)
    with pytest.raises(AssertionError):
        _ = canvas.get_process_group_status('root','invalid')


def test_get_flow():
    r = canvas.get_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'
    with pytest.raises(ValueError):
        _ = canvas.get_flow('definitelyNotAPG')


def test_recurse_flow(fix_pg, regress):
    _ = fix_pg.generate()
    r = canvas.recurse_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'
    assert isinstance(
        r.process_group_flow.flow.process_groups[0].nipyapi_extended,
        ProcessGroupFlowEntity
    )


def test_list_all_process_groups(fix_pg, regress):
    _ = fix_pg.generate()
    r = canvas.list_all_process_groups()
    assert isinstance(r, list)
    for pg in r:
        assert isinstance(pg, ProcessGroupEntity)


def test_create_process_group(regress):
    r = canvas.create_process_group(
        canvas.get_process_group(canvas.get_root_pg_id(), 'id'),
        conftest.test_pg_name,
        location=(400.0,400.0)
    )
    assert r.component.name == conftest.test_pg_name
    assert r.position.x == r.position.y == 400
    assert r.component.parent_group_id == canvas.get_root_pg_id()
    assert isinstance(r, nifi.ProcessGroupEntity)
    with pytest.raises(ApiException):
        parent_pg = canvas.get_process_group('NiFi Flow')
        parent_pg.id = 'invalid'
        _ = canvas.create_process_group(
            parent_pg,
            'irrelevant',
            (0, 0)
        )


def test_get_process_group(fix_pg, regress):
    with pytest.raises(AssertionError):
        _ = canvas.get_process_group('nipyapi_test', 'invalid')
    f_pg = fix_pg.generate()
    pg1 = canvas.get_process_group(f_pg.id, 'id')
    assert isinstance(pg1, ProcessGroupEntity)
    duplicate_pg = fix_pg.generate()
    pg2 = canvas.get_process_group(duplicate_pg.id, 'id')
    assert pg2.id != pg1.id
    pg_list = canvas.get_process_group(f_pg.status.name)
    assert isinstance(pg_list, list)
    # the two duplicates, and root = 3
    assert len(pg_list) == 3


def test_delete_process_group(fix_pg, regress, fix_proc):
    # Delete stopped PG
    f_pg1 = fix_pg.generate()
    r1 = canvas.delete_process_group(f_pg1)
    assert r1.id == f_pg1.id
    assert r1.status is None
    # Test deleting a running PG
    pg_2 = fix_pg.generate()
    _ = fix_proc.generate(parent_pg=pg_2)
    canvas.schedule_process_group(pg_2.id, True)
    with pytest.raises(ValueError):
        _ = canvas.delete_process_group(pg_2)
    # Once more with feeling
    r2 = canvas.delete_process_group(
        pg_2,
        force=True
    )
    assert r2.status is None


def test_schedule_process_group(fix_proc, fix_pg):
    f_pg = fix_pg.generate()
    _ = fix_proc.generate(parent_pg=f_pg)
    r1 = canvas.schedule_process_group(
        f_pg.id,
        True
    )
    status = canvas.get_process_group(f_pg.id, 'id')
    assert r1 is True
    assert status.running_count == 1
    r2= canvas.schedule_process_group(
        f_pg.id,
        False
    )
    assert r2 is True
    status = canvas.get_process_group(f_pg.id, 'id')
    assert status.running_count == 0
    assert status.stopped_count == 1
    with pytest.raises(AssertionError):
        _ = canvas.schedule_process_group(
            f_pg.id,
            'BANANA'
        )


def test_list_all_processor_types(regress):
    r = canvas.list_all_processor_types()
    assert isinstance(r, ProcessorTypesEntity)
    assert len(r.processor_types) > 1


def test_get_processor_type(regress):
    r1 = canvas.get_processor_type('twitter')
    assert r1.type == 'org.apache.nifi.processors.twitter.GetTwitter'
    assert isinstance(r1, DocumentedTypeDTO)
    r2 = canvas.get_processor_type("syslog", 'tag')
    assert isinstance(r2, list)
    r3 = canvas.get_processor_type('standard')
    assert isinstance(r3, list)
    assert len(r3) > 10


def test_create_processor(fix_pg, regress):
    f_pg = fix_pg.generate()
    r1 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 400.0),
        name=conftest.test_processor_name
    )
    assert isinstance(r1, nifi.ProcessorEntity)
    assert r1.status.name == conftest.test_processor_name


def test_list_all_processors(fix_proc, regress):
    _ = fix_proc.generate()
    _ = fix_proc.generate()
    r = canvas.list_all_processors()
    assert len(r) >= 2
    assert isinstance(r[0], nifi.ProcessorEntity)


def test_get_processor(fix_proc, regress):
    f_p1 = fix_proc.generate()
    r1 = canvas.get_processor(f_p1.status.name)
    assert isinstance(r1, nifi.ProcessorEntity)
    r2 = canvas.get_processor('ClearlyNotAProcessor')
    assert r2 is None
    f_p2 = fix_proc.generate()
    r3 = canvas.get_processor(f_p1.status.name)
    assert isinstance(r3, list)
    r4 = canvas.get_processor(f_p2.id, 'id')
    assert isinstance(r4, nifi.ProcessorEntity)
    assert r4.id != r1.id


def test_schedule_processor(fix_proc):
    f_p1 = fix_proc.generate()
    r1 = canvas.schedule_processor(
        f_p1,
        True
    )
    status = canvas.get_processor(f_p1.id, 'id')
    assert r1 is True
    assert status.status.run_status == 'Running'
    r2 = canvas.schedule_processor(
        f_p1,
        False
    )
    status = canvas.get_processor(f_p1.id, 'id')
    assert status.status.run_status == 'Stopped'
    assert r2 is True
    with pytest.raises(AssertionError):
        _ = canvas.schedule_processor(
            f_p1,
            'BANANA'
        )


def test_delete_processor(fix_proc, regress):
    f_p1 = fix_proc.generate()
    r1 = canvas.delete_processor(f_p1)
    assert r1.status is None
    assert isinstance(r1, nifi.ProcessorEntity)
    # try to delete processor twice
    with pytest.raises(ValueError):
        _ = canvas.delete_processor(f_p1)
    # try to delete running processor
    f_p2 = fix_proc.generate()
    canvas.schedule_processor(f_p2, True)
    with pytest.raises(ValueError):
        _ = canvas.delete_processor(f_p2)
    # and once more with feeling, er, force
    r2 = canvas.delete_processor(f_p2, force=True)
    assert r2.status is None


def test_update_processor(fix_proc, regress):
    # TODO: Add way more tests to this
    f_p1 = fix_proc.generate()
    update = nifi.ProcessorConfigDTO(
        scheduling_period='3s'
    )
    r1 = canvas.update_processor(f_p1, update)
    with pytest.raises(ValueError, match='update param is not an instance'):
        _ = canvas.update_processor(f_p1, 'FakeNews')


def test_get_variable_registry(fix_pg):
    test_pg = fix_pg.generate()
    r1 = canvas.get_variable_registry(test_pg)
    assert isinstance(r1, nifi.VariableRegistryEntity)
    with pytest.raises(ValueError, match='Unable to locate group with id'):
        canvas.delete_process_group(test_pg)
        _ = canvas.get_variable_registry(test_pg)


def test_update_variable_registry(fix_pg):
    test_pg = fix_pg.generate()
    r1 = canvas.update_variable_registry(
        test_pg,
        conftest.test_variable_registry_entry
    )
    assert isinstance(r1, nifi.VariableRegistryEntity)
    with pytest.raises(ValueError,
                       match='param update is not a valid list of'
                       ):
        _ = canvas.update_variable_registry(test_pg, '')


def test_get_connections():
    # TODO: Waiting for create_connection to generate fixture
    pass


def test_purge_connection():
    # TODO: Waiting for create_connection to generate fixture
    pass


def test_purge_process_group():
    # TODO: Waiting for create_connection to generate fixture
    pass


def test_get_bulletins():
    r = canvas.get_bulletins()
    assert isinstance(r, nifi.ControllerBulletinsEntity)


def test_get_bulletin_board():
    r = canvas.get_bulletin_board()
    assert isinstance(r, nifi.BulletinBoardEntity)
