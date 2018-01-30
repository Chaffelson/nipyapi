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
    with pytest.raises(ValueError):
        _ = canvas.get_process_group_status('root','invalid')


def test_get_flow():
    r = canvas.get_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'
    with pytest.raises(ValueError):
        _ = canvas.get_flow('definitelyNotAPG')


def test_recurse_flow(fixture_pg, regress):
    _ = fixture_pg.generate()
    r = canvas.recurse_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'
    assert isinstance(
        r.process_group_flow.flow.process_groups[0].nipyapi_extended,
        ProcessGroupFlowEntity
    )


def test_list_all_process_groups(fixture_pg, regress):
    _ = fixture_pg.generate()
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
    with pytest.raises(ApiException):
        parent_pg = canvas.get_process_group('NiFi Flow')
        parent_pg.id = 'invalid'
        _ = canvas.create_process_group(
            parent_pg,
            'irrelevant',
            (0, 0)
        )


def test_get_process_group(fixture_pg, regress):
    with pytest.raises(ValueError):
        _ = canvas.get_process_group('nipyapi_test', 'invalid')
    single_pg = fixture_pg.generate()
    pg1 = canvas.get_process_group(single_pg.id, 'id')
    assert isinstance(pg1, ProcessGroupEntity)
    duplicate_pg = fixture_pg.generate()
    pg2 = canvas.get_process_group(duplicate_pg.id, 'id')
    assert pg2.id != pg1.id
    pg_list = canvas.get_process_group(single_pg.status.name)
    assert isinstance(pg_list, list)
    # the two duplicates, and root = 3
    assert len(pg_list) == 3


def test_delete_process_group(fixture_pg, regress, fixture_processor):
    # Delete stopped PG
    pg_1 = fixture_pg.generate()
    r1 = canvas.delete_process_group(
        pg_1.id,
        pg_1.revision
    )
    assert r1.id == pg_1.id
    assert r1.status is None
    # Test deleting a running PG
    pg_2 = fixture_pg.generate()
    p_1 = fixture_processor.generate(parent_pg=pg_2)
    canvas.schedule_process_group(pg_2.id, 'RUNNING')
    with pytest.raises(ValueError):
        _ = canvas.delete_process_group(
            pg_2.id,
            pg_2.revision
        )


def test_schedule_process_group(fixture_processor, fixture_pg):
    test_pg = fixture_pg.generate()
    _ = fixture_processor.generate(parent_pg=test_pg)
    r1 = canvas.schedule_process_group(
        test_pg.id,
        'RUNNING'
    )
    assert r1.state == 'RUNNING'
    r2 = canvas.schedule_process_group(
        test_pg.id,
        'STOPPED'
    )
    assert r2.state == 'STOPPED'
    with pytest.raises(ValueError):
        _ = canvas.schedule_process_group(
            test_pg.id,
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
    r3 = canvas.get_processor_type('amqp', 'bundle')
    assert isinstance(r3, list)


def test_create_processor(fixture_pg, regress):
    test_pg = fixture_pg.generate()
    r1 = canvas.create_processor(
        parent_pg=test_pg,
        processor=canvas.get_processor_type('ListenSyslog'),
        location=(400.0, 400.0),
        name=conftest.test_processor_name
    )
    assert isinstance(r1, nifi.ProcessorEntity)
    assert r1.status.name == conftest.test_processor_name


def test_list_all_processors(fixture_processor, regress):
    p1 = fixture_processor.generate()
    p2 = fixture_processor.generate()
    r = canvas.list_all_processors()
    assert len(r) >= 2


def test_get_processor(fixture_processor, regress):
    p1 = fixture_processor.generate()
    r1 = canvas.get_processor(p1.status.name)
    assert isinstance(r1, nifi.ProcessorEntity)
    r2 = canvas.get_processor('ClearlyNotAProcessor')
    assert r2 is None
    p2 = fixture_processor.generate()
    r3 = canvas.get_processor(p1.status.name)
    assert isinstance(r3, list)


def test_delete_processor(fixture_processor, regress):
    test_proc = fixture_processor.generate()
    assert test_proc.status.name == conftest.test_processor_name
    # try to delete running processor
    canvas.schedule_processor(test_proc, 'RUNNING')
    with pytest.raises(ValueError):
        _ = canvas.delete_processor(test_proc)
    canvas.schedule_processor(test_proc, 'STOPPED')
    r = canvas.delete_processor(test_proc)
    assert r.status is None
    assert isinstance(r, nifi.ProcessorEntity)
    # try to delete twice
    with pytest.raises(ValueError):
        _ = canvas.delete_processor(test_proc)


def test_schedule_processor(fixture_processor):
    p1 = fixture_processor.generate()
    r1 = canvas.schedule_processor(
        p1,
        'RUNNING'
    )
    assert r1.component.state == 'RUNNING'
    assert isinstance(r1, nifi.ProcessorEntity)
    r2 = canvas.schedule_processor(
        p1,
        'STOPPED'
    )
    assert r2.component.state == 'STOPPED'
    assert isinstance(r2, nifi.ProcessorEntity)
    with pytest.raises(ValueError):
        _ = canvas.schedule_process_group(
            p1,
            'BANANA'
        )


def test_update_processor(fixture_processor, regress):
    test_proc = fixture_processor.generate()
    update = nifi.ProcessorConfigDTO(
        scheduling_period='3s'
    )
    r1 = canvas.update_processor(test_proc, update)
    with pytest.raises(ValueError, match='update param is not an instance'):
        _ = canvas.update_processor(test_proc, 'FakeNews')


def test_get_variable_registry(fixture_pg):
    test_pg = fixture_pg.generate()
    r1 = canvas.get_variable_registry(test_pg)
    assert isinstance(r1, nifi.VariableRegistryEntity)
    with pytest.raises(ValueError, match='Unable to locate group with id'):
        canvas.delete_process_group(test_pg.id, test_pg.revision)
        _ = canvas.get_variable_registry(test_pg)


def test_update_variable_registry(fixture_pg):
    test_pg = fixture_pg.generate()
    r1 = canvas.update_variable_registry(
        test_pg,
        conftest.test_variable_registry_entry
    )
    assert isinstance(r1, nifi.VariableRegistryEntity)
    with pytest.raises(ValueError,
                       match='param update is not a valid list of'
                       ):
        _ = canvas.update_variable_registry(test_pg, '')
