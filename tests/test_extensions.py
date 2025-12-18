"""
Tests for nipyapi.extensions module - NAR file management.

All tests use the fix_test_nar fixture which generates valid Python
processor NARs dynamically. No external NAR files required.
"""

import os
import tempfile

import pytest

import nipyapi

pytestmark = pytest.mark.usefixtures("fix_profiles")


class TestListNars:
    """Tests for list_nars function."""

    def test_list_nars_returns_list(self):
        """list_nars should return a list."""
        result = nipyapi.extensions.list_nars()
        assert isinstance(result, list)

    def test_list_nars_structure(self):
        """list_nars results should have expected structure."""
        nars = nipyapi.extensions.list_nars()
        for nar in nars:
            # Should be NarSummaryDTO objects
            assert hasattr(nar, "identifier")
            assert hasattr(nar, "coordinate")
            assert hasattr(nar, "state")


class TestGetNar:
    """Tests for get_nar function."""

    def test_get_nar_not_found(self):
        """get_nar returns None for non-existent NAR."""
        result = nipyapi.extensions.get_nar("non-existent-id")
        assert result is None

    def test_get_nar_by_coordinate_not_found(self):
        """get_nar_by_coordinate returns None when not found."""
        result = nipyapi.extensions.get_nar_by_coordinate(
            "non-existent", "fake-nar", "0.0.0"
        )
        assert result is None


