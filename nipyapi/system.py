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
    with nipyapi.utils.rest_exceptions():
        try:
            about = nipyapi.nifi.FlowApi().get_about_info()
            return nipyapi.nifi.VersionInfoDTO(ni_fi_version=about.about.version)
        except Exception:  # pylint: disable=broad-exception-caught
            diags = get_system_diagnostics()
            return diags.system_diagnostics.aggregate_snapshot.version_info


def get_registry_version_info():
    """
    Returns the version information of the connected NiFi Registry instance.

    Uses About endpoint which is sufficient for version probes.
    Returns (str): The version string (e.g., "2.5.0")
    """
    details = nipyapi.registry.AboutApi().get_version()
    # The generated model for Registry 2.5.0 exposes `registry_about_version`
    # but we normalize and attempt multiple shapes for forward/backward compat.
    # Always return a plain version string.
    try:
        # Direct attribute on the model (current generator)
        ver = getattr(details, 'registry_about_version', None)
        if ver:
            return ver
        # Sometimes models expose a top-level `version`
        ver = getattr(details, 'version', None)
        if ver:
            return ver
        # Attempt dict conversion and look for common keys
        if hasattr(details, 'to_dict'):
            d = details.to_dict() or {}
        elif isinstance(details, dict):
            d = details
        else:
            d = {}
        for key in (
            'registry_about_version', 'registryAboutVersion', 'version',
            'registry_version', 'registryVersion'
        ):
            if key in d and d[key]:
                return d[key]
        # If details is already a string, return it as-is
        if isinstance(details, str):
            return details
    except Exception:  # pylint: disable=broad-exception-caught
        pass
    # Could not determine; raise to allow caller to handle defaults
    raise ValueError('Unable to determine NiFi Registry version from About API response')
