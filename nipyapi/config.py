# coding: utf-8

"""
NiPyAPI: A convenient Python wrapper for the Apache NiFi Rest API
"""

from __future__ import absolute_import
from nipyapi.nifi import configuration as nifi_config
from nipyapi.registry import configuration as registry_config

# Method to check if we're compatible with the API endpoint
# If None, then no check has been done
# If True, then we have tested and there are no issues
# If False, then we believe we are incompatible
nifi_config.version_check = None
registry_config.version_check = None

# Set Default Host for NiFi
nifi_config.host = 'http://localhost:8080/nifi-api'

# Set Default Host for NiFi-Registry
registry_config.host = 'http://localhost:18080/nifi-registry-api'
