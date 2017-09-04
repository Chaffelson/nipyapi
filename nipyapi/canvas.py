# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
"""

from __future__ import absolute_import

from nipyapi import swagger_client


class Canvas:
    """
    Class to contain Wrapper methods for Canvas interaction
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

    def get_root_pg_id(self):
        con = swagger_client.FlowApi()
        pg_root = con.get_process_group_status('root')
        return pg_root.process_group_status.id
