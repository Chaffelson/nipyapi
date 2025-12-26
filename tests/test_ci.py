"""Tests for `nipyapi.ci` module."""

import os
from urllib.parse import urlparse

import pytest
from unittest.mock import patch, MagicMock

from nipyapi import ci


# =============================================================================
# Pure Logic Tests (no NiFi required)
# =============================================================================


class TestEnvBool:
    """Test _env_bool helper function used by stop_flow and cleanup."""

    def test_env_bool_true_values(self):
        """Test that true-like values return True."""
        from nipyapi.ci.stop_flow import _env_bool

        with patch.dict(os.environ, {"TEST_VAR": "true"}):
            assert _env_bool("TEST_VAR") is True
        with patch.dict(os.environ, {"TEST_VAR": "1"}):
            assert _env_bool("TEST_VAR") is True
        with patch.dict(os.environ, {"TEST_VAR": "yes"}):
            assert _env_bool("TEST_VAR") is True
        with patch.dict(os.environ, {"TEST_VAR": "TRUE"}):
            assert _env_bool("TEST_VAR") is True

    def test_env_bool_false_values(self):
        """Test that false-like values return False."""
        from nipyapi.ci.stop_flow import _env_bool

        with patch.dict(os.environ, {"TEST_VAR": "false"}):
            assert _env_bool("TEST_VAR") is False
        with patch.dict(os.environ, {"TEST_VAR": "0"}):
            assert _env_bool("TEST_VAR") is False
        with patch.dict(os.environ, {"TEST_VAR": "no"}):
            assert _env_bool("TEST_VAR") is False

    def test_env_bool_default(self):
        """Test default value when env var not set."""
        from nipyapi.ci.stop_flow import _env_bool

        # Clear the var if it exists
        env = os.environ.copy()
        env.pop("NONEXISTENT_VAR", None)
        with patch.dict(os.environ, env, clear=True):
            assert _env_bool("NONEXISTENT_VAR", default=False) is False
            assert _env_bool("NONEXISTENT_VAR", default=True) is True


class TestMaskValue:
    """Test _mask_value utility function."""

    def test_mask_short_value(self):
        """Test short values are not masked."""
        from nipyapi.ci.configure_inherited_params import _mask_value

        assert _mask_value("short") == "short"
        assert _mask_value("exactly20chars1234") == "exactly20chars1234"

    def test_mask_long_value(self):
        """Test long values are truncated with ellipsis."""
        from nipyapi.ci.configure_inherited_params import _mask_value

        result = _mask_value("this is a very long value that should be truncated")
        assert result == "this is a very long ..."
        assert len(result) == 23  # 20 + 3 for "..."

    def test_mask_none_value(self):
        """Test None values show as <empty>."""
        from nipyapi.ci.configure_inherited_params import _mask_value

        assert _mask_value(None) == "<empty>"

    def test_mask_custom_length(self):
        """Test custom max_len parameter."""
        from nipyapi.ci.configure_inherited_params import _mask_value

        result = _mask_value("hello world", max_len=5)
        assert result == "hello..."


class TestEnsureRegistryValidation:
    """Test ensure_registry validation logic (no NiFi required)."""

    def test_invalid_provider(self):
        """Test invalid provider raises ValueError."""
        with pytest.raises(ValueError, match="Invalid provider"):
            ci.ensure_registry(provider="invalid", token="token", repo="owner/repo")

    def test_missing_token(self):
        """Test missing token raises ValueError."""
        old_gh = os.environ.pop("GH_REGISTRY_TOKEN", None)
        old_gl = os.environ.pop("GL_REGISTRY_TOKEN", None)
        try:
            with pytest.raises(ValueError, match="token is required"):
                ci.ensure_registry(repo="owner/repo")
        finally:
            if old_gh:
                os.environ["GH_REGISTRY_TOKEN"] = old_gh
            if old_gl:
                os.environ["GL_REGISTRY_TOKEN"] = old_gl

    def test_invalid_repo_format(self):
        """Test repo without slash raises ValueError."""
        with pytest.raises(ValueError, match="owner/repo format"):
            ci.ensure_registry(token="token", repo="invalid-repo-format")

    @patch("nipyapi.versioning.ensure_registry_client")
    def test_gitlab_uses_gl_token_first(self, mock_ensure):
        """Test GitLab provider prefers GL_REGISTRY_TOKEN over GH_REGISTRY_TOKEN."""
        # Mock the NiFi call to capture what token was used
        mock_client = MagicMock()
        mock_client.id = "test-id"
        mock_client.component.name = "test-name"
        mock_ensure.return_value = mock_client

        old_gh = os.environ.get("GH_REGISTRY_TOKEN")
        old_gl = os.environ.get("GL_REGISTRY_TOKEN")
        try:
            os.environ["GH_REGISTRY_TOKEN"] = "github-token"
            os.environ["GL_REGISTRY_TOKEN"] = "gitlab-token"

            ci.ensure_registry(provider="gitlab", repo="owner/repo")

            # Verify the GL token was used (not GH)
            call_kwargs = mock_ensure.call_args[1]
            assert call_kwargs["properties"]["Access Token"] == "gitlab-token"
        finally:
            if old_gh:
                os.environ["GH_REGISTRY_TOKEN"] = old_gh
            else:
                os.environ.pop("GH_REGISTRY_TOKEN", None)
            if old_gl:
                os.environ["GL_REGISTRY_TOKEN"] = old_gl
            else:
                os.environ.pop("GL_REGISTRY_TOKEN", None)

    @patch("nipyapi.versioning.ensure_registry_client")
    def test_github_uses_gh_token_first(self, mock_ensure):
        """Test GitHub provider prefers GH_REGISTRY_TOKEN over GL_REGISTRY_TOKEN."""
        mock_client = MagicMock()
        mock_client.id = "test-id"
        mock_client.component.name = "test-name"
        mock_ensure.return_value = mock_client

        old_gh = os.environ.get("GH_REGISTRY_TOKEN")
        old_gl = os.environ.get("GL_REGISTRY_TOKEN")
        try:
            os.environ["GH_REGISTRY_TOKEN"] = "github-token"
            os.environ["GL_REGISTRY_TOKEN"] = "gitlab-token"

            ci.ensure_registry(provider="github", repo="owner/repo")

            # Verify the GH token was used (not GL)
            call_kwargs = mock_ensure.call_args[1]
            assert call_kwargs["properties"]["Personal Access Token"] == "github-token"
        finally:
            if old_gh:
                os.environ["GH_REGISTRY_TOKEN"] = old_gh
            else:
                os.environ.pop("GH_REGISTRY_TOKEN", None)
            if old_gl:
                os.environ["GL_REGISTRY_TOKEN"] = old_gl
            else:
                os.environ.pop("GL_REGISTRY_TOKEN", None)


