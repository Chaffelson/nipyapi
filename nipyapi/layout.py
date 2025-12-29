"""
NiFi Canvas Layout Module.

Provides a block-based system for positioning components on the NiFi canvas.
Component dimensions are empirically derived from the NiFi UI, and all positions
snap to NiFi's 8-pixel grid for UI compatibility.

Two Layout Patterns:

    1. FLOW LAYOUT - For components with connections (processors, funnels, ports)
       Components need padding for queue labels and retry loops. Use:
       - below(), above(), left_of(), right_of() for sequential flow building
       - fork() for diagonal side branches
       - new_flow() for starting independent flows with separation

    2. PROCESS GROUP GRID - For organizing PGs without connections
       PGs are packed in a simple grid with minimal padding. Use:
       - align_pg_grid() to arrange existing PGs into a grid
       - suggest_pg_position() to find the next slot in a grid

Block System:
    - BLOCK_WIDTH (400px): Horizontal spacing for grid layouts
    - BLOCK_HEIGHT (200px): Vertical spacing (includes room for connection queues)
    - FORK_SPACING (640px): Diagonal fork spacing (processor + queue box + padding)

Component Dimensions (empirically verified):
    - Processor: 352 x 128 px
    - Process Group: 384 x 176 px
    - Port (Input/Output): 240 x 48 px
    - Funnel: 48 x 48 px
    - Queue Box: 224 x 56 px (connection label)
    - Label: User-definable (default 150 x 150 px)

Flow Layout Example::

    import nipyapi

    # Start a new flow on empty canvas (returns DEFAULT_ORIGIN: 400, 400)
    first_pos = nipyapi.layout.new_flow()
    proc1 = nipyapi.canvas.create_processor(pg, proc_type, location=first_pos)

    # Create next processor below
    proc2 = nipyapi.canvas.create_processor(pg, proc_type,
        location=nipyapi.layout.below(proc1))

    # Place a funnel centered below (for smaller components)
    funnel = nipyapi.canvas.create_funnel(pg.id,
        position=nipyapi.layout.below(proc2, align="center"))

    # Fork a side branch (diagonal: right and down)
    side_proc = nipyapi.canvas.create_processor(pg, proc_type,
        location=nipyapi.layout.fork(proc1, direction="right"))

Process Group Grid Example::

    # Arrange all PGs in root canvas into a sorted grid
    nipyapi.layout.align_pg_grid(root_id, sort_by_name=True)

    # Add a new PG in the next available grid slot
    pos = nipyapi.layout.suggest_pg_position(root_id)
    nipyapi.canvas.create_process_group(root_pg, "New PG", location=pos)

Automatic Flow Layout::

    plan = nipyapi.layout.suggest_flow_layout(pg.id)
    for item in plan['spine'] + plan['branches']:
        comp = get_component(item['id'])
        nipyapi.layout.move_component(comp, item['position'])

This typically achieves 90% organization. See limitations below.

Limitations of suggest_flow_layout():
    The automatic layout handles most cases well but has known limitations that
    require post-layout visual inspection and manual adjustment:

    1. TERMINAL BRANCH OVERLAPS: Multiple branches ending at similar depths may
       place components at overlapping positions. Fix by nudging components
       horizontally using move_component().

    2. FEEDBACK LOOP ROUTING: Long connections that loop back to earlier
       components (e.g., retry loops) create diagonal lines across the layout.
       The algorithm clears all bends for clean straight lines, but feedback
       loops may benefit from manual bend placement to route around components.

    3. QUEUE BOX COLLISIONS: Connection label boxes are not collision-detected.
       Some queue labels may overlap components or each other. Adjust by adding
       bends to reroute connections or moving components slightly.

    4. SEMANTIC VS LONGEST PATH: The spine is the longest forward path, which
       may include error handling rather than the "success" path. Use
       prefer_success=True in find_flow_spine() to weight success relationships,
       though significantly longer paths may still win.

    Recommended workflow for complex flows:
        1. Run suggest_flow_layout() for initial organization
        2. Visual inspection (screenshot or UI review)
        3. Adjust overlapping terminals with move_component()
        4. Add bends to feedback loops for clean routing
        5. Verify queue label positions
"""

import math
from collections import deque
from typing import Tuple

import nipyapi

# =============================================================================
# GRID SYSTEM - NiFi UI snaps to an 8-pixel grid
# =============================================================================

GRID_SIZE = 8  # NiFi UI snap grid in pixels

# =============================================================================
# COMPONENT DIMENSIONS (empirically verified, all grid-aligned)
# =============================================================================

PROCESSOR_WIDTH = 352  # 44 grid units
PROCESSOR_HEIGHT = 128  # 16 grid units

PROCESS_GROUP_WIDTH = 384  # 48 grid units
PROCESS_GROUP_HEIGHT = 176  # 22 grid units

FUNNEL_WIDTH = 48  # 6 grid units
FUNNEL_HEIGHT = 48  # 6 grid units

PORT_WIDTH = 240  # 30 grid units
PORT_HEIGHT = 48  # 6 grid units (same as funnel)

# Queue box - connection label displaying relationship name and queue stats
QUEUE_BOX_WIDTH = 224  # 28 grid units - fits "Name: success" + stats
QUEUE_BOX_HEIGHT = 56  # 7 grid units - two lines of text

# =============================================================================
# BLOCK DIMENSIONS - Standard spacing for all grid layouts
# =============================================================================

# Block dimensions are used for:
# - Flow layouts (processor stacking with room for connections)
# - Process group grids (organized arrangement of PGs)
# Values are grid-aligned and sized to fit the largest component (process group)
# plus comfortable padding.
BLOCK_WIDTH = 400  # Horizontal spacing (grid-aligned: 50 units)
BLOCK_HEIGHT = 200  # Vertical spacing (grid-aligned: 25 units)

# =============================================================================
# DERIVED SPACING CONSTANTS
# =============================================================================

# Vertical stacking (building a flow top-to-bottom)
VERTICAL_SPACING = BLOCK_HEIGHT  # 200px

# Horizontal stacking (components side-by-side)
HORIZONTAL_SPACING = BLOCK_WIDTH  # 400px

# Independent flows (separate flows with room for side-connections/retry loops)
# One block provides space for retry loops plus visual separation
FLOW_SEPARATION = BLOCK_WIDTH  # 400px

