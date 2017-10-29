# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
"""

from __future__ import absolute_import

from nipyapi import swagger_client


class System(object):
    """
    Class to contain Wrapper methods for NiFi System vinteraction
    """

    def __init__(self, host=None):
        """
        Constructor
        :param host: The NiFi host base url to talk to
        """
        if host is None:
            self.host = swagger_client.configuration.host
        else:
            self.host = host

    @staticmethod
    def get_system_diagnostics():
        """
        Returns NiFi Sytems diagnostics page
        :return JSON object:
        """
        con = swagger_client.SystemdiagnosticsApi()
        return con.get_system_diagnostics()

    # TODO: Redo these with getters and setters
    @staticmethod
    def get_cluster():
        """
        Returns the contents of the NiFi cluster
        :return:
        """
        return swagger_client.ControllerApi.get_cluster()

    @staticmethod
    def get_node(nid):
        """
        Returns the cluster node information
        :param nid: NiFi ID (nid) from Node information
        :return:
        """
        return swagger_client.ControllerApi.get_node(nid)
