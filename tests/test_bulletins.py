"""Tests for `nipyapi.bulletins` module."""

from datetime import datetime, timezone

import pytest

import nipyapi
from nipyapi import bulletins, canvas, nifi


# --- Test Helpers ---


def create_test_bulletin(message, level='INFO', category='Test'):
    """
    Create a controller-level bulletin for testing.

    Creates a FLOW_CONTROLLER type bulletin. These bulletins cannot be cleared
    via API and expire automatically after 5 minutes.
    """
    bulletin_dto = nifi.BulletinDTO(
        level=level,
        category=category,
        message=message,
        source_type='FLOW_CONTROLLER'
    )
    bulletin_entity = nifi.BulletinEntity(bulletin=bulletin_dto)
    return nifi.ControllerApi().create_bulletin(body=bulletin_entity)


# --- Retrieval Tests ---


def test_get_bulletins():
    """Test basic bulletin retrieval."""
    r = bulletins.get_bulletins()
    assert isinstance(r, nifi.ControllerBulletinsEntity)


def test_get_bulletin_board():
    """Test bulletin board returns list."""
    r = bulletins.get_bulletin_board()
    assert isinstance(r, list)


def test_get_bulletin_board_with_pg_filter(fix_pg):
    """Test bulletin board filtering by process group."""
    pg = fix_pg.generate()
    r = bulletins.get_bulletin_board(pg_id=pg.id)
    assert isinstance(r, list)
    for b in r:
        assert b.group_id == pg.id


def test_get_bulletin_board_with_limit():
    """Test bulletin board with limit parameter."""
    r = bulletins.get_bulletin_board(limit=5)
    assert isinstance(r, list)
    assert len(r) <= 5


def test_get_bulletin_board_with_source_filter():
    """Test bulletin board filtering by source name pattern."""
    r = bulletins.get_bulletin_board(source_name=".*Generate.*")
    assert isinstance(r, list)
    # Now returns BulletinDTO directly, so access fields directly
    for b in r:
        assert "Generate" in (b.source_name or "")


# --- Deprecation Tests ---


def test_canvas_get_bulletins_alias():
    """Test that canvas.get_bulletins works as an alias."""
    r = canvas.get_bulletins()
    assert isinstance(r, nifi.ControllerBulletinsEntity)


def test_canvas_get_bulletin_board_alias():
    """Test that canvas.get_bulletin_board works as an alias."""
    r = canvas.get_bulletin_board()
    assert isinstance(r, list)


# --- Test Utility Tests ---


# --- Utility Function Tests ---


def test_format_timestamp_none():
    """Test timestamp formatting with None returns current time."""
    ts = nipyapi.utils.format_timestamp(None)
    assert isinstance(ts, str)
    assert 'T' in ts
    assert ts.endswith('Z')


def test_format_timestamp_datetime():
    """Test timestamp formatting with datetime object."""
    dt = datetime(2025, 1, 15, 12, 30, 45, 123456, tzinfo=timezone.utc)
    ts = nipyapi.utils.format_timestamp(dt)
    assert ts == "2025-01-15T12:30:45.123Z"


def test_format_timestamp_naive_datetime():
    """Test timestamp formatting with naive datetime assumes UTC."""
    dt = datetime(2025, 1, 15, 12, 30, 45, 123456)
    ts = nipyapi.utils.format_timestamp(dt)
    assert ts == "2025-01-15T12:30:45.123Z"


def test_format_timestamp_string_parsing():
    """Test timestamp formatting parses and reformats strings."""
    ts_str = "2025-01-15T12:30:45.123Z"
    # Default format returns same ISO 8601 format
    ts = nipyapi.utils.format_timestamp(ts_str)
    assert ts == ts_str
    # Can reformat to different format
    ts = nipyapi.utils.format_timestamp(ts_str, fmt="%Y-%m-%d")
    assert ts == "2025-01-15"


def test_format_timestamp_custom_format():
    """Test timestamp formatting with custom format string."""
    dt = datetime(2025, 1, 15, 12, 30, 45, 123456, tzinfo=timezone.utc)
    ts = nipyapi.utils.format_timestamp(dt, fmt="%Y-%m-%d")
    assert ts == "2025-01-15"
    ts = nipyapi.utils.format_timestamp(dt, fmt="%H:%M:%S")
    assert ts == "12:30:45"


# --- Clearing Tests (NiFi 2.7.0+) ---