class TestDeployFlowValidation:
    """Test deploy_flow validation logic (no NiFi required)."""

    def test_missing_registry_client(self):
        """Test missing registry_client raises ValueError."""
        old_val = os.environ.pop("NIFI_REGISTRY_CLIENT_ID", None)
        try:
            with pytest.raises(ValueError, match="registry_client is required"):
                ci.deploy_flow(bucket="test", flow="test")
        finally:
            if old_val:
                os.environ["NIFI_REGISTRY_CLIENT_ID"] = old_val

    def test_missing_bucket(self):
        """Test missing bucket raises ValueError."""
        old_val = os.environ.pop("NIFI_BUCKET", None)
        try:
            with pytest.raises(ValueError, match="bucket is required"):
                ci.deploy_flow(registry_client="test-client", flow="test")
        finally:
            if old_val:
                os.environ["NIFI_BUCKET"] = old_val

    def test_missing_flow(self):
        """Test missing flow raises ValueError."""
        old_val = os.environ.pop("NIFI_FLOW", None)
        try:
            with pytest.raises(ValueError, match="flow is required"):
                ci.deploy_flow(registry_client="test-client", bucket="test")
        finally:
            if old_val:
                os.environ["NIFI_FLOW"] = old_val


class TestListRegistryFlowsValidation:
    """Test list_registry_flows validation logic (no NiFi required)."""

    def test_missing_registry_client(self):
        """Test missing registry_client raises ValueError."""
        old_val = os.environ.pop("NIFI_REGISTRY_CLIENT_ID", None)
        try:
            with pytest.raises(ValueError, match="registry_client is required"):
                ci.list_registry_flows(bucket="test")
        finally:
            if old_val:
                os.environ["NIFI_REGISTRY_CLIENT_ID"] = old_val

    def test_missing_bucket(self):
        """Test missing bucket raises ValueError."""
        old_val = os.environ.pop("NIFI_BUCKET", None)
        try:
            with pytest.raises(ValueError, match="bucket is required"):
                ci.list_registry_flows(registry_client="test-client")
        finally:
            if old_val:
                os.environ["NIFI_BUCKET"] = old_val


