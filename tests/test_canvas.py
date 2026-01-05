"""Tests for `nipyapi` package."""

import pytest
import time
import uuid
from tests import conftest
import nipyapi
from nipyapi import canvas, nifi, utils, config, parameters
from nipyapi.nifi import ProcessGroupFlowEntity, ProcessGroupEntity
from nipyapi.nifi import ProcessorTypesEntity, DocumentedTypeDTO


def test_get_root_pg_id():
    r = canvas.get_root_pg_id()
    assert isinstance(r, str)


def test_get_process_group_status():
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


def test_deser_flow():
    r = canvas.get_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    s = utils.dump(r, 'json')
    f = utils.load(s, ('nifi', 'ProcessGroupFlowEntity'))
    assert isinstance(f, ProcessGroupFlowEntity)


def test_recurse_flow(fix_pg):
    _ = fix_pg.generate()
    r = canvas.recurse_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'
    assert isinstance(
        r.process_group_flow.flow.process_groups[0].nipyapi_extended,
        ProcessGroupFlowEntity
    )


def test_list_all_process_groups(fix_pg):
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


def test_create_process_group():
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


def test_create_process_group_with_string_id():
    """Test create_process_group accepts a string ID instead of ProcessGroupEntity."""
    # Test with "root" as parent_pg
    pg_name = conftest.test_pg_name + "_string_root"
    r = canvas.create_process_group(
        parent_pg="root",
        new_pg_name=pg_name,
        location=(500.0, 500.0),
        comment="created with string root"
    )
    try:
        assert r.component.name == pg_name
        assert r.position.x == r.position.y == 500
        assert r.component.parent_group_id == canvas.get_root_pg_id()
        assert isinstance(r, nifi.ProcessGroupEntity)
    finally:
        canvas.delete_process_group(r)

    # Test with actual UUID string
    root_id = canvas.get_root_pg_id()
    pg_name2 = conftest.test_pg_name + "_string_uuid"
    s = canvas.create_process_group(
        parent_pg=root_id,
        new_pg_name=pg_name2,
        location=(600.0, 600.0)
    )
    try:
        assert s.component.name == pg_name2
        assert s.component.parent_group_id == root_id
        assert isinstance(s, nifi.ProcessGroupEntity)
    finally:
        canvas.delete_process_group(s)


def test_create_process_group_invalid_type():
    """Test create_process_group raises TypeError for invalid parent_pg types."""
    with pytest.raises(TypeError) as exc_info:
        _ = canvas.create_process_group(
            parent_pg=12345,
            new_pg_name="should_fail",
            location=(0, 0)
        )
    assert "must be a string ID or ProcessGroupEntity" in str(exc_info.value)
    assert "int" in str(exc_info.value)


def test_get_process_group(fix_pg):
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


def test_delete_process_group(fix_pg, fix_proc):
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


def test_update_process_group(fix_pg):
    f_pg1 = fix_pg.generate()
    r1 = canvas.update_process_group(
        f_pg1,
        {
            'comments': 'test comment'
        }
    )
    assert isinstance(r1, nifi.ProcessGroupEntity)
    assert r1.component.comments == 'test comment'


def test_list_all_processor_types():
    r = canvas.list_all_processor_types()
    assert isinstance(r, ProcessorTypesEntity)
    assert len(r.processor_types) > 1


def test_get_processor_type():
    r1 = canvas.get_processor_type('GenerateFlowFile')
    assert r1.type == 'org.apache.nifi.processors.standard.GenerateFlowFile'
    assert isinstance(r1, DocumentedTypeDTO)
    r2 = canvas.get_processor_type("syslog", 'tag')
    assert isinstance(r2, list)
    r3 = canvas.get_processor_type('standard')
    assert isinstance(r3, list)
    assert len(r3) > 10


def test_get_processor_docs(fix_proc):
    """Test get_processor_docs with various input types."""
    # Test with string (processor type name)
    r1 = canvas.get_processor_docs('GenerateFlowFile')
    assert r1 is not None
    assert isinstance(r1, nifi.ProcessorDefinition)
    assert 'tags' in dir(r1)
    assert isinstance(r1.tags, list)
    assert 'property_descriptors' in dir(r1)
    assert isinstance(r1.property_descriptors, dict)

    # Test with DocumentedTypeDTO
    proc_type = canvas.get_processor_type('UpdateRecord')
    r2 = canvas.get_processor_docs(proc_type)
    assert r2 is not None
    assert isinstance(r2, nifi.ProcessorDefinition)
    # UpdateRecord should have record-related tags
    assert any('record' in tag.lower() for tag in r2.tags)

    # Test with ProcessorEntity
    proc = fix_proc.generate()
    r3 = canvas.get_processor_docs(proc)
    assert r3 is not None
    assert isinstance(r3, nifi.ProcessorDefinition)

    # Test with invalid input
    with pytest.raises(ValueError, match="processor must be"):
        canvas.get_processor_docs(12345)

    # Test with non-existent processor type returns None
    r4 = canvas.get_processor_docs('NonExistentProcessor')
    assert r4 is None


def test_create_processor(fix_pg):
    f_pg = fix_pg.generate()
    r1 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 400.0),
        name=conftest.test_processor_name,
        config=nifi.ProcessorConfigDTO(scheduling_period='3s')
    )
    assert isinstance(r1, nifi.ProcessorEntity)
    assert r1.status.name == conftest.test_processor_name


def test_list_all_processors(fix_proc):
    _ = fix_proc.generate()
    _ = fix_proc.generate()
    r = canvas.list_all_processors()
    assert len(r) >= 2
    assert isinstance(r[0], nifi.ProcessorEntity)


def test_list_nested_processors(fix_pg, fix_proc):
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


def test_get_processor(fix_proc):
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
    r5 = canvas.get_processor(str(uuid.uuid4()), 'id')
    assert r5 is None

def test_schedule_processor(fix_proc):
    f_p1 = fix_proc.generate()
    # Test bool True -> RUNNING (backwards compatible)
    r1 = canvas.schedule_processor(f_p1, True)
    processor_info = canvas.get_processor(f_p1.id, 'id')
    assert r1 is True
    assert isinstance(processor_info, nifi.ProcessorEntity)
    assert processor_info.component.state == 'RUNNING'

    # Test bool False -> STOPPED (backwards compatible)
    r2 = canvas.schedule_processor(f_p1, False)
    status = canvas.get_processor(f_p1.id, 'id')
    assert status.component.state == 'STOPPED'
    assert r2 is True

    # Test with processor ID string instead of object
    r3 = canvas.schedule_processor(f_p1.id, "RUNNING")
    assert r3 is True
    assert canvas.get_processor(f_p1.id, 'id').component.state == 'RUNNING'

    # Test string "STOPPED"
    r4 = canvas.schedule_processor(f_p1, "STOPPED")
    assert r4 is True
    assert canvas.get_processor(f_p1.id, 'id').component.state == 'STOPPED'

    # Test RUN_ONCE - processor executes once then returns to STOPPED
    r5 = canvas.schedule_processor(f_p1, "RUN_ONCE")
    assert r5 is True
    final_state = canvas.get_processor(f_p1.id, 'id')
    assert final_state.component.state == 'STOPPED'

    # Test DISABLED - prevents processor from being started
    r6 = canvas.schedule_processor(f_p1, "DISABLED")
    assert r6 is True
    assert canvas.get_processor(f_p1.id, 'id').component.state == 'DISABLED'

    # Re-enable (stop) to allow cleanup
    r7 = canvas.schedule_processor(f_p1, "STOPPED")
    assert r7 is True

    # Test invalid value raises ValueError
    with pytest.raises(ValueError, match="scheduled must be bool or one of"):
        _ = canvas.schedule_processor(f_p1, 'BANANA')


