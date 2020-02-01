#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
import time
from tests import conftest
from nipyapi import canvas, nifi
from nipyapi.nifi import ProcessGroupFlowEntity, ProcessGroupEntity
from nipyapi.nifi import ProcessorTypesEntity, DocumentedTypeDTO


def test_get_root_pg_id():
    r = canvas.get_root_pg_id()
    assert isinstance(r, str)


def test_get_process_group_status(regress_nifi):
    r = canvas.get_process_group_status(pg_id='root', detail='names')
    assert isinstance(r, dict)
    r = canvas.get_process_group_status('root', 'all')
    assert isinstance(r, ProcessGroupEntity)
    # We rely on this int for testing if a PG is running or not
    assert isinstance(r.running_count, int)
    with pytest.raises(AssertionError):
        _ = canvas.get_process_group_status('root', 'invalid')


def test_get_flow():
    r = canvas.get_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'
    with pytest.raises(ValueError):
        _ = canvas.get_flow('definitelyNotAPG')


def test_recurse_flow(regress_nifi, fix_pg):
    _ = fix_pg.generate()
    r = canvas.recurse_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'
    assert isinstance(
        r.process_group_flow.flow.process_groups[0].nipyapi_extended,
        ProcessGroupFlowEntity
    )


def test_list_all_process_groups(regress_nifi, fix_pg):
    _ = fix_pg.generate()
    r1 = canvas.list_all_process_groups()
    assert isinstance(r1, list)
    for pg in r1:
        assert isinstance(pg, ProcessGroupEntity)
    # Test for Issue #129 where nested process groups aren't being listed properly
    pg_1 = fix_pg.generate()
    pg_2 = fix_pg.generate(parent_pg=pg_1)
    r2 = canvas.list_all_process_groups(pg_2.id)
    assert len(r2) == 1
    assert r2[0].id == pg_2.id


def test_create_process_group(regress_nifi):
    r = canvas.create_process_group(
        parent_pg=canvas.get_process_group(canvas.get_root_pg_id(), 'id'),
        new_pg_name=conftest.test_pg_name,
        location=(400.0, 400.0),
        comment='some comment'
    )
    assert r.component.name == conftest.test_pg_name
    assert r.position.x == r.position.y == 400
    assert r.component.parent_group_id == canvas.get_root_pg_id()
    assert isinstance(r, nifi.ProcessGroupEntity)

    # Test process group creation on other than root process group.
    s = canvas.create_process_group(parent_pg=canvas.get_process_group(conftest.test_pg_name), location=(200.0, 200.0),
                                    new_pg_name=conftest.test_another_pg_name)
    assert s.component.name == conftest.test_another_pg_name
    assert s.position.x == s.position.y == 200
    assert s.component.parent_group_id == canvas.get_process_group(conftest.test_pg_name, "name").id
    assert isinstance(s, nifi.ProcessGroupEntity)

    with pytest.raises(ValueError):
        parent_pg = canvas.get_process_group('NiFi Flow')
        parent_pg.id = 'invalid'
        _ = canvas.create_process_group(
            parent_pg,
            'irrelevant',
            (0, 0)
        )


def test_get_process_group(regress_nifi, fix_pg):
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


def test_delete_process_group(regress_nifi, fix_pg, fix_proc):
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
    r2 = canvas.schedule_process_group(
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


def test_update_process_group(regress_nifi, fix_pg):
    f_pg1 = fix_pg.generate()
    r1 = canvas.update_process_group(
        f_pg1,
        {
            'comments': 'test comment'
        }
    )
    assert isinstance(r1, nifi.ProcessGroupEntity)
    assert r1.component.comments == 'test comment'


def test_list_all_processor_types(regress_nifi):
    r = canvas.list_all_processor_types()
    assert isinstance(r, ProcessorTypesEntity)
    assert len(r.processor_types) > 1


def test_get_processor_type(regress_nifi):
    r1 = canvas.get_processor_type('twitter')
    assert r1.type == 'org.apache.nifi.processors.twitter.GetTwitter'
    assert isinstance(r1, DocumentedTypeDTO)
    r2 = canvas.get_processor_type("syslog", 'tag')
    assert isinstance(r2, list)
    r3 = canvas.get_processor_type('standard')
    assert isinstance(r3, list)
    assert len(r3) > 10


def test_create_processor(regress_nifi, fix_pg):
    f_pg = fix_pg.generate()
    r1 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 400.0),
        name=conftest.test_processor_name
    )
    assert isinstance(r1, nifi.ProcessorEntity)
    assert r1.status.name == conftest.test_processor_name


