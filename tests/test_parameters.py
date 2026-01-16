"""Tests for `nipyapi.parameters` package."""

from tests import conftest
import uuid
import pytest
from nipyapi import parameters
from nipyapi.nifi import ParameterContextEntity
from nipyapi.nifi.rest import ApiException
from nipyapi.utils import check_version


def test_create_parameter_context(fix_context):
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


def test_get_parameter_context(fix_context):
    # Regression tests are parametrized, skip inside function to work properly
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    r1 = parameters.get_parameter_context('fake news', 'name')
    assert r1 is None
    c2 = parameters.get_parameter_context(
        identifier=str(uuid.uuid4()), identifier_type='id'
    )
    assert c2 is None
    c1 = fix_context.generate(name=conftest.test_basename + 'instance_1')
    r3 = parameters.get_parameter_context(c1.id, identifier_type='id')
    assert r3.component.name == conftest.test_basename + 'instance_1'
    c2 = fix_context.generate(name=conftest.test_basename + 'instance_2')
    r4 = parameters.get_parameter_context(
        conftest.test_basename + 'instance_2', identifier_type='name'
    )
    assert r4.id == c2.id


def test_list_all_parameter_contexts(fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    _ = fix_context.generate()
    r1 = parameters.list_all_parameter_contexts()
    assert isinstance(r1, list)
    for pc in r1:
        assert isinstance(pc, ParameterContextEntity)
    _ = fix_context.generate(name=conftest.test_basename + 'instance_1')
    r2 = [
        x for x in parameters.list_all_parameter_contexts()
        if conftest.test_basename in x.component.name
    ]
    assert isinstance(r2, list)
    assert len(r2) == 2
    for pc in r2:
        assert isinstance(pc, ParameterContextEntity)


def test_list_orphaned_contexts(fix_context):
    """Test listing parameter contexts not bound to any process groups."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    # Create an unbound context (orphan)
    orphan = fix_context.generate(name=conftest.test_basename + '_orphan')
    assert orphan is not None

    # List orphaned contexts
    orphans = parameters.list_orphaned_contexts()
    assert isinstance(orphans, list)

    # Our newly created context should be in the orphaned list
    orphan_ids = [ctx.id for ctx in orphans]
    assert orphan.id in orphan_ids

    # All returned contexts should have no bound process groups
    for ctx in orphans:
        assert not ctx.component.bound_process_groups


def test_delete_parameter_context(fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    assert c1.revision is not None
    r1 = parameters.delete_parameter_context(c1)
    assert isinstance(r1, ParameterContextEntity)
    assert r1.revision is None
    with pytest.raises(ApiException):
        _ = parameters.delete_parameter_context(c1)

    # Test deletion by ID string
    c2 = fix_context.generate(name=conftest.test_parameter_context_name + '_id_delete')
    r2 = parameters.delete_parameter_context(c2.id)
    assert r2.id == c2.id

    # Test deletion by name string
    c3 = fix_context.generate(name=conftest.test_parameter_context_name + '_name_delete')
    r3 = parameters.delete_parameter_context(
        c3.component.name, identifier_type="name", greedy=False
    )
    assert r3.id == c3.id


def test_update_parameter_context(fix_context):
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


def test_rename_parameter_context(fix_context):
    """Test renaming a parameter context without affecting parameters."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    # Create context with a parameter
    c1 = fix_context.generate()
    c1.component.parameters.append(
        parameters.prepare_parameter('test_param', 'test_value')
    )
    c1 = parameters.update_parameter_context(c1)
    original_name = c1.component.name
    new_name = original_name + '_renamed'

    # Rename the context
    r1 = parameters.rename_parameter_context(c1, new_name)
    assert isinstance(r1, ParameterContextEntity)
    assert r1.component.name == new_name

    # Verify parameters are preserved
    assert len(r1.component.parameters) == 1
    assert r1.component.parameters[0].parameter.name == 'test_param'
    assert r1.component.parameters[0].parameter.value == 'test_value'


def test_delete_parameter_from_context(fix_context):
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


def test_upsert_parameter_to_context(fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    r1 = parameters.upsert_parameter_to_context(
        c1,
        parameters.prepare_parameter('Black', 'Lives', 'Matter', True)
    )
    assert r1.component.parameters[0].parameter.description == 'Matter'


def test_assign_context_to_process_group(fix_pg, fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    pg1 = fix_pg.generate()
    r1 = parameters.assign_context_to_process_group(pg1, c1.id)
    assert r1.component.parameter_context.id == c1.id

    # Test with pg as ID string
    c2 = fix_context.generate(name=conftest.test_parameter_context_name + '_assign_id')
    pg2 = fix_pg.generate(suffix='_assign_id')
    r2 = parameters.assign_context_to_process_group(pg2.id, c2.id)
    assert r2.component.parameter_context.id == c2.id


def test_remove_context_from_process_group(fix_pg, fix_context):
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")
    c1 = fix_context.generate()
    pg1 = fix_pg.generate()
    r1 = parameters.assign_context_to_process_group(pg1, c1.id)
    assert r1.component.parameter_context.id == c1.id
    r2 = parameters.remove_context_from_process_group(pg1)
    assert r2.component.parameter_context is None


# =============================================================================
# Asset Management Tests
# =============================================================================


def test_upload_asset_from_bytes(fix_context):
    """Test uploading an asset from bytes - validates octet-stream handling."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    c1 = fix_context.generate()

    # Create test file content (simple text, but sent as binary)
    test_content = b"This is test content for asset upload validation."
    test_filename = "test_asset.txt"

    # Upload the asset using file_bytes
    result = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=test_content,
        filename=test_filename
    )

    # Verify the result structure
    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result
    assert "digest" in result
    assert result["name"] == test_filename
    # Digest should be a SHA-256 hash (64 hex chars)
    assert len(result["digest"]) == 64

    # Clean up - delete the asset
    parameters.delete_asset(context_id=c1.id, asset_id=result["id"])


def test_list_assets(fix_context):
    """Test listing assets in a parameter context."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    c1 = fix_context.generate()

    # Initially should be empty
    assets = parameters.list_assets(c1.id)
    assert isinstance(assets, list)
    initial_count = len(assets)

    # Upload two assets
    asset1 = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"asset one content",
        filename="asset1.txt"
    )
    asset2 = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"asset two content",
        filename="asset2.txt"
    )

    # List should now have 2 more assets
    assets = parameters.list_assets(c1.id)
    assert len(assets) == initial_count + 2

    # Verify asset structure
    asset_names = [a["name"] for a in assets]
    assert "asset1.txt" in asset_names
    assert "asset2.txt" in asset_names

    for asset in assets:
        assert "id" in asset
        assert "name" in asset
        assert "digest" in asset
        assert "missing_content" in asset

    # Clean up
    parameters.delete_asset(context_id=c1.id, asset_id=asset1["id"])
    parameters.delete_asset(context_id=c1.id, asset_id=asset2["id"])


def test_delete_asset(fix_context):
    """Test deleting an asset from a parameter context."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    c1 = fix_context.generate()

    # Upload an asset
    asset = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"content to delete",
        filename="to_delete.txt"
    )

    # Verify it exists
    assets_before = parameters.list_assets(c1.id)
    asset_ids_before = [a["id"] for a in assets_before]
    assert asset["id"] in asset_ids_before

    # Delete it
    result = parameters.delete_asset(context_id=c1.id, asset_id=asset["id"])
    assert isinstance(result, dict)
    assert result["id"] == asset["id"]
    assert result["name"] == "to_delete.txt"

    # Verify it's gone
    assets_after = parameters.list_assets(c1.id)
    asset_ids_after = [a["id"] for a in assets_after]
    assert asset["id"] not in asset_ids_after


def test_prepare_parameter_with_asset(fix_context):
    """Test preparing a parameter that references an asset."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    c1 = fix_context.generate()

    # Upload an asset first
    asset = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"JDBC driver content simulation",
        filename="postgresql-42.7.6.jar"
    )

    # Prepare a parameter referencing the asset
    param = parameters.prepare_parameter_with_asset(
        name="PostgreSQL Driver",
        asset_id=asset["id"],
        asset_name=asset["name"],
        description="JDBC driver for PostgreSQL database connections"
    )

    # Verify the parameter structure
    assert param.parameter.name == "PostgreSQL Driver"
    assert param.parameter.description == "JDBC driver for PostgreSQL database connections"
    assert len(param.parameter.referenced_assets) == 1
    assert param.parameter.referenced_assets[0].id == asset["id"]
    assert param.parameter.referenced_assets[0].name == asset["name"]

    # Clean up
    parameters.delete_asset(context_id=c1.id, asset_id=asset["id"])


