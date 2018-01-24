# coding: utf-8

"""
NiPyAPI: A convenient Python wrapper for the Apache NiFi Rest API
"""

from __future__ import absolute_import
import nipyapi.nifi
import nipyapi.registry

nifi_config = nipyapi.nifi.configuration
registry_config = nipyapi.registry.configuration

# Method to check if we're compatible with the API endpoint
# If None, then no check has been done
# If True, then we have tested and there are no issues
# If False, then we believe we are incompatible
nifi_config.version_check = None


# Set Default Host for NiFi
nifi_config.host = 'http://localhost:8080/nifi-api'

# Set Default Host for NiFi-Registry
registry_config.host = 'http://localhost:18080/nifi-registry-api'


# Test Configuration parameters
test_docker_registry_endpoint = 'http://registry:18080'
test_pg_name = "nipyapi_test_ProcessGroup"
test_registry_client_name = 'nipyapi_test_0'
test_processor_name = 'nipyapi_test_0'