def test_list_all_processors(regress_nifi, fix_proc):
    _ = fix_proc.generate()
    _ = fix_proc.generate()
    r = canvas.list_all_processors()
    assert len(r) >= 2
    assert isinstance(r[0], nifi.ProcessorEntity)


def test_list_nested_processors(regress_nifi, fix_pg, fix_proc):
    pg_1 = fix_pg.generate(
        parent_pg=canvas.get_process_group(canvas.get_root_pg_id(), 'id')
    )
    pg_2 = fix_pg.generate(parent_pg=pg_1)
    root_proc_1 = fix_proc.generate()
    pg_1_proc_1 = fix_proc.generate(parent_pg=pg_1)
    pg_1_proc_2 = fix_proc.generate(parent_pg=pg_1)
    pg_2_proc_1 = fix_proc.generate(parent_pg=pg_2)
    pg_2_proc_2 = fix_proc.generate(parent_pg=pg_2)
    pg_2_proc_3 = fix_proc.generate(parent_pg=pg_2)
    pg_2_proc_4 = fix_proc.generate(parent_pg=pg_2)
    r1 = [x for x in canvas.list_all_processors('root')
          if conftest.test_basename in x.status.name]
    assert len(r1) == 7
    r2 = [x for x in canvas.list_all_processors(pg_2.id)
          if conftest.test_basename in x.status.name]
    assert len(r2) == 4
    r3 = [x for x in canvas.list_all_processors(pg_1.id)
          if conftest.test_basename in x.status.name]
    assert len(r3) == 6


def test_get_processor(regress_nifi, fix_proc):
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


def test_schedule_processor(regress_nifi, fix_proc):
    f_p1 = fix_proc.generate()
    r1 = canvas.schedule_processor(
        f_p1,
        True
    )
    processor_info = canvas.get_processor(f_p1.id, 'id')
    assert r1 is True
    assert isinstance(processor_info, nifi.ProcessorEntity)
    assert processor_info.component.state == 'RUNNING'
    r2 = canvas.schedule_processor(
        f_p1,
        False
    )
    status = canvas.get_processor(f_p1.id, 'id')
    assert status.component.state == 'STOPPED'
    assert r2 is True
    with pytest.raises(AssertionError):
        _ = canvas.schedule_processor(
            f_p1,
            'BANANA'
        )


def test_delete_processor(regress_nifi, fix_proc):
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


def test_update_processor(regress_nifi, fix_proc):
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
    with pytest.raises(ValueError, match='not the most up-to-date revision'):
        _ = canvas.update_variable_registry(
            test_pg,
            conftest.test_variable_registry_entry,
            refresh=False
        )
    r2 = canvas.update_variable_registry(
        test_pg,
        conftest.test_variable_registry_entry,
        refresh=True
    )
    assert isinstance(r2, nifi.VariableRegistryEntity)
    r3 = canvas.update_variable_registry(
        test_pg,
        [
            ('key1', 'value1'),
            ('key2', 'value2')
        ],
        refresh=True
    )
    assert isinstance(r3, nifi.VariableRegistryEntity)
    with pytest.raises(ValueError,
                       match='param update is not a valid list of'
                       ):
        _ = canvas.update_variable_registry(test_pg, '')



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


def test_list_invalid_processors():
    # TODO: write test for new feature
    pass


def test_list_sensitive_processors():
    # TODO: write test for new feature
    pass


def test_create_connection_processors(regress_nifi, fix_proc):
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    # connect single relationship
    r1 = canvas.create_connection(
        f_p1, f_p2, ['success'], conftest.test_basename)
    assert isinstance(r1, nifi.ConnectionEntity)
    # connect all relationships by default
    r2 = canvas.create_connection(f_p1, f_p2, name=conftest.test_basename)
    assert isinstance(r2, nifi.ConnectionEntity)
    with pytest.raises(AssertionError):
        _ = canvas.create_connection(f_p1, f_p2, ['not a connection'])


