"""
A set of defaults and parameters used elsewhere in the project.
Also provides a handy link to the low-level client SDK configuration singleton
objects.

Notes for NiFi/Registry 2.x:

- Prefer configuring TLS on the configuration objects directly:

  - nifi_config.ssl_ca_cert, nifi_config.cert_file, nifi_config.key_file
  - registry_config.ssl_ca_cert, registry_config.cert_file, registry_config.key_file

- Then connect via utils.set_endpoint(url, ssl=True, login=True|False)

  - For mTLS, pass login=False and rely on the configured client cert/key
- Supported environment toggles for tests and convenience:
  - REQUESTS_CA_BUNDLE (CA bundle)
  - NIPYAPI_VERIFY_SSL (0/1) and NIPYAPI_CHECK_HOSTNAME (0/1)

For a step-by-step guide on configuring NiFi/Registry authentication
(single-user, LDAP, mTLS, OIDC),
see the project documentation: docs/profiles.rst and docs/security.rst or the online guide at
https://nipyapi.readthedocs.io/en/latest/profiles.html

Deprecated (kept for backward compatibility; prefer explicit configuration):
- NIFI_CA_CERT / NIFI_CLIENT_CERT / NIFI_CLIENT_KEY
- REGISTRY_CA_CERT / REGISTRY_CLIENT_CERT / REGISTRY_CLIENT_KEY
- Demo/test credentials (default_nifi_username/password, default_registry_username/password)
"""

import os
import warnings
from nipyapi.nifi import configuration as nifi_config
from nipyapi.registry import configuration as registry_config


# --- Default Host URLs -----
# Note that changing the default hosts below will not
# affect an API connection that's already running.
# You'll need to change the .api_client.host for that, and there is a
# convenience function for this in nipyapi.utils.set_endpoint

# Set Default Host for NiFi
default_host = "localhost"  # Default to localhost for release
#
nifi_config.host = os.getenv(
    "NIFI_API_ENDPOINT", "https://" + default_host + ":9443/nifi-api"
)
# Set Default Host for NiFi-Registry (default secure in 2.x single/ldap profiles use
# 18444/18445; single-user registry is http 18080)
registry_config.host = os.getenv(
    "REGISTRY_API_ENDPOINT", "http://" + default_host + ":18080/nifi-registry-api"
)

# ---  Project Root ------
# Is is helpful to have a reference to the root directory of the project
PROJECT_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


# --- Profiles Configuration ------
# Default path to profiles file (can be overridden programmatically or via environment)
default_profiles_file = 'examples/profiles.yml'


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
    'FlowRegistryClientEntity': {'id': ['id'], 'name': ['component', 'name']},
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
    'ParameterContextEntity': {'id': ['id'], 'name': ['component', 'name']},
    'ReportingTaskEntity': {'id': ['id'], 'name': ['component', 'name']}
}


# --- Simple Cache
# This is a simple session-wide insecure cache for certain slow calls to speed
# up subsequent requests. It is very stupid, so do not expect session handling,
# or on-demand refresh if not handled by the function itself
cache = {}


# --- SSL Configuration Values ---

# Read environment variables and set intelligent defaults
_verify_env = os.getenv("NIPYAPI_VERIFY_SSL")
_host_env = os.getenv("NIPYAPI_CHECK_HOSTNAME")

# Global SSL settings based on environment (defaults: verify=True, check_hostname=True)
global_ssl_verify = True if _verify_env is None else _verify_env.lower() not in ("0", "false", "no")
global_ssl_host_check = True if _host_env is None else _host_env.lower() not in ("0", "false", "no")
disable_insecure_request_warnings = False

# Set default values for individual service configs (no application logic)
nifi_config.verify_ssl = global_ssl_verify
registry_config.verify_ssl = global_ssl_verify

# Note: SSL contexts and warnings are NOT automatically applied at import.
# Call nipyapi.security.apply_ssl_configuration() to apply current settings.

# --- Environment Variable Certificate Setup ---

# Back-compat TLS envs (DEPRECATED): prefer REQUESTS_CA_BUNDLE or direct config
_nifi_ca = os.getenv("NIFI_CA_CERT")
if _nifi_ca is not None:
    warnings.warn(
        "NIFI_CA_CERT / NIFI_CLIENT_CERT / NIFI_CLIENT_KEY are deprecated; "
        "set configuration.ssl_ca_cert/cert_file/key_file explicitly or use REQUESTS_CA_BUNDLE",
        DeprecationWarning,
        stacklevel=2,
    )
    nifi_config.ssl_ca_cert = _nifi_ca
    nifi_config.cert_file = os.getenv("NIFI_CLIENT_CERT")
    nifi_config.key_file = os.getenv("NIFI_CLIENT_KEY")

# Optional: registry-specific CA envs
_reg_ca = os.getenv("REGISTRY_CA_CERT")
if _reg_ca is not None:
    warnings.warn(
        "REGISTRY_CA_CERT / REGISTRY_CLIENT_CERT / REGISTRY_CLIENT_KEY are deprecated; "
        "set configuration.ssl_ca_cert/cert_file/key_file explicitly or use REQUESTS_CA_BUNDLE",
        DeprecationWarning,
        stacklevel=2,
    )
    registry_config.ssl_ca_cert = _reg_ca
    registry_config.cert_file = os.getenv("REGISTRY_CLIENT_CERT")
    registry_config.key_file = os.getenv("REGISTRY_CLIENT_KEY")

# Fallback: shared TLS CA for both services (e.g., local test CA)
_shared_ca = os.getenv("TLS_CA_CERT_PATH") or os.getenv("REQUESTS_CA_BUNDLE")
if _shared_ca:
    # Only set if not already configured from deprecated variables above
    if not nifi_config.ssl_ca_cert and not registry_config.ssl_ca_cert:
        nifi_config.ssl_ca_cert = _shared_ca
        registry_config.ssl_ca_cert = _shared_ca
        # Enable SSL verification when CA is provided via environment
        global_ssl_verify = True
        nifi_config.verify_ssl = True
        registry_config.verify_ssl = True


# --- Encoding
# URL Encoding bypass characters will not be encoded during submission
default_safe_chars = ""

# Default String Encoding
default_string_encoding = "utf8"
