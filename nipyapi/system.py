# -*- coding: utf-8 -*-

"""
For system and cluster level functions interacting with the underlying NiFi
Services
"""

from __future__ import absolute_import
import nipyapi


__all__ = [
    "get_system_diagnostics", "get_cluster", "get_node",
    "get_nifi_version_info"
]


def get_system_diagnostics():
    """
    Returns NiFi Sytems diagnostics page

    Returns (json):
    """
    return nipyapi.nifi.SystemdiagnosticsApi().get_system_diagnostics()


def get_cluster():
    """
    EXPERIMENTAL
    Returns the contents of the NiFi cluster

    Returns (json):
    """
    return nipyapi.nifi.ControllerApi().get_cluster()


def get_node(nid):
    """
    Returns the cluster node information

    Args:
        nid (str): The UUID of the Node to target

    Returns:

    """
    return nipyapi.nifi.ControllerApi().get_node(nid)


def get_nifi_version_info():
    """
    Returns the version information of the connected NiFi instance

    Returns (VersionInfoDTO):
    """
    diags = get_system_diagnostics()
    return diags.system_diagnostics.aggregate_snapshot.version_info
