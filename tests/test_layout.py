"""Tests for `nipyapi.layout` module."""

import pytest
from tests import conftest
from nipyapi import canvas, layout, nifi


# =============================================================================
# PURE FUNCTION TESTS (no NiFi required)
# =============================================================================


def test_snap_to_grid():
    """Test grid snapping to 8-pixel boundaries."""
    # Exact grid values unchanged
    assert layout.snap_to_grid(0) == 0
    assert layout.snap_to_grid(8) == 8
    assert layout.snap_to_grid(400) == 400

    # Values snap to nearest grid
    assert layout.snap_to_grid(1) == 0
    assert layout.snap_to_grid(4) == 0
    assert layout.snap_to_grid(5) == 8
    assert layout.snap_to_grid(7) == 8
    assert layout.snap_to_grid(401) == 400
    assert layout.snap_to_grid(404) == 400
    assert layout.snap_to_grid(405) == 408


def test_grid_position():
    """Test grid position calculation."""
    # Default origin (400, 400)
    pos = layout.grid_position(0, 0)
    assert pos == (400, 400)

    pos = layout.grid_position(0, 1)
    assert pos == (400 + layout.BLOCK_WIDTH, 400)

    pos = layout.grid_position(1, 0)
    assert pos == (400, 400 + layout.BLOCK_HEIGHT)

    pos = layout.grid_position(2, 3)
    assert pos == (400 + 3 * layout.BLOCK_WIDTH, 400 + 2 * layout.BLOCK_HEIGHT)

    # Custom origin
    pos = layout.grid_position(0, 0, origin=(0, 0))
    assert pos == (0, 0)

    pos = layout.grid_position(1, 1, origin=(100, 100))
    assert pos == (100 + layout.BLOCK_WIDTH, 100 + layout.BLOCK_HEIGHT)


def test_constants_grid_aligned():
    """Verify all dimension constants are grid-aligned."""
    assert layout.PROCESSOR_WIDTH % layout.GRID_SIZE == 0
    assert layout.PROCESSOR_HEIGHT % layout.GRID_SIZE == 0
    assert layout.PROCESS_GROUP_WIDTH % layout.GRID_SIZE == 0
    assert layout.PROCESS_GROUP_HEIGHT % layout.GRID_SIZE == 0
    assert layout.FUNNEL_WIDTH % layout.GRID_SIZE == 0
    assert layout.FUNNEL_HEIGHT % layout.GRID_SIZE == 0
    assert layout.PORT_WIDTH % layout.GRID_SIZE == 0
    assert layout.PORT_HEIGHT % layout.GRID_SIZE == 0
    assert layout.BLOCK_WIDTH % layout.GRID_SIZE == 0
    assert layout.BLOCK_HEIGHT % layout.GRID_SIZE == 0


def test_default_origin():
    """Test DEFAULT_ORIGIN is grid-aligned."""
    assert layout.DEFAULT_ORIGIN[0] % layout.GRID_SIZE == 0
    assert layout.DEFAULT_ORIGIN[1] % layout.GRID_SIZE == 0


# =============================================================================
# COMPONENT POSITION TESTS
# =============================================================================


def test_get_position_processor(fix_pg, fix_proc):
    """Test extracting position from a processor."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)
    pos = layout.get_position(f_p1)
    assert isinstance(pos, tuple)
    assert len(pos) == 2
    assert pos[0] == 400.0
    assert pos[1] == 400.0


def test_get_position_funnel(fix_pg, fix_funnel):
    """Test extracting position from a funnel."""
    f_pg = fix_pg.generate()
    f_f1 = fix_funnel.generate(parent_pg=f_pg, position=(200, 300))
    pos = layout.get_position(f_f1)
    assert pos[0] == 200.0
    assert pos[1] == 300.0


def test_get_position_invalid():
    """Test get_position raises on invalid input."""
    with pytest.raises(ValueError):
        layout.get_position("not a component")


# =============================================================================
# RELATIVE POSITIONING TESTS
# =============================================================================


def test_below(fix_pg, fix_proc):
    """Test below() positioning."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)

    # Default: 1 block below, left-aligned
    pos = layout.below(f_p1)
    original = layout.get_position(f_p1)
    assert pos[0] == original[0]  # Same X
    assert pos[1] == original[1] + layout.VERTICAL_SPACING

    # Multiple blocks
    pos = layout.below(f_p1, blocks=2)
    assert pos[1] == original[1] + 2 * layout.VERTICAL_SPACING

    # Center alignment (for smaller components like funnels)
    pos = layout.below(f_p1, align="center")
    expected_x = original[0] + (layout.PROCESSOR_WIDTH - layout.FUNNEL_WIDTH) / 2
    assert pos[0] == layout.snap_to_grid(expected_x)