# Centering offsets - to center smaller components relative to processors
# Funnel: (352 - 48) / 2 = 152px
FUNNEL_CENTER_OFFSET = (PROCESSOR_WIDTH - FUNNEL_WIDTH) // 2  # 152px
# Port: (352 - 240) / 2 = 56px
PORT_CENTER_OFFSET = (PROCESSOR_WIDTH - PORT_WIDTH) // 2  # 56px
# Vertical centering for side placement
FUNNEL_VCENTER_OFFSET = (PROCESSOR_HEIGHT - FUNNEL_HEIGHT) // 2  # 40px
PORT_VCENTER_OFFSET = (PROCESSOR_HEIGHT - PORT_HEIGHT) // 2  # 40px

# =============================================================================
# FORK SPACING - Component-based calculation for side branches
# =============================================================================

# Fork spacing = processor width + queue box width + padding (8 grid units)
# This ensures the queue label box fits between source and forked processors
# without overlapping either component.
#
# Note: The resulting ratio of FORK_SPACING/BLOCK_WIDTH = 640/400 = 1.6 closely
# approximates the golden ratio (phi = 1.618...), which may contribute to the
# visually pleasing aesthetic of the layout.
#
# Verification: BLOCK_HEIGHT is also component-derived:
# PROCESSOR_HEIGHT (128) + QUEUE_BOX_HEIGHT (56) + padding (16 = 2 grid units) = 200px
FORK_SPACING = PROCESSOR_WIDTH + QUEUE_BOX_WIDTH + GRID_SIZE * 8  # 352+224+64=640px


# =============================================================================
# CANVAS DEFAULTS
# =============================================================================

# Default starting position for new flows on an empty canvas.
# (400, 400) places the first component roughly centered in the initial viewport,
# leaving room for expansion in all directions. Both values are block-aligned.
DEFAULT_ORIGIN = (400, 400)

# =============================================================================
# GRID SNAPPING
# =============================================================================


def snap_to_grid(value: float) -> int:
    """
    Snap a coordinate value to the nearest grid point.

    NiFi's UI uses an 8-pixel grid for drag-and-drop positioning. While the
    API accepts any coordinate value, aligning to the UI grid ensures users
    can reposition components manually without unexpected shifts.

    Args:
        value: Coordinate value to snap

    Returns:
        Value rounded to nearest multiple of GRID_SIZE (8)

    Example::

        x = snap_to_grid(145)  # Returns 144
        y = snap_to_grid(150)  # Returns 152
    """
    return round(value / GRID_SIZE) * GRID_SIZE


def snap_position(position: Tuple[float, float]) -> Tuple[int, int]:
    """
    Snap a position tuple to the grid.

    Args:
        position: (x, y) tuple

    Returns:
        Grid-aligned (x, y) tuple

    Example::

        pos = snap_position((145, 203))  # Returns (144, 200)
    """
    return (snap_to_grid(position[0]), snap_to_grid(position[1]))


# =============================================================================
# POSITION EXTRACTION
# =============================================================================


def get_position(component) -> Tuple[float, float]:
    """
    Extract the (x, y) position from any canvas component.

    Args:
        component: Any NiFi canvas component (processor, process group,
            funnel, port, etc.)

    Returns:
        Tuple of (x, y) coordinates

    Raises:
        ValueError: If component has no position attribute
    """
    if hasattr(component, "position") and component.position:
        return (component.position.x, component.position.y)
    if hasattr(component, "component") and hasattr(component.component, "position"):
        pos = component.component.position
        if pos:
            return (pos.x, pos.y)
    raise ValueError(f"Cannot extract position from {type(component).__name__}")


# =============================================================================
# RELATIVE POSITIONING FUNCTIONS
# =============================================================================


def below(component, blocks: int = 1, align: str = "aligned") -> Tuple[float, float]:
    """
    Calculate position below a component.

    Use this for building vertical flows where components connect top-to-bottom.

    Args:
        component: Reference component to position relative to
        blocks: Number of blocks below (default 1)
        align: Horizontal alignment:
            - "aligned": Same X position (default)
            - "center": Centered for funnels (152px offset)
            - "center_port": Centered for ports (56px offset)

    Returns:
        Position tuple (x, y) for the new component

    Example::

        proc2_pos = nipyapi.layout.below(proc1)
        funnel_pos = nipyapi.layout.below(proc1, align="center")
        port_pos = nipyapi.layout.below(proc1, align="center_port")
    """
    x, y = get_position(component)
    if align == "center":
        x = x + FUNNEL_CENTER_OFFSET
    elif align == "center_port":
        x = x + PORT_CENTER_OFFSET
    return (x, y + (BLOCK_HEIGHT * blocks))


def above(component, blocks: int = 1, align: str = "aligned") -> Tuple[float, float]:
    """
    Calculate position above a component.

    Args:
        component: Reference component to position relative to
        blocks: Number of blocks above (default 1)
        align: Horizontal alignment:
            - "aligned": Same X position (default)
            - "center": Centered for funnels
            - "center_port": Centered for ports

    Returns:
        Position tuple (x, y) for the new component
    """
    x, y = get_position(component)
    if align == "center":
        x = x + FUNNEL_CENTER_OFFSET
    elif align == "center_port":
        x = x + PORT_CENTER_OFFSET
    return (x, y - (BLOCK_HEIGHT * blocks))


def right_of(component, blocks: int = 1, align: str = "aligned") -> Tuple[float, float]:
    """
    Calculate position to the right of a component.

    Use this for placing related components side-by-side within the same flow.

    Args:
        component: Reference component to position relative to
        blocks: Number of blocks to the right (default 1)
        align: Vertical alignment:
            - "aligned": Same Y position (default)
            - "center": Vertically centered for funnels
            - "center_port": Vertically centered for ports

    Returns:
        Position tuple (x, y) for the new component

    Example::

        proc2_pos = nipyapi.layout.right_of(proc1)
        funnel_pos = nipyapi.layout.right_of(proc1, align="center")
    """
    x, y = get_position(component)
    if align == "center":
        y = y + FUNNEL_VCENTER_OFFSET
    elif align == "center_port":
        y = y + PORT_VCENTER_OFFSET
    return (x + (BLOCK_WIDTH * blocks), y)


