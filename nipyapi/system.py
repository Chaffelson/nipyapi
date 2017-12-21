# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
"""

from __future__ import absolute_import
from swagger_client import ControllerApi, SystemdiagnosticsApi


__all__ = [
    "get_system_diagnostics", "get_cluster", "get_node",
    "get_nifi_version_info"
]


def get_system_diagnostics():
    """
    Returns NiFi Sytems diagnostics page
    :return JSON object:
    """
    return SystemdiagnosticsApi().get_system_diagnostics()


def get_cluster():
    """
    Returns the contents of the NiFi cluster
    :return:
    """
    return ControllerApi().get_cluster()


def get_node(nid):
    """
    Returns the cluster node information
    :param nid: NiFi ID (nid) from Node information
    :return:
    """
    return ControllerApi().get_node(nid)


def get_nifi_version_info():
    """
    Returns the version of the connected NiFi instance
    :return VersionInfoDTO:
    """
    diags = get_system_diagnostics()
    return diags.system_diagnostics.aggregate_snapshot.version_info
