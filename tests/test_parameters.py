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


def test_list_all_parameter_contexts(fix_context):
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