def left_of(component, blocks: int = 1, align: str = "aligned") -> Tuple[float, float]:
    """
    Calculate position to the left of a component.

    Args:
        component: Reference component to position relative to
        blocks: Number of blocks to the left (default 1)
        align: Vertical alignment:
            - "aligned": Same Y position (default)
            - "center": Vertically centered for funnels
            - "center_port": Vertically centered for ports

    Returns:
        Position tuple (x, y) for the new component
    """
    x, y = get_position(component)
    if align == "center":
        y = y + FUNNEL_VCENTER_OFFSET
    elif align == "center_port":
        y = y + PORT_VCENTER_OFFSET
    return (x - (BLOCK_WIDTH * blocks), y)


def suggest_bend_position(source, target) -> Tuple[float, float]:
    """
    Calculate an optimal bend position for a connection between two components.

    Creates a clean right-angle path by placing the bend at the intersection of:
    - Horizontal line from the source component's exit point
    - Vertical line to the target component's entry point

    This produces an L-shaped connection that is geometrically clean and
    easy to follow visually.

    Args:
        source: Source component entity
        target: Target component entity

    Returns:
        Position tuple (x, y) for the bend point

    Example::

        bend = nipyapi.layout.suggest_bend_position(proc1, proc2)
        nipyapi.canvas.create_connection(proc1, proc2, bends=[bend])
    """
    src_pos = get_position(source)
    tgt_pos = get_position(target)

    # Determine component dimensions (use processor size as default)
    # src_height is used for vertical center calculation
    # tgt_width is used for horizontal center calculation
    src_height = PROCESSOR_HEIGHT
    tgt_width = PROCESSOR_WIDTH

    # Adjust for smaller components
    src_type = type(source).__name__
    tgt_type = type(target).__name__
    if "FunnelEntity" in src_type:
        src_height = FUNNEL_HEIGHT
    elif "PortEntity" in src_type:
        src_height = PORT_HEIGHT

    if "FunnelEntity" in tgt_type:
        tgt_width = FUNNEL_WIDTH
    elif "PortEntity" in tgt_type:
        tgt_width = PORT_WIDTH

    # Calculate exit and entry points
    # Source exits from right side at vertical center
    src_exit_y = src_pos[1] + src_height / 2

    # Target enters at horizontal center
    tgt_center_x = tgt_pos[0] + tgt_width / 2

    # Bend at intersection: target's X, source's Y
    # This creates an L-shape: horizontal from source, then vertical to target
    bend_x = snap_to_grid(tgt_center_x)
    bend_y = snap_to_grid(src_exit_y)

    return (float(bend_x), float(bend_y))


def fork(component, direction: str = "right", rows: int = 1) -> Tuple[float, float]:
    """
    Calculate position for a forked side branch from a flow.

    Uses component-based spacing: processor width + queue box width + padding.
    This ensures the queue label on the diagonal connection doesn't overlap
    either the source or the forked processor.

    Args:
        component: Source component (fork point)
        direction: "right" or "left" (default "right")
        rows: Number of rows below source (default 1)

    Returns:
        Position tuple (x, y) for the forked processor

    Example::

        # Fork a side path from a processor
        side_pos = nipyapi.layout.fork(main_proc, direction="right")
        side_proc = nipyapi.canvas.create_processor(pg, proc_type, location=side_pos)
    """
    x, y = get_position(component)
    y_offset = BLOCK_HEIGHT * rows

    if direction == "right":
        return (x + FORK_SPACING, y + y_offset)
    if direction == "left":
        return (x - FORK_SPACING, y + y_offset)
    raise ValueError(f"Invalid direction: {direction}. Use 'right' or 'left'.")


# =============================================================================
# FLOW LAYOUT FUNCTIONS
# =============================================================================


def new_flow(component=None, direction: str = "right") -> Tuple[float, float]:
    """
    Calculate position for a new flow relative to a known component.

    Use this when you have a specific reference component and want to start
    a new independent flow next to it. Creates 2 blocks (800px) separation
    to allow room for side-connections and retry loops on both flows.

    If no component is provided (empty canvas), returns DEFAULT_ORIGIN.

    When to use new_flow vs suggest_empty_position:
        - new_flow(): You know which component to start next to
        - suggest_empty_position(): Find empty space by scanning all components

    Args:
        component: Reference component (typically the top of an existing flow).
            If None, returns DEFAULT_ORIGIN for starting on an empty canvas.
        direction: "right" or "left" (default "right")

    Returns:
        Position tuple (x, y) for the new flow's first component

    Example::

        # Start first flow on empty canvas
        first_pos = nipyapi.layout.new_flow()  # Returns DEFAULT_ORIGIN

        # Start a new flow to the right of an existing one
        new_flow_pos = nipyapi.layout.new_flow(existing_flow_top)
        proc1 = nipyapi.canvas.create_processor(pg, proc_type, location=new_flow_pos)
    """
    if component is None:
        return DEFAULT_ORIGIN

    x, y = get_position(component)
    if direction == "right":
        return (x + FLOW_SEPARATION, y)
    if direction == "left":
        return (x - FLOW_SEPARATION, y)
    raise ValueError(f"Invalid direction: {direction}. Use 'right' or 'left'.")


# =============================================================================
# GRID POSITIONING
# =============================================================================


def grid_position(row: int, col: int, origin: tuple = DEFAULT_ORIGIN) -> tuple:
    """
    Calculate position in a grid layout.

    Useful for creating organized layouts of related components.

    Args:
        row: Row index (0-based, increases downward)
        col: Column index (0-based, increases rightward)
        origin: Starting position for the grid (default (0, 0))

    Returns:
        Position tuple (x, y) for the grid cell

    Example::

        # Create a 2x2 grid of processors
        for row in range(2):
            for col in range(2):
                pos = nipyapi.layout.grid_position(row, col)
                create_processor(pg, proc_type, location=pos)
    """
    origin_x, origin_y = origin
    x = origin_x + (col * BLOCK_WIDTH)
    y = origin_y + (row * BLOCK_HEIGHT)
    return (x, y)


# =============================================================================
# CANVAS ANALYSIS
# =============================================================================