class TestUploadDeleteNar:
    """Tests for upload_nar and delete_nar functions."""

    def test_upload_nar_missing_args(self):
        """upload_nar requires file_path or file_bytes."""
        with pytest.raises(ValueError, match="Either file_path or file_bytes"):
            nipyapi.extensions.upload_nar()

    def test_upload_nar_file_not_found(self):
        """upload_nar raises FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError, match="NAR file not found"):
            nipyapi.extensions.upload_nar("/nonexistent/path.nar")

    def test_upload_nar_bytes_requires_filename(self):
        """upload_nar with file_bytes requires filename."""
        with pytest.raises(ValueError, match="filename is required"):
            nipyapi.extensions.upload_nar(file_bytes=b"fake-nar-content")

    def test_upload_and_delete_roundtrip(self, fix_test_nar):
        """Test uploading a NAR and then deleting it."""
        nar_path = fix_test_nar(version="0.0.1")

        # Upload (waits for installation automatically)
        nar = nipyapi.extensions.upload_nar(nar_path)
        assert nar is not None
        assert hasattr(nar, "identifier")
        nar_id = nar.identifier

        # Verify installation completed
        assert str(nar.state).upper() == "INSTALLED"

        try:
            # Verify it appears in list
            nars = nipyapi.extensions.list_nars()
            assert any(n.identifier == nar_id for n in nars)

            # Get by coordinate
            coord = nar.coordinate
            found = nipyapi.extensions.get_nar_by_coordinate(
                coord.group, coord.artifact, coord.version
            )
            assert found is not None
            assert found.identifier == nar_id

            # Get details
            details = nipyapi.extensions.get_nar_details(nar_id)
            assert details is not None
            assert hasattr(details, "processor_types")

        finally:
            # Clean up - delete the NAR
            nipyapi.extensions.delete_nar(nar_id)

            # Verify deletion
            nars = nipyapi.extensions.list_nars()
            assert not any(n.identifier == nar_id for n in nars)

    def test_download_nar(self, fix_test_nar):
        """Test downloading a NAR to file."""
        nar_path = fix_test_nar(version="0.0.1")

        # Upload (waits for installation automatically)
        nar = nipyapi.extensions.upload_nar(nar_path)
        nar_id = nar.identifier

        try:
            # Download to temp file
            with tempfile.NamedTemporaryFile(suffix=".nar", delete=False) as f:
                temp_path = f.name

            try:
                result = nipyapi.extensions.download_nar(nar_id, temp_path)
                assert result == temp_path
                assert os.path.exists(temp_path)
                assert os.path.getsize(temp_path) > 0

                # Downloaded NAR should be valid (non-empty)
                with open(temp_path, "rb") as f:
                    downloaded = f.read()
                    assert len(downloaded) > 0
            finally:
                os.unlink(temp_path)

        finally:
            nipyapi.extensions.delete_nar(nar_id)

    def test_download_nar_bytes(self, fix_test_nar):
        """Test downloading a NAR as bytes."""
        nar_path = fix_test_nar(version="0.0.1")

        # Upload (waits for installation automatically)
        nar = nipyapi.extensions.upload_nar(nar_path)
        nar_id = nar.identifier

        try:
            # Download as bytes
            nar_bytes = nipyapi.extensions.download_nar(nar_id)
            assert isinstance(nar_bytes, bytes)
            assert len(nar_bytes) > 0

        finally:
            nipyapi.extensions.delete_nar(nar_id)


class TestNarWithNoProcessors:
    """Tests for NAR files that upload but contain no valid processors."""

    def test_invalid_nar_uploads_but_has_no_processors(self, fix_test_nar):
        """NAR without Java implements uploads but has no processor types."""
        # Create NAR without Java implements declaration
        nar_path = fix_test_nar(version="0.0.1", valid=False)

        # Upload should succeed - NAR format is valid
        nar = nipyapi.extensions.upload_nar(nar_path)
        assert nar is not None
        assert str(nar.state).upper() == "INSTALLED"

        try:
            # NAR details should be retrievable
            details = nipyapi.extensions.get_nar_details(nar.identifier)
            assert details is not None

            # Processor types should be empty - NiFi doesn't recognize
            # the processor without the Java implements declaration
            processor_count = len(details.processor_types) if details.processor_types else 0
            assert processor_count == 0, "Invalid NAR should have no processor types"

            # Should still be able to list and delete
            nars = nipyapi.extensions.list_nars()
            assert any(n.identifier == nar.identifier for n in nars)

        finally:
            nipyapi.extensions.delete_nar(nar.identifier)

    def test_valid_nar_has_processor_types(self, fix_test_nar):
        """NAR with Java implements has recognizable processor types."""
        # Create valid NAR (default)
        nar_path = fix_test_nar(version="0.0.1", valid=True)

        nar = nipyapi.extensions.upload_nar(nar_path)
        assert nar is not None

        try:
            details = nipyapi.extensions.get_nar_details(nar.identifier)
            assert details is not None

            # Valid NAR should have processor types
            processor_count = len(details.processor_types) if details.processor_types else 0
            assert processor_count == 1, "Valid NAR should have processor types"
            # Processor name is dynamically generated based on test name
            # (ends with 'Proc' suffix from fixture)
            proc_type = details.processor_types[0].type
            assert proc_type.endswith("Proc"), f"Expected processor name ending with 'Proc', got: {proc_type}"

        finally:
            nipyapi.extensions.delete_nar(nar.identifier)


class TestProcessorInitialization:
    """Tests for processor initialization functions."""

    def test_get_processor_init_status_not_found(self):
        """get_processor_init_status handles missing processor."""
        status = nipyapi.extensions.get_processor_init_status("non-existent-id")
        assert status["status"] == "error"
        assert status["is_ready"] is False
        assert "not found" in status["init_message"]

    def test_processor_init_lifecycle(self, fix_test_nar):
        """Test full processor initialization lifecycle."""
        nar_path = fix_test_nar(version="0.0.1")

        # Upload NAR
        nar = nipyapi.extensions.upload_nar(nar_path)
        details = nipyapi.extensions.get_nar_details(nar.identifier)
        proc_type = nipyapi.canvas.get_processor_type(details.processor_types[0].type)

        # Create processor
        root_pg = nipyapi.canvas.get_process_group("root", "name")
        proc = nipyapi.canvas.create_processor(
            parent_pg=root_pg,
            processor=proc_type,
            location=(400, 400),
            name="TestInitLifecycle",
        )

        try:
            # Initial status should be initializing or ready
            status = nipyapi.extensions.get_processor_init_status(proc)
            assert status["status"] in ("initializing", "ready")

            # Wait for initialization
            proc = nipyapi.extensions.wait_for_processor_init(proc)

            # Should now be ready
            status = nipyapi.extensions.get_processor_init_status(proc)
            assert status["status"] == "ready"
            assert status["is_ready"] is True
            # Note: has_properties may be False for minimal test processors with no
            # defined properties - this is expected and valid

        finally:
            proc = nipyapi.canvas.get_processor(proc.id, "id")
            if proc:
                nipyapi.canvas.delete_processor(proc)
            nipyapi.extensions.delete_nar(nar.identifier, force=True)

    def test_missing_nar_detection(self, fix_test_nar):
        """Test that force-deleting NAR leaves processors in a halting state.

        After force-deleting a NAR, processors may be either:
        - Deleted entirely by NiFi (status='error', 'not found')
        - Orphaned with missing NAR (status='missing_nar')

        Both are valid halting states - the key is that the processor is
        no longer in 'ready' or 'initializing' state.
        """
        nar_path = fix_test_nar(version="0.0.1")

        # Upload NAR and create processor
        nar = nipyapi.extensions.upload_nar(nar_path)
        details = nipyapi.extensions.get_nar_details(nar.identifier)
        proc_type = nipyapi.canvas.get_processor_type(details.processor_types[0].type)

        root_pg = nipyapi.canvas.get_process_group("root", "name")
        proc = nipyapi.canvas.create_processor(
            parent_pg=root_pg,
            processor=proc_type,
            location=(500, 500),
            name="TestMissingNar",
        )

        try:
            # Wait for init
            proc = nipyapi.extensions.wait_for_processor_init(proc)

            # Force delete NAR - this now waits for cleanup to complete
            result = nipyapi.extensions.delete_nar(nar.identifier, force=True)

            # Verify cleanup completed
            assert result["cleanup_complete"], "NAR cleanup should complete"

            # Check processor status - should be in a halting state
            status = nipyapi.extensions.get_processor_init_status(proc.id)

            # Accept either 'missing_nar' (orphaned) or 'error' (deleted by NiFi)
            halting_states = {"missing_nar", "error"}
            assert status["status"] in halting_states, (
                f"Expected halting state, got: {status['status']}"
            )
            assert status["is_ready"] is False

        finally:
            # Processor may have been deleted by NiFi during force-delete
            proc = nipyapi.canvas.get_processor(proc.id, "id")
            if proc:
                nipyapi.canvas.delete_processor(proc)


class TestProcessorBundleVersions:
    """Tests for processor bundle version functions."""

    def test_get_processor_bundle_versions_no_match(self):
        """get_processor_bundle_versions returns empty for unknown type."""
        result = nipyapi.extensions.get_processor_bundle_versions("NonExistentProcessor")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_processor_bundle_versions_structure(self, fix_test_nar):
        """get_processor_bundle_versions returns expected structure."""
        nar_path = fix_test_nar(version="0.0.1")

        # Upload NAR first
        nar = nipyapi.extensions.upload_nar(nar_path)
        details = nipyapi.extensions.get_nar_details(nar.identifier)
        proc_type_name = details.processor_types[0].type

        try:
            versions = nipyapi.extensions.get_processor_bundle_versions(proc_type_name)
            assert isinstance(versions, list)
            assert len(versions) >= 1

            for v in versions:
                assert "bundle" in v
                assert "type" in v
                assert hasattr(v["bundle"], "group")
                assert hasattr(v["bundle"], "artifact")
                assert hasattr(v["bundle"], "version")

        finally:
            nipyapi.extensions.delete_nar(nar.identifier)

    def test_change_processor_bundle_version_not_found(self):
        """change_processor_bundle_version raises for missing processor."""
        with pytest.raises(ValueError, match="Processor not found"):
            nipyapi.extensions.change_processor_bundle_version(
                "non-existent-id", "1.0.0"
            )

    def test_change_processor_bundle_version_invalid_version(self, fix_test_nar):
        """change_processor_bundle_version raises for unavailable version."""
        nar_path = fix_test_nar(version="0.0.1")

        # Upload NAR and create processor
        nar = nipyapi.extensions.upload_nar(nar_path)
        details = nipyapi.extensions.get_nar_details(nar.identifier)
        proc_type = nipyapi.canvas.get_processor_type(details.processor_types[0].type)

        root_pg = nipyapi.canvas.get_process_group("root", "name")
        proc = nipyapi.canvas.create_processor(
            parent_pg=root_pg,
            processor=proc_type,
            location=(600, 600),
            name="TestVersionChange",
        )

        try:
            proc = nipyapi.extensions.wait_for_processor_init(proc)

            with pytest.raises(ValueError, match="not available"):
                nipyapi.extensions.change_processor_bundle_version(
                    proc, "nonexistent-version"
                )

        finally:
            proc = nipyapi.canvas.get_processor(proc.id, "id")
            nipyapi.canvas.delete_processor(proc)
            nipyapi.extensions.delete_nar(nar.identifier)


class TestMultiVersionWorkflow:
    """Tests for multi-version processor workflows."""

    def test_get_processor_type_version(self, fix_test_nar):
        """get_processor_type_version returns correct versioned type."""
        # Upload both versions
        nar_v1 = nipyapi.extensions.upload_nar(fix_test_nar(version="0.0.1"))
        nar_v2 = nipyapi.extensions.upload_nar(fix_test_nar(version="0.0.2"))

        try:
            # Get details to find processor type name
            details = nipyapi.extensions.get_nar_details(nar_v1.identifier)
            proc_type_name = details.processor_types[0].type

            # Get available versions
            versions = nipyapi.extensions.get_processor_bundle_versions(proc_type_name)
            assert len(versions) >= 2

            # Get specific version
            v1_bundle_version = versions[0]["bundle"].version
            proc_type = nipyapi.extensions.get_processor_type_version(
                proc_type_name, v1_bundle_version
            )
            assert proc_type.bundle.version == v1_bundle_version

        finally:
            nipyapi.extensions.delete_nar(nar_v1.identifier)
            nipyapi.extensions.delete_nar(nar_v2.identifier)

    def test_get_processor_type_version_not_found(self, fix_test_nar):
        """get_processor_type_version raises for unknown version."""
        nar = nipyapi.extensions.upload_nar(fix_test_nar(version="0.0.1"))

        try:
            details = nipyapi.extensions.get_nar_details(nar.identifier)
            proc_type_name = details.processor_types[0].type

            with pytest.raises(ValueError, match="not available"):
                nipyapi.extensions.get_processor_type_version(
                    proc_type_name, "nonexistent-version"
                )

        finally:
            nipyapi.extensions.delete_nar(nar.identifier)

    def test_create_processor_with_specific_version(self, fix_test_nar):
        """Create processors with specific bundle versions."""
        nar_v1 = nipyapi.extensions.upload_nar(fix_test_nar(version="0.0.1"))
        nar_v2 = nipyapi.extensions.upload_nar(fix_test_nar(version="0.0.2"))
        proc_v1 = None
        proc_v2 = None

        try:
            # Get processor type name
            details_v1 = nipyapi.extensions.get_nar_details(nar_v1.identifier)
            details_v2 = nipyapi.extensions.get_nar_details(nar_v2.identifier)
            proc_type_name = details_v1.processor_types[0].type

            v1_bundle = details_v1.processor_types[0].bundle.version
            v2_bundle = details_v2.processor_types[0].bundle.version

            # Get versioned types
            proc_type_v1 = nipyapi.extensions.get_processor_type_version(
                proc_type_name, v1_bundle
            )
            proc_type_v2 = nipyapi.extensions.get_processor_type_version(
                proc_type_name, v2_bundle
            )

            root_pg = nipyapi.canvas.get_process_group("root", "name")

            # Create v1 processor
            proc_v1 = nipyapi.canvas.create_processor(
                parent_pg=root_pg,
                processor=proc_type_v1,
                location=(700, 100),
                name="TestMultiV1",
            )
            assert proc_v1.component.bundle.version == v1_bundle

            # Create v2 processor alongside
            proc_v2 = nipyapi.canvas.create_processor(
                parent_pg=root_pg,
                processor=proc_type_v2,
                location=(700, 200),
                name="TestMultiV2",
            )
            assert proc_v2.component.bundle.version == v2_bundle

            # Wait for both to initialize (avoids NiFi bug where force delete
            # blocks indefinitely during processor initialization)
            proc_v1 = nipyapi.extensions.wait_for_processor_init(proc_v1)
            proc_v2 = nipyapi.extensions.wait_for_processor_init(proc_v2)

        finally:
            # Cleanup processors first (must complete before NAR deletion)
            for proc in [proc_v1, proc_v2]:
                if proc:
                    try:
                        p = nipyapi.canvas.get_processor(proc.id, "id")
                        if p:
                            nipyapi.canvas.delete_processor(p)
                    except Exception:
                        pass
            # Cleanup NARs (safe now that processors are deleted)
            nipyapi.extensions.delete_nar(nar_v1.identifier, force=True)
            nipyapi.extensions.delete_nar(nar_v2.identifier, force=True)

    def test_change_processor_bundle_version_roundtrip(self, fix_test_nar):
        """Change processor between bundle versions."""
        nar_v1 = nipyapi.extensions.upload_nar(fix_test_nar(version="0.0.1"))
        nar_v2 = nipyapi.extensions.upload_nar(fix_test_nar(version="0.0.2"))
        proc = None

        try:
            # Get processor type info
            details_v1 = nipyapi.extensions.get_nar_details(nar_v1.identifier)
            details_v2 = nipyapi.extensions.get_nar_details(nar_v2.identifier)
            proc_type_name = details_v1.processor_types[0].type

            v1_bundle = details_v1.processor_types[0].bundle.version
            v2_bundle = details_v2.processor_types[0].bundle.version

            # Create processor with v1
            proc_type_v1 = nipyapi.extensions.get_processor_type_version(
                proc_type_name, v1_bundle
            )
            root_pg = nipyapi.canvas.get_process_group("root", "name")
            proc = nipyapi.canvas.create_processor(
                parent_pg=root_pg,
                processor=proc_type_v1,
                location=(800, 100),
                name="TestVersionRoundtrip",
            )

            # Wait for initialization
            proc = nipyapi.extensions.wait_for_processor_init(proc)
            assert proc.component.bundle.version == v1_bundle

            # Change to v2
            proc = nipyapi.extensions.change_processor_bundle_version(proc, v2_bundle)
            assert proc.component.bundle.version == v2_bundle

            # Change back to v1
            proc = nipyapi.extensions.change_processor_bundle_version(proc, v1_bundle)
            assert proc.component.bundle.version == v1_bundle

        finally:
            if proc:
                try:
                    p = nipyapi.canvas.get_processor(proc.id, "id")
                    if p:
                        nipyapi.canvas.delete_processor(p)
                except Exception:
                    pass
            nipyapi.extensions.delete_nar(nar_v1.identifier, force=True)
            nipyapi.extensions.delete_nar(nar_v2.identifier, force=True)
