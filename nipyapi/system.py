# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
"""

from __future__ import absolute_import

from nipyapi import swagger_client


class System:
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

    def get_system_diagnostics(self):
        con = swagger_client.SystemdiagnosticsApi()
        return con.get_system_diagnostics()
