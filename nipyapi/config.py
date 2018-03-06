# coding: utf-8

"""
A set of defaults and parameters used elsewhere in the project.
Also provides a handy link to the low-level client SDK configuration singleton
objects.
"""

from __future__ import absolute_import
import logging
import os
from nipyapi.nifi import configuration as nifi_config
from nipyapi.registry import configuration as registry_config


# --- Logging ------
logging.basicConfig(level=logging.WARNING)


# --- Default Host URLs -----
# Note that changing the default hosts below will not
# affect an API connection that's already running.
# You'll need to change the .api_client.host for that, and there is a
# convenience function for this in nipyapi.utils

# Set Default Host for NiFi
nifi_config.host = 'http://localhost:8080/nifi-api'
# Set Default Host for NiFi-Registry
registry_config.host = 'http://localhost:18080/nifi-registry-api'


# ---  Project Root ------
# Is is helpful to have a reference to the root directory of the project
PROJECT_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


# --- Task wait delays ------
# Set how fast to recheck for completion of a short running task in seconds
short_retry_delay = 0.5
# Set the max amount of time we will wait for a short running task to complete
# in seconds
short_max_wait = 3
# Long running task delay
long_retry_delay = 5
# and long max wait
long_max_wait = 120


# --- Object Filters ------
# This sets the mappings of where in the native datatype objects to find
# particularly useful fields, like UUID or NAME.
# This saves hunting them down all the damn time.
# The format is the string to be used in the identifier_type field, followed by
# a list of which parameters form a tree to that field.
# Note that 'id' is used for UUID by convention, but should not be confused
# with 'identity' in security contexts.
registered_filters = {
    'Bucket': {'id': ['identifier'], 'name': ['name']},
    'VersionedFlow': {'id': ['identifier'], 'name': ['name']},
    'RegistryClientEntity': {'id': ['id'], 'name': ['component', 'name']},
    'ProcessGroupEntity': {'id': ['id'], 'name': ['status', 'name']},
    'DocumentedTypeDTO': {'bundle': ['bundle', 'artifact'],
                          'name': ['type'],
                          'tag': ['tags']},  # This is Processor Types
    'ProcessorEntity': {'id': ['id'], 'name': ['status', 'name']},
    'User': {'identity': ['identity'], 'id': ['identifier']},  # Registry User
    'UserEntity': {'identity': ['component', 'identity'], 'id': ['id']},
    'TemplateEntity': {'id': ['id'], 'name': ['template', 'name']}
}


# --- Version Checking
# Method to check if we're compatible with the API endpoint
# NOT YET IMPLEMENTED
# If None, then no check has been done
# If True, then we have tested and there are no issues
# If False, then we believe we are incompatible
nifi_config.version_check = None
registry_config.version_check = None