def test_create_connection_funnels(regress_nifi, fix_proc, fix_funnel):
    f_p1 = fix_proc.generate()
    f_f1 = fix_funnel.generate()
    r1 = canvas.create_connection(
        source=f_p1,
        target=f_f1
    )
    assert isinstance(r1, nifi.ConnectionEntity)
    f_p2 = fix_proc.generate()
    r2 = canvas.create_connection(
        source=f_f1,
        target=f_p2
    )
    assert isinstance(r2, nifi.ConnectionEntity)


def test_delete_connection(regress_nifi, fix_proc):
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    # connect single relationship
    c1 = canvas.create_connection(
        f_p1, f_p2, ['success'], conftest.test_basename)
    r1 = canvas.delete_connection(c1)
    assert isinstance(r1, nifi.ConnectionEntity)
    assert r1.status is None


def test_list_all_connections(regress_nifi, fix_pg, fix_proc):
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    r1 = [x for x in canvas.list_all_connections()
          if conftest.test_basename in x.component.name]
    assert not r1
    # connect single relationship
    c1 = canvas.create_connection(
        f_p1, f_p2, ['success'], conftest.test_basename)
    r2 = [x for x in canvas.list_all_connections('root')
          if conftest.test_basename in x.component.name]
    assert len(r2) == 1
    r3 = [x for x in canvas.list_all_connections(canvas.get_root_pg_id())
          if conftest.test_basename in x.component.name]
    assert len(r3) == 1
    assert isinstance(r2[0], nifi.ConnectionEntity)
    c2 = canvas.create_connection(f_p1, f_p2, name=conftest.test_basename)
    r2 = [x for x in canvas.list_all_connections('root')
          if conftest.test_basename in x.component.name]
    assert len(r2) == 2
    _ = canvas.delete_connection(c1)
    _ = canvas.delete_connection(c2)
    r4 = [x for x in canvas.list_all_connections('root')
          if conftest.test_basename in x.component.name]
    assert not r4
    # Test Issue #129 - nested PGs with descendents missing nested content
    f_pg1 = fix_pg.generate()
    f_pg2 = fix_pg.generate(parent_pg=f_pg1)
    f_p3 = fix_proc.generate(parent_pg=f_pg2)
    f_p4 = fix_proc.generate(parent_pg=f_pg2)
    c2 = canvas.create_connection(
        f_p3, f_p4, ['success'], conftest.test_basename)
    r5 = [x for x in canvas.list_all_connections(f_pg2.id)
          if conftest.test_basename in x.component.name]
    assert len(r5) == 1
    assert r5[0].id == c2.id


def test_get_component_connections(regress_nifi, fix_proc):
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    f_p3 = canvas.create_processor(
        parent_pg=canvas.get_process_group(canvas.get_root_pg_id(), 'id'),
        processor=canvas.get_processor_type('AttributesToJSON'),
        location=(400.0, 425.0),
        name=conftest.test_processor_name + '_inbound'
    )
    canvas.create_connection(f_p1, f_p3, name=conftest.test_basename)
    canvas.create_connection(f_p2, f_p3, name=conftest.test_basename)
    r1 = canvas.get_component_connections(f_p1)
    assert len(r1) == 1
    assert r1[0].source_id == f_p1.id
    r2 = canvas.get_component_connections(f_p3)
    assert len(r2) == 2
    assert r2[0].destination_id == f_p3.id
    assert r2[1].source_id in [f_p1.id, f_p2.id]


def test_list_all_controller_types(regress_nifi):
    r1 = canvas.list_all_controller_types()
    assert len(r1) > 5
    assert isinstance(r1[0], nifi.DocumentedTypeDTO)


def test_list_all_controllers(regress_nifi, fix_pg, fix_cont):
    f_c1 = fix_cont(parent_pg=fix_pg.generate())
    assert isinstance(f_c1, nifi.ControllerServiceEntity)
    r1 = canvas.list_all_controllers()
    assert f_c1.id in [x.id for x in r1]
    r2 = canvas.list_all_controllers(
        pg_id='root',
        descendants=False)
    r2 = [x for x in r2 if conftest.test_basename in x.component.name]
    assert not r2
    with pytest.raises(AssertionError):
        _ = canvas.list_all_controllers(pg_id=['bob'])
    with pytest.raises(AssertionError):
        _ = canvas.list_all_controllers(descendants=['pie'])


