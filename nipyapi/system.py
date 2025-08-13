"""
For system and cluster level functions interacting with the underlying NiFi
Services
"""

import nipyapi


__all__ = [
    "get_system_diagnostics", "get_cluster", "get_node",
    "get_nifi_version_info", "get_registry_version_info"
]


def get_system_diagnostics():
    """
    Returns NiFi Sytems diagnostics page

    Returns (json):
    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.SystemDiagnosticsApi().get_system_diagnostics()


def get_cluster():
    """
    EXPERIMENTAL
    Returns the contents of the NiFi cluster

    Returns (json):
    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ControllerApi().get_cluster()


def get_node(nid):
    """
    Returns the cluster node information

    Args:
        nid (str): The UUID of the Node to target

    Returns:

    """
    with nipyapi.utils.rest_exceptions():
        return nipyapi.nifi.ControllerApi().get_node(nid)


def get_nifi_version_info():
    """
    Returns version info for the connected NiFi instance.

    - In 2.x, the non-privileged About endpoint is used first.
    - For backward compatibility with callers expecting a VersionInfoDTO,
      we return a VersionInfoDTO with only ni_fi_version set when About
      succeeds.
    - If About is unavailable, fall back to system diagnostics DTO.

    Returns (VersionInfoDTO):
    """
    try:
        about = nipyapi.nifi.FlowApi().get_about_info()
        # Build a minimal VersionInfoDTO carrying the version string
        return nipyapi.nifi.VersionInfoDTO(ni_fi_version=about.about.version)
    except Exception:
        diags = get_system_diagnostics()
        return diags.system_diagnostics.aggregate_snapshot.version_info


def get_registry_version_info():
    """
    Returns the version information of the connected NiFi Registry instance.

    Uses About endpoint which is sufficient for version probes.
    Returns (str):
    """
    details = nipyapi.registry.AboutApi().get_version()
    return details.registry_about.version