def test_above(fix_pg, fix_proc):
    """Test above() positioning."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)

    pos = layout.above(f_p1)
    original = layout.get_position(f_p1)
    assert pos[0] == original[0]
    assert pos[1] == original[1] - layout.VERTICAL_SPACING


def test_right_of(fix_pg, fix_proc):
    """Test right_of() positioning."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)

    pos = layout.right_of(f_p1)
    original = layout.get_position(f_p1)
    assert pos[0] == original[0] + layout.HORIZONTAL_SPACING
    assert pos[1] == original[1]


def test_left_of(fix_pg, fix_proc):
    """Test left_of() positioning."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)

    pos = layout.left_of(f_p1)
    original = layout.get_position(f_p1)
    assert pos[0] == original[0] - layout.HORIZONTAL_SPACING
    assert pos[1] == original[1]


def test_fork(fix_pg, fix_proc):
    """Test fork() positioning for side branches."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)
    original = layout.get_position(f_p1)

    # Right fork (default)
    pos = layout.fork(f_p1, direction="right")
    assert pos[0] == original[0] + layout.FORK_SPACING
    assert pos[1] == original[1] + layout.BLOCK_HEIGHT

    # Left fork
    pos = layout.fork(f_p1, direction="left")
    assert pos[0] == original[0] - layout.FORK_SPACING
    assert pos[1] == original[1] + layout.BLOCK_HEIGHT

    # Multiple rows down
    pos = layout.fork(f_p1, direction="right", rows=2)
    assert pos[1] == original[1] + 2 * layout.BLOCK_HEIGHT

    # Invalid direction
    with pytest.raises(ValueError):
        layout.fork(f_p1, direction="up")


def test_new_flow(fix_pg, fix_proc):
    """Test new_flow() positioning."""
    # Empty canvas returns default origin
    pos = layout.new_flow()
    assert pos == layout.DEFAULT_ORIGIN

    # With existing component
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)
    original = layout.get_position(f_p1)

    pos = layout.new_flow(f_p1, direction="right")
    assert pos[0] == original[0] + layout.FLOW_SEPARATION
    assert pos[1] == original[1]

    pos = layout.new_flow(f_p1, direction="left")
    assert pos[0] == original[0] - layout.FLOW_SEPARATION

    with pytest.raises(ValueError):
        layout.new_flow(f_p1, direction="up")


# =============================================================================
# CANVAS BOUNDS TESTS
# =============================================================================


def test_get_canvas_bounds_empty(fix_pg):
    """Test bounds on empty process group."""
    f_pg = fix_pg.generate()
    bounds = layout.get_canvas_bounds(f_pg.id)
    assert bounds["min_x"] is None
    assert bounds["max_x"] is None


def test_get_canvas_bounds_with_components(fix_pg, fix_proc, fix_funnel):
    """Test bounds calculation with components."""
    f_pg = fix_pg.generate()
    # Create processors at known positions (variables unused but create components)
    _ = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(100.0, 100.0),
        name=conftest.test_processor_name + '_bounds1'
    )
    _ = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(500.0, 400.0),
        name=conftest.test_processor_name + '_bounds2'
    )

    bounds = layout.get_canvas_bounds(f_pg.id)
    assert bounds["min_x"] == 100.0
    assert bounds["min_y"] == 100.0
    assert bounds["max_x"] == 500.0
    assert bounds["max_y"] == 400.0


def test_get_canvas_bounds_with_component_list(fix_pg, fix_proc):
    """Test bounds calculation with explicit component list."""
    f_pg = fix_pg.generate()
    p1 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(200.0, 200.0),
        name=conftest.test_processor_name + '_list1'
    )
    p2 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(600.0, 500.0),
        name=conftest.test_processor_name + '_list2'
    )

    # Pass component list directly
    bounds = layout.get_canvas_bounds(f_pg.id, components=[p1, p2])
    assert bounds["min_x"] == 200.0
    assert bounds["max_x"] == 600.0


# =============================================================================
# MOVE FUNCTION TESTS
# =============================================================================