def test_schedule_port(fix_proc):
    """Test schedule_port for input and output ports."""
    # NiFi requires ports to have connections before they can be started
    # Create: input_port -> processor -> output_port at root level
    root_pg_id = canvas.get_root_pg_id()

    f_input_port = canvas.create_port(
        pg_id=root_pg_id,
        port_type='INPUT_PORT',
        name=conftest.test_basename + 'schedule_input_port',
        state='STOPPED'
    )
    assert isinstance(f_input_port, nifi.PortEntity)

    f_output_port = canvas.create_port(
        pg_id=root_pg_id,
        port_type='OUTPUT_PORT',
        name=conftest.test_basename + 'schedule_output_port',
        state='STOPPED'
    )
    assert isinstance(f_output_port, nifi.PortEntity)

    # Create processor to connect between ports
    f_proc = fix_proc.generate()

    # Connect: input_port -> processor -> output_port
    conn1 = canvas.create_connection(f_input_port, f_proc)
    assert conn1 is not None
    conn2 = canvas.create_connection(f_proc, f_output_port, ['success'])
    assert conn2 is not None

    try:
        # Test bool True -> RUNNING (input port)
        r1 = canvas.schedule_port(f_input_port, True)
        assert r1 is True
        port_info = canvas.get_port(f_input_port.id, "id")
        assert port_info.component.state == 'RUNNING'

        # Test bool False -> STOPPED
        r2 = canvas.schedule_port(f_input_port, False)
        assert r2 is True
        port_info = canvas.get_port(f_input_port.id, "id")
        assert port_info.component.state == 'STOPPED'

        # Test with port ID string instead of object
        r3 = canvas.schedule_port(f_input_port.id, "RUNNING")
        assert r3 is True
        assert canvas.get_port(f_input_port.id, "id").component.state == 'RUNNING'

        # Test string "STOPPED"
        r4 = canvas.schedule_port(f_input_port, "STOPPED")
        assert r4 is True
        assert canvas.get_port(f_input_port.id, "id").component.state == 'STOPPED'

        # Test DISABLED - prevents port from being started
        r5 = canvas.schedule_port(f_input_port, "DISABLED")
        assert r5 is True
        assert canvas.get_port(f_input_port.id, "id").component.state == 'DISABLED'

        # Re-enable (stop) to allow cleanup
        r6 = canvas.schedule_port(f_input_port, "STOPPED")
        assert r6 is True

        # Test invalid value raises ValueError
        with pytest.raises(ValueError, match="scheduled must be bool or one of"):
            _ = canvas.schedule_port(f_input_port, 'BANANA')

        # Test output port scheduling
        r7 = canvas.schedule_port(f_output_port, True)
        assert r7 is True
        assert canvas.get_port(f_output_port.id, "id").component.state == 'RUNNING'

        r8 = canvas.schedule_port(f_output_port, False)
        assert r8 is True
        assert canvas.get_port(f_output_port.id, "id").component.state == 'STOPPED'

    finally:
        # Cleanup - stop ports, delete connections, then delete ports
        canvas.schedule_port(f_input_port.id, "STOPPED")
        canvas.schedule_port(f_output_port.id, "STOPPED")
        canvas.delete_connection(conn1, purge=True)
        canvas.delete_connection(conn2, purge=True)
        canvas.delete_port(canvas.get_port(f_input_port.id, "id"))
        canvas.delete_port(canvas.get_port(f_output_port.id, "id"))


def test_delete_processor(fix_proc):
    f_p1 = fix_proc.generate()
    r1 = canvas.delete_processor(f_p1)
    assert r1.status is None
    assert isinstance(r1, nifi.ProcessorEntity)
    # try to delete processor twice, should get None as it won't be found
    r2 = canvas.delete_processor(f_p1)
    assert r2 is None
    # try to delete running processor
    f_p2 = fix_proc.generate()
    canvas.schedule_processor(f_p2, True)
    with pytest.raises(ValueError):
        _ = canvas.delete_processor(f_p2)
    # and once more with feeling, er, force
    r3 = canvas.delete_processor(f_p2, force=True)
    assert r3.status is None


def test_update_processor(fix_proc):
    """Test update_processor with config, name, and both."""
    f_p1 = fix_proc.generate()
    original_name = f_p1.component.name

    # Test config update (processor is stopped, no auto_stop needed)
    update = nifi.ProcessorConfigDTO(scheduling_period='3s')
    r1 = canvas.update_processor(f_p1, update=update)
    assert r1 is not None

    # Test invalid update type
    with pytest.raises(ValueError, match='update param is not an instance'):
        canvas.update_processor(f_p1, update='FakeNews')

    # Test rename (processor is stopped, no auto_stop needed)
    new_name = original_name + '_RENAMED'
    r2 = canvas.update_processor(r1, name=new_name)
    assert r2.component.name == new_name

    # Test rename back
    r3 = canvas.update_processor(r2, name=original_name)
    assert r3.component.name == original_name

    # Test both config and name together
    update2 = nifi.ProcessorConfigDTO(scheduling_period='5s')
    r4 = canvas.update_processor(r3, update=update2, name=original_name + '_BOTH')
    assert r4.component.name == original_name + '_BOTH'

    # Restore name
    canvas.update_processor(r4, name=original_name)

    # Test error when neither update nor name provided
    with pytest.raises(ValueError, match="Must provide"):
        canvas.update_processor(f_p1)


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
    # Test basic call returns list
    r = canvas.get_bulletin_board()
    assert isinstance(r, list)


def test_get_bulletin_board_with_pg_filter(fix_pg):
    """Test bulletin board filtering by process group."""
    pg = fix_pg.generate()
    # Filter by process group ID - should return list (possibly empty)
    r = canvas.get_bulletin_board(pg_id=pg.id)
    assert isinstance(r, list)
    # Any returned bulletins should be from this PG
    for b in r:
        assert b.group_id == pg.id


def test_get_bulletin_board_with_limit():
    """Test bulletin board with limit parameter."""
    r = canvas.get_bulletin_board(limit=5)
    assert isinstance(r, list)
    assert len(r) <= 5


def test_get_bulletin_board_with_source_filter():
    """Test bulletin board filtering by source name pattern."""
    r = canvas.get_bulletin_board(source_name=".*Generate.*")
    assert isinstance(r, list)
    # All returned bulletins should match the pattern (now returns BulletinDTO directly)
    for b in r:
        assert "Generate" in (b.source_name or "")


def test_list_invalid_processors():
    # TODO: write test for new feature
    pass


def test_list_sensitive_processors():
    # TODO: write test for new feature
    pass


def test_create_connection_processors(fix_proc):
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


def test_create_connection_funnels(fix_proc, fix_funnel):
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


def test_delete_connection(fix_proc):
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    # connect single relationship
    c1 = canvas.create_connection(
        f_p1, f_p2, ['success'], conftest.test_basename)
    r1 = canvas.delete_connection(c1)
    assert isinstance(r1, nifi.ConnectionEntity)
    assert r1.status is None


def test_list_all_connections(fix_pg, fix_proc):
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


def test_get_component_connections(fix_proc):
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