def test_create_controller(regress_nifi, fix_cont):
    root_pg = canvas.get_process_group(canvas.get_root_pg_id(), 'id')
    cont_type = canvas.list_all_controller_types()[0]
    r1 = canvas.create_controller(
        parent_pg=root_pg,
        controller=cont_type
    )
    assert isinstance(r1, nifi.ControllerServiceEntity)
    with pytest.raises(AssertionError):
        _ = canvas.create_controller('pie', cont_type)
    with pytest.raises(AssertionError):
        _ = canvas.create_controller(root_pg, 'pie')


def test_get_controller(regress_nifi, fix_pg, fix_cont):
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)
    r1 = canvas.get_controller(f_c1.id, 'id')
    assert r1 is not None
    assert isinstance(r1, nifi.ControllerServiceEntity)
    r2 = canvas.get_controller(f_c1.component.name)
    assert r2.component.name == f_c1.component.name
    _ = fix_cont(parent_pg=f_pg, kind='DistributedMapCacheServer')
    r3 = canvas.get_controller('DistributedMapCache')
    assert len(r3) == 2


def test_schedule_controller(regress_nifi, fix_pg, fix_cont):
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)
    f_c1 = canvas.update_controller(
        f_c1, nifi.ControllerServiceDTO(properties={'Server Hostname': 'Bob'}))
    with pytest.raises(AssertionError):
        _ = canvas.schedule_controller('pie', False)
    with pytest.raises(AssertionError):
        _ = canvas.schedule_controller(f_c1, 'pie')
    r1 = canvas.schedule_controller(f_c1, True)
    assert r1.component.state == 'ENABLED'
    r2 = canvas.schedule_controller(r1, False)
    assert r2.component.state == 'DISABLED'


def test_delete_controller(regress_nifi, fix_pg, fix_cont):
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)
    r1 = canvas.delete_controller(f_c1)
    assert r1.revision is None
    f_c2 = fix_cont(parent_pg=f_pg)
    f_c2 = canvas.update_controller(
        f_c2, nifi.ControllerServiceDTO(properties={'Server Hostname': 'Bob'}))
    f_c2 = canvas.schedule_controller(f_c2, True)
    with pytest.raises(AssertionError):
        _ = canvas.delete_controller('pie')
    with pytest.raises(AssertionError):
        _ = canvas.delete_controller(f_c2, 'pie')
    with pytest.raises(ValueError):
        _ = canvas.delete_controller(f_c2)
    assert f_c2.revision is not None
    r2 = canvas.delete_controller(f_c2, True)
    assert r2.revision is None


def test_update_controller(regress_nifi, fix_pg, fix_cont):
    f_c1 = fix_cont(parent_pg=fix_pg.generate())
    r1 = canvas.update_controller(f_c1, nifi.ControllerServiceDTO(name='Bob'))
    assert isinstance(r1, nifi.ControllerServiceEntity)
    assert r1.component.name == 'Bob'


def test_input_output_ports(regress_nifi, fix_pg):
    root_input_port = canvas.create_port(
        pg_id=canvas.get_root_pg_id(),
        port_type='INPUT_PORT',
        name=conftest.test_basename + 'input_port',
        state='STOPPED'
    )
    assert isinstance(root_input_port, nifi.PortEntity)
    root_output_port = canvas.create_port(
        pg_id=canvas.get_root_pg_id(),
        port_type='OUTPUT_PORT',
        name=conftest.test_basename + 'output_port',
        state='STOPPED'
    )
    assert isinstance(root_output_port, nifi.PortEntity)
    input_ports = [x for x in canvas.list_all_by_kind('input_ports')
                   if conftest.test_basename in x.status.name]
    assert len(input_ports) == 1
    output_ports = [x for x in canvas.list_all_by_kind('output_ports')
                    if conftest.test_basename in x.status.name]
    assert len(output_ports) == 1
    f_pg = fix_pg.generate()
    f_pg_input_port = canvas.create_port(
        pg_id=f_pg.id,
        port_type='INPUT_PORT',
        name=conftest.test_basename + 'input_port',
        state='STOPPED'
    )
    assert isinstance(f_pg_input_port, nifi.PortEntity)
    f_pg_output_port = canvas.create_port(
        pg_id=f_pg.id,
        port_type='OUTPUT_PORT',
        name=conftest.test_basename + 'output_port',
        state='STOPPED'
    )
    assert isinstance(f_pg_output_port, nifi.PortEntity)
    input_ports = [x for x in canvas.list_all_by_kind('input_ports')
                   if conftest.test_basename in x.status.name]
    assert len(input_ports) == 2
    output_ports = [x for x in canvas.list_all_by_kind('output_ports')
                    if conftest.test_basename in x.status.name]
    assert len(output_ports) == 2
    d1 = canvas.delete_port(root_input_port)
    assert isinstance(d1, nifi.PortEntity)
    assert d1.status is None