def test_move_processor(fix_pg, fix_proc):
    """Test moving a processor to a new position."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)

    new_pos = (600.0, 700.0)
    result = layout.move_processor(f_p1, new_pos)

    assert isinstance(result, nifi.ProcessorEntity)
    assert result.position.x == 600.0
    assert result.position.y == 700.0


def test_move_process_group(fix_pg):
    """Test moving a process group."""
    f_pg = fix_pg.generate()
    # Original position not needed for assertion, just verifying move works

    new_pos = (800.0, 200.0)
    result = layout.move_process_group(f_pg, new_pos)

    assert isinstance(result, nifi.ProcessGroupEntity)
    assert result.position.x == 800.0
    assert result.position.y == 200.0


def test_move_funnel(fix_pg, fix_funnel):
    """Test moving a funnel."""
    f_pg = fix_pg.generate()
    f_f1 = fix_funnel.generate(parent_pg=f_pg)

    new_pos = (300.0, 500.0)
    result = layout.move_funnel(f_f1, new_pos)

    assert isinstance(result, nifi.FunnelEntity)
    updated_pos = layout.get_position(result)
    assert updated_pos[0] == 300.0
    assert updated_pos[1] == 500.0


def test_move_component_auto_detect(fix_pg, fix_proc, fix_funnel):
    """Test move_component auto-detects component type."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)
    f_f1 = fix_funnel.generate(parent_pg=f_pg)

    # Move processor
    result = layout.move_component(f_p1, (100.0, 100.0))
    assert layout.get_position(result) == (100.0, 100.0)

    # Move funnel
    result = layout.move_component(f_f1, (200.0, 200.0))
    assert layout.get_position(result) == (200.0, 200.0)


# =============================================================================
# SUGGEST EMPTY POSITION TESTS
# =============================================================================


def test_suggest_empty_position_empty_canvas(fix_pg):
    """Test suggest_empty_position on empty canvas."""
    f_pg = fix_pg.generate()
    pos = layout.suggest_empty_position(f_pg.id)
    assert pos == layout.DEFAULT_ORIGIN


def test_suggest_empty_position_with_components(fix_pg, fix_proc):
    """Test suggest_empty_position finds space around existing components."""
    f_pg = fix_pg.generate()
    _ = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 400.0),
        name=conftest.test_processor_name + '_suggest1'
    )

    # Right of existing
    pos = layout.suggest_empty_position(f_pg.id, prefer="right")
    assert pos[0] > 400.0

    # Below existing
    pos = layout.suggest_empty_position(f_pg.id, prefer="below")
    assert pos[1] > 400.0


# =============================================================================
# BEND POSITION TESTS
# =============================================================================


def test_suggest_bend_position(fix_pg, fix_proc):
    """Test bend position calculation for L-shaped connections."""
    f_pg = fix_pg.generate()
    p1 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(100.0, 100.0),
        name=conftest.test_processor_name + '_bend1'
    )
    p2 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(500.0, 400.0),
        name=conftest.test_processor_name + '_bend2'
    )

    bend = layout.suggest_bend_position(p1, p2)
    assert isinstance(bend, tuple)
    assert len(bend) == 2
    # Bend should be grid-aligned
    assert bend[0] % layout.GRID_SIZE == 0
    assert bend[1] % layout.GRID_SIZE == 0


# =============================================================================
# PROCESS GROUP GRID TESTS
# =============================================================================


def test_align_pg_grid_dry_run(fix_pg):
    """Test align_pg_grid dry run mode."""
    # Create a parent PG with nested PGs (variables unused - created for side effect)
    parent = fix_pg.generate(suffix='_parent')
    _ = canvas.create_process_group(parent, conftest.test_pg_name + '_child1', (100, 100))
    _ = canvas.create_process_group(parent, conftest.test_pg_name + '_child2', (200, 300))

    # Dry run should return moves without executing
    moves = layout.align_pg_grid(parent.id, dry_run=True)
    assert isinstance(moves, list)
    assert len(moves) == 2
    for move in moves:
        assert 'id' in move
        assert 'name' in move
        assert 'from' in move
        assert 'to' in move