class TestResolveGitRef:
    """Test resolve_git_ref function."""

    def test_resolve_git_ref_none(self):
        """Test None ref returns None."""
        result = ci.resolve_git_ref(None)
        assert result is None

    def test_resolve_git_ref_empty(self):
        """Test empty ref returns None."""
        result = ci.resolve_git_ref("")
        assert result is None

    def test_resolve_git_ref_sha_short(self):
        """Test short SHA (7 chars) is returned as-is."""
        result = ci.resolve_git_ref("abc1234")
        assert result == "abc1234"

    def test_resolve_git_ref_sha_full(self):
        """Test full SHA (40 chars) is returned as-is."""
        sha = "a" * 40
        result = ci.resolve_git_ref(sha)
        assert result == sha

    def test_resolve_git_ref_sha_various_lengths(self):
        """Test various valid SHA lengths."""
        for length in [7, 8, 10, 20, 40]:
            sha = "abcdef1234567890" * 3  # Long enough
            sha = sha[:length]
            result = ci.resolve_git_ref(sha)
            assert result == sha

    def test_resolve_git_ref_tag_no_repo(self):
        """Test resolving tag without repo raises error."""
        with pytest.raises(ValueError, match="repository not specified"):
            ci.resolve_git_ref("v1.0.0")

    def test_resolve_git_ref_tag_no_token(self):
        """Test resolving tag without token raises error."""
        with pytest.raises(ValueError, match="token not available"):
            ci.resolve_git_ref("v1.0.0", repo="owner/repo")

    @patch("requests.get")
    def test_resolve_git_ref_github(self, mock_get):
        """Test resolving ref via GitHub API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"sha": "abc123def456"}
        mock_get.return_value = mock_response

        result = ci.resolve_git_ref("v1.0.0", repo="owner/repo", token="ghp_xxx")

        assert result == "abc123def456"
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert urlparse(call_args[0][0]).hostname == "api.github.com"
        assert call_args[1]["headers"]["Authorization"] == "Bearer ghp_xxx"

    @patch("requests.get")
    def test_resolve_git_ref_gitlab(self, mock_get):
        """Test resolving ref via GitLab API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "def456abc789"}
        mock_get.return_value = mock_response

        result = ci.resolve_git_ref(
            "main", repo="namespace/project", token="glpat-xxx", provider="gitlab"
        )

        assert result == "def456abc789"
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "gitlab.com" in call_args[0][0]
        assert call_args[1]["headers"]["PRIVATE-TOKEN"] == "glpat-xxx"

    @patch("requests.get")
    def test_resolve_git_ref_not_found(self, mock_get):
        """Test 404 response raises ValueError."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="not found"):
            ci.resolve_git_ref("nonexistent", repo="owner/repo", token="token")


# =============================================================================
# Integration Tests (require NiFi connection)
# =============================================================================


def test_get_status_root(fix_pg):
    """Test get_status on root process group."""
    result = ci.get_status()

    assert isinstance(result, dict)
    assert "process_group_id" in result
    assert "process_group_name" in result
    assert "state" in result
    assert result["is_root"] == "true"
    assert "total_processors" in result
    assert "running_processors" in result
    assert "stopped_processors" in result


def test_get_status_specific_pg(fix_pg):
    """Test get_status on a specific process group."""
    pg = fix_pg.generate()

    result = ci.get_status(process_group_id=pg.id)

    assert isinstance(result, dict)
    assert result["process_group_id"] == pg.id
    assert result["process_group_name"] == pg.component.name
    assert result["is_root"] == "false"


def test_get_status_invalid_pg():
    """Test get_status with invalid process group ID."""
    import uuid
    from nipyapi.nifi.rest import ApiException
    # Invalid PG ID raises either ValueError or ApiException depending on NiFi version
    with pytest.raises((ValueError, ApiException)):
        ci.get_status(process_group_id=str(uuid.uuid4()))


def test_stop_flow_missing_pg_id():
    """Test stop_flow without process_group_id raises error."""
    # Clear env var if set
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.stop_flow()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_stop_flow(fix_pg):
    """Test stopping a process group."""
    pg = fix_pg.generate()

    result = ci.stop_flow(process_group_id=pg.id)

    assert isinstance(result, dict)
    assert result["stopped"] == "true"
    assert result["process_group_name"] == pg.component.name
    assert result["controllers_disabled"] == "false"


def test_stop_flow_with_disable_controllers(fix_pg):
    """Test stopping with controller disable option."""
    pg = fix_pg.generate()

    result = ci.stop_flow(process_group_id=pg.id, disable_controllers=True)

    assert result["stopped"] == "true"
    assert result["controllers_disabled"] == "true"


def test_start_flow(fix_pg):
    """Test starting a process group."""
    pg = fix_pg.generate()

    result = ci.start_flow(process_group_id=pg.id)

    assert isinstance(result, dict)
    assert result["started"] == "true"
    assert result["process_group_name"] == pg.component.name


def test_start_flow_missing_pg_id():
    """Test start_flow without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.start_flow()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_cleanup_missing_pg_id():
    """Test cleanup without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.cleanup()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_cleanup(fix_pg):
    """Test cleanup (stop and delete) a process group."""
    # Create a PG specifically for deletion (not using fixture cleanup)
    import nipyapi

    pg = nipyapi.canvas.create_process_group(
        nipyapi.canvas.get_process_group("root", "name"),
        "test_ci_cleanup_target",
        location=(100, 100)
    )

    result = ci.cleanup(process_group_id=pg.id)

    assert isinstance(result, dict)
    assert result["deleted"] == "true"
    assert result["process_group_name"] == "test_ci_cleanup_target"

    # Verify it's gone - get_process_group raises ValueError for missing PG
    with pytest.raises(ValueError, match="Unable to locate"):
        nipyapi.canvas.get_process_group(pg.id, "id")


def test_cleanup_with_orphaned_contexts():
    """Test cleanup with delete_orphaned_contexts option."""
    import nipyapi
    import uuid

    ctx_name = f"test_ci_cleanup_orphan_ctx_{uuid.uuid4().hex[:8]}"
    pg_name = f"test_ci_cleanup_orphan_target_{uuid.uuid4().hex[:8]}"

    # Create a PG with a parameter context
    root = nipyapi.canvas.get_process_group("root", "name")
    ctx = nipyapi.parameters.create_parameter_context(
        name=ctx_name,
        description="Will become orphaned"
    )

    try:
        pg = nipyapi.canvas.create_process_group(
            root,
            pg_name,
            location=(200, 200)
        )
        # Assign context to PG (pass the context ID, not the object)
        nipyapi.parameters.assign_context_to_process_group(pg, ctx.id)

        # Refresh PG to get updated reference
        pg = nipyapi.canvas.get_process_group(pg.id, "id")

        # Cleanup with orphan deletion
        result = ci.cleanup(
            process_group_id=pg.id,
            delete_orphaned_contexts=True
        )

        assert result["deleted"] == "true"
        # The orphaned_contexts_deleted should include our context
        assert isinstance(result["orphaned_contexts_deleted"], list)

        # Context should be deleted (it became orphaned when PG was deleted)
        deleted_ctx = nipyapi.parameters.get_parameter_context(
            ctx.id, identifier_type="id"
        )
        assert deleted_ctx is None

    except Exception:
        # Manual cleanup on failure
        try:
            nipyapi.parameters.delete_parameter_context(ctx)
        except Exception:
            pass
        raise


def test_revert_flow_missing_pg_id():
    """Test revert_flow without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.revert_flow()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_purge_flowfiles_missing_pg_id():
    """Test purge_flowfiles without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.purge_flowfiles()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_purge_flowfiles():
    """Test purging flowfiles from a process group."""
    import nipyapi

    # Create a fresh PG for this test
    root = nipyapi.canvas.get_process_group("root", "name")
    pg = nipyapi.canvas.create_process_group(
        root, "test_ci_purge_target", location=(200, 200)
    )

    try:
        result = ci.purge_flowfiles(process_group_id=pg.id)

        assert isinstance(result, dict)
        # purge_flowfiles returns purged=true on success, or has error key on failure
        assert "purged" in result or "error" in result
        if result.get("purged") == "true":
            assert "connections_purged" in result
    finally:
        # Clean up
        try:
            nipyapi.canvas.delete_process_group(pg, force=True)
        except Exception:
            pass  # Best effort cleanup


def test_configure_params_missing_pg_id():
    """Test configure_params without process_group_id raises error."""
    old_pg = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.configure_params()
    finally:
        if old_pg:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_pg


def test_configure_params_missing_parameters():
    """Test configure_params without parameters raises error."""
    old_params = os.environ.pop("NIFI_PARAMETERS", None)
    try:
        with pytest.raises(ValueError, match="parameters is required"):
            ci.configure_params(process_group_id="test-id")
    finally:
        if old_params:
            os.environ["NIFI_PARAMETERS"] = old_params


def test_configure_params_invalid_json():
    """Test configure_params with invalid JSON raises error."""
    with pytest.raises(ValueError, match="Invalid JSON"):
        ci.configure_params(process_group_id="test-id", parameters="{invalid json}")


def test_configure_params_non_dict():
    """Test configure_params with non-dict JSON raises error."""
    with pytest.raises(ValueError, match="must be a JSON object"):
        ci.configure_params(process_group_id="test-id", parameters="[1, 2, 3]")


def test_list_flows_default_root():
    """Test list_flows defaults to root when no PG ID provided."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        # list_flows defaults to root PG, doesn't raise error
        result = ci.list_flows()
        assert isinstance(result, dict)
        assert "parent_id" in result
        assert "total_count" in result
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_change_flow_version_missing_pg_id():
    """Test change_flow_version without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.change_flow_version()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


# =============================================================================
# Upload Asset Tests (validates octet-stream in CI context)
# =============================================================================


def test_upload_asset_missing_params():
    """Test upload_asset without required params raises error."""
    old_pg = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    old_ctx = os.environ.pop("NIFI_PARAMETER_CONTEXT_ID", None)
    try:
        with pytest.raises(ValueError, match="Either process_group_id or context_id"):
            ci.upload_asset()
    finally:
        if old_pg:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_pg
        if old_ctx:
            os.environ["NIFI_PARAMETER_CONTEXT_ID"] = old_ctx


def test_upload_asset_missing_file():
    """Test upload_asset without file source raises error."""
    old_path = os.environ.pop("NIFI_ASSET_FILE_PATH", None)
    old_url = os.environ.pop("NIFI_ASSET_URL", None)
    try:
        with pytest.raises(ValueError, match="Either file_path or url"):
            ci.upload_asset(context_id="fake-id")
    finally:
        if old_path:
            os.environ["NIFI_ASSET_FILE_PATH"] = old_path
        if old_url:
            os.environ["NIFI_ASSET_URL"] = old_url


# =============================================================================
# Configure Inherited Params Integration Tests
# =============================================================================


def test_configure_inherited_params_missing_pg_id():
    """Test configure_inherited_params without process_group_id raises error."""
    old_pg = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.configure_inherited_params(parameters='{"key": "value"}')
    finally:
        if old_pg:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_pg


def test_configure_inherited_params_missing_parameters():
    """Test configure_inherited_params without parameters raises error."""
    old_params = os.environ.pop("NIFI_PARAMETERS", None)
    try:
        with pytest.raises(ValueError, match="parameters is required"):
            ci.configure_inherited_params(process_group_id="test-id")
    finally:
        if old_params:
            os.environ["NIFI_PARAMETERS"] = old_params


def test_configure_inherited_params_invalid_json():
    """Test configure_inherited_params with invalid JSON raises error."""
    with pytest.raises(ValueError, match="Invalid JSON"):
        ci.configure_inherited_params(
            process_group_id="test-id",
            parameters="{not valid json}"
        )


def test_configure_inherited_params_non_dict():
    """Test configure_inherited_params with non-dict JSON raises error."""
    with pytest.raises(ValueError, match="must be a JSON object"):
        ci.configure_inherited_params(
            process_group_id="test-id",
            parameters='["list", "not", "dict"]'
        )


def test_configure_inherited_params_pg_not_found():
    """Test configure_inherited_params with non-existent PG raises error."""
    import uuid
    with pytest.raises(ValueError, match="Unable to locate group"):
        ci.configure_inherited_params(
            process_group_id=str(uuid.uuid4()),
            parameters='{"key": "value"}'
        )


def test_configure_inherited_params_no_context(fix_pg):
    """Test configure_inherited_params on PG without parameter context."""
    pg = fix_pg.generate()

    with pytest.raises(ValueError, match="has no parameter context"):
        ci.configure_inherited_params(
            process_group_id=pg.id,
            parameters='{"key": "value"}'
        )


def test_configure_inherited_params_dry_run(fix_pg, fix_context):
    """Test configure_inherited_params dry run mode."""
    import nipyapi
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    # Create context with a parameter
    ctx = fix_context.generate()
    param = nipyapi.parameters.prepare_parameter(
        name="TestParam",
        value="initial_value",
        description="Test parameter"
    )
    nipyapi.parameters.upsert_parameter_to_context(ctx, param)

    # Create PG and attach context
    pg = fix_pg.generate()
    nipyapi.parameters.assign_context_to_process_group(pg, ctx.id)

    # Dry run should return plan without making changes
    result = ci.configure_inherited_params(
        process_group_id=pg.id,
        parameters='{"TestParam": "new_value"}',
        dry_run=True
    )

    assert result["dry_run"] == "true"
    assert result["parameters_updated"] == "0"
    assert "TestParam" in result["plan"]

    # Verify value was NOT changed
    updated_ctx = nipyapi.parameters.get_parameter_context(ctx.id, "id")
    test_param = next(
        p for p in updated_ctx.component.parameters
        if p.parameter.name == "TestParam"
    )
    assert test_param.parameter.value == "initial_value"


def test_configure_inherited_params_execute(fix_pg, fix_context):
    """Test configure_inherited_params actually updates parameter."""
    import nipyapi
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    # Create context with a parameter
    ctx = fix_context.generate()
    param = nipyapi.parameters.prepare_parameter(
        name="ExecuteTestParam",
        value="old_value",
        description="Test parameter for execution"
    )
    nipyapi.parameters.upsert_parameter_to_context(ctx, param)

    # Create PG and attach context
    pg = fix_pg.generate()
    nipyapi.parameters.assign_context_to_process_group(pg, ctx.id)

    # Execute update (not dry run)
    result = ci.configure_inherited_params(
        process_group_id=pg.id,
        parameters='{"ExecuteTestParam": "new_value"}',
        dry_run=False
    )

    assert result["dry_run"] == "false"
    assert result["parameters_updated"] == "1"
    assert result["contexts_modified"] == "1"

    # Verify value WAS changed
    updated_ctx = nipyapi.parameters.get_parameter_context(ctx.id, "id")
    test_param = next(
        p for p in updated_ctx.component.parameters
        if p.parameter.name == "ExecuteTestParam"
    )
    assert test_param.parameter.value == "new_value"


def test_configure_inherited_params_not_found_error(fix_pg, fix_context):
    """Test configure_inherited_params with non-existent parameter."""
    import nipyapi
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    # Create empty context
    ctx = fix_context.generate()

    # Create PG and attach context
    pg = fix_pg.generate()
    nipyapi.parameters.assign_context_to_process_group(pg, ctx.id)

    # Try to update non-existent parameter (without allow_override)
    result = ci.configure_inherited_params(
        process_group_id=pg.id,
        parameters='{"NonExistentParam": "value"}',
        dry_run=False,
        allow_override=False
    )

    # Should have error about parameter not found
    assert "errors" in result
    assert "NonExistentParam" in result["errors"]
    assert "not found" in result["errors"]


def test_configure_inherited_params_allow_override(fix_pg, fix_context):
    """Test configure_inherited_params with allow_override creates new param."""
    import nipyapi
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    # Create empty context
    ctx = fix_context.generate()

    # Create PG and attach context
    pg = fix_pg.generate()
    nipyapi.parameters.assign_context_to_process_group(pg, ctx.id)

    # Create non-existent parameter with allow_override
    result = ci.configure_inherited_params(
        process_group_id=pg.id,
        parameters='{"NewOverrideParam": "created_value"}',
        dry_run=False,
        allow_override=True
    )

    assert result["dry_run"] == "false"
    assert result["parameters_updated"] == "1"
    # Plan shows "ParamName→ContextName" format
    assert "NewOverrideParam" in result["plan"]

    # Verify parameter was created
    updated_ctx = nipyapi.parameters.get_parameter_context(ctx.id, "id")
    param_names = [p.parameter.name for p in updated_ctx.component.parameters]
    assert "NewOverrideParam" in param_names


# =============================================================================
# Upload Asset Integration Tests
# =============================================================================


def test_upload_asset_from_file_path(fix_context, tmp_path):
    """Test ci.upload_asset from local file path."""
    import nipyapi
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Create a temp file
    test_file = tmp_path / "test_driver.jar"
    test_file.write_bytes(b"fake jar content for testing")

    result = ci.upload_asset(
        context_id=ctx.id,
        file_path=str(test_file)
    )

    assert result["asset_name"] == "test_driver.jar"
    assert result["context_id"] == ctx.id
    assert "asset_id" in result
    assert "asset_digest" in result
    assert result["parameter_updated"] == "false"

    # Clean up
    nipyapi.parameters.delete_asset(ctx.id, result["asset_id"])


def test_upload_asset_from_process_group(fix_pg, fix_context, tmp_path):
    """Test ci.upload_asset resolves context from process group."""
    import nipyapi
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    # Create context and attach to PG
    ctx = fix_context.generate()
    pg = fix_pg.generate()
    nipyapi.parameters.assign_context_to_process_group(pg, ctx.id)

    # Create a temp file
    test_file = tmp_path / "pg_asset.txt"
    test_file.write_bytes(b"content via pg resolution")

    result = ci.upload_asset(
        process_group_id=pg.id,
        file_path=str(test_file)
    )

    assert result["asset_name"] == "pg_asset.txt"
    assert result["context_id"] == ctx.id
    assert result["context_name"] == ctx.component.name

    # Clean up
    nipyapi.parameters.delete_asset(ctx.id, result["asset_id"])


def test_upload_asset_with_param_link(fix_context, tmp_path):
    """Test ci.upload_asset with parameter linking."""
    import nipyapi
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Create a temp file
    test_file = tmp_path / "linked_driver.jar"
    test_file.write_bytes(b"driver content")

    result = ci.upload_asset(
        context_id=ctx.id,
        file_path=str(test_file),
        param_name="JDBC Driver"
    )

    assert result["parameter_updated"] == "true"
    assert result["parameter_name"] == "JDBC Driver"
    assert result["asset_name"] == "linked_driver.jar"

    # Verify parameter was created with asset reference
    updated_ctx = nipyapi.parameters.get_parameter_context(ctx.id, "id")
    driver_param = next(
        (p for p in updated_ctx.component.parameters if p.parameter.name == "JDBC Driver"),
        None
    )
    assert driver_param is not None
    assert driver_param.parameter.referenced_assets is not None
    assert len(driver_param.parameter.referenced_assets) == 1
    assert driver_param.parameter.referenced_assets[0].id == result["asset_id"]

    # Clean up
    nipyapi.parameters.delete_parameter_from_context(updated_ctx, "JDBC Driver")
    nipyapi.parameters.delete_asset(ctx.id, result["asset_id"])


def test_upload_asset_custom_filename(fix_context, tmp_path):
    """Test ci.upload_asset with custom filename override."""
    import nipyapi
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    # Create a temp file with one name
    test_file = tmp_path / "original_name.txt"
    test_file.write_bytes(b"some content")

    # Upload with different name
    result = ci.upload_asset(
        context_id=ctx.id,
        file_path=str(test_file),
        filename="custom_name.txt"
    )

    assert result["asset_name"] == "custom_name.txt"

    # Clean up
    nipyapi.parameters.delete_asset(ctx.id, result["asset_id"])


def test_upload_asset_file_not_found(fix_context):
    """Test ci.upload_asset with non-existent file raises error."""
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    ctx = fix_context.generate()

    with pytest.raises(ValueError, match="File not found"):
        ci.upload_asset(
            context_id=ctx.id,
            file_path="/non/existent/path/file.jar"
        )


def test_upload_asset_invalid_context():
    """Test ci.upload_asset with invalid context_id raises error."""
    import uuid
    from nipyapi.utils import check_version

    if check_version('1.10.0') > 0:
        pytest.skip("NiFi not 1.10+")

    with pytest.raises(ValueError, match="Parameter context not found"):
        ci.upload_asset(
            context_id=str(uuid.uuid4()),
            file_path="/some/path.jar"
        )


# =============================================================================
# commit_flow Tests
# =============================================================================


def test_commit_flow_missing_pg_id():
    """Test commit_flow without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.commit_flow()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_commit_flow_initial_missing_registry(fix_pg):
    """Test commit_flow initial commit requires registry_client."""
    pg = fix_pg.generate()
    old_reg = os.environ.pop("NIFI_REGISTRY_CLIENT", None)
    try:
        with pytest.raises(ValueError, match="registry_client is required"):
            ci.commit_flow(process_group_id=pg.id)
    finally:
        if old_reg:
            os.environ["NIFI_REGISTRY_CLIENT"] = old_reg


