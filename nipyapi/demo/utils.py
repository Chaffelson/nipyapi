# coding: utf-8

"""
Common utils for demos
"""

from __future__ import absolute_import
import requests


class DockerContainer(object):
    """
    Helper class for Docker containiner automation without using Ansible
    """
    def __init__(self, name=None, image_name=None, image_tag=None, ports=None,
                 env=None, test_url=None, endpoint=None):
        self.name = name
        self.image_name = image_name
        self.image_tag = image_tag
        self.ports = ports
        self.env = env
        self.test_url = test_url
        self.endpoint = endpoint

    def get_test_url_status(self):
        """
        Checks if a URL is available
        :return: status code if available, String 'ConnectionError' if not
        """
        try:
            return requests.get(self.test_url).status_code
        except requests.ConnectionError:
            return 'ConnectionError'