def test_upload_asset_and_link_to_parameter(fix_context):
    """Test full workflow: upload asset and link it to a parameter."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    c1 = fix_context.generate()

    # Upload an asset
    asset = parameters.upload_asset(
        context_id=c1.id,
        file_bytes=b"Driver binary content here",
        filename="mysql-connector-j-8.3.0.jar"
    )

    # Prepare parameter referencing the asset
    param = parameters.prepare_parameter_with_asset(
        name="MySQL Driver",
        asset_id=asset["id"],
        asset_name=asset["name"]
    )

    # Add parameter to context
    updated_context = parameters.upsert_parameter_to_context(c1, param)

    # Verify the parameter was added with asset reference
    param_names = [p.parameter.name for p in updated_context.component.parameters]
    assert "MySQL Driver" in param_names

    # Find the parameter and verify asset reference
    mysql_param = next(
        p for p in updated_context.component.parameters
        if p.parameter.name == "MySQL Driver"
    )
    assert mysql_param.parameter.referenced_assets is not None
    assert len(mysql_param.parameter.referenced_assets) == 1
    assert mysql_param.parameter.referenced_assets[0].id == asset["id"]

    # Clean up - delete parameter first, then asset
    parameters.delete_parameter_from_context(updated_context, "MySQL Driver")
    parameters.delete_asset(context_id=c1.id, asset_id=asset["id"])


def test_upload_asset_validation_errors():
    """Test that upload_asset raises appropriate validation errors."""
    # No file_path or file_bytes
    with pytest.raises(ValueError, match="Either file_path or file_bytes"):
        parameters.upload_asset(context_id="fake-id")

    # file_bytes without filename
    with pytest.raises(ValueError, match="filename is required"):
        parameters.upload_asset(context_id="fake-id", file_bytes=b"content")


# =============================================================================
# Parameter Context Hierarchy Tests
# =============================================================================


def test_get_parameter_context_hierarchy_simple(fix_context):
    """Test get_parameter_context_hierarchy with a single context."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Add a parameter
    param = parameters.prepare_parameter(
        name="HierarchyTestParam",
        value="test_value",
        description="Test for hierarchy"
    )
    parameters.upsert_parameter_to_context(ctx, param)

    # Get hierarchy
    hierarchy = parameters.get_parameter_context_hierarchy(ctx.id)

    assert hierarchy["id"] == ctx.id
    assert hierarchy["name"] == ctx.component.name
    assert isinstance(hierarchy["parameters"], list)
    assert isinstance(hierarchy["inherited"], list)
    assert len(hierarchy["inherited"]) == 0  # No inherited contexts

    # Verify parameter is in the list
    param_names = [p["name"] for p in hierarchy["parameters"]]
    assert "HierarchyTestParam" in param_names

    # Verify parameter fields including description
    test_param = next(p for p in hierarchy["parameters"] if p["name"] == "HierarchyTestParam")
    assert test_param["value"] == "test_value"
    assert test_param["description"] == "Test for hierarchy"
    assert test_param["sensitive"] is False
    assert "has_asset" in test_param
    assert "asset_name" in test_param