def test_get_connection(fix_proc):
    """Test getting a connection by ID or entity."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    conn = canvas.create_connection(f_p1, f_p2, name=conftest.test_basename)

    # Get by ID string
    result = canvas.get_connection(conn.id)
    assert isinstance(result, nifi.ConnectionEntity)
    assert result.id == conn.id

    # Get by entity (refresh)
    result2 = canvas.get_connection(conn)
    assert isinstance(result2, nifi.ConnectionEntity)
    assert result2.id == conn.id


def test_update_connection_name(fix_proc):
    """Test updating a connection's name."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    conn = canvas.create_connection(f_p1, f_p2, name=conftest.test_basename)

    # Update name
    new_name = conftest.test_basename + '_updated'
    result = canvas.update_connection(conn, name=new_name)
    assert result.component.name == new_name


def test_update_connection_clear_bends(fix_proc):
    """Test clearing bends from a connection."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    # Create connection with bends
    bends = [(500.0, 350.0), (500.0, 450.0)]
    conn = canvas.create_connection(f_p1, f_p2, name=conftest.test_basename, bends=bends)
    assert len(conn.component.bends) == 2

    # Clear bends by passing empty list
    result = canvas.update_connection(conn, bends=[])
    assert result.component.bends == [] or result.component.bends is None


def test_update_connection_set_bends(fix_proc):
    """Test setting bends on a connection."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    conn = canvas.create_connection(f_p1, f_p2, name=conftest.test_basename)

    # Set new bends
    new_bends = [(600.0, 400.0), (600.0, 500.0)]
    result = canvas.update_connection(conn, bends=new_bends)
    assert len(result.component.bends) == 2
    assert result.component.bends[0].x == 600.0


def test_update_connection_by_id(fix_proc):
    """Test updating a connection by ID string."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    conn = canvas.create_connection(f_p1, f_p2, name=conftest.test_basename)

    # Update by ID string
    new_name = conftest.test_basename + '_by_id'
    result = canvas.update_connection(conn.id, name=new_name)
    assert result.component.name == new_name


def test_list_all_controller_types():
    r1 = canvas.list_all_controller_types()
    assert len(r1) > 5
    assert isinstance(r1[0], nifi.DocumentedTypeDTO)


def test_list_all_controllers(fix_pg, fix_cont):
    f_pg_1 = fix_pg.generate()
    f_pg_2 = fix_pg.generate(parent_pg=f_pg_1)
    f_c1 = fix_cont()
    f_c2 = fix_cont(parent_pg=f_pg_1)
    f_c3 = fix_cont(parent_pg=f_pg_2)
    assert isinstance(f_c1, nifi.ControllerServiceEntity)
    assert isinstance(f_c2, nifi.ControllerServiceEntity)
    assert isinstance(f_c3, nifi.ControllerServiceEntity)
    # Find all and l0 l1 and l2
    r1 = canvas.list_all_controllers()
    assert all(y.id in [x.id for x in r1] for y in [f_c1, f_c2, f_c3])
    # find just l0
    r2 = canvas.list_all_controllers(
        pg_id='root',
        descendants=False)
    r2 = [x for x in r2 if conftest.test_basename in x.component.name]
    assert len(r2) == 1
    assert f_c1.id in [x.id for x in r2]
    # find just l1
    r3 = canvas.list_all_controllers(
        pg_id=f_pg_1.id,
        descendants=False)
    r3 = [x for x in r3 if conftest.test_basename in x.component.name]
    assert len(r3) == 2
    assert all(y.id in [x.id for x in r3] for y in [f_c1, f_c2])
    # Find l1 and l2
    # This will fail if duplicates are introduced in the listing
    r4 = canvas.list_all_controllers(
        pg_id=f_pg_1.id,
        descendants=True)
    r4 = [x for x in r4 if conftest.test_basename in x.component.name]
    assert len(r4) == 3
    assert all(y.id in [x.id for x in r4] for y in [f_c1, f_c2, f_c3])
    # test errors
    with pytest.raises(AssertionError):
        _ = canvas.list_all_controllers(pg_id=['bob'])
    with pytest.raises(AssertionError):
        _ = canvas.list_all_controllers(descendants=['pie'])


def test_create_controller(fix_cont):
    root_pg = canvas.get_process_group(canvas.get_root_pg_id(), 'id')
    cont_type = canvas.list_all_controller_types()[0]
    r1 = canvas.create_controller(
        parent_pg=root_pg,
        controller=cont_type
    )
    try:
        assert isinstance(r1, nifi.ControllerServiceEntity)
        with pytest.raises(AssertionError):
            _ = canvas.create_controller('pie', cont_type)
        with pytest.raises(AssertionError):
            _ = canvas.create_controller(root_pg, 'pie')
    finally:
        # Clean up controller created directly (not via fixture)
        canvas.delete_controller(r1, force=True)


def test_get_controller(fix_pg, fix_cont):
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)
    r1 = canvas.get_controller(f_c1.id, 'id')
    assert r1 is not None
    assert isinstance(r1, nifi.ControllerServiceEntity)
    r2 = canvas.get_controller(f_c1.component.name)
    assert r2.component.name == f_c1.component.name
    _ = fix_cont(parent_pg=f_pg, kind='CSVReader')
    r3 = canvas.get_controller('CSVReader')
    assert len(r3) == 2


def test_schedule_controller(fix_pg, fix_cont):
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)
    with pytest.raises(AssertionError):
        _ = canvas.schedule_controller('pie', False)
    with pytest.raises(AssertionError):
        _ = canvas.schedule_controller(f_c1, 'pie')
    r1 = canvas.schedule_controller(f_c1, True)
    assert r1.component.state == 'ENABLED'
    r2 = canvas.schedule_controller(r1, False)
    assert r2.component.state == 'DISABLED'


def test_schedule_all_controllers(fix_pg, fix_cont):
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)
    f_c2 = fix_cont(parent_pg=f_pg)
    # Verify both start disabled
    assert f_c1.component.state == 'DISABLED'
    assert f_c2.component.state == 'DISABLED'
    # Enable all
    with pytest.raises(AssertionError):
        _ = canvas.schedule_all_controllers(123, True)
    with pytest.raises(AssertionError):
        _ = canvas.schedule_all_controllers(f_pg.id, 'pie')
    r1 = canvas.schedule_all_controllers(f_pg.id, True)
    assert r1.state == 'ENABLED'
    # Verify controllers are enabled
    c1 = canvas.get_controller(f_c1.id, 'id')
    c2 = canvas.get_controller(f_c2.id, 'id')
    assert c1.component.state == 'ENABLED'
    assert c2.component.state == 'ENABLED'
    # Disable all
    r2 = canvas.schedule_all_controllers(f_pg.id, False)
    assert r2.state == 'DISABLED'
    # Verify controllers are disabled
    c1 = canvas.get_controller(f_c1.id, 'id')
    c2 = canvas.get_controller(f_c2.id, 'id')
    assert c1.component.state == 'DISABLED'
    assert c2.component.state == 'DISABLED'


def test_delete_controller(fix_pg, fix_cont):
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)
    r1 = canvas.delete_controller(f_c1)
    assert r1.revision is None
    # Test delete by ID string
    f_c1b = fix_cont(parent_pg=f_pg)
    r1b = canvas.delete_controller(f_c1b.id)
    assert r1b.revision is None
    f_c2 = fix_cont(parent_pg=f_pg)
    f_c2 = canvas.schedule_controller(f_c2, True)
    with pytest.raises(ValueError):
        _ = canvas.delete_controller('pie')  # Invalid ID string
    with pytest.raises(AssertionError):
        _ = canvas.delete_controller(f_c2, 'pie')  # Invalid force parameter
    with pytest.raises(ValueError):
        _ = canvas.delete_controller(f_c2)
    assert f_c2.revision is not None
    r2 = canvas.delete_controller(f_c2, True)
    assert r2.revision is None
    # Test for only delete within a PG
    f_c_root = fix_cont()
    f_c_pg = fix_cont(parent_pg=f_pg)
    r3 = canvas.delete_process_group(f_pg)
    assert r3.revision is None
    r4 = canvas.get_controller(identifier=f_c_root.id, identifier_type='id')
    assert r4.revision is not None


def test_update_controller(fix_pg, fix_cont):
    f_c1 = fix_cont(parent_pg=fix_pg.generate())
    r1 = canvas.update_controller(f_c1, nifi.ControllerServiceDTO(name='Bob'))
    assert isinstance(r1, nifi.ControllerServiceEntity)
    assert r1.component.name == 'Bob'


def test_input_output_ports(fix_pg):
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


def test_connect_output_ports(fix_pg):
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


def test_get_port():
    """Test get_port for input and output ports."""
    root_pg_id = canvas.get_root_pg_id()

    # Create test ports
    f_input_port = canvas.create_port(
        pg_id=root_pg_id,
        port_type='INPUT_PORT',
        name=conftest.test_basename + 'get_input_port',
        state='STOPPED'
    )
    f_output_port = canvas.create_port(
        pg_id=root_pg_id,
        port_type='OUTPUT_PORT',
        name=conftest.test_basename + 'get_output_port',
        state='STOPPED'
    )

    try:
        # Test get by ID - input port
        result = canvas.get_port(f_input_port.id, "id")
        assert isinstance(result, nifi.PortEntity)
        assert result.id == f_input_port.id
        assert "INPUT" in result.port_type

        # Test get by ID - output port
        result = canvas.get_port(f_output_port.id, "id")
        assert isinstance(result, nifi.PortEntity)
        assert result.id == f_output_port.id
        assert "OUTPUT" in result.port_type

        # Test get by name - input port
        result = canvas.get_port(conftest.test_basename + 'get_input_port', "name")
        assert isinstance(result, nifi.PortEntity)
        assert result.id == f_input_port.id

        # Test get by name - output port
        result = canvas.get_port(conftest.test_basename + 'get_output_port', "name")
        assert isinstance(result, nifi.PortEntity)
        assert result.id == f_output_port.id

        # Test not found by ID
        with pytest.raises(ValueError, match="Port not found"):
            canvas.get_port("nonexistent-id-12345", "id")

        # Test not found by name returns None
        result = canvas.get_port("nonexistent_port_name", "name")
        assert result is None

        # Test invalid identifier_type
        with pytest.raises(ValueError, match="identifier_type must be"):
            canvas.get_port(f_input_port.id, "invalid")

    finally:
        # Cleanup
        canvas.delete_port(canvas.get_port(f_input_port.id, "id"))
        canvas.delete_port(canvas.get_port(f_output_port.id, "id"))


def test_create_funnel(fix_funnel):
    f_f1 = fix_funnel.generate()
    assert isinstance(f_f1, nifi.FunnelEntity)
    assert f_f1.component.position.x == 400
    assert f_f1.component.position.y == 400


def test_delete_funnel(fix_funnel):
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


def test_create_connection_self_loop(fix_proc):
    """Test that self-loop connections automatically get bends for visibility."""
    f_p1 = fix_proc.generate()
    # Create a self-loop connection (processor to itself)
    # The create_connection function should automatically add bends
    r1 = canvas.create_connection(
        source=f_p1,
        target=f_p1,
        relationships=['success'],
        name=conftest.test_basename + '_selfloop'
    )
    assert isinstance(r1, nifi.ConnectionEntity)
    assert r1.source_id == r1.destination_id
    # Verify bends were auto-created for visibility
    assert r1.component.bends is not None
    assert len(r1.component.bends) == 2  # Self-loops get 2 bends


def test_create_connection_with_bends(fix_proc):
    """Test creating connections with explicit bends."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()
    # Create connection with explicit bends
    bends = [(500.0, 350.0), (500.0, 450.0)]
    r1 = canvas.create_connection(
        source=f_p1,
        target=f_p2,
        relationships=['success'],
        name=conftest.test_basename + '_bends',
        bends=bends
    )
    assert isinstance(r1, nifi.ConnectionEntity)
    assert r1.component.bends is not None
    assert len(r1.component.bends) == 2