def test_connect_output_ports(regress_nifi, fix_pg):
    f_pg_1 = fix_pg.generate()
    f_pg_2 = fix_pg.generate()
    f_pg_1_output = canvas.create_port(
        f_pg_1.id,
        'OUTPUT_PORT',
        conftest.test_basename + 'output',
        'STOPPED'
    )
    f_pg_2_input = canvas.create_port(
        f_pg_2.id,
        'INPUT_PORT',
        conftest.test_basename + 'input',
        'STOPPED'
    )
    r1 = canvas.create_connection(
        source=f_pg_1_output,
        target=f_pg_2_input,
        name=conftest.test_basename
    )
    assert isinstance(r1, nifi.ConnectionEntity)


def test_create_funnel(regress_nifi, fix_funnel):
    f_f1 = fix_funnel.generate()
    assert isinstance(f_f1, nifi.FunnelEntity)


def test_delete_funnel(regress_nifi, fix_funnel):
    f_f1 = fix_funnel.generate()
    assert isinstance(f_f1, nifi.FunnelEntity)
    r1 = canvas.delete_funnel(f_f1)
    assert r1.revision is None
    with pytest.raises(ValueError):
        _ = canvas.delete_funnel(f_f1)


@pytest.mark.skip
def test_client_recursion_limit(fix_pg, fix_funnel, target=450):
    # https://github.com/Chaffelson/nipyapi/issues/147
    parent_pg = canvas.get_process_group('root')
    for i in range(0, target):
        parent_pg = fix_pg.generate(parent_pg, str(i))
        fix_funnel.generate(parent_pg)
    start = time.time()
    r1 = canvas.list_all_process_groups(canvas.get_root_pg_id())
    end = time.time()
    assert len(r1) == target + 1  # +1 to allow for root PG
    print("Len {0}  Set {1}".format(len(r1), len(set([x.id for x in r1]))))
    print("Elapsed r1: {0}".format((end - start)))


def test_remote_process_group_controls(fix_proc):
    rpg1 = canvas.create_remote_process_group('http://localhost:8080/nifi')
    assert isinstance(rpg1, nifi.RemoteProcessGroupEntity)
    assert rpg1.revision is not None
    r1 = canvas.set_remote_process_group_transmission(rpg1)
    assert isinstance(r1, nifi.RemoteProcessGroupEntity)
    assert r1.status.transmission_status == 'Transmitting'
    r2 = canvas.set_remote_process_group_transmission(rpg1, False)
    assert isinstance(r2, nifi.RemoteProcessGroupEntity)
    assert r2.status.transmission_status == 'NotTransmitting'
    # Handle connecting to an RPG
    # p1 = fix_proc.generate()
    # ip = canvas.create_port(
    #     pg_id=canvas.get_root_pg_id(),
    #     port_type='INPUT_PORT',
    #     name=conftest.test_basename + 'input_port',
    #     state='STOPPED'
    # )
    # op = canvas.create_port(
    #     pg_id=canvas.get_root_pg_id(),
    #     port_type='OUTPUT_PORT',
    #     name=conftest.test_basename + 'input_port',
    #     state='STOPPED'
    # )
    # c1 = canvas.create_connection(p1, rpg1)
    # c2 = canvas.create_connection(rpg1, op)
    # TODO: Need to test connecting to remote environment, not just loopback
    r3 = canvas.delete_remote_process_group(rpg1)
    assert isinstance(r3, nifi.RemoteProcessGroupEntity)
    assert r3.revision is None