def test_get_parameter_context_hierarchy_with_inheritance(fix_context):
    """Test get_parameter_context_hierarchy with inherited contexts."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    # Create child context (will be inherited)
    child_ctx = fix_context.generate(name=conftest.test_parameter_context_name + "_child")
    child_param = parameters.prepare_parameter(
        name="ChildParam",
        value="child_value"
    )
    parameters.upsert_parameter_to_context(child_ctx, child_param)

    # Create parent context that inherits from child
    parent_ctx = parameters.create_parameter_context(
        name=conftest.test_parameter_context_name + "_parent",
        inherited_contexts=[child_ctx]
    )
    parent_param = parameters.prepare_parameter(
        name="ParentParam",
        value="parent_value"
    )
    parameters.upsert_parameter_to_context(parent_ctx, parent_param)

    try:
        # Get hierarchy from parent
        hierarchy = parameters.get_parameter_context_hierarchy(parent_ctx.id)

        assert hierarchy["id"] == parent_ctx.id
        assert hierarchy["name"] == parent_ctx.component.name
        assert len(hierarchy["inherited"]) == 1

        # Verify parent parameter
        parent_param_names = [p["name"] for p in hierarchy["parameters"]]
        assert "ParentParam" in parent_param_names

        # Verify child context in hierarchy
        child_hierarchy = hierarchy["inherited"][0]
        assert child_hierarchy["id"] == child_ctx.id
        child_param_names = [p["name"] for p in child_hierarchy["parameters"]]
        assert "ChildParam" in child_param_names

    finally:
        # Clean up parent context
        parameters.delete_parameter_context(parent_ctx)


def test_get_parameter_context_hierarchy_not_found():
    """Test get_parameter_context_hierarchy with invalid context."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    import uuid
    with pytest.raises(ValueError, match="Parameter context not found"):
        parameters.get_parameter_context_hierarchy(str(uuid.uuid4()))