def test_get_flow_components(fix_pg, fix_proc, fix_funnel):
    """Test finding all connected components in a flow."""
    f_pg = fix_pg.generate()
    # Create a simple flow: proc1 -> proc2 -> funnel
    f_p1 = fix_proc.generate(parent_pg=f_pg, suffix='_flow1')
    f_p2 = fix_proc.generate(parent_pg=f_pg, suffix='_flow2')
    f_f1 = fix_funnel.generate(parent_pg=f_pg)
    # Connect them
    conn1 = canvas.create_connection(f_p1, f_p2, name=conftest.test_basename)
    conn2 = canvas.create_connection(f_p2, f_f1, name=conftest.test_basename)
    # Find all components starting from proc1 - returns FlowSubgraph
    flow = canvas.get_flow_components(f_p1)
    # Verify it's a FlowSubgraph named tuple
    assert hasattr(flow, 'components')
    assert hasattr(flow, 'connections')
    # Verify components
    assert len(flow.components) == 3
    component_ids = [c.id for c in flow.components]
    assert f_p1.id in component_ids
    assert f_p2.id in component_ids
    assert f_f1.id in component_ids
    # Verify connections are also returned
    assert len(flow.connections) == 2
    connection_ids = [c.id for c in flow.connections]
    assert conn1.id in connection_ids
    assert conn2.id in connection_ids


def test_get_flow_components_separate_flows(fix_pg, fix_proc):
    """Test that separate flows are not connected."""
    f_pg = fix_pg.generate()
    # Create two separate flows
    f_p1 = fix_proc.generate(parent_pg=f_pg, suffix='_flowA1')
    f_p2 = fix_proc.generate(parent_pg=f_pg, suffix='_flowA2')
    f_p3 = fix_proc.generate(parent_pg=f_pg, suffix='_flowB1')
    f_p4 = fix_proc.generate(parent_pg=f_pg, suffix='_flowB2')
    # Connect flow A
    canvas.create_connection(f_p1, f_p2, name=conftest.test_basename)
    # Connect flow B (separate)
    canvas.create_connection(f_p3, f_p4, name=conftest.test_basename)
    # Find components starting from flow A
    flow_a = canvas.get_flow_components(f_p1)
    assert len(flow_a.components) == 2
    component_ids_a = [c.id for c in flow_a.components]
    assert f_p1.id in component_ids_a
    assert f_p2.id in component_ids_a
    assert f_p3.id not in component_ids_a
    assert f_p4.id not in component_ids_a
    # Find components starting from flow B
    flow_b = canvas.get_flow_components(f_p3)
    assert len(flow_b.components) == 2


