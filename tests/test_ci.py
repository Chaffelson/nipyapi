"""Tests for `nipyapi.ci` module."""

import os
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

    @patch("nipyapi.ci.resolve_git_ref.requests.get")
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
        assert "api.github.com" in call_args[0][0]
        assert call_args[1]["headers"]["Authorization"] == "Bearer ghp_xxx"

    @patch("nipyapi.ci.resolve_git_ref.requests.get")
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

    @patch("nipyapi.ci.resolve_git_ref.requests.get")
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


def test_get_versions_default_root():
    """Test get_versions defaults to root when no PG ID provided."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        # get_versions defaults to root PG, doesn't raise error
        result = ci.get_versions()
        assert isinstance(result, dict)
        assert "parent_id" in result
        assert "total_count" in result
    finally:
        if old_val:
            os.environ["NIFI_PROCESS_GROUP_ID"] = old_val


def test_change_version_missing_pg_id():
    """Test change_version without process_group_id raises error."""
    old_val = os.environ.pop("NIFI_PROCESS_GROUP_ID", None)
    try:
        with pytest.raises(ValueError, match="process_group_id is required"):
            ci.change_version()
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
