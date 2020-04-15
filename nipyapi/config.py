# coding: utf-8

"""
A set of defaults and parameters used elsewhere in the project.
Also provides a handy link to the low-level client SDK configuration singleton
objects.
"""

from __future__ import absolute_import
import logging
import os
import urllib3
from nipyapi.nifi import configuration as nifi_config
from nipyapi.registry import configuration as registry_config


# --- Logging ------
logging.basicConfig(level=logging.WARNING)


# --- Default Host URLs -----
# Note that changing the default hosts below will not
# affect an API connection that's already running.
# You'll need to change the .api_client.host for that, and there is a
# convenience function for this in nipyapi.utils.set_endpoint

# Set Default Host for NiFi
default_host = 'localhost'  # Default to localhost for release
#
nifi_config.host = os.getenv(
    'NIFI_API_ENDPOINT',
    'http://' + default_host + ':8080/nifi-api'
)
# Set Default Host for NiFi-Registry
registry_config.host = 'http://' + default_host + ':18080/nifi-registry-api'


# Set Default Auth Types
# Set list to the Auth type you want to use
# Currently basicAuth trumps tokenAuth if both are enabled
default_auth = ['tokenAuth']
# NiFi valid options: ['tokenAuth', 'basicAuth']
# Registry valid options: ['tokenAuth', 'basicAuth', 'Authorization']
nifi_config.enabled_auth = default_auth  # tokenAuth was default before 0.14.2


# Set SSL Handling
# When operating with self signed certs, your log can fill up with
# unnecessary warnings
# Set to True by default, change to false if necessary
global_ssl_verify = True

nifi_config.verify_ssl = global_ssl_verify
registry_config.verify_ssl = global_ssl_verify
if not global_ssl_verify:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if os.getenv('NIFI_CA_CERT') is not None:
    nifi_config.ssl_ca_cert = os.getenv('NIFI_CA_CERT')
    nifi_config.cert_file = os.getenv('NIFI_CLIENT_CERT')
    nifi_config.key_file = os.getenv('NIFI_CLIENT_KEY')

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
    'User': {'identity': ['identity'], 'id': ['identifier']},
    'UserGroupEntity': {'identity': ['component', 'identity'], 'id': ['id']},
    'UserGroup': {'identity': ['identity'], 'id': ['identifier']},
    'UserEntity': {'identity': ['component', 'identity'], 'id': ['id']},
    'TemplateEntity': {'id': ['id'], 'name': ['template', 'name']},
    'ControllerServiceEntity': {'is': ['id'], 'name': ['component', 'name']}
}


# --- Version Checking
# Method to check if we're compatible with the API endpoint
# NOT YET IMPLEMENTED
# If None, then no check has been done
# If True, then we have tested and there are no issues
# If False, then we believe we are incompatible
nifi_config.version_check = None
registry_config.version_check = None


# --- Simple Cache
# This is a simple session-wide insecure cache for certain slow calls to speed
# up subsequent requests. It is very stupid, so do not expect session handling,
# or on-demand refresh if not handled by the function itself
cache = {}


# --- Security Context
# This allows easy reference to a set of certificates for use in automation
# By default it points to our demo certs, change it for your environment
default_certs_path = os.path.join(PROJECT_ROOT_DIR, 'demo/keys')
default_ssl_context = {
    'ca_file': os.path.join(default_certs_path, 'localhost-ts.pem'),
    'client_cert_file': os.path.join(default_certs_path, 'client-cert.pem'),
    'client_key_file': os.path.join(default_certs_path, 'client-key.pem'),
    'client_key_password': 'clientPassword'
}
# Identities and passwords to be used for service login if called for
default_nifi_username = 'nobel'
default_nifi_password = 'password'
default_registry_username = 'nobel'
default_registry_password = 'password'
# Identity to be used in the Registry Client Proxy setup
# If called for during policy setup, particularly bootstrap_policies
default_proxy_user = 'CN=localhost, OU=nifi'


# URL Encoding bypass characters will not be encoded during submission
default_safe_chars = ''