def get_canvas_bounds(pg_id: str = None, components: list = None) -> dict:
    """
    Get the bounding box of components.

    Can operate in two modes:
        1. pg_id provided: Get bounds of all components in the process group
        2. components provided: Get bounds of a specific list of components

    Args:
        pg_id: Process group ID (fetches all components in PG)
        components: List of component entities to calculate bounds for

    Returns:
        Dict with keys: min_x, max_x, min_y, max_y, width, height
        Returns None values if no components found.

    Example::

        # Get bounds of entire canvas
        bounds = nipyapi.layout.get_canvas_bounds(pg_id=pg.id)

        # Get bounds of a specific flow (from get_flow_components)
        flow_components = nipyapi.canvas.get_flow_components(proc1)
        bounds = nipyapi.layout.get_canvas_bounds(components=flow_components)
    """
    all_positions = []

    if components is not None:
        # Mode 2: Calculate from provided component list
        for comp in components:
            pos = get_position(comp)
            all_positions.append(pos)
    elif pg_id is not None:
        # Mode 1: Fetch all components from process group
        flow = nipyapi.canvas.get_flow(pg_id)
        fc = flow.process_group_flow.flow

        for component_list in [
            fc.processors or [],
            fc.process_groups or [],
            fc.funnels or [],
            fc.input_ports or [],
            fc.output_ports or [],
        ]:
            for comp in component_list:
                if hasattr(comp, "position") and comp.position:
                    all_positions.append((comp.position.x, comp.position.y))
    else:
        raise ValueError("Must provide either pg_id or components")

    if not all_positions:
        return {
            "min_x": None,
            "max_x": None,
            "min_y": None,
            "max_y": None,
            "width": None,
            "height": None,
        }

    x_coords = [p[0] for p in all_positions]
    y_coords = [p[1] for p in all_positions]

    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    return {
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
        "width": max_x - min_x + BLOCK_WIDTH,  # Include component width
        "height": max_y - min_y + BLOCK_HEIGHT,  # Include component height
    }


# =============================================================================
# FLOW ANALYSIS
# =============================================================================


def find_flow_spine(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    pg_id: str, start_component=None, prefer_success: bool = False
) -> list:
    """
    Find the main artery (spine) of a flow - the longest chain of connections.

    Flows typically branch like arteries: a main vertical path with smaller
    side branches. This function identifies the spine by finding the longest
    path from any entry point (component with no incoming connections) to
    any exit point (component with no outgoing connections).

    The spine can be used to:
    - Lay out the main flow vertically
    - Identify side branches (components not on the spine)
    - Restructure a messy flow into a logical layout

    Algorithm:
        1. Build directed graph from connections (skip self-loops)
        2. Track which edges use "success" relationship
        3. Find entry points (in-degree = 0)
        4. Use DFS to find best path based on strategy
        5. Return the path as a list of component IDs

    Args:
        pg_id: Process group ID containing the flow to analyze
        start_component: Optional component to start from. If provided, finds
            the longest path starting from this component. If None, finds the
            globally longest path.
        prefer_success: Strategy for choosing between paths. False (default)
            picks longest path with success count as tiebreaker, giving the
            simplest shape. True heavily weights "success" relationships, so
            shorter paths with more success edges may win.

    Returns:
        List of component IDs representing the spine, ordered from entry to exit.
        Returns empty list if no connections exist.

    Example::

        # Find the longest spine (default - simplest shape)
        spine_ids = nipyapi.layout.find_flow_spine(pg.id)

        # Find the semantic "success" spine
        spine_ids = nipyapi.layout.find_flow_spine(pg.id, prefer_success=True)

        # Get actual component entities
        flow = nipyapi.canvas.get_flow(pg.id)
        components_map = {p.id: p for p in flow.process_group_flow.flow.processors}
        spine = [components_map[cid] for cid in spine_ids if cid in components_map]

        # Lay out spine vertically
        for i, comp in enumerate(spine):
            pos = nipyapi.layout.grid_position(row=i, col=0)
            nipyapi.layout.move_component(comp, pos)
    """
    flow = nipyapi.canvas.get_flow(pg_id)
    fc = flow.process_group_flow.flow
    connections = fc.connections or []

    if not connections:
        return []

    # Build directed graph (adjacency list) and track in-degrees
    # graph[node] = list of (downstream_node, is_success) tuples
    graph = {}
    in_degree = {}

    for conn in connections:
        src_id = conn.component.source.id
        dst_id = conn.component.destination.id

        # Skip self-loops (retry connections) - they don't contribute to path length
        if src_id == dst_id:
            continue

        # Check if this is a "success" relationship
        relationships = conn.component.selected_relationships or []
        is_success = "success" in [r.lower() for r in relationships]

        # Initialize nodes
        if src_id not in graph:
            graph[src_id] = []
        if dst_id not in graph:
            graph[dst_id] = []

        # Add edge with success flag
        graph[src_id].append((dst_id, is_success))

        # Track in-degree for finding entry points
        in_degree[dst_id] = in_degree.get(dst_id, 0) + 1
        if src_id not in in_degree:
            in_degree[src_id] = 0

    if not graph:
        return []

    # Find entry points (nodes with in_degree == 0)
    entry_points = [node for node, deg in in_degree.items() if deg == 0]

    # If start_component provided, use it as the only entry point
    if start_component is not None:
        entry_points = [start_component.id]

    # Step 1: Calculate minimum depth for each node using BFS
    # This establishes the "natural" flow order - components reachable via
    # shorter paths are earlier in the flow
    node_depth = {}
    bfs_queue = deque()

    for entry in entry_points:
        bfs_queue.append((entry, 0))
        node_depth[entry] = 0

    while bfs_queue:
        node, depth = bfs_queue.popleft()
        for downstream, _ in graph.get(node, []):
            if downstream not in node_depth:
                node_depth[downstream] = depth + 1
                bfs_queue.append((downstream, depth + 1))

    # Step 2: DFS to find best FORWARD path
    # Only follow edges that go to components with greater depth
    # This prevents following feedback loops (like Retry→Transform)
    def best_forward_path_from(node, visited):
        """Find best forward path from node (no backward edges)."""
        if node in visited:
            return ([], 0)
        if node not in graph or not graph[node]:
            return ([node], 0)

        visited = visited | {node}
        best = ([node], 0)
        current_depth = node_depth.get(node, 0)

        for downstream, is_success in graph[node]:
            downstream_depth = node_depth.get(downstream, 0)

            # Only follow FORWARD edges (to nodes with greater depth)
            # This skips feedback loops like Retry→Transform
            if downstream_depth > current_depth and downstream not in visited:
                sub_path, sub_success = best_forward_path_from(downstream, visited)
                path = [node] + sub_path
                success_count = sub_success + (1 if is_success else 0)

                # Compare paths based on strategy
                if prefer_success:
                    new_score = len(path) + (success_count * 0.5)
                    best_score = len(best[0]) + (best[1] * 0.5)
                    if new_score > best_score:
                        best = (path, success_count)
                else:
                    if len(path) > len(best[0]) or (
                        len(path) == len(best[0]) and success_count > best[1]
                    ):
                        best = (path, success_count)

        return best

    # Find best forward path from any entry point
    spine = []
    best_success_count = 0

    for entry in entry_points:
        path, success_count = best_forward_path_from(entry, set())

        if prefer_success:
            new_score = len(path) + (success_count * 0.5)
            best_score = len(spine) + (best_success_count * 0.5)
            if new_score > best_score:
                spine = path
                best_success_count = success_count
        else:
            if len(path) > len(spine) or (
                len(path) == len(spine) and success_count > best_success_count
            ):
                spine = path
                best_success_count = success_count

    return spine