def test_get_parameter_context_hierarchy_include_bindings(fix_context, fix_pg):
    """Test get_parameter_context_hierarchy with include_bindings=True."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Add a parameter
    param = parameters.prepare_parameter(
        name="BindingTestParam",
        value="test_value"
    )
    parameters.upsert_parameter_to_context(ctx, param)

    # Create a PG and bind the context to it
    pg = fix_pg.generate()
    parameters.assign_context_to_process_group(pg, ctx.id)

    # Get hierarchy with bindings
    hierarchy = parameters.get_parameter_context_hierarchy(
        ctx.id, include_bindings=True
    )

    assert hierarchy["id"] == ctx.id
    assert "bound_process_groups" in hierarchy
    assert isinstance(hierarchy["bound_process_groups"], list)
    assert len(hierarchy["bound_process_groups"]) == 1
    assert hierarchy["bound_process_groups"][0]["id"] == pg.id
    assert hierarchy["bound_process_groups"][0]["name"] == pg.component.name

    # Parameters should still be included by default
    assert "parameters" in hierarchy
    assert len(hierarchy["parameters"]) >= 1


def test_get_parameter_context_hierarchy_exclude_parameters(fix_context):
    """Test get_parameter_context_hierarchy with include_parameters=False."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Add a parameter
    param = parameters.prepare_parameter(
        name="ExcludeTestParam",
        value="test_value"
    )
    parameters.upsert_parameter_to_context(ctx, param)

    # Get hierarchy without parameters
    hierarchy = parameters.get_parameter_context_hierarchy(
        ctx.id, include_parameters=False
    )

    assert hierarchy["id"] == ctx.id
    assert hierarchy["name"] == ctx.component.name
    assert "parameters" not in hierarchy
    assert "inherited" in hierarchy

    # Bindings should not be included by default
    assert "bound_process_groups" not in hierarchy


def test_get_parameter_context_hierarchy_bindings_only(fix_context, fix_pg):
    """Test get_parameter_context_hierarchy with bindings only (no parameters)."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    # Create child context
    child_ctx = fix_context.generate(name=conftest.test_parameter_context_name + "_bind_child")
    child_param = parameters.prepare_parameter(name="ChildBindParam", value="child")
    parameters.upsert_parameter_to_context(child_ctx, child_param)

    # Create parent context that inherits from child
    parent_ctx = parameters.create_parameter_context(
        name=conftest.test_parameter_context_name + "_bind_parent",
        inherited_contexts=[child_ctx]
    )

    # Bind parent to a PG
    pg = fix_pg.generate()
    parameters.assign_context_to_process_group(pg, parent_ctx.id)

    try:
        # Get structure with bindings, no parameters
        hierarchy = parameters.get_parameter_context_hierarchy(
            parent_ctx.id,
            include_bindings=True,
            include_parameters=False
        )

        # Verify parent structure
        assert hierarchy["id"] == parent_ctx.id
        assert "parameters" not in hierarchy
        assert "bound_process_groups" in hierarchy
        assert len(hierarchy["bound_process_groups"]) == 1

        # Verify child inherits the flags
        assert len(hierarchy["inherited"]) == 1
        child_hierarchy = hierarchy["inherited"][0]
        assert child_hierarchy["id"] == child_ctx.id
        assert "parameters" not in child_hierarchy
        assert "bound_process_groups" in child_hierarchy
        # NiFi reports transitive bindings - inherited contexts show the PG that
        # binds their parent. This is correct behavior (shows all contexts in use).
        assert len(child_hierarchy["bound_process_groups"]) == 1
        assert child_hierarchy["bound_process_groups"][0]["id"] == pg.id

    finally:
        # Clean up parent context
        parameters.delete_parameter_context(parent_ctx)


def test_get_parameter_context_hierarchy_defaults_backwards_compatible(fix_context):
    """Test that default behavior is backwards compatible."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    param = parameters.prepare_parameter(name="BackwardsParam", value="test")
    parameters.upsert_parameter_to_context(ctx, param)

    # Call with no extra arguments (original signature)
    hierarchy = parameters.get_parameter_context_hierarchy(ctx.id)

    # Should have parameters (default: True)
    assert "parameters" in hierarchy
    assert len(hierarchy["parameters"]) >= 1

    # Should NOT have bound_process_groups (default: False)
    assert "bound_process_groups" not in hierarchy

    # Basic structure preserved
    assert "id" in hierarchy
    assert "name" in hierarchy
    assert "inherited" in hierarchy


