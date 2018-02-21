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


# Note that changing the default hosts below will not affect an API connection
# that's already running, you'll need to change the .api_client.host for that

# Set Default Host for NiFi
nifi_config.host = 'http://localhost:8080/nifi-api'

# Set Default Host for NiFi-Registry
registry_config.host = 'http://localhost:18080/nifi-registry-api'

# Task wait delays
# Set how fast to recheck for completion of a long running task in seconds
retry_delay = 1
# Set the max amount of time we will wait for a task to complete in seconds
retry_max_wait = 3


registered_filters = {
    'Bucket': {'id': ['identifier'], 'name': ['name']},
    'VersionedFlow': {'id': ['identifier'], 'name': ['name']},
    'RegistryClientEntity': {'id': ['id'], 'name': ['component', 'name']},
    'ProcessGroupEntity': {'id': ['id'], 'name': ['status', 'name']},
    'DocumentedTypeDTO': {'bundle': ['bundle', 'artifact'],
                          'name': ['type'],
                          'tag': ['tags']},  # This is Processor Types
    'ProcessorEntity': {'id': ['id'], 'name': ['status', 'name']},
}