def get_side_branches(pg_id: str, spine: list = None, recursive: bool = True) -> dict:
    """
    Find all side branches that fork off from the spine.

    A side branch is any path that diverges from the main spine. This function
    recursively finds branches of branches, building a complete picture of
    the flow structure.

    Args:
        pg_id: Process group ID containing the flow
        spine: List of component IDs representing the spine. If None, will be
            calculated using find_flow_spine().
        recursive: If True (default), also find branches of branches.
            If False, only find direct branches from spine components.

    Returns:
        Dict mapping component IDs to lists of their branch component IDs.
        Keys are component IDs that have branches, values are lists of branch
        component IDs. If recursive=True, branch components that have their
        own sub-branches will also appear as keys.

    Example::

        spine = nipyapi.layout.find_flow_spine(pg.id)
        branches = nipyapi.layout.get_side_branches(pg.id, spine)

        # Layout: spine vertical, branches to the right
        for i, comp_id in enumerate(spine):
            main_pos = nipyapi.layout.grid_position(row=i, col=0)
            # ... move main component

            for j, branch_id in enumerate(branches.get(comp_id, [])):
                branch_pos = nipyapi.layout.fork(main_component, direction="right")
                # ... move branch component
    """
    if spine is None:
        spine = find_flow_spine(pg_id)

    if not spine:
        return {}

    # Get connections to map out the graph
    flow = nipyapi.canvas.get_flow(pg_id)
    connections = flow.process_group_flow.flow.connections or []

    # Build adjacency list
    graph = {}
    for conn in connections:
        src_id = conn.component.source.id
        dst_id = conn.component.destination.id
        if src_id == dst_id:
            continue  # Skip self-loops
        if src_id not in graph:
            graph[src_id] = []
        graph[src_id].append(dst_id)

    # Track which components are already placed (spine + found branches)
    placed = set(spine)
    branches = {}

    # Find branches recursively using BFS
    to_process = list(spine)  # Start with spine components

    while to_process:
        current = to_process.pop(0)

        for downstream in graph.get(current, []):
            if downstream not in placed:
                # This is a branch!
                if current not in branches:
                    branches[current] = []
                branches[current].append(downstream)
                placed.add(downstream)

                # If recursive, also process this branch to find sub-branches
                if recursive:
                    to_process.append(downstream)

    return branches


def suggest_flow_layout(  # pylint: disable=too-many-locals,too-many-branches
    pg_id: str,
) -> dict:
    """
    Analyze a flow and suggest an organized layout.

    Returns a structured plan for laying out the flow with spine components
    vertically (column 0) and side branches to the right. The algorithm finds
    the spine, recursively finds all branches, then assigns grid positions.

    Args:
        pg_id: Process group ID containing the flow

    Returns:
        Dict with 'spine' and 'branches' keys. Each contains a list of dicts
        with 'id', 'row', 'col', and 'position' keys. Branch items also have
        'fork_from' indicating the parent component ID.

    Example::

        plan = nipyapi.layout.suggest_flow_layout(pg.id)

        for item in plan['spine'] + plan['branches']:
            comp = get_component_by_id(item['id'])
            nipyapi.layout.move_component(comp, item['position'])
    """
    spine = find_flow_spine(pg_id)
    branches = get_side_branches(pg_id, spine, recursive=True)

    plan = {"spine": [], "branches": []}

    # Track positions: comp_id -> (row, col)
    comp_positions = {}

    # Build a map of component types for centering decisions
    flow = nipyapi.canvas.get_flow(pg_id)
    fc = flow.process_group_flow.flow
    component_types = {}
    for p in fc.processors or []:
        component_types[p.id] = "processor"
    for f in fc.funnels or []:
        component_types[f.id] = "funnel"
    for ip in fc.input_ports or []:
        component_types[ip.id] = "port"
    for op in fc.output_ports or []:
        component_types[op.id] = "port"

    # Place spine components vertically in column 0
    for row, comp_id in enumerate(spine):
        base_pos = grid_position(row=row, col=0)

        # Center smaller components (funnels, ports) under processor-sized space
        comp_type = component_types.get(comp_id, "processor")
        if comp_type == "funnel":
            pos = (base_pos[0] + FUNNEL_CENTER_OFFSET, base_pos[1])
        elif comp_type == "port":
            pos = (base_pos[0] + PORT_CENTER_OFFSET, base_pos[1])
        else:
            pos = base_pos

        plan["spine"].append({"id": comp_id, "row": row, "col": 0, "position": pos})
        comp_positions[comp_id] = (row, 0)

    # Place branches using BFS to handle nesting correctly
    # Process in order: first direct spine branches, then their sub-branches
    to_process = []

    # Start with direct branches from spine
    for spine_id in spine:
        if spine_id in branches:
            for branch_id in branches[spine_id]:
                to_process.append((branch_id, spine_id))

    while to_process:
        branch_id, parent_id = to_process.pop(0)

        if branch_id in comp_positions:
            continue  # Already placed

        parent_row, parent_col = comp_positions.get(parent_id, (0, 0))

        # Branch goes one column to the right, one row down
        branch_row = parent_row + 1
        branch_col = parent_col + 1

        # Calculate position using fork spacing for horizontal, block height for vertical
        base_pos = (
            DEFAULT_ORIGIN[0] + (branch_col * FORK_SPACING),
            DEFAULT_ORIGIN[1] + (branch_row * BLOCK_HEIGHT),
        )

        # Center smaller components (funnels, ports)
        comp_type = component_types.get(branch_id, "processor")
        if comp_type == "funnel":
            pos = (base_pos[0] + FUNNEL_CENTER_OFFSET, base_pos[1])
        elif comp_type == "port":
            pos = (base_pos[0] + PORT_CENTER_OFFSET, base_pos[1])
        else:
            pos = base_pos

        plan["branches"].append(
            {
                "id": branch_id,
                "fork_from": parent_id,
                "row": branch_row,
                "col": branch_col,
                "position": pos,
            }
        )
        comp_positions[branch_id] = (branch_row, branch_col)

        # Queue sub-branches of this branch
        if branch_id in branches:
            for sub_branch_id in branches[branch_id]:
                to_process.append((sub_branch_id, branch_id))

    return plan


