"""Upload a NAR extension to NiFi."""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def upload_nar(
    file_path: Optional[str] = None,
    timeout: Optional[int] = None,
) -> dict:
    """
    Upload a NAR extension file to NiFi and wait for installation.

    Args:
        file_path: Path to the NAR file.
            Env: NIFI_NAR_FILE_PATH
        timeout: Seconds to wait for installation. Defaults to 120.
            Env: NIFI_NAR_TIMEOUT

    Returns:
        dict with:
            - identifier: NAR identifier
            - group: Maven group ID
            - artifact: Maven artifact ID
            - version: Maven version
            - state: Installation state
            - extension_count: Number of extensions in the NAR
            - processors: List of processor types
            - controller_services: List of controller service types

    Raises:
        ValueError: Missing required parameters, file not found, or installation fails

    Example::

        nipyapi ci upload_nar --file_path /path/to/my-nar-1.0.0.nar
    """
    # Get from environment if not provided
    file_path = file_path or os.environ.get("NIFI_NAR_FILE_PATH")
    if timeout is None:
        timeout = int(os.environ.get("NIFI_NAR_TIMEOUT", "120"))

    # Validate
    if not file_path:
        raise ValueError("file_path is required (or set NIFI_NAR_FILE_PATH)")

    if not os.path.exists(file_path):
        raise ValueError(f"NAR file not found: {file_path}")

    log.info("Uploading NAR: %s (timeout=%ds)", file_path, timeout)

    # Upload and wait for installation (built into module function)
    nar = nipyapi.extensions.upload_nar(file_path, timeout=timeout)
    coord = nar.coordinate

    log.info(
        "Installed: %s:%s:%s (%d extensions)",
        coord.group if coord else None,
        coord.artifact if coord else None,
        coord.version if coord else None,
        nar.extension_count or 0,
    )

    # Get component details
    processors = []
    controller_services = []
    details = nipyapi.extensions.get_nar_details(nar.identifier)
    if details:
        processors = [p.type for p in (details.processor_types or [])]
        controller_services = [c.type for c in (details.controller_service_types or [])]

    return {
        "identifier": nar.identifier,
        "group": coord.group if coord else None,
        "artifact": coord.artifact if coord else None,
        "version": coord.version if coord else None,
        "state": nar.state,
        "extension_count": nar.extension_count or 0,
        "processors": processors,
        "controller_services": controller_services,
    }