class TestClearBulletins:
    """Tests for bulletin clearing functionality (requires NiFi 2.7.0+)."""

    @pytest.fixture
    def error_processor(self, fix_pg):
        """Create a processor that generates error bulletins."""
        pg = fix_pg.generate()

        # Create a processor that will generate errors
        proc_type = canvas.get_processor_type('InvokeHTTP')
        proc = canvas.create_processor(
            pg, proc_type, (100, 100), 'bulletin_test_http'
        )

        # Configure with invalid URL to generate errors
        config = nifi.ProcessorConfigDTO(
            properties={'Remote URL': 'http://localhost:99999/invalid'}
        )
        canvas.update_processor(proc, config)

        # Create a GenerateFlowFile to feed it
        gen_type = canvas.get_processor_type('GenerateFlowFile')
        gen_proc = canvas.create_processor(
            pg, gen_type, (100, 200), 'bulletin_test_gen'
        )
        gen_config = nifi.ProcessorConfigDTO(properties={'Batch Size': '1'})
        canvas.update_processor(gen_proc, gen_config)

        # Connect and auto-terminate failure
        canvas.create_connection(gen_proc, proc, ['success'], 'success')

        # Refresh to get latest state
        proc = canvas.get_processor(proc.id, 'id')

        yield {
            'pg': pg,
            'processor': proc,
            'generator': gen_proc
        }

    def test_clear_processor_bulletins(self, error_processor):
        """Test clearing bulletins for a processor."""
        proc = error_processor['processor']

        # Clear any existing bulletins
        result = bulletins.clear_processor_bulletins(proc.id)

        # Should return a result entity
        assert result is not None

    def test_clear_processor_bulletins_with_timestamp(self, error_processor):
        """Test clearing processor bulletins with specific timestamp."""
        proc = error_processor['processor']

        # Use a specific timestamp
        ts = datetime.now(timezone.utc)
        result = bulletins.clear_processor_bulletins(proc.id, before=ts)

        assert result is not None

    def test_clear_process_group_bulletins(self, error_processor):
        """Test clearing bulletins for a process group with component IDs."""
        pg = error_processor['pg']
        proc = error_processor['processor']
        gen = error_processor['generator']

        # NiFi API requires component_ids to be specified
        result = bulletins.clear_process_group_bulletins(
            pg.id, component_ids=[proc.id, gen.id]
        )

        assert result is not None

    def test_clear_process_group_bulletins_targeted(self, error_processor):
        """Test clearing bulletins for specific components in a PG."""
        pg = error_processor['pg']
        proc = error_processor['processor']

        result = bulletins.clear_process_group_bulletins(
            pg.id, component_ids=[proc.id]
        )

        assert result is not None

    def test_clear_all_bulletins(self, error_processor):
        """Test comprehensive bulletin clearing."""
        pg = error_processor['pg']

        result = bulletins.clear_all_bulletins(pg_id=pg.id)

        assert isinstance(result, int)
        assert result >= 0

    def test_clear_all_bulletins_root(self):
        """Test clearing all bulletins from root PG."""
        result = bulletins.clear_all_bulletins()

        assert isinstance(result, int)
        assert result >= 0


class TestClearControllerServiceBulletins:
    """Tests for controller service bulletin clearing."""

    @pytest.fixture
    def controller_service(self, fix_pg):
        """Create a controller service for testing."""
        pg = fix_pg.generate()

        # Create a controller service
        cs_type = canvas.get_controller_type('StandardSSLContextService')
        cs = canvas.create_controller(pg, cs_type, 'bulletin_test_ssl')

        yield {'pg': pg, 'cs': cs}

    def test_clear_controller_service_bulletins(self, controller_service):
        """Test clearing bulletins for a controller service."""
        cs = controller_service['cs']

        result = bulletins.clear_controller_service_bulletins(cs.id)

        assert result is not None


# --- Stack Trace Access Tests ---


def test_bulletin_dto_has_stack_trace_field():
    """Test that BulletinDTO has stack_trace field (NiFi 2.7.0+)."""
    # Verify the model has the stack_trace attribute
    dto = nifi.BulletinDTO()
    assert hasattr(dto, 'stack_trace')
    assert 'stack_trace' in dto.swagger_types


def test_bulletin_dto_has_timestamp_iso_field():
    """Test that BulletinDTO has timestamp_iso field (NiFi 2.7.0+)."""
    dto = nifi.BulletinDTO()
    assert hasattr(dto, 'timestamp_iso')
    assert 'timestamp_iso' in dto.swagger_types