def test_commit_flow_initial_missing_bucket(fix_pg):
    """Test commit_flow initial commit requires bucket."""
    pg = fix_pg.generate()
    old_bucket = os.environ.pop("NIFI_BUCKET", None)
    try:
        with pytest.raises(ValueError, match="bucket is required"):
            ci.commit_flow(process_group_id=pg.id, registry_client="test-client")
    finally:
        if old_bucket:
            os.environ["NIFI_BUCKET"] = old_bucket


def test_commit_flow_no_changes(fix_deployed_git_flow):
    """Test commit_flow on UP_TO_DATE flow returns no-changes message."""
    pg = fix_deployed_git_flow.pg

    result = ci.commit_flow(process_group_id=pg.id)

    assert isinstance(result, dict)
    assert "message" in result
    assert result["initial_commit"] is False


# =============================================================================
# get_flow_versions Tests
# =============================================================================


def test_get_flow_versions_missing_pg_id():
    """Test get_flow_versions without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.get_flow_versions()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_get_flow_versions_not_versioned(fix_pg):
    """Test get_flow_versions on non-versioned PG raises error."""
    pg = fix_pg.generate()

    with pytest.raises(ValueError, match="not under version control"):
        ci.get_flow_versions(process_group_id=pg.id)


def test_get_flow_versions_success(fix_deployed_git_flow):
    """Test get_flow_versions returns version history."""
    pg = fix_deployed_git_flow.pg

    result = ci.get_flow_versions(process_group_id=pg.id)

    assert isinstance(result, dict)
    assert "flow_id" in result
    assert "bucket_id" in result
    assert "registry_id" in result
    assert "current_version" in result
    assert "state" in result
    assert "version_count" in result
    assert "versions" in result
    assert isinstance(result["versions"], list)
    assert result["version_count"] >= 1


# =============================================================================
# detach_flow Tests
# =============================================================================


def test_detach_flow_missing_pg_id():
    """Test detach_flow without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.detach_flow()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_detach_flow_not_versioned(fix_pg):
    """Test detach_flow on non-versioned PG raises error."""
    pg = fix_pg.generate()

    with pytest.raises(ValueError, match="not under version control"):
        ci.detach_flow(process_group_id=pg.id)


