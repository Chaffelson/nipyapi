# coding: utf-8

"""
NiPyAPI: A convenient Python wrapper for the Apache NiFi Rest API
"""

from __future__ import absolute_import
import nipyapi.nifi

nifi_config = nipyapi.nifi.configuration

# Method to check if we're compatible with the API endpoint
# If None, then no check has been done
# If True, then we have tested and there are no issues
# If False, then we believe we are incompatible
nifi_config.version_check = None


# Set Default Host for NiFi
nifi_config.host = 'http://localhost:8080/nifi-api'


# Test Configuration parameters
test_pg_name = "nipyapi_test_ProcessGroup"
