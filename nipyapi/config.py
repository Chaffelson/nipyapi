# coding: utf-8

"""
A set of defaults and parameters used elsewhere in the project.
Also provides a handy link to the low-level client SDK configuration singleton
objects.
"""

from __future__ import absolute_import
import logging
import os
import ssl
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
                          'tag': ['tags']},
    'ProcessorEntity': {'id': ['id'], 'name': ['status', 'name']},
    'User': {'identity': ['identity'], 'id': ['identifier']},
    'UserGroupEntity': {'identity': ['component', 'identity'], 'id': ['id']},
    'UserGroup': {'identity': ['identity'], 'id': ['identifier']},
    'UserEntity': {'identity': ['component', 'identity'], 'id': ['id']},
    'TemplateEntity': {'id': ['id'], 'name': ['template', 'name']},
    'ControllerServiceEntity': {'id': ['id'], 'name': ['component', 'name']},
    'ParameterContextEntity': {'id': ['id'], 'name': ['component', 'name']}
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

# Auth handling
# If set, NiPyAPI will always include the Basic Authorization header
global_force_basic_auth = False
nifi_config.username = default_nifi_username
nifi_config.password = default_nifi_password
nifi_config.force_basic_auth = global_force_basic_auth
registry_config.username = default_registry_username
registry_config.password = default_registry_password
registry_config.force_basic_auth = global_force_basic_auth

# Set SSL Handling
# When operating with self signed certs, your log can fill up with
# unnecessary warnings
# Set to True by default, change to false if necessary
global_ssl_verify = True

nifi_config.verify_ssl = global_ssl_verify
registry_config.verify_ssl = global_ssl_verify
if not global_ssl_verify:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Enforce no host checking when SSL context is disabled
global_ssl_host_check = False
if not global_ssl_host_check:
    nifi_config.ssl_context = ssl.create_default_context()
    nifi_config.ssl_context.check_hostname = False
    nifi_config.ssl_context.verify_mode = ssl.CERT_NONE

    registry_config.ssl_context = ssl.create_default_context()
    registry_config.ssl_context.check_hostname = False
    registry_config.ssl_context.verify_mode = ssl.CERT_NONE

if os.getenv('NIFI_CA_CERT') is not None:
    nifi_config.ssl_ca_cert = os.getenv('NIFI_CA_CERT')
    nifi_config.cert_file = os.getenv('NIFI_CLIENT_CERT')
    nifi_config.key_file = os.getenv('NIFI_CLIENT_KEY')

# --- Encoding
# URL Encoding bypass characters will not be encoded during submission
default_safe_chars = ''

# Default String Encoding
default_string_encoding = 'utf8'
