"""List installed NAR extensions."""

import logging

import nipyapi

log = logging.getLogger(__name__)


def list_nars() -> dict:
    """
    List all installed NAR extensions in NiFi.

    Returns:
        dict with:
            - count: Number of installed NARs
            - nars: List of NAR summaries with coordinate, state, extensions

    Example:
        nipyapi ci list_nars
    """
    log.info("Listing installed NARs")

    nars = nipyapi.extensions.list_nars()

    log.info("Found %d installed NARs", len(nars))

    return {
        "count": len(nars),
        "nars": [
            {
                "identifier": nar.identifier,
                "group": nar.coordinate.group if nar.coordinate else None,
                "artifact": nar.coordinate.artifact if nar.coordinate else None,
                "version": nar.coordinate.version if nar.coordinate else None,
                "state": nar.state,
                "extension_count": nar.extension_count or 0,
            }
            for nar in nars
        ],
    }