def test_get_parameter_ownership_map(fix_context):
    """Test get_parameter_ownership_map with simple context."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Add parameters
    param1 = parameters.prepare_parameter(name="OwnerParam1", value="value1")
    param2 = parameters.prepare_parameter(
        name="OwnerParam2", value="value2", sensitive=True
    )
    parameters.upsert_parameter_to_context(ctx, param1)

    # Refresh context before adding second param
    ctx = parameters.get_parameter_context(ctx.id, "id")
    parameters.upsert_parameter_to_context(ctx, param2)

    # Get ownership map
    ownership = parameters.get_parameter_ownership_map(ctx.id)

    assert "OwnerParam1" in ownership
    assert "OwnerParam2" in ownership

    # Verify structure
    owner1 = ownership["OwnerParam1"]
    assert owner1["context_id"] == ctx.id
    assert owner1["context_name"] == ctx.component.name
    assert owner1["sensitive"] is False
    assert owner1["current_value"] == "value1"

    owner2 = ownership["OwnerParam2"]
    assert owner2["sensitive"] is True
    assert owner2["current_value"] is None  # Sensitive values not returned


def test_get_parameter_ownership_map_with_inheritance(fix_context):
    """Test get_parameter_ownership_map tracks correct owning context."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    # Create child context with a parameter
    child_ctx = fix_context.generate(name=conftest.test_parameter_context_name + "_owner_child")
    child_param = parameters.prepare_parameter(name="ChildOwned", value="child_owns_this")
    parameters.upsert_parameter_to_context(child_ctx, child_param)

    # Create parent that inherits child
    parent_ctx = parameters.create_parameter_context(
        name=conftest.test_parameter_context_name + "_owner_parent",
        inherited_contexts=[child_ctx]
    )
    parent_param = parameters.prepare_parameter(name="ParentOwned", value="parent_owns_this")
    parameters.upsert_parameter_to_context(parent_ctx, parent_param)

    try:
        # Get ownership from parent's perspective
        ownership = parameters.get_parameter_ownership_map(parent_ctx.id)

        # Both parameters should be in map
        assert "ParentOwned" in ownership
        assert "ChildOwned" in ownership

        # Verify ownership attribution
        assert ownership["ParentOwned"]["context_id"] == parent_ctx.id
        assert ownership["ParentOwned"]["context_name"] == parent_ctx.component.name

        assert ownership["ChildOwned"]["context_id"] == child_ctx.id
        assert ownership["ChildOwned"]["context_name"] == child_ctx.component.name

    finally:
        parameters.delete_parameter_context(parent_ctx)


def test_update_parameter_in_context(fix_context):
    """Test update_parameter_in_context updates existing parameter."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Create initial parameter
    param = parameters.prepare_parameter(name="UpdateMe", value="initial")
    parameters.upsert_parameter_to_context(ctx, param)

    # Update it
    result = parameters.update_parameter_in_context(
        context_id=ctx.id,
        param_name="UpdateMe",
        value="updated"
    )

    # Verify update
    updated_param = next(
        p for p in result.component.parameters
        if p.parameter.name == "UpdateMe"
    )
    assert updated_param.parameter.value == "updated"


def test_update_parameter_in_context_not_found(fix_context):
    """Test update_parameter_in_context raises error for missing parameter."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    with pytest.raises(ValueError, match="not found in context"):
        parameters.update_parameter_in_context(
            context_id=ctx.id,
            param_name="NonExistent",
            value="value"
        )