def suggest_empty_position(pg_id: str, prefer: str = "right") -> tuple:
    """
    Find empty space by scanning all components in a process group.

    Analyzes all existing components to find the bounding box, then suggests
    a position at the edge of existing content that won't overlap.

    When to use suggest_empty_position vs new_flow:
        - suggest_empty_position(): Find empty space without knowing a reference
        - new_flow(): Position relative to a specific known component

    Args:
        pg_id: Process group ID to scan for existing components
        prefer: Direction to expand from existing content:
            - "right": Next column to the right, same top row (default)
            - "left": Next column to the left, same top row
            - "below": Next row below, same left column
            - "above": Next row above, same left column

    Returns:
        Position tuple (x, y) for new component. Returns DEFAULT_ORIGIN if
        the canvas is empty.

    Example::

        # Find empty space to the right of all existing flows
        pos = nipyapi.layout.suggest_empty_position(pg.id, prefer="right")
        proc = nipyapi.canvas.create_processor(pg, proc_type, location=pos)
    """
    bounds = get_canvas_bounds(pg_id)

    # Empty canvas - start at origin
    if bounds["min_x"] is None:
        return DEFAULT_ORIGIN

    # Suggest position based on preference
    # For right: 1 block past max_x (matches visual testing)
    # For others: 2 blocks to account for component size + visual separation
    if prefer == "right":
        # New flow: 1 block right of rightmost, at top
        return (snap_to_grid(bounds["max_x"] + BLOCK_WIDTH), bounds["min_y"])
    if prefer == "left":
        # New flow: 2 blocks left (component + gap), at top
        return (snap_to_grid(bounds["min_x"] - BLOCK_WIDTH * 2), bounds["min_y"])
    if prefer == "below":
        # New row: 2 blocks below (accounts for connections/queue labels), at left
        return (bounds["min_x"], snap_to_grid(bounds["max_y"] + BLOCK_HEIGHT * 2))
    if prefer == "above":
        # New row: 2 blocks above (component + gap), at left
        return (bounds["min_x"], snap_to_grid(bounds["min_y"] - BLOCK_HEIGHT * 2))
    raise ValueError(f"Invalid prefer direction: {prefer}")


# =============================================================================
# COMPONENT POSITION UPDATES
# =============================================================================


def move_processor(processor, position: tuple, refresh: bool = True, include_retry: bool = True):
    """
    Move a processor to a new position.

    Args:
        processor: ProcessorEntity to move
        position: New (x, y) position tuple
        refresh: Whether to refresh the processor before updating (default True)
        include_retry: If True (default), also move bends on retry (self-loop)
            connections to preserve their visual shape. This matches NiFi UI
            behavior when dragging a processor.

    Returns:
        Updated ProcessorEntity
    """
    # Calculate offset before refreshing (for retry bend adjustment)
    current_pos = get_position(processor)
    offset = (position[0] - current_pos[0], position[1] - current_pos[1])

    if refresh:
        processor = nipyapi.canvas.get_processor(processor.id, "id")

    result = nipyapi.nifi.ProcessorsApi().update_processor(
        id=processor.id,
        body=nipyapi.nifi.ProcessorEntity(
            revision=processor.revision,
            component=nipyapi.nifi.ProcessorDTO(
                id=processor.component.id,
                position=nipyapi.nifi.PositionDTO(x=float(position[0]), y=float(position[1])),
            ),
        ),
    )

    # Move retry bends to match UI behavior
    if include_retry:
        pg_id = processor.component.parent_group_id
        for conn in nipyapi.canvas.list_all_connections(pg_id, descendants=False):
            if conn.source_id == conn.destination_id == processor.id:
                if conn.component.bends:
                    new_bends = [
                        (bend.x + offset[0], bend.y + offset[1]) for bend in conn.component.bends
                    ]
                    nipyapi.canvas.update_connection(conn, bends=new_bends)

    return result


def move_process_group(process_group, position: tuple, refresh: bool = True):
    """
    Move a process group to a new position.

    Args:
        process_group: ProcessGroupEntity to move
        position: New (x, y) position tuple
        refresh: Whether to refresh the process group before updating (default True)

    Returns:
        Updated ProcessGroupEntity
    """
    if refresh:
        process_group = nipyapi.canvas.get_process_group(process_group.id, "id")

    return nipyapi.nifi.ProcessGroupsApi().update_process_group(
        id=process_group.id,
        body=nipyapi.nifi.ProcessGroupEntity(
            revision=process_group.revision,
            component=nipyapi.nifi.ProcessGroupDTO(
                id=process_group.component.id,
                position=nipyapi.nifi.PositionDTO(x=float(position[0]), y=float(position[1])),
            ),
        ),
    )


def move_funnel(funnel, position: tuple, refresh: bool = True):
    """
    Move a funnel to a new position.

    Args:
        funnel: FunnelEntity to move
        position: New (x, y) position tuple
        refresh: Whether to refresh the funnel before updating (default True)

    Returns:
        Updated FunnelEntity
    """
    if refresh:
        funnel = nipyapi.canvas.get_funnel(funnel.id)

    return nipyapi.nifi.FunnelsApi().update_funnel(
        id=funnel.id,
        body=nipyapi.nifi.FunnelEntity(
            revision=funnel.revision,
            component=nipyapi.nifi.FunnelDTO(
                id=funnel.component.id,
                position=nipyapi.nifi.PositionDTO(x=float(position[0]), y=float(position[1])),
            ),
        ),
    )