def test_align_pg_grid_execute(fix_pg):
    """Test align_pg_grid actually moves PGs."""
    parent = fix_pg.generate(suffix='_grid_parent')
    child1 = canvas.create_process_group(parent, conftest.test_pg_name + '_grid1', (50, 50))
    child2 = canvas.create_process_group(parent, conftest.test_pg_name + '_grid2', (300, 500))

    # Execute alignment
    _ = layout.align_pg_grid(parent.id, columns=2, origin=(0, 0))

    # Verify PGs were moved to grid positions
    updated_pg1 = canvas.get_process_group(child1.id, 'id')
    updated_pg2 = canvas.get_process_group(child2.id, 'id')

    # Both should be at grid positions
    assert updated_pg1.position.x % layout.BLOCK_WIDTH == 0
    assert updated_pg1.position.y % layout.BLOCK_HEIGHT == 0
    assert updated_pg2.position.x % layout.BLOCK_WIDTH == 0
    assert updated_pg2.position.y % layout.BLOCK_HEIGHT == 0


def test_align_pg_grid_sort_by_name(fix_pg):
    """Test align_pg_grid with alphabetical sorting."""
    parent = fix_pg.generate(suffix='_sort_parent')
    # Create in reverse alphabetical order
    child_z = canvas.create_process_group(parent, conftest.test_pg_name + '_Z', (100, 100))
    child_a = canvas.create_process_group(parent, conftest.test_pg_name + '_A', (200, 200))

    # Align with sorting
    _ = layout.align_pg_grid(parent.id, sort_by_name=True, origin=(0, 0))

    # A should be first (position 0,0)
    pg_a = canvas.get_process_group(child_a.id, 'id')
    pg_z = canvas.get_process_group(child_z.id, 'id')

    # A should be at origin or first position
    assert pg_a.position.x <= pg_z.position.x or pg_a.position.y < pg_z.position.y


def test_suggest_pg_position(fix_pg):
    """Test suggest_pg_position finds empty grid slots."""
    parent = fix_pg.generate(suffix='_suggest_parent')

    # First suggestion on empty parent
    pos1 = layout.suggest_pg_position(parent.id)
    assert pos1 == layout.DEFAULT_ORIGIN

    # Create a PG at suggested position
    _ = canvas.create_process_group(parent, conftest.test_pg_name + '_pos1', pos1)

    # Next suggestion should be different
    pos2 = layout.suggest_pg_position(parent.id)
    assert pos2 != pos1


# =============================================================================
# FLOW SPINE AND BRANCH TESTS
# =============================================================================


def test_find_flow_spine_simple(fix_pg, fix_proc):
    """Test finding spine in a simple linear flow."""
    f_pg = fix_pg.generate()
    p1 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 100.0),
        name=conftest.test_processor_name + '_spine1'
    )
    p2 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 300.0),
        name=conftest.test_processor_name + '_spine2'
    )
    p3 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 500.0),
        name=conftest.test_processor_name + '_spine3'
    )

    # Connect p1 -> p2 -> p3
    canvas.create_connection(p1, p2, name=conftest.test_basename)
    canvas.create_connection(p2, p3, name=conftest.test_basename)

    spine = layout.find_flow_spine(f_pg.id)
    assert isinstance(spine, list)
    assert len(spine) == 3


def test_get_side_branches(fix_pg, fix_proc, fix_funnel):
    """Test finding side branches off a spine."""
    f_pg = fix_pg.generate()
    # Create a flow with a clearly longer main spine than any branch
    # Main spine: p1 -> p2 -> p3 -> p4 (length 4)
    # Side branch: p2 -> funnel (length 2 from p1, shorter than main)
    p1 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 100.0),
        name=conftest.test_processor_name + '_main1'
    )
    p2 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 300.0),
        name=conftest.test_processor_name + '_main2'
    )
    p3 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 500.0),
        name=conftest.test_processor_name + '_main3'
    )
    p4 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 700.0),
        name=conftest.test_processor_name + '_main4'
    )
    # Create side branch as funnel (clearly terminal, no further connections)
    f_side = fix_funnel.generate(parent_pg=f_pg, position=(700, 300))

    # Connect main spine (4 components = length 4)
    canvas.create_connection(p1, p2, name=conftest.test_basename)
    canvas.create_connection(p2, p3, name=conftest.test_basename)
    canvas.create_connection(p3, p4, name=conftest.test_basename)
    # Connect side branch (shorter path: p1->p2->funnel = length 3)
    canvas.create_connection(p2, f_side, name=conftest.test_basename)

    spine = layout.find_flow_spine(f_pg.id)

    # find_flow_spine returns list of component IDs (strings)
    assert isinstance(spine, list)
    # Spine should be the longest path: p1 -> p2 -> p3 -> p4
    assert len(spine) == 4, f"Expected spine length 4, got {len(spine)}: {spine}"
    # All main spine components should be in the list
    assert p1.id in spine, "p1 should be in spine"
    assert p2.id in spine, "p2 should be in spine"
    assert p3.id in spine, "p3 should be in spine"
    assert p4.id in spine, "p4 should be in spine"
    # Funnel should NOT be in spine (it's a branch)
    assert f_side.id not in spine, "funnel should NOT be in spine"

    branches = layout.get_side_branches(f_pg.id, spine=spine)

    # get_side_branches returns a dict: {component_id: [branch_ids]}
    assert isinstance(branches, dict)
    # p2 has a branch to f_side, so branches should contain this
    all_branch_ids = []
    for branch_list in branches.values():
        all_branch_ids.extend(branch_list)
    assert f_side.id in all_branch_ids, f"funnel should be in branches: {branches}"


