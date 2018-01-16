# coding: utf-8

"""
NiPyAPI: A convenient Python wrapper for the Apache NiFi Rest API
"""

from __future__ import absolute_import
import swagger_client

swagger_config = swagger_client.configuration

# Method to check if we're compatible with the API endpoint
# If None, then no check has been done
# If True, then we have tested and there are no issues
# If False, then we believe we are incompatible
swagger_config.version_check = None


# Set Default Host
swagger_config.host = 'http://localhost:8080/nifi-api'