def test_detach_flow_success(fix_deployed_git_flow):
    """Test detach_flow removes version control."""
    import nipyapi

    # Deploy a fresh flow for this test since we'll modify version control
    token = os.environ.get('GH_REGISTRY_TOKEN')
    if not token:
        pytest.skip("GH_REGISTRY_TOKEN not set")

    root_id = nipyapi.canvas.get_root_pg_id()
    pg = nipyapi.versioning.deploy_git_registry_flow(
        registry_client_id=fix_deployed_git_flow.client.id,
        bucket_id='flows',
        flow_id='cicd-demo-flow',
        parent_id=root_id,
        location=(700, 700),
        version=None
    )

    try:
        # Verify it's under version control
        vci = pg.component.version_control_information
        assert vci is not None

        # Detach
        result = ci.detach_flow(process_group_id=pg.id)

        assert isinstance(result, dict)
        assert result["detached"] is True
        assert result["process_group_name"] == pg.component.name
        assert "previous_flow_id" in result

        # Verify no longer under version control
        updated_pg = nipyapi.canvas.get_process_group(pg.id, 'id')
        assert updated_pg.component.version_control_information is None
    finally:
        # Cleanup
        try:
            nipyapi.canvas.schedule_process_group(pg.id, scheduled=False)
            nipyapi.canvas.delete_process_group(pg, force=True)
        except Exception:
            pass


