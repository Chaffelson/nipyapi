"""Delete an installed NAR extension."""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


def delete_nar(
    identifier: Optional[str] = None,
    group: Optional[str] = None,
    artifact: Optional[str] = None,
    version: Optional[str] = None,
    force: Optional[bool] = None,
) -> dict:
    """
    Delete an installed NAR extension from NiFi.

    Can specify NAR by identifier or by Maven coordinate (group:artifact:version).

    Args:
        identifier: NAR identifier (UUID).
            Env: NIFI_NAR_ID
        group: Maven group ID (alternative to identifier).
            Env: NIFI_NAR_GROUP
        artifact: Maven artifact ID (required with group).
            Env: NIFI_NAR_ARTIFACT
        version: Maven version (required with group).
            Env: NIFI_NAR_VERSION
        force: Force deletion even if components are in use.
            Env: NIFI_NAR_FORCE. Defaults to False.

    Returns:
        dict with:
            - deleted: "true" if deletion succeeded
            - identifier: The deleted NAR's identifier
            - group: Maven group ID
            - artifact: Maven artifact ID
            - version: Maven version

    Raises:
        ValueError: Missing required parameters or NAR not found

    Example:
        # Delete by identifier
        nipyapi ci delete_nar --identifier abc-123-def

        # Delete by coordinate
        nipyapi ci delete_nar --group com.example --artifact my-nar --version 1.0.0

        # Force delete
        nipyapi ci delete_nar --identifier abc-123-def --force
    """
    # Get from environment if not provided
    identifier = identifier or os.environ.get("NIFI_NAR_ID")
    group = group or os.environ.get("NIFI_NAR_GROUP")
    artifact = artifact or os.environ.get("NIFI_NAR_ARTIFACT")
    version = version or os.environ.get("NIFI_NAR_VERSION")
    if force is None:
        force = nipyapi.utils.getenv_bool("NIFI_NAR_FORCE", False)

    # Find NAR by identifier or coordinate
    if identifier:
        log.info("Deleting NAR by identifier: %s", identifier)
    elif group and artifact and version:
        log.info("Finding NAR by coordinate: %s:%s:%s", group, artifact, version)
        nar = nipyapi.extensions.get_nar_by_coordinate(group, artifact, version)
        if nar is None:
            raise ValueError(f"NAR not found: {group}:{artifact}:{version}")
        identifier = nar.identifier
        log.info("Found NAR: %s", identifier)
    else:
        raise ValueError(
            "Either identifier or (group, artifact, version) is required "
            "(or set NIFI_NAR_ID or NIFI_NAR_GROUP/ARTIFACT/VERSION)"
        )

    # Delete the NAR
    result = nipyapi.extensions.delete_nar(identifier, force=force)
    coord = result.coordinate

    log.info("Deleted NAR: %s", identifier)

    return {
        "deleted": "true",
        "identifier": identifier,
        "group": coord.group if coord else None,
        "artifact": coord.artifact if coord else None,
        "version": coord.version if coord else None,
    }