def move_port(port, position: tuple, refresh: bool = True):
    """
    Move an input or output port to a new position.

    Args:
        port: PortEntity to move (input or output)
        position: New (x, y) position tuple
        refresh: Whether to refresh the port before updating (default True)

    Returns:
        Updated PortEntity
    """
    port_type = port.component.type if hasattr(port.component, "type") else None

    if refresh:
        if port_type == "INPUT_PORT":
            port = nipyapi.nifi.InputPortsApi().get_input_port(id=port.id)
        else:
            port = nipyapi.nifi.OutputPortsApi().get_output_port(id=port.id)

    body = nipyapi.nifi.PortEntity(
        revision=port.revision,
        component=nipyapi.nifi.PortDTO(
            id=port.component.id,
            position=nipyapi.nifi.PositionDTO(x=float(position[0]), y=float(position[1])),
        ),
    )

    if port_type == "INPUT_PORT":
        return nipyapi.nifi.InputPortsApi().update_input_port(id=port.id, body=body)
    return nipyapi.nifi.OutputPortsApi().update_output_port(id=port.id, body=body)


def move_label(label, position: tuple, refresh: bool = True):
    """
    Move a label to a new position.

    Args:
        label: LabelEntity to move
        position: New (x, y) position tuple
        refresh: Whether to refresh the label before updating (default True)

    Returns:
        Updated LabelEntity
    """
    if refresh:
        label = nipyapi.nifi.LabelsApi().get_label(id=label.id)

    return nipyapi.nifi.LabelsApi().update_label(
        id=label.id,
        body=nipyapi.nifi.LabelEntity(
            revision=label.revision,
            component=nipyapi.nifi.LabelDTO(
                id=label.component.id,
                position=nipyapi.nifi.PositionDTO(x=float(position[0]), y=float(position[1])),
            ),
        ),
    )


def move_component(component, position: tuple, refresh: bool = True, include_retry: bool = True):
    """
    Move any canvas component to a new position.

    Automatically detects the component type and calls the appropriate move function.

    Args:
        component: Any canvas component (processor, process group, funnel, port, label)
        position: New (x, y) position tuple
        refresh: Whether to refresh the component before updating (default True)
        include_retry: If True (default), also move bends on retry (self-loop)
            connections to preserve their visual shape. This matches NiFi UI
            behavior when dragging a single component. Only applies to processors.

    Returns:
        Updated component entity

    Example::

        # Move a processor down by one block
        new_pos = nipyapi.layout.below(proc1)
        nipyapi.layout.move_component(proc1, new_pos)

        # Move without adjusting retry bends (for batch operations)
        nipyapi.layout.move_component(proc1, new_pos, include_retry=False)
    """
    component_type = type(component).__name__

    if "ProcessorEntity" in component_type:
        return move_processor(component, position, refresh, include_retry)
    if "ProcessGroupEntity" in component_type:
        return move_process_group(component, position, refresh)
    if "FunnelEntity" in component_type:
        return move_funnel(component, position, refresh)
    if "PortEntity" in component_type:
        return move_port(component, position, refresh)
    if "LabelEntity" in component_type:
        return move_label(component, position, refresh)
    raise ValueError(f"Unsupported component type: {component_type}")


def transpose_flow(components: list, offset: tuple, pg_id: str = None, connections=None):
    """
    Move an entire flow by the given offset, including all connection bends.

    This function handles the complexity of moving a flow as a unit. It moves
    all components by the offset, then moves bends on all connections within
    the flow (both retry loops and cross-component connections).

    This matches the behavior of selecting multiple components in the NiFi UI
    and dragging them together.

    Args:
        components: List of component entities to move (from get_flow_components)
        offset: Tuple (dx, dy) representing the movement offset
        pg_id: Process group ID containing the flow. If None, inferred from
            first component.
        connections: Optional list of ConnectionEntity objects. If provided,
            these connections will be used for bend updates (avoiding an API call).
            Typically obtained from get_flow_components().connections.

    Returns:
        List of updated component entities

    Example::

        # Get the complete flow subgraph (single API call)
        flow = nipyapi.canvas.get_flow_components(start_proc)

        # Move entire flow with connections pre-fetched (no additional API calls)
        nipyapi.layout.transpose_flow(
            flow.components, offset=(400, 0), connections=flow.connections
        )

        # Or without pre-fetched connections (connections will be fetched)
        nipyapi.layout.transpose_flow(flow.components, offset=(400, 0))
    """
    if not components:
        return []

    # Infer pg_id from first component if not provided
    if pg_id is None:
        first = components[0]
        if hasattr(first, "component") and hasattr(first.component, "parent_group_id"):
            pg_id = first.component.parent_group_id
        else:
            raise ValueError("Cannot infer pg_id. Please provide explicitly.")

    # Fetch connections once if not provided
    if connections is None:
        connections = nipyapi.canvas.list_all_connections(pg_id, descendants=False)

    # Build set of component IDs being moved
    component_ids = {c.id for c in components}

    # Step 1: Move all components WITHOUT individual retry handling
    # We handle all bends together in step 2 for efficiency
    updated_components = []
    for c in components:
        current_pos = get_position(c)
        new_pos = (current_pos[0] + offset[0], current_pos[1] + offset[1])
        updated = move_component(c, new_pos, refresh=True, include_retry=False)
        updated_components.append(updated)

    # Step 2: Move bends on all connections within the flow
    # This includes both retry loops (self-loops) and cross-component connections
    for conn in connections:
        src_in_flow = conn.source_id in component_ids
        dst_in_flow = conn.destination_id in component_ids

        # Move bends if both endpoints are in the flow being moved
        # For self-loops, src == dst so this naturally includes them
        if src_in_flow and dst_in_flow and conn.component.bends:
            new_bends = [(bend.x + offset[0], bend.y + offset[1]) for bend in conn.component.bends]
            nipyapi.canvas.update_connection(conn, bends=new_bends)

    return updated_components


def clear_flow_bends(pg_id: str, include_self_loops: bool = False) -> int:
    """
    Clear all bends from connections in a process group.

    Use this before reorganizing a flow layout. Old bends look wrong after
    components are moved to new positions, so clearing them first ensures
    clean straight-line connections after the layout is applied.

    By default, self-loop bends (retry loops) are preserved because they are
    required for the connection to render correctly in the NiFi UI.

    Args:
        pg_id: Process group ID containing the connections to clear
        include_self_loops: If True, also clear bends on self-loop connections.
            Default False preserves self-loop shapes which are required for
            correct UI rendering.

    Returns:
        int: Number of connections that had bends cleared

    Example::

        # Before reorganizing a messy flow
        nipyapi.layout.clear_flow_bends(pg.id)

        # Apply new layout
        plan = nipyapi.layout.suggest_flow_layout(pg.id)
        for item in plan['spine'] + plan['branches']:
            comp = get_component(item['id'])
            nipyapi.layout.move_component(comp, item['position'])
    """
    connections = nipyapi.canvas.list_all_connections(pg_id, descendants=False)
    cleared_count = 0

    for conn in connections:
        # Skip self-loops unless explicitly requested
        if conn.source_id == conn.destination_id and not include_self_loops:
            continue

        # Clear bends if present
        if conn.component.bends:
            nipyapi.canvas.update_connection(conn, bends=[])
            cleared_count += 1

    return cleared_count