# =============================================================================
# get_flow_diff Tests
# =============================================================================


def test_get_flow_diff_missing_pg_id():
    """Test get_flow_diff without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.get_flow_diff()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_get_flow_diff_not_versioned(fix_pg):
    """Test get_flow_diff on non-versioned PG raises error."""
    pg = fix_pg.generate()

    with pytest.raises(ValueError, match="not under version control"):
        ci.get_flow_diff(process_group_id=pg.id)


def test_get_flow_diff_no_modifications(fix_deployed_git_flow):
    """Test get_flow_diff on clean flow returns empty modifications."""
    pg = fix_deployed_git_flow.pg

    result = ci.get_flow_diff(process_group_id=pg.id)

    assert isinstance(result, dict)
    assert "process_group_id" in result
    assert "process_group_name" in result
    assert "flow_id" in result
    assert "current_version" in result
    assert "state" in result
    assert "modification_count" in result
    assert "modifications" in result
    assert isinstance(result["modifications"], list)
    # Clean flow should have no modifications
    assert result["modification_count"] == 0


def test_get_flow_diff_with_modifications(fix_deployed_git_flow):
    """Test get_flow_diff detects local changes."""
    import nipyapi

    pg = fix_deployed_git_flow.pg

    # Make a local modification - update a processor's scheduling
    processors = nipyapi.canvas.list_all_processors(pg.id)
    if not processors:
        pytest.skip("No processors in test flow")

    proc = processors[0]
    original_period = proc.component.config.scheduling_period

    # Modify the processor
    nipyapi.canvas.update_processor(
        proc,
        nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period="999 sec"
        )
    )

    try:
        result = ci.get_flow_diff(process_group_id=pg.id)

        assert isinstance(result, dict)
        assert result["modification_count"] >= 1
        assert len(result["modifications"]) >= 1

        # Check the modification structure
        mod = result["modifications"][0]
        assert "component_id" in mod
        assert "component_name" in mod
        assert "component_type" in mod
        assert "changes" in mod
    finally:
        # Revert the modification
        nipyapi.versioning.revert_flow_ver(pg, wait=True)


# =============================================================================
# export_flow_definition Tests
# =============================================================================


def test_export_flow_definition_missing_pg_id():
    """Test export_flow_definition without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.export_flow_definition()
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_export_flow_definition_invalid_mode():
    """Test export_flow_definition with invalid mode raises error."""
    with pytest.raises(ValueError, match="mode must be 'json' or 'yaml'"):
        ci.export_flow_definition(process_group_id="test-id", mode="xml")


