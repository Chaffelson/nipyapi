"""
A set of defaults and parameters used elsewhere in the project.
Also provides a handy link to the low-level client SDK configuration singleton
objects.
"""

import os

from nipyapi.nifi import configuration as nifi_config
from nipyapi.registry import configuration as registry_config

# --- Default Host URLs -----
# Note that changing the default hosts below will not
# affect an API connection that's already running.
# You should use nipyapi.profiles.switch to set the profile you want to use.

# Set Default Host for NiFi
default_host = "localhost"  # Default to localhost for release
#
nifi_config.host = os.getenv("NIFI_API_ENDPOINT", "https://" + default_host + ":9443/nifi-api")
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
default_profiles_file = "examples/profiles.yml"


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
    "Bucket": {"id": ["identifier"], "name": ["name"]},
    "VersionedFlow": {"id": ["identifier"], "name": ["name"]},
    "FlowRegistryClientEntity": {"id": ["id"], "name": ["component", "name"]},
    "ProcessGroupEntity": {"id": ["id"], "name": ["status", "name"]},
    "DocumentedTypeDTO": {"bundle": ["bundle", "artifact"], "name": ["type"], "tag": ["tags"]},
    "ProcessorEntity": {"id": ["id"], "name": ["status", "name"]},
    "User": {"identity": ["identity"], "id": ["identifier"]},
    "UserGroupEntity": {"identity": ["component", "identity"], "id": ["id"]},
    "UserGroup": {"identity": ["identity"], "id": ["identifier"]},
    "UserEntity": {"identity": ["component", "identity"], "id": ["id"]},
    "TemplateEntity": {"id": ["id"], "name": ["template", "name"]},
    "ControllerServiceEntity": {"id": ["id"], "name": ["component", "name"]},
    "ParameterContextEntity": {"id": ["id"], "name": ["component", "name"]},
    "ReportingTaskEntity": {"id": ["id"], "name": ["component", "name"]},
}


# --- Simple Cache
# This is a simple session-wide insecure cache for certain slow calls to speed
# up subsequent requests. It is very stupid, so do not expect session handling,
# or on-demand refresh if not handled by the function itself
cache = {}


# --- Environment Variable Certificate Setup ---

# Shared TLS CA for both services (e.g., local test CA)
_shared_ca = os.getenv("TLS_CA_CERT_PATH") or os.getenv("REQUESTS_CA_BUNDLE")
if _shared_ca:
    nifi_config.ssl_ca_cert = _shared_ca
    registry_config.ssl_ca_cert = _shared_ca
    # Enable default SSL verification when CA is provided via environment
    nifi_config.verify_ssl = True
    registry_config.verify_ssl = True


# --- Encoding
# URL Encoding bypass characters will not be encoded during submission
default_safe_chars = ""

# Default String Encoding
default_string_encoding = "utf8"