# =============================================================================
# PROCESS GROUP GRID LAYOUT
# =============================================================================


def get_pg_grid_position(row: int, col: int, origin: tuple = DEFAULT_ORIGIN) -> tuple:
    """
    Calculate position for a process group in a standard grid.

    Uses BLOCK_WIDTH for horizontal spacing and BLOCK_HEIGHT for vertical spacing.
    This is typically used internally by align_pg_grid() and suggest_pg_position().

    Args:
        row: Row index (0-based, increases downward)
        col: Column index (0-based, increases rightward)
        origin: Grid origin position, top-left corner (default DEFAULT_ORIGIN)

    Returns:
        Position tuple (x, y) for the grid cell

    Example::

        # Get position for row 2, column 3
        pos = get_pg_grid_position(2, 3)  # Returns (1600, 800) with default origin
    """
    x = origin[0] + (col * BLOCK_WIDTH)
    y = origin[1] + (row * BLOCK_HEIGHT)
    return (x, y)


def _check_overlap(pos1: tuple, pos2: tuple, width: int, height: int) -> bool:
    """
    Check if two axis-aligned rectangles overlap.

    Both rectangles are assumed to have the same dimensions (width x height).
    Used internally for collision detection when placing process groups.

    Args:
        pos1: Top-left corner (x, y) of first rectangle
        pos2: Top-left corner (x, y) of second rectangle
        width: Width of both rectangles
        height: Height of both rectangles

    Returns:
        True if rectangles overlap, False otherwise
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return not (x1 + width <= x2 or x2 + width <= x1 or y1 + height <= y2 or y2 + height <= y1)


def suggest_pg_position(parent_pg_id: str) -> tuple:
    """
    Suggest a position for a new process group that doesn't overlap existing ones.

    Finds a position within a square-ish grid layout. Prefers filling gaps in
    existing rows before extending the grid.

    For best results, first call align_pg_grid() to organize existing PGs,
    then this function will find gaps in that organized grid.

    Args:
        parent_pg_id: ID of the parent process group

    Returns:
        Position tuple (x, y) for the new process group

    Example::

        pos = nipyapi.layout.suggest_pg_position(root_pg_id)
        new_pg = nipyapi.canvas.create_process_group(root, "New PG", location=pos)
    """
    flow = nipyapi.canvas.get_flow(parent_pg_id)
    fc = flow.process_group_flow.flow

    existing_pgs = fc.process_groups or []

    if not existing_pgs:
        return DEFAULT_ORIGIN

    # Get all existing PG positions
    existing_positions = [(pg.position.x, pg.position.y) for pg in existing_pgs]

    # Calculate optimal columns for a square-ish grid (including the new item)
    total_items = len(existing_positions) + 1
    columns = math.ceil(math.sqrt(total_items))

    # Search within the optimal column count to maintain square-ish layout
    for row in range(20):
        for col in range(columns):
            candidate = get_pg_grid_position(row, col)

            # Check if this position overlaps with any existing PG
            overlaps = False
            for existing_pos in existing_positions:
                if _check_overlap(
                    candidate, existing_pos, PROCESS_GROUP_WIDTH, PROCESS_GROUP_HEIGHT
                ):
                    overlaps = True
                    break

            if not overlaps:
                return candidate

    # Fallback: extend to next column
    max_x = max(p[0] for p in existing_positions)
    return (snap_to_grid(max_x + BLOCK_WIDTH), 0)


def align_pg_grid(  # pylint: disable=too-many-locals
    parent_pg_id: str,
    columns: int = None,
    sort_by_name: bool = False,
    origin: tuple = DEFAULT_ORIGIN,
    dry_run: bool = False,
):
    """
    Align all process groups within a parent to a standard grid.

    Args:
        parent_pg_id: ID of the parent process group containing PGs to align
        columns: Number of columns in the grid. If None (default), auto-calculates
                 the optimal number to create a square-ish layout using ceil(sqrt(n))
        sort_by_name: If True, sort PGs alphabetically by name (default False)
        origin: Grid starting position (default (0, 0))
        dry_run: If True, return planned moves without executing (default False)

    Returns:
        List of dicts with move details: [{'name', 'id', 'from', 'to'}, ...]

    Example::

        # Auto-calculate columns, sort alphabetically
        nipyapi.layout.align_pg_grid(pg_id, sort_by_name=True)

        # Preview moves without executing
        moves = nipyapi.layout.align_pg_grid(pg_id, dry_run=True)
        for m in moves:
            print(f"{m['name']}: {m['from']} -> {m['to']}")
    """
    flow = nipyapi.canvas.get_flow(parent_pg_id)
    fc = flow.process_group_flow.flow

    existing_pgs = fc.process_groups or []

    if not existing_pgs:
        return []

    # Auto-calculate optimal columns for a square-ish grid
    if columns is None:
        columns = math.ceil(math.sqrt(len(existing_pgs)))

    # Sort by name if requested, otherwise by current position
    if sort_by_name:
        sorted_pgs = sorted(
            existing_pgs, key=lambda p: p.component.name.lower() if p.component else ""
        )
    else:
        # Sort by position: top-to-bottom, left-to-right
        sorted_pgs = sorted(existing_pgs, key=lambda p: (p.position.y, p.position.x))

    moves = []

    for idx, pg in enumerate(sorted_pgs):
        row = idx // columns
        col = idx % columns

        old_pos = (pg.position.x, pg.position.y)
        new_pos = get_pg_grid_position(row, col, origin)

        move_info = {
            "name": pg.component.name if pg.component else pg.id,
            "id": pg.id,
            "from": old_pos,
            "to": new_pos,
            "row": row,
            "col": col,
        }
        moves.append(move_info)

        if not dry_run and old_pos != new_pos:
            move_process_group(pg, new_pos, refresh=True)

    return moves