# =============================================================================
# FLOW LAYOUT TESTS
# =============================================================================


def test_suggest_flow_layout(fix_pg, fix_proc):
    """Test automatic flow layout suggestion."""
    f_pg = fix_pg.generate()
    p1 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(100.0, 50.0),
        name=conftest.test_processor_name + '_layout1'
    )
    p2 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(500.0, 400.0),
        name=conftest.test_processor_name + '_layout2'
    )

    canvas.create_connection(p1, p2, name=conftest.test_basename)

    plan = layout.suggest_flow_layout(f_pg.id)

    # Verify plan structure
    assert isinstance(plan, dict)
    assert 'spine' in plan
    assert 'branches' in plan
    assert isinstance(plan['spine'], list)

    # Verify spine contains actual layout items with positions
    assert len(plan['spine']) == 2, f"Spine should have 2 components, got {len(plan['spine'])}"
    for item in plan['spine']:
        assert 'id' in item, "Spine item should have 'id'"
        assert 'position' in item, "Spine item should have 'position'"
        # Position should be a tuple/list of 2 coordinates
        assert len(item['position']) == 2, "Position should be (x, y)"

    # Verify both processors are in the plan
    spine_ids = [item['id'] for item in plan['spine']]
    assert p1.id in spine_ids, "p1 should be in spine"
    assert p2.id in spine_ids, "p2 should be in spine"


# =============================================================================
# TRANSPOSE FLOW TESTS
# =============================================================================


def test_transpose_flow(fix_pg, fix_proc):
    """Test moving an entire flow by an offset."""
    f_pg = fix_pg.generate()
    p1 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(100.0, 100.0),
        name=conftest.test_processor_name + '_trans1'
    )
    p2 = canvas.create_processor(
        parent_pg=f_pg,
        processor=canvas.get_processor_type('GenerateFlowFile'),
        location=(100.0, 300.0),
        name=conftest.test_processor_name + '_trans2'
    )

    canvas.create_connection(p1, p2, name=conftest.test_basename)

    # Get flow components
    components = canvas.get_flow_components(p1, pg_id=f_pg.id)
    assert len(components) == 2

    # Transpose by offset
    offset = (200.0, 50.0)
    layout.transpose_flow(components, offset)

    # Verify positions moved
    p1_new = canvas.get_processor(p1.id, 'id')
    p2_new = canvas.get_processor(p2.id, 'id')

    assert p1_new.position.x == 300.0  # 100 + 200
    assert p1_new.position.y == 150.0  # 100 + 50
    assert p2_new.position.x == 300.0
    assert p2_new.position.y == 350.0  # 300 + 50


# =============================================================================
# PORT AND LABEL MOVEMENT TESTS
# =============================================================================


def test_move_port_input(fix_pg):
    """Test moving an input port."""
    f_pg = fix_pg.generate()

    # Create an input port using correct signature
    port = canvas.create_port(
        pg_id=f_pg.id,
        port_type='INPUT_PORT',
        name=conftest.test_basename + '_input_port',
        state='STOPPED',
        position=(100, 100)
    )

    try:
        # Move the port
        new_position = (300, 400)
        result = layout.move_port(port, new_position)

        # Verify position changed
        assert result.position.x == 300
        assert result.position.y == 400
    finally:
        # Clean up - use result which has updated revision
        canvas.delete_port(result)