def test_export_flow_definition_to_stdout(fix_pg):
    """Test export_flow_definition returns flow definition when no file_path."""
    pg = fix_pg.generate()

    result = ci.export_flow_definition(process_group_id=pg.id)

    assert isinstance(result, dict)
    assert result["process_group_id"] == pg.id
    assert result["process_group_name"] == pg.component.name
    assert result["file_path"] == "stdout"
    assert result["format"] == "json"
    assert "flow_definition" in result
    assert len(result["flow_definition"]) > 0


def test_export_flow_definition_to_file(fix_pg, tmp_path):
    """Test export_flow_definition writes to file."""
    pg = fix_pg.generate()
    output_file = tmp_path / "exported_flow.json"

    result = ci.export_flow_definition(
        process_group_id=pg.id,
        file_path=str(output_file)
    )

    assert isinstance(result, dict)
    assert result["process_group_id"] == pg.id
    assert result["file_path"] == str(output_file)
    assert result["format"] == "json"
    assert "flow_definition" not in result  # Not included when writing to file
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_export_flow_definition_yaml_format(fix_pg):
    """Test export_flow_definition with YAML format."""
    pg = fix_pg.generate()

    result = ci.export_flow_definition(process_group_id=pg.id, mode="yaml")

    assert result["format"] == "yaml"
    assert "flow_definition" in result
    # YAML should not start with { like JSON
    flow_def = result["flow_definition"]
    assert not flow_def.strip().startswith("{")


# =============================================================================
# import_flow_definition Tests
# =============================================================================


def test_import_flow_definition_missing_source():
    """Test import_flow_definition without file_path or flow_definition raises error."""
    old_path = os.environ.pop("NIFI_FLOW_FILE_PATH", None)
    old_def = os.environ.pop("NIFI_FLOW_DEFINITION", None)
    try:
        with pytest.raises(ValueError, match="Either file_path or flow_definition"):
            ci.import_flow_definition()
    finally:
        if old_path:
            os.environ["NIFI_FLOW_FILE_PATH"] = old_path
        if old_def:
            os.environ["NIFI_FLOW_DEFINITION"] = old_def


def test_import_flow_definition_both_sources():
    """Test import_flow_definition with both sources raises error."""
    with pytest.raises(ValueError, match="Provide either file_path or flow_definition"):
        ci.import_flow_definition(
            file_path="/some/path.json",
            flow_definition='{"flowContents": {}}'
        )


def test_import_flow_definition_file_not_found():
    """Test import_flow_definition with non-existent file raises error."""
    with pytest.raises(ValueError, match="Flow definition file not found"):
        ci.import_flow_definition(file_path="/non/existent/flow.json")


def test_import_flow_definition_roundtrip(fix_pg, tmp_path):
    """Test export then import creates equivalent process group."""
    import nipyapi

    # Create a PG with some content
    pg = fix_pg.generate()

    # Add a processor to make it non-empty
    nipyapi.canvas.create_processor(
        parent_pg=pg,
        processor=nipyapi.canvas.get_processor_type('GenerateFlowFile'),
        location=(100, 100),
        name="test_roundtrip_processor",
        config=nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period='10s',
            auto_terminated_relationships=['success']
        )
    )

    # Export it
    export_result = ci.export_flow_definition(process_group_id=pg.id)
    flow_def = export_result["flow_definition"]

    # Import it as a new PG
    import_result = ci.import_flow_definition(flow_definition=flow_def)

    try:
        assert import_result["process_group_name"] == pg.component.name
        assert import_result["source"] == "string"

        # Verify the imported PG has the processor
        imported_pg = nipyapi.canvas.get_process_group(
            import_result["process_group_id"], "id"
        )
        processors = nipyapi.canvas.list_all_processors(imported_pg.id)
        assert len(processors) >= 1
        proc_names = [p.component.name for p in processors]
        assert "test_roundtrip_processor" in proc_names
    finally:
        # Clean up the imported PG
        try:
            imported = nipyapi.canvas.get_process_group(
                import_result["process_group_id"], "id"
            )
            nipyapi.canvas.delete_process_group(imported, force=True)
        except Exception:
            pass


def test_import_flow_definition_from_file(fix_pg, tmp_path):
    """Test import_flow_definition from a file."""
    import nipyapi

    pg = fix_pg.generate()

    # Export to file
    output_file = tmp_path / "flow_to_import.json"
    ci.export_flow_definition(
        process_group_id=pg.id,
        file_path=str(output_file)
    )

    # Import from file
    import_result = ci.import_flow_definition(
        file_path=str(output_file),
        location=(500, 500)
    )

    try:
        assert import_result["source"] == "file"
        assert import_result["process_group_name"] == pg.component.name
    finally:
        # Clean up
        try:
            imported = nipyapi.canvas.get_process_group(
                import_result["process_group_id"], "id"
            )
            nipyapi.canvas.delete_process_group(imported, force=True)
        except Exception:
            pass


# =============================================================================
# NAR Management CI Tests
# =============================================================================

# Test NAR file path - set via environment variable
TEST_NAR_PATH = os.environ.get("TEST_NAR_PATH")


def test_list_nars():
    """Test list_nars CI function."""
    result = ci.list_nars()
    assert isinstance(result, dict)
    assert "count" in result
    assert "nars" in result
    assert isinstance(result["nars"], list)


def test_upload_nar_missing_file():
    """Test upload_nar without file_path raises error."""
    old_val = os.environ.pop("NIFI_NAR_FILE_PATH", None)
    try:
        with pytest.raises(ValueError, match="file_path is required"):
            ci.upload_nar()
    finally:
        if old_val:
            os.environ["NIFI_NAR_FILE_PATH"] = old_val


def test_upload_nar_file_not_found():
    """Test upload_nar with non-existent file raises error."""
    with pytest.raises(ValueError, match="NAR file not found"):
        ci.upload_nar(file_path="/non/existent/file.nar")