def test_get_flow_components_with_self_loop(fix_pg, fix_proc):
    """Test flow component detection with self-loop connections."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg, suffix='_loop1')
    f_p2 = fix_proc.generate(parent_pg=f_pg, suffix='_loop2')
    # Create flow with self-loop
    canvas.create_connection(f_p1, f_p2, name=conftest.test_basename)
    canvas.create_connection(f_p1, f_p1, relationships=['success'],
                             name=conftest.test_basename + '_self')
    # Should find both processors
    flow = canvas.get_flow_components(f_p1)
    assert len(flow.components) == 2


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


# =============================================================================
# CONFIG VERIFICATION TESTS
# =============================================================================


def test_verify_controller_disabled(fix_pg, fix_cont):
    """Test verifying a disabled controller service configuration."""
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)

    # Controller starts disabled, should be verifiable
    assert f_c1.component.state == 'DISABLED'

    # Verify configuration - CSVReader may pass or fail depending on setup
    results = canvas.verify_controller(f_c1)

    # Result should be a list of ConfigVerificationResultDTO
    assert isinstance(results, list)
    for r in results:
        assert hasattr(r, 'verification_step_name')
        assert hasattr(r, 'outcome')
        assert r.outcome in ('SUCCESSFUL', 'FAILED', 'SKIPPED')


def test_verify_controller_by_id(fix_pg, fix_cont):
    """Test verifying a controller service by ID string."""
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)

    # Verify by ID string
    results = canvas.verify_controller(f_c1.id)

    assert isinstance(results, list)


def test_verify_controller_enabled_fails(fix_pg, fix_cont):
    """Test that verifying an enabled controller raises ValueError."""
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)

    # Enable the controller
    f_c1 = canvas.schedule_controller(f_c1, True)
    assert f_c1.component.state == 'ENABLED'

    # Verification should fail with clear error
    with pytest.raises(ValueError, match="must be DISABLED"):
        canvas.verify_controller(f_c1)

    # Cleanup: disable the controller
    canvas.schedule_controller(f_c1, False)


def test_verify_processor_stopped(fix_pg, fix_proc):
    """Test verifying a stopped processor configuration."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)

    # Processor should be stopped/invalid initially
    results = canvas.verify_processor(f_p1)

    # Result should be a list of ConfigVerificationResultDTO
    assert isinstance(results, list)
    for r in results:
        assert hasattr(r, 'verification_step_name')
        assert hasattr(r, 'outcome')
        assert r.outcome in ('SUCCESSFUL', 'FAILED', 'SKIPPED')