def test_move_port_output(fix_pg):
    """Test moving an output port."""
    f_pg = fix_pg.generate()

    # Create an output port
    port = canvas.create_port(
        pg_id=f_pg.id,
        port_type='OUTPUT_PORT',
        name=conftest.test_basename + '_output_port',
        state='STOPPED',
        position=(100, 100)
    )

    try:
        # Move the port
        new_position = (500, 200)
        result = layout.move_port(port, new_position)

        # Verify position changed
        assert result.position.x == 500
        assert result.position.y == 200
    finally:
        # Clean up - use result which has updated revision
        canvas.delete_port(result)


def test_move_port_no_refresh(fix_pg):
    """Test moving a port without pre-fetch refresh."""
    f_pg = fix_pg.generate()

    # Create a port
    port = canvas.create_port(
        pg_id=f_pg.id,
        port_type='INPUT_PORT',
        name=conftest.test_basename + '_port_noref',
        state='STOPPED',
        position=(100, 100)
    )

    try:
        # Move without refresh (no pre-fetch)
        # Still returns updated entity from the API call
        result = layout.move_port(port, (200, 200), refresh=False)
        assert result is not None
        assert result.position.x == 200
        assert result.position.y == 200
    finally:
        # Clean up - use result which has updated revision
        canvas.delete_port(result)


def test_move_component_with_port(fix_pg):
    """Test move_component auto-detects and moves ports."""
    f_pg = fix_pg.generate()

    # Create an input port
    port = canvas.create_port(
        pg_id=f_pg.id,
        port_type='INPUT_PORT',
        name=conftest.test_basename + '_mc_port',
        state='STOPPED',
        position=(100, 100)
    )

    try:
        # Move using generic function
        result = layout.move_component(port, (600, 400))

        # Verify
        assert result.position.x == 600
        assert result.position.y == 400
    finally:
        # Clean up - use result which has updated revision
        canvas.delete_port(result)


def test_snap_position():
    """Test snap_position snaps both coordinates to grid."""
    # Test normal coordinates - snaps to nearest 8
    # 123.5 / 8 = 15.4375 -> round(15.4375) = 15 -> 15 * 8 = 120
    # 234.7 / 8 = 29.3375 -> round(29.3375) = 29 -> 29 * 8 = 232
    result = layout.snap_position((123.5, 234.7))
    assert result == (120, 232)

    # Test already aligned
    result = layout.snap_position((200.0, 400.0))
    assert result == (200, 400)

    # Test rounding behavior
    # 199 / 8 = 24.875 -> round = 25 -> 200
    # 401 / 8 = 50.125 -> round = 50 -> 400
    result = layout.snap_position((199.0, 401.0))
    assert result == (200, 400)


def test_get_pg_grid_position():
    """Test process group grid positioning."""
    # First position (0,0) should return DEFAULT_ORIGIN
    pos = layout.get_pg_grid_position(0, 0)
    assert pos == layout.DEFAULT_ORIGIN


def test_new_flow_invalid_direction(fix_pg, fix_proc):
    """Test new_flow with invalid direction raises error."""
    f_pg = fix_pg.generate()
    proc = fix_proc.generate(f_pg)

    # Invalid direction should raise ValueError
    with pytest.raises(ValueError, match="Invalid direction"):
        layout.new_flow(proc, direction="below")


def test_left_of_component(fix_pg, fix_proc):
    """Test left_of positioning with multiple blocks."""
    f_pg = fix_pg.generate()
    proc = fix_proc.generate(f_pg)

    # Get position 2 blocks to the left
    new_pos = layout.left_of(proc, blocks=2, align="aligned")

    proc_pos = layout.get_position(proc)
    # left_of uses BLOCK_WIDTH (400) not GRID_SIZE
    expected_x = proc_pos[0] - (2 * layout.BLOCK_WIDTH)
    assert new_pos[0] == expected_x
    assert new_pos[1] == proc_pos[1]  # Same Y when aligned


def test_check_overlap():
    """Test _check_overlap internal function."""
    # Test overlapping positions
    assert layout._check_overlap((100, 100), (150, 150), 100, 100) is True

    # Test non-overlapping positions
    assert layout._check_overlap((100, 100), (300, 300), 100, 100) is False

    # Test edge case - just touching
    assert layout._check_overlap((100, 100), (200, 100), 100, 100) is False