def test_update_parameter_in_context_create_if_missing(fix_context):
    """Test update_parameter_in_context with create_if_missing=True."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Create a new parameter with create_if_missing
    result = parameters.update_parameter_in_context(
        context_id=ctx.id,
        param_name="CreatedParam",
        value="created_value",
        create_if_missing=True
    )

    # Verify it was created
    param_names = [p.parameter.name for p in result.component.parameters]
    assert "CreatedParam" in param_names

    created_param = next(
        p for p in result.component.parameters
        if p.parameter.name == "CreatedParam"
    )
    assert created_param.parameter.value == "created_value"


def test_update_parameter_in_context_invalid_context():
    """Test update_parameter_in_context with invalid context raises error."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    import uuid
    with pytest.raises(ValueError, match="Parameter context not found"):
        parameters.update_parameter_in_context(
            context_id=str(uuid.uuid4()),
            param_name="Param",
            value="value"
        )


# =============================================================================
# prepare_parameter Value Handling Tests
# =============================================================================


def test_prepare_parameter_with_value():
    """Test prepare_parameter with explicit value sets the value."""
    param = parameters.prepare_parameter("TestParam", value="test_value")
    assert param.parameter.name == "TestParam"
    assert param.parameter.value == "test_value"
    assert param.parameter.value_removed is None


def test_prepare_parameter_with_empty_string():
    """Test prepare_parameter with empty string sets empty string value."""
    param = parameters.prepare_parameter("TestParam", value="")
    assert param.parameter.name == "TestParam"
    assert param.parameter.value == ""
    assert param.parameter.value_removed is None


def test_prepare_parameter_with_none_unsets_value():
    """Test prepare_parameter with value=None sets value_removed=True."""
    param = parameters.prepare_parameter("TestParam", value=None)
    assert param.parameter.name == "TestParam"
    assert param.parameter.value is None
    assert param.parameter.value_removed is True


def test_prepare_parameter_omitted_value_leaves_unchanged():
    """Test prepare_parameter without value arg doesn't include value in DTO."""
    param = parameters.prepare_parameter("TestParam")
    assert param.parameter.name == "TestParam"
    assert param.parameter.value is None
    assert param.parameter.value_removed is None  # Not set = leave unchanged


def test_prepare_parameter_update_description_only():
    """Test prepare_parameter can update description without touching value."""
    param = parameters.prepare_parameter("TestParam", description="New description")
    assert param.parameter.name == "TestParam"
    assert param.parameter.description == "New description"
    assert param.parameter.value is None
    assert param.parameter.value_removed is None  # Value not touched


def test_prepare_parameter_unset_value_integration(fix_context):
    """Integration test: create param with value, then unset it."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Create parameter with a value
    param = parameters.prepare_parameter("UnsetTest", value="initial_value")
    result = parameters.upsert_parameter_to_context(ctx, param)

    # Verify it has a value
    created = next(
        p for p in result.component.parameters if p.parameter.name == "UnsetTest"
    )
    assert created.parameter.value == "initial_value"

    # Now unset the value
    unset_param = parameters.prepare_parameter("UnsetTest", value=None)
    result = parameters.upsert_parameter_to_context(result, unset_param)

    # Verify the value is now unset
    updated = next(
        p for p in result.component.parameters if p.parameter.name == "UnsetTest"
    )
    assert updated.parameter.value is None


def test_prepare_parameter_update_description_preserves_value(fix_context):
    """Integration test: update description without changing existing value."""
    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Create parameter with a value
    param = parameters.prepare_parameter(
        "DescTest", value="keep_this", description="Original"
    )
    result = parameters.upsert_parameter_to_context(ctx, param)

    # Verify initial state
    created = next(
        p for p in result.component.parameters if p.parameter.name == "DescTest"
    )
    assert created.parameter.value == "keep_this"
    assert created.parameter.description == "Original"

    # Update only description (omit value)
    desc_only = parameters.prepare_parameter("DescTest", description="Updated")
    result = parameters.upsert_parameter_to_context(result, desc_only)

    # Verify value preserved, description updated
    updated = next(
        p for p in result.component.parameters if p.parameter.name == "DescTest"
    )
    assert updated.parameter.value == "keep_this"
    assert updated.parameter.description == "Updated"