def test_verify_processor_by_id(fix_pg, fix_proc):
    """Test verifying a processor by ID string."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)

    # Verify by ID string
    results = canvas.verify_processor(f_p1.id)

    assert isinstance(results, list)


def test_verify_processor_shows_failures(fix_pg):
    """Test that verification shows detailed failure information."""
    f_pg = fix_pg.generate()

    # Create a DBCPConnectionPool which requires configuration
    dbcp_type = [t for t in canvas.list_all_controller_types()
                 if t.type == 'org.apache.nifi.dbcp.DBCPConnectionPool']
    if not dbcp_type:
        pytest.skip("DBCPConnectionPool not available")

    controller = canvas.create_controller(f_pg, dbcp_type[0], name='TestDBCP')

    try:
        # Verify - should fail because required properties not set
        results = canvas.verify_controller(controller)
        failures = [r for r in results if r.outcome == "FAILED"]

        # Should have failures
        assert len(failures) > 0

        # Failures should have step names and explanations
        for failure in failures:
            assert failure.verification_step_name is not None
            assert failure.explanation is not None

    finally:
        # Cleanup
        canvas.delete_controller(controller)


# =============================================================================
# Verification with Parameter Context Tests
# =============================================================================


def test_verify_controller_with_parameter_set(fix_pg):
    """Test verification when a controller uses a parameter that IS set correctly."""
    f_pg = fix_pg.generate()

    # Create a parameter context with a parameter
    param = parameters.prepare_parameter(
        name="test.schema",
        value='{"type":"record","name":"test","fields":[{"name":"id","type":"string"}]}',
        description="Test schema parameter"
    )
    ctx = parameters.create_parameter_context(
        name="VerifyParamTestCtx",
        parameters=[param]
    )

    try:
        # Assign context to PG
        parameters.assign_context_to_process_group(f_pg, ctx.id)

        # Create a CSVReader that references the parameter
        csv_type = [t for t in canvas.list_all_controller_types()
                    if 'CSVReader' in t.type]
        if not csv_type:
            pytest.skip("CSVReader not available")

        controller = canvas.create_controller(f_pg, csv_type[0], name='ParamCSVReader')

        # Update to use the parameter reference
        update = nifi.ControllerServiceDTO(
            properties={"Schema Text": "#{test.schema}"}
        )
        controller = canvas.update_controller(controller, update)

        # Verify - should succeed because parameter is defined
        results = canvas.verify_controller(controller)
        assert isinstance(results, list)

        # Check that there are results (verification ran)
        assert len(results) > 0

        # Log results for debugging
        for r in results:
            print(f"  {r.verification_step_name}: {r.outcome}")
            if r.explanation:
                print(f"    {r.explanation}")

    finally:
        # Cleanup
        canvas.delete_controller(controller)
        parameters.delete_parameter_context(ctx)


def test_verify_controller_with_missing_parameter(fix_pg):
    """Test verification when a controller references a parameter that DOES NOT exist."""
    f_pg = fix_pg.generate()

    # Create an EMPTY parameter context (no parameters defined)
    ctx = parameters.create_parameter_context(
        name="VerifyMissingParamCtx",
        parameters=[]
    )

    try:
        # Assign context to PG
        parameters.assign_context_to_process_group(f_pg, ctx.id)

        # Create a CSVReader that references a non-existent parameter
        csv_type = [t for t in canvas.list_all_controller_types()
                    if 'CSVReader' in t.type]
        if not csv_type:
            pytest.skip("CSVReader not available")

        controller = canvas.create_controller(f_pg, csv_type[0], name='MissingParamCSV')

        # Update to use a parameter that doesn't exist
        # Note: NiFi may reject this at update time, so we catch that
        try:
            update = nifi.ControllerServiceDTO(
                properties={"Schema Text": "#{nonexistent.param}"}
            )
            controller = canvas.update_controller(controller, update)
        except nifi.rest.ApiException as e:
            # NiFi rejects unknown parameter references at update time
            # This is expected behavior - the update itself fails
            assert "parameter" in str(e).lower() or "does not exist" in str(e).lower()
            pytest.skip("NiFi rejected parameter reference at update time (expected)")

        # If we get here, verify should detect the issue
        results = canvas.verify_controller(controller)

        # Should have some verification result
        assert isinstance(results, list)

    finally:
        # Cleanup
        try:
            canvas.delete_controller(controller)
        except Exception:
            pass  # May have failed to create
        parameters.delete_parameter_context(ctx)


def test_verify_controller_with_empty_parameter(fix_pg):
    """Test verification when a controller references a parameter that is EMPTY."""
    f_pg = fix_pg.generate()

    # Create a parameter context with an EMPTY parameter value
    param = parameters.prepare_parameter(
        name="empty.param",
        value="",  # Empty value
        description="Empty test parameter"
    )
    ctx = parameters.create_parameter_context(
        name="VerifyEmptyParamCtx",
        parameters=[param]
    )

    try:
        # Assign context to PG
        parameters.assign_context_to_process_group(f_pg, ctx.id)

        # Create a controller that references the empty parameter
        csv_type = [t for t in canvas.list_all_controller_types()
                    if 'CSVReader' in t.type]
        if not csv_type:
            pytest.skip("CSVReader not available")

        controller = canvas.create_controller(f_pg, csv_type[0], name='EmptyParamCSV')

        # Update to use the empty parameter
        update = nifi.ControllerServiceDTO(
            properties={"Schema Text": "#{empty.param}"}
        )
        controller = canvas.update_controller(controller, update)

        # Verify - may pass or fail depending on what CSVReader requires
        results = canvas.verify_controller(controller)
        assert isinstance(results, list)

        # Log all results
        for r in results:
            print(f"  {r.verification_step_name}: {r.outcome}")
            if r.explanation:
                print(f"    {r.explanation}")

    finally:
        # Cleanup
        canvas.delete_controller(controller)
        parameters.delete_parameter_context(ctx)


def test_verify_processor_with_parameter_set(fix_pg):
    """Test verification when a processor uses a parameter that IS set correctly."""
    f_pg = fix_pg.generate()

    # Create a parameter context with a parameter
    param = parameters.prepare_parameter(
        name="file.size",
        value="1 KB",
        description="File size parameter"
    )
    ctx = parameters.create_parameter_context(
        name="VerifyProcParamCtx",
        parameters=[param]
    )

    try:
        # Assign context to PG
        parameters.assign_context_to_process_group(f_pg, ctx.id)

        # Create a GenerateFlowFile processor
        proc_type = canvas.get_processor_type("GenerateFlowFile")
        processor = canvas.create_processor(f_pg, proc_type, location=(400, 400),
                                            name='ParamGenFF')

        # Update to use the parameter reference
        update = nifi.ProcessorConfigDTO(
            properties={"File Size": "#{file.size}"}
        )
        processor = canvas.update_processor(processor, update)

        # Verify - should succeed because parameter is defined
        results = canvas.verify_processor(processor)
        assert isinstance(results, list)

        # Check results
        for r in results:
            print(f"  {r.verification_step_name}: {r.outcome}")

    finally:
        # Cleanup
        canvas.delete_processor(processor)
        parameters.delete_parameter_context(ctx)


def test_verify_processor_with_invalid_parameter_value(fix_pg):
    """Test verification when a processor uses a parameter with an invalid value type."""
    f_pg = fix_pg.generate()

    # Create a parameter context with an INVALID value for the expected type
    # GenerateFlowFile "File Size" expects a data size like "1 KB", not random text
    param = parameters.prepare_parameter(
        name="bad.file.size",
        value="not-a-valid-size",  # Invalid for DataSize property
        description="Invalid file size parameter"
    )
    ctx = parameters.create_parameter_context(
        name="VerifyBadValueCtx",
        parameters=[param]
    )

    try:
        # Assign context to PG
        parameters.assign_context_to_process_group(f_pg, ctx.id)

        # Create a GenerateFlowFile processor
        proc_type = canvas.get_processor_type("GenerateFlowFile")
        processor = canvas.create_processor(f_pg, proc_type, location=(400, 400),
                                            name='BadValueGenFF')

        # Update to use the invalid parameter
        try:
            update = nifi.ProcessorConfigDTO(
                properties={"File Size": "#{bad.file.size}"}
            )
            processor = canvas.update_processor(processor, update)
        except nifi.rest.ApiException:
            # NiFi may reject invalid values at update time
            pytest.skip("NiFi rejected invalid parameter value at update time")

        # Verify - should detect the invalid value
        results = canvas.verify_processor(processor)
        assert isinstance(results, list)

        # Log all results
        for r in results:
            print(f"  {r.verification_step_name}: {r.outcome}")
            if r.explanation:
                print(f"    {r.explanation}")

    finally:
        # Cleanup
        try:
            canvas.delete_processor(processor)
        except Exception:
            pass
        parameters.delete_parameter_context(ctx)


def test_verify_dbcp_with_connection_parameters(fix_pg):
    """Test DBCPConnectionPool verification with database connection parameters.

    This simulates a real deployment scenario where a connector needs
    database credentials and connection info from parameters.
    """
    f_pg = fix_pg.generate()

    # Create parameter context with database connection parameters
    params = [
        parameters.prepare_parameter(
            name="db.url",
            value="jdbc:h2:mem:testdb",
            description="Database connection URL"
        ),
        parameters.prepare_parameter(
            name="db.driver.class",
            value="org.h2.Driver",
            description="Database driver class"
        ),
    ]
    ctx = parameters.create_parameter_context(
        name="VerifyDBCPParamsCtx",
        parameters=params
    )

    # Find DBCPConnectionPool controller type
    dbcp_type = [t for t in canvas.list_all_controller_types()
                 if t.type == 'org.apache.nifi.dbcp.DBCPConnectionPool']
    if not dbcp_type:
        parameters.delete_parameter_context(ctx)
        pytest.skip("DBCPConnectionPool not available")

    controller = None
    try:
        # Assign context to PG
        parameters.assign_context_to_process_group(f_pg, ctx.id)

        # Create DBCP controller
        controller = canvas.create_controller(f_pg, dbcp_type[0], name='ParamDBCP')

        # Update to use parameters
        update = nifi.ControllerServiceDTO(
            properties={
                "Database Connection URL": "#{db.url}",
                "Database Driver Class Name": "#{db.driver.class}",
            }
        )
        controller = canvas.update_controller(controller, update)

        # Verify - will likely fail because driver isn't available,
        # but should show meaningful verification results
        results = canvas.verify_controller(controller)
        assert isinstance(results, list)
        assert len(results) > 0

        # Log all verification steps
        print("\nDBCP Verification Results:")
        for r in results:
            status = "[PASS]" if r.outcome == "SUCCESSFUL" else "[FAIL]"
            print(f"  {status} {r.verification_step_name}")
            if r.outcome == "FAILED" and r.explanation:
                print(f"       -> {r.explanation}")

        # Check that we got meaningful step names
        step_names = [r.verification_step_name for r in results]
        assert len(step_names) > 0

    finally:
        # Cleanup
        if controller:
            canvas.delete_controller(controller)
        parameters.delete_parameter_context(ctx)


def test_verify_controller_with_asset_parameter(fix_pg):
    """Test verification when a controller uses a parameter that references an asset.

    This simulates a real deployment scenario where a JDBC driver JAR is uploaded
    as an asset and referenced by a database connection pool.
    """
    f_pg = fix_pg.generate()

    # Create a parameter context
    ctx = parameters.create_parameter_context(
        name="VerifyAssetParamCtx",
        parameters=[]
    )

    # Find DBCPConnectionPool controller type
    dbcp_type = [t for t in canvas.list_all_controller_types()
                 if t.type == 'org.apache.nifi.dbcp.DBCPConnectionPool']
    if not dbcp_type:
        parameters.delete_parameter_context(ctx)
        pytest.skip("DBCPConnectionPool not available")

    controller = None
    try:
        # Upload a fake "driver" file as an asset
        # In real usage this would be an actual JAR file
        fake_driver_content = b"This is a fake driver file for testing"
        asset = parameters.upload_asset(
            context_id=ctx.id,
            file_bytes=fake_driver_content,
            filename="test-driver.jar"
        )
        print(f"Uploaded asset: {asset['name']} (id={asset['id']})")

        # Create a parameter that references the asset
        driver_param = parameters.prepare_parameter_with_asset(
            name="jdbc.driver.path",
            asset_id=asset['id'],
            asset_name=asset['name'],
            description="JDBC driver JAR file"
        )

        # Also add connection parameters
        url_param = parameters.prepare_parameter(
            name="db.url",
            value="jdbc:h2:mem:testdb",
            description="Database URL"
        )

        # Update context with both parameters
        ctx.component.parameters = [driver_param, url_param]
        ctx = parameters.update_parameter_context(ctx)

        # Assign context to PG
        parameters.assign_context_to_process_group(f_pg, ctx.id)

        # Create DBCP controller
        controller = canvas.create_controller(f_pg, dbcp_type[0], name='AssetDBCP')

        # Update to use parameters (including the asset-backed parameter)
        update = nifi.ControllerServiceDTO(
            properties={
                "Database Connection URL": "#{db.url}",
                # Note: the actual property name for driver location varies
                # This tests that asset parameters are resolved
            }
        )
        controller = canvas.update_controller(controller, update)

        # Verify - the verification should complete and show results
        results = canvas.verify_controller(controller)
        assert isinstance(results, list)
        assert len(results) > 0

        # Log all verification steps
        print("\nAsset-backed Controller Verification Results:")
        for r in results:
            status = "[PASS]" if r.outcome == "SUCCESSFUL" else "[FAIL]"
            print(f"  {status} {r.verification_step_name}")
            if r.outcome == "FAILED" and r.explanation:
                print(f"       -> {r.explanation}")

    finally:
        # Cleanup
        if controller:
            canvas.delete_controller(controller)
        # Clear parameters first (they reference assets), then delete context
        # delete_parameter_context handles this automatically
        parameters.delete_parameter_context(ctx)


def test_verify_controller_with_asset_no_reference(fix_pg):
    """Test verification when a controller has an asset uploaded but not referenced.

    This tests the basic asset upload and parameter creation workflow,
    verifying that the controller can be verified even without using
    the asset-backed parameter directly.
    """
    f_pg = fix_pg.generate()

    # Create a parameter context
    ctx = parameters.create_parameter_context(
        name="VerifyAssetNoRefCtx",
        parameters=[]
    )

    # Find a controller type
    csv_type = [t for t in canvas.list_all_controller_types()
                if 'CSVReader' in t.type]
    if not csv_type:
        parameters.delete_parameter_context(ctx)
        pytest.skip("CSVReader not available")

    controller = None
    try:
        # Upload an asset
        fake_schema_content = b'{"type":"record","name":"test","fields":[]}'
        asset = parameters.upload_asset(
            context_id=ctx.id,
            file_bytes=fake_schema_content,
            filename="schema.avsc"
        )
        print(f"Uploaded asset: {asset['name']} (id={asset['id']})")

        # Create parameter referencing the asset
        schema_param = parameters.prepare_parameter_with_asset(
            name="schema.file",
            asset_id=asset['id'],
            asset_name=asset['name'],
            description="Schema file asset"
        )

        # Update context with the asset parameter
        ctx.component.parameters = [schema_param]
        ctx = parameters.update_parameter_context(ctx)

        # Assign context to PG
        parameters.assign_context_to_process_group(f_pg, ctx.id)

        # Create controller (not using the asset parameter directly)
        controller = canvas.create_controller(f_pg, csv_type[0], name='AssetNoRefCSV')

        # Verify - should work, just verifying the controller itself
        results = canvas.verify_controller(controller)
        assert isinstance(results, list)

        # Log results
        print("\nAsset No-Reference Verification Results:")
        for r in results:
            status = "[PASS]" if r.outcome == "SUCCESSFUL" else "[FAIL]"
            print(f"  {status} {r.verification_step_name}")
            if r.explanation:
                print(f"       -> {r.explanation}")

        # Check assets are listed
        assets = parameters.list_assets(ctx.id)
        assert len(assets) == 1
        print(f"\nAsset still present: {assets[0]['name']}")

    finally:
        # Cleanup
        if controller:
            canvas.delete_controller(controller)
        # delete_parameter_context handles asset cleanup
        parameters.delete_parameter_context(ctx)


# --- State Management Tests ---


def test_get_processor_state(fix_state_flow):
    """Test getting processor state from ListFile."""
    state = canvas.get_processor_state(fix_state_flow.list_file_proc)

    assert isinstance(state, nifi.ComponentStateEntity)
    assert state.component_state is not None
    assert state.component_state.component_id == fix_state_flow.list_file_proc.id

    # ListFile should have state entries after running
    local_state = state.component_state.local_state
    assert local_state is not None
    assert local_state.total_entry_count > 0
    assert len(local_state.state) > 0


def test_get_processor_state_by_id(fix_state_flow):
    """Test getting processor state using ID string."""
    state = canvas.get_processor_state(fix_state_flow.list_file_proc.id)

    assert isinstance(state, nifi.ComponentStateEntity)
    assert state.component_state.component_id == fix_state_flow.list_file_proc.id


def test_get_controller_state(fix_state_flow):
    """Test getting controller state from MapCacheServer."""
    state = canvas.get_controller_state(fix_state_flow.cache_server)

    assert isinstance(state, nifi.ComponentStateEntity)
    assert state.component_state is not None
    assert state.component_state.component_id == fix_state_flow.cache_server.id

    # MapCacheServer may or may not have visible state entries
    # (internal cache isn't always exposed via state API)
    # Key test: the API call succeeds and returns valid structure
    local_state = state.component_state.local_state
    assert local_state is not None
    assert hasattr(local_state, 'total_entry_count')
    assert hasattr(local_state, 'state')


def test_get_controller_state_by_id(fix_state_flow):
    """Test getting controller state using ID string."""
    state = canvas.get_controller_state(fix_state_flow.cache_server.id)

    assert isinstance(state, nifi.ComponentStateEntity)
    assert state.component_state.component_id == fix_state_flow.cache_server.id


def test_clear_processor_state(fix_state_flow):
    """Test clearing processor state."""
    # Verify state exists before clearing
    state_before = canvas.get_processor_state(fix_state_flow.list_file_proc)
    assert state_before.component_state.local_state.total_entry_count > 0

    # Clear state
    result = canvas.clear_processor_state(fix_state_flow.list_file_proc)
    assert isinstance(result, nifi.ComponentStateEntity)

    # Verify state is cleared
    state_after = canvas.get_processor_state(fix_state_flow.list_file_proc)
    assert state_after.component_state.local_state.total_entry_count == 0


def test_clear_controller_state(fix_state_flow):
    """Test clearing controller state."""
    # Controller must be disabled before clearing state
    canvas.schedule_controller(fix_state_flow.cache_server, scheduled=False, refresh=True)

    # Clear state (works even if empty)
    result = canvas.clear_controller_state(fix_state_flow.cache_server)
    assert isinstance(result, nifi.ComponentStateEntity)

    # Verify state is cleared (should be 0 entries)
    state_after = canvas.get_controller_state(fix_state_flow.cache_server)
    assert state_after.component_state.local_state.total_entry_count == 0


# =============================================================================
# CONTROLLER SERVICE DOCS TESTS
# =============================================================================


def test_get_controller_service_docs():
    """Test get_controller_service_docs with various input types."""
    # Test with string (controller type name)
    r1 = canvas.get_controller_service_docs('JsonTreeReader')
    assert r1 is not None
    assert 'property_descriptors' in dir(r1)
    assert isinstance(r1.property_descriptors, dict)

    # Test with DocumentedTypeDTO
    cs_type = canvas.get_controller_type('AvroReader')
    r2 = canvas.get_controller_service_docs(cs_type)
    assert r2 is not None

    # Test with non-existent type returns None
    r3 = canvas.get_controller_service_docs('NonExistentController')
    assert r3 is None


def test_get_controller_service_docs_with_entity(fix_pg, fix_cont):
    """Test get_controller_service_docs with a ControllerServiceEntity."""
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)

    r1 = canvas.get_controller_service_docs(f_c1)
    assert r1 is not None
    assert 'property_descriptors' in dir(r1)


# =============================================================================
# FLOWFILE INSPECTION TESTS
# =============================================================================


def test_list_flowfiles_empty(fix_proc):
    """Test listing FlowFiles in an empty connection."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    # Create connection
    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)

    # List should return empty list
    result = canvas.list_flowfiles(conn)
    assert isinstance(result, list)
    assert len(result) == 0

    # Cleanup
    canvas.delete_connection(conn)