def test_delete_nar_missing_args():
    """Test delete_nar without identifier or coordinate raises error."""
    # Clear relevant env vars
    old_id = os.environ.pop("NIFI_NAR_ID", None)
    old_group = os.environ.pop("NIFI_NAR_GROUP", None)
    old_artifact = os.environ.pop("NIFI_NAR_ARTIFACT", None)
    old_version = os.environ.pop("NIFI_NAR_VERSION", None)
    try:
        with pytest.raises(ValueError, match="Either identifier or"):
            ci.delete_nar()
    finally:
        if old_id:
            os.environ["NIFI_NAR_ID"] = old_id
        if old_group:
            os.environ["NIFI_NAR_GROUP"] = old_group
        if old_artifact:
            os.environ["NIFI_NAR_ARTIFACT"] = old_artifact
        if old_version:
            os.environ["NIFI_NAR_VERSION"] = old_version


def test_delete_nar_not_found():
    """Test delete_nar with non-existent coordinate raises error."""
    with pytest.raises(ValueError, match="NAR not found"):
        ci.delete_nar(
            group="non-existent-group",
            artifact="non-existent-nar",
            version="0.0.0"
        )


@pytest.mark.skipif(TEST_NAR_PATH is None, reason="TEST_NAR_PATH not set")
def test_upload_delete_nar_roundtrip():
    """Test uploading and deleting a NAR via CI functions."""
    # Upload
    upload_result = ci.upload_nar(file_path=TEST_NAR_PATH)

    assert isinstance(upload_result, dict)
    assert "identifier" in upload_result
    assert "group" in upload_result
    assert "artifact" in upload_result
    assert "version" in upload_result
    assert upload_result["state"] == "Installed"

    try:
        # Verify it appears in list
        list_result = ci.list_nars()
        assert any(
            n["identifier"] == upload_result["identifier"]
            for n in list_result["nars"]
        )
    finally:
        # Delete it
        delete_result = ci.delete_nar(identifier=upload_result["identifier"])
        assert delete_result["deleted"] == "true"

        # Verify deletion
        list_result = ci.list_nars()
        assert not any(
            n["identifier"] == upload_result["identifier"]
            for n in list_result["nars"]
        )


# =============================================================================
# Config Verification CI Tests
# =============================================================================


class TestVerifyConfigValidation:
    """Test verify_config validation logic (no NiFi required)."""

    def test_missing_process_group_id(self):
        """Test missing process_group_id raises ValueError."""
        old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
        try:
            with pytest.raises(ValueError, match="process_group_id is required"):
                ci.verify_config()
        finally:
            if old_val:
                os.environ["NIFI_PROCESS_GROUP_ID"] = old_val

    def test_process_group_id_from_env(self):
        """Test that process_group_id can be read from environment."""
        # Mock canvas functions to avoid actual NiFi calls
        mock_pg = MagicMock()
        mock_pg.component.name = "TestPG"

        with patch.dict(os.environ, {"NIFI_PROCESS_GROUP_ID": "test-pg-id"}):
            with patch("nipyapi.canvas.get_process_group", return_value=mock_pg):
                with patch("nipyapi.canvas.list_all_controllers", return_value=[]):
                    with patch("nipyapi.canvas.list_all_processors", return_value=[]):
                        result = ci.verify_config()
                        assert result["verified"] == "true"
                        assert result["process_group_name"] == "TestPG"


def test_verify_config_empty_pg(fix_pg):
    """Test verify_config on empty process group succeeds."""
    f_pg = fix_pg.generate()

    result = ci.verify_config(process_group_id=f_pg.id, fail_on_error=False)

    assert result["verified"] == "true"
    assert result["failed_count"] == 0
    assert result["controller_results"] == []
    assert result["processor_results"] == []


def test_verify_config_with_processor(fix_pg, fix_proc):
    """Test verify_config verifies processors."""
    f_pg = fix_pg.generate()
    f_p1 = fix_proc.generate(parent_pg=f_pg)

    result = ci.verify_config(process_group_id=f_pg.id, fail_on_error=False)

    assert "processor_results" in result
    assert len(result["processor_results"]) == 1
    assert result["processor_results"][0]["id"] == f_p1.id


def test_verify_config_with_controller(fix_pg, fix_cont):
    """Test verify_config verifies controller services."""
    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)

    result = ci.verify_config(process_group_id=f_pg.id, fail_on_error=False)

    assert "controller_results" in result
    assert len(result["controller_results"]) == 1
    assert result["controller_results"][0]["id"] == f_c1.id


def test_verify_config_fail_on_error(fix_pg):
    """Test verify_config raises when fail_on_error=True and verification fails."""
    import nipyapi

    f_pg = fix_pg.generate()

    # Create a DBCPConnectionPool which will fail verification (missing config)
    dbcp_type = [t for t in nipyapi.canvas.list_all_controller_types()
                 if t.type == 'org.apache.nifi.dbcp.DBCPConnectionPool']
    if not dbcp_type:
        pytest.skip("DBCPConnectionPool not available")

    controller = nipyapi.canvas.create_controller(f_pg, dbcp_type[0], name='TestDBCP')

    try:
        # Should raise ValueError because verification fails
        with pytest.raises(ValueError, match="Verification failed"):
            ci.verify_config(process_group_id=f_pg.id, fail_on_error=True)

        # With fail_on_error=False, should return result instead
        result = ci.verify_config(process_group_id=f_pg.id, fail_on_error=False)
        assert result["verified"] == "false"
        assert result["failed_count"] > 0

    finally:
        nipyapi.canvas.delete_controller(controller)


def test_verify_config_skips_enabled_controllers(fix_pg, fix_cont):
    """Test that verify_config skips enabled controller services."""
    import nipyapi

    f_pg = fix_pg.generate()
    f_c1 = fix_cont(parent_pg=f_pg)

    # Enable the controller
    f_c1 = nipyapi.canvas.schedule_controller(f_c1, True)

    try:
        result = ci.verify_config(process_group_id=f_pg.id, fail_on_error=False)

        # Controller should be skipped
        assert len(result["controller_results"]) == 1
        assert result["controller_results"][0]["skipped"] is True

    finally:
        # Cleanup: disable the controller
        nipyapi.canvas.schedule_controller(f_c1, False)