def test_list_flowfiles_with_data(fix_proc):
    """Test listing FlowFiles when data is in the queue."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    # Configure first processor to generate data
    canvas.update_processor(
        f_p1, update=nifi.ProcessorConfigDTO(properties={'File Size': '10 B'})
    )

    # Create connection
    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)

    # Run first processor once to generate a FlowFile
    canvas.schedule_processor(f_p1, 'RUN_ONCE')

    # List FlowFiles in the connection
    result = canvas.list_flowfiles(conn)
    assert isinstance(result, list)
    assert len(result) >= 1

    # Check FlowFile summary has expected fields
    ff = result[0]
    assert hasattr(ff, 'uuid')
    assert hasattr(ff, 'filename')
    assert hasattr(ff, 'size')
    assert hasattr(ff, 'queued_duration')

    # Cleanup
    canvas.purge_connection(conn.id)
    canvas.delete_connection(conn)


def test_get_flowfile_details(fix_proc):
    """Test getting full FlowFile details including attributes."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    # Create connection and generate data
    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)
    canvas.schedule_processor(f_p1, 'RUN_ONCE')

    # List to get UUID
    summaries = canvas.list_flowfiles(conn)
    assert len(summaries) >= 1

    # Get full details
    details = canvas.get_flowfile_details(conn, summaries[0].uuid)
    assert details is not None
    assert hasattr(details, 'attributes')
    assert isinstance(details.attributes, dict)
    # Standard attributes should exist
    assert 'uuid' in details.attributes
    assert 'filename' in details.attributes

    # Cleanup
    canvas.purge_connection(conn.id)
    canvas.delete_connection(conn)


def test_peek_flowfiles(fix_proc):
    """Test peek_flowfiles convenience function."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    # Create connection and generate data
    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)
    canvas.schedule_processor(f_p1, 'RUN_ONCE')

    # Peek at first FlowFile
    result = canvas.peek_flowfiles(conn, limit=1)
    assert isinstance(result, list)
    assert len(result) >= 1

    # Should have full details including attributes
    ff = result[0]
    assert hasattr(ff, 'attributes')
    assert isinstance(ff.attributes, dict)

    # Cleanup
    canvas.purge_connection(conn.id)
    canvas.delete_connection(conn)


def test_list_flowfiles_by_id(fix_proc):
    """Test list_flowfiles accepts connection ID string."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)

    # Should work with ID string
    result = canvas.list_flowfiles(conn.id)
    assert isinstance(result, list)

    canvas.delete_connection(conn)


def test_get_flowfile_content(fix_proc, tmpdir):
    """Test downloading FlowFile content with various options."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    # Configure first processor to generate data with specific size
    canvas.update_processor(
        f_p1, update=nifi.ProcessorConfigDTO(properties={'File Size': '10 B'})
    )

    # Create connection and generate data
    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)
    canvas.schedule_processor(f_p1, 'RUN_ONCE')

    # List to get UUID
    summaries = canvas.list_flowfiles(conn)
    assert len(summaries) >= 1
    ff_uuid = summaries[0].uuid

    # Test 1: Default - returns bytes (random content, no text mime type)
    content = canvas.get_flowfile_content(conn, ff_uuid)
    assert isinstance(content, bytes)
    assert len(content) == 10

    # Test 2: Force text decode
    content_text = canvas.get_flowfile_content(conn, ff_uuid, decode='text')
    assert isinstance(content_text, str)

    # Test 3: Force bytes
    content_bytes = canvas.get_flowfile_content(conn, ff_uuid, decode='bytes')
    assert isinstance(content_bytes, bytes)

    # Test 4: Save to specific file path
    out_path = str(tmpdir.join("flowfile_content.bin"))
    result_path = canvas.get_flowfile_content(conn, ff_uuid, output_file=out_path)
    assert result_path.endswith("flowfile_content.bin")
    with open(result_path, "rb") as f:
        saved_content = f.read()
    assert saved_content == content

    # Test 5: Save to directory (uses FlowFile's filename)
    dir_path = str(tmpdir.mkdir("subdir"))
    result_path = canvas.get_flowfile_content(conn, ff_uuid, output_file=dir_path)
    assert dir_path in result_path
    with open(result_path, "rb") as f:
        saved_content = f.read()
    assert saved_content == content

    # Cleanup
    canvas.purge_connection(conn.id)
    canvas.delete_connection(conn)


def test_peek_flowfiles_preserves_cluster_node_id(fix_proc):
    """Test that peek_flowfiles preserves cluster_node_id on returned FlowFileDTOs."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    # Create connection and generate data
    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)
    canvas.schedule_processor(f_p1, 'RUN_ONCE')

    # Get summaries to see the cluster_node_id from listing
    summaries = canvas.list_flowfiles(conn)
    assert len(summaries) >= 1
    summary_node_id = summaries[0].cluster_node_id

    # Peek should preserve cluster_node_id on returned FlowFileDTO
    result = canvas.peek_flowfiles(conn, limit=1)
    assert len(result) >= 1
    ff = result[0]

    # FlowFileDTO should have the same cluster_node_id as the summary
    assert ff.cluster_node_id == summary_node_id

    # Cleanup
    canvas.purge_connection(conn.id)
    canvas.delete_connection(conn)


def test_get_flowfile_details_auto_resolves_cluster_node(fix_proc):
    """Test get_flowfile_details works without explicit cluster_node_id."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    # Create connection and generate data
    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)
    canvas.schedule_processor(f_p1, 'RUN_ONCE')

    # Get UUID from listing
    summaries = canvas.list_flowfiles(conn)
    assert len(summaries) >= 1
    ff_uuid = summaries[0].uuid

    # Should work without cluster_node_id (auto-resolves)
    details = canvas.get_flowfile_details(conn, ff_uuid)
    assert details is not None
    assert details.uuid == ff_uuid
    assert hasattr(details, 'attributes')

    # Cleanup
    canvas.purge_connection(conn.id)
    canvas.delete_connection(conn)


def test_get_flowfile_content_auto_resolves_cluster_node(fix_proc):
    """Test get_flowfile_content works without explicit cluster_node_id."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    # Configure first processor to generate data
    canvas.update_processor(
        f_p1, update=nifi.ProcessorConfigDTO(properties={'File Size': '10 B'})
    )

    # Create connection and generate data
    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)
    canvas.schedule_processor(f_p1, 'RUN_ONCE')

    # Get UUID from listing
    summaries = canvas.list_flowfiles(conn)
    assert len(summaries) >= 1
    ff_uuid = summaries[0].uuid

    # Should work without cluster_node_id (auto-resolves)
    content = canvas.get_flowfile_content(conn, ff_uuid)
    assert content is not None
    assert len(content) == 10

    # Cleanup
    canvas.purge_connection(conn.id)
    canvas.delete_connection(conn)


def test_get_flowfile_details_with_explicit_cluster_node(fix_proc):
    """Test get_flowfile_details with explicit cluster_node_id skips auto-resolve."""
    f_p1 = fix_proc.generate()
    f_p2 = fix_proc.generate()

    # Create connection and generate data
    conn = canvas.create_connection(f_p1, f_p2, ['success'], conftest.test_basename)
    canvas.schedule_processor(f_p1, 'RUN_ONCE')

    # Get UUID and cluster_node_id from listing
    summaries = canvas.list_flowfiles(conn)
    assert len(summaries) >= 1
    ff_uuid = summaries[0].uuid
    cluster_node_id = summaries[0].cluster_node_id

    # Should work with explicit cluster_node_id
    details = canvas.get_flowfile_details(conn, ff_uuid, cluster_node_id=cluster_node_id)
    assert details is not None
    assert details.uuid == ff_uuid

    # Cleanup
    canvas.purge_connection(conn.id)
    canvas.delete_connection(conn)
