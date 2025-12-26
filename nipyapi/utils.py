"""
Convenience utility functions for NiPyApi, not really intended for external use
"""

import base64
import io
import json
import logging
import operator
import os
import re
import time
from contextlib import contextmanager
from copy import copy
from functools import reduce, wraps
from typing import Optional

import requests
import yaml
from packaging import version
from requests.models import Response

import nipyapi
from nipyapi.config import default_string_encoding as DEF_ENCODING

__all__ = [
    "dump",
    "load",
    "fs_read",
    "fs_write",
    "filter_obj",
    "is_uuid",
    "wait_to_complete",
    "is_endpoint_up",
    "set_endpoint",
    "infer_object_label_from_class",
    "bypass_slash_encoding",
    "exception_handler",
    "enforce_min_ver",
    "check_version",
    "validate_parameters_versioning_support",
    "extract_oidc_user_identity",
    "getenv",
    "getenv_bool",
    "resolve_relative_paths",
]

log = logging.getLogger(__name__)
DOCKER_AVAILABLE = False  # Docker management removed in 1.x (NiFi 2.x)

# UUID pattern: 8-4-4-4-12 hexadecimal characters
_UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)


def is_uuid(value):
    """
    Check if a string looks like a UUID.

    Args:
        value (str): The string to check

    Returns:
        bool: True if the string matches UUID format (8-4-4-4-12 hex pattern)
    """
    if not isinstance(value, str):
        return False
    return bool(_UUID_PATTERN.match(value))


def dump(obj, mode="json"):
    """
    Dumps a native datatype object or swagger entity to json or yaml
        defaults to json

    Args:
        obj (varies): The native datatype object or swagger type to serialise
        mode (str): 'json' or 'yaml', the supported export modes

    Returns (str): The serialised object

    """
    assert mode in ["json", "yaml"]
    api_client = nipyapi.nifi.ApiClient()
    prepared_obj = api_client.sanitize_for_serialization(obj)
    if mode == "json":
        try:
            return json.dumps(obj=prepared_obj, sort_keys=True, indent=4)
        except TypeError as e:
            raise e
    if mode == "yaml":
        # Use 'safe' dumping to prevent arbitrary code execution
        # Force block style to avoid inline flow mappings that can break parsing
        return yaml.safe_dump(prepared_obj, default_flow_style=False, sort_keys=True, indent=4)
    raise ValueError("Invalid dump Mode specified {0}".format(mode))


def load(obj, dto=None):
    """
    Loads a serialised object back into native datatypes, and optionally
    imports it back into the native NiFi DTO

    Warning: Using this on objects not produced by this Package may have
    unintended results! While efforts have been made to ensure that unsafe
    loading is not possible, no stringent security testing has been completed.

    Args:
        obj (dict, list): The serialised object to import
        dto (Optional [tuple{str, str}]): A Tuple describing the service and
        object that should be constructed.

        e.g. dto = ('registry', 'VersionedFlowSnapshot')

    Returns: Either the loaded object in native Python datatypes, or the
        constructed native datatype object

    """
    assert isinstance(obj, (str, bytes))
    assert dto is None or isinstance(dto, tuple)
    # Use safe_load to prevent arbitrary code execution
    loaded_obj = yaml.safe_load(obj)
    if dto:
        assert dto[0] in ["nifi", "registry"]
        assert isinstance(dto[1], str)
        obj_as_json = dump(loaded_obj)
        response = Response()
        response.data = obj_as_json
        if "nifi" in dto[0]:
            return nipyapi.config.nifi_config.api_client.deserialize(
                response=response, response_type=dto[1]
            )
        return nipyapi.config.registry_config.api_client.deserialize(
            response=response, response_type=dto[1]
        )
    return loaded_obj


def fs_write(obj, file_path):
    """
    Convenience function to write an Object to a FilePath

    Args:
        obj (varies): The Object to write out
        file_path (str): The Full path including filename to write to

    Returns: The object that was written
    """
    try:
        with io.open(str(file_path), "w", encoding=DEF_ENCODING) as f:
            if isinstance(obj, bytes):
                obj_str = obj.decode(DEF_ENCODING)
            else:
                obj_str = obj
            f.write(obj_str)
        return obj
    except TypeError as e:
        raise e


def fs_read(file_path):
    """
    Convenience function to read an Object from a FilePath

    Args:
        file_path (str): The Full path including filename to read from

    Returns: The object that was read
    """
    try:
        with io.open(str(file_path), "r", encoding=DEF_ENCODING) as f:
            return f.read()
    except IOError as e:
        raise e


def filter_obj(obj, value, key, greedy=True):
    """
    Implements a custom filter method because native datatypes don't have
    consistently named or located fields.

    Note that each object used by this function must be registered with
    identifier_types and identifiers in config

    Args:
        obj (varies): the NiFi or NiFi-Registry object to filter on
        value (str): the String value to look for
        key (str): the object key to filter against
        greedy (bool): If True, the value will be matched anywhere in the
            string, if False it will require exact match

    Returns: None if 0 matches, list if > 1, single Object entity if ==1

    """
    # Using the object class name as a lookup as they are unique within the
    # NiFi DTOs
    if isinstance(obj, list) and not obj:
        return None
    try:
        obj_class_name = obj[0].__class__.__name__
    except (TypeError, IndexError) as e:
        raise TypeError(
            "The passed object {0} is not a filterable nipyapi object".format(
                obj.__class__.__name__
            )
        ) from e
    # Check if this class has a registered filter in Nipyapi.config
    this_filter = nipyapi.config.registered_filters.get(obj_class_name, False)
    if not this_filter:
        registered_filters = " ".join(nipyapi.config.registered_filters.keys())
        raise ValueError(
            "{0} is not a registered NiPyApi filterable class, registered "
            "classes are {1}".format(obj_class_name, registered_filters)
        )
    # Check if the supplied key is part of the registered filter
    key_lookup = nipyapi.config.registered_filters[obj_class_name].get(key, False)
    if not key_lookup:
        valid_keys = " ".join(nipyapi.config.registered_filters[obj_class_name].keys())
        raise ValueError(
            "{0} is not a registered filter method for object {1}, valid "
            "methods are {2}".format(key, obj_class_name, valid_keys)
        )
    # List comprehension using reduce to unpack the list of keys in the filter
    if greedy:
        out = [i for i in obj if value in reduce(operator.getitem, key_lookup, i.to_dict())]
    else:
        out = [i for i in obj if value == reduce(operator.getitem, key_lookup, i.to_dict())]
    # Manage our return contract
    if not out:
        return None
    if len(out) > 1:
        return out
    return out[0]


def wait_to_complete(test_function, *args, **kwargs):
    """
    Implements a basic return loop for a given function which is capable of a
    True|False output

    Args:
        test_function: Function which returns a bool once the target
            state is reached
        delay (int): The number of seconds between each attempt, defaults to
            config.short_retry_delay
        max_wait (int): the maximum number of seconds before issuing a Timeout,
            defaults to config.short_max_wait
        *args: Any args to pass through to the test function
        **kwargs: Any Keword Args to pass through to the test function

    Returns (bool): True for success, False for not

    """
    log.info("Called wait_to_complete for function %s", test_function.__name__)
    delay = kwargs.pop("nipyapi_delay", nipyapi.config.short_retry_delay)
    max_wait = kwargs.pop("nipyapi_max_wait", nipyapi.config.short_max_wait)
    timeout = time.time() + max_wait
    while time.time() < timeout:
        log.debug("Calling test_function")
        test_result = test_function(*args, **kwargs)
        log.debug("Checking result")
        if test_result:
            log.info("Function output evaluated to True, returning output")
            return test_result
        log.info("Function output evaluated to False, sleeping...")
        time.sleep(delay)
    log.info("Hit Timeout, raising TimeOut Error")
    raise ValueError("Timed Out waiting for {0} to complete".format(test_function.__name__))


def is_endpoint_up(endpoint_url):  # pylint: disable=too-many-return-statements
    """
    Tests if a URL is available for requests

    A service is considered "up" if it responds with:
    - Success codes (200-399)
    - Authentication required codes (401, 403) - service is ready for auth
    - SSL certificate verification errors - service up but cert issues

    SSL handshake failures (UNEXPECTED_EOF, etc.) indicate service not ready.

    Args:
        endpoint_url (str): The URL to test

    Returns (bool): True if service is ready for requests, False if not

    """
    log.info("Called is_endpoint_up with args %s", locals())
    try:
        response = requests.get(endpoint_url, timeout=nipyapi.config.short_max_wait)
        if response.status_code:
            # Service ready: success codes or auth required
            if (200 <= response.status_code < 400) or response.status_code in (401, 403):
                log.info("Got status %s from endpoint, service ready", response.status_code)
                return True
            log.info("Got status code %s from endpoint, service not ready", response.status_code)
        return False
    except (
        requests.ConnectionError,
        requests.exceptions.SSLError,
        requests.exceptions.ReadTimeout,
    ) as e:
        log.info("Got Error of type %s with details %s", type(e), str(e))
        if "SSLError" in str(type(e)):
            error_str = str(e)
            # Only treat specific SSL errors as "service ready"
            if any(
                indicator in error_str
                for indicator in [
                    "CERTIFICATE_VERIFY_FAILED",
                    "WRONG_VERSION_NUMBER",
                    "certificate verify failed",
                ]
            ):
                log.info("Got SSL cert error, service up but certificate issues")
                return True
            log.info("Got SSL handshake error, service not ready yet")
            return False
        if "ReadTimeout" in str(type(e)):
            # Check if this is an SSL handshake timeout
            error_str = str(e)
            if "handshake" in error_str.lower() or "ssl" in error_str.lower():
                log.info("Got SSL handshake timeout, service not ready yet")
                return False
            log.info("Got read timeout, service not ready")
            return False
        log.info("Got ConnectionError, service not ready")
        return False


def set_endpoint(endpoint_url, ssl=False, login=False, username=None, password=None):
    """Sets the endpoint when switching between instances of NiFi or other projects.

    Args:
        endpoint_url (str): The URL to set as the endpoint
        ssl (bool): Whether to use SSL context for HTTPS connections
        login (bool): Whether to attempt token-based login
        username (str): The username to use for login
        password (str): The password to use for login

    Returns (bool): True for success
    """
    log.info("Called set_endpoint with args %s", locals())

    if "nifi-api" in endpoint_url:
        configuration = nipyapi.config.nifi_config
        service = "nifi"
    elif "registry-api" in endpoint_url:
        configuration = nipyapi.config.registry_config
        service = "registry"
    else:
        raise ValueError("Endpoint not recognised")

    log.info("Setting %s endpoint to %s", service, endpoint_url)
    if configuration.api_client:
        nipyapi.security.service_logout(service)
        configuration.api_client = None

    # remove any trailing slash to avoid hard to spot errors
    configuration.host = endpoint_url.rstrip("/")

    # Handle authentication - maintain backwards compatibility with ssl parameter
    if ssl and login and "https://" in endpoint_url:
        # Original behavior: only login when ssl=True, login=True, AND HTTPS URL
        # Registry HTTP doesn't require authentication, only HTTPS does
        nipyapi.security.service_login(service, username=username, password=password)
    elif login and not endpoint_url.startswith("https://"):
        # Warn about insecure login attempts over HTTP
        log.warning(
            "Login requested for HTTP URL %s. Consider using HTTPS for secure authentication.",
            endpoint_url,
        )

    # One-time supported-version enforcement
    try:
        enforce_min_ver("2", service=service)
    except Exception as e:  # pylint: disable=broad-except
        log.debug("Version check skipped or failed for %s: %s", service, e)
    return True


# pylint: disable=R0913,R0902,R0917,R0903
class DockerContainer:  # pragma: no cover
    """Removed in 1.x (NiFi 2.x). Use Docker Compose or external tooling.

    This class is kept as a stub to raise a clear error for callers
    who still import it. It will be removed in a future release.
    """

    def __init__(self, *args, **kwargs):
        raise RuntimeError(
            "DockerContainer has been removed. Use Docker Compose or external tooling."
        )


# pylint: disable=W0703,R1718
def start_docker_containers(*args, **kwargs):  # pragma: no cover
    """
    Removed in 1.x (NiFi 2.x). Use Docker Compose or external tooling.

    This function is kept as a stub to raise a clear error for callers
    who still import it. It will be removed in a future release.
    """
    raise RuntimeError(
        "start_docker_containers has been removed. Use Docker Compose or external tooling."
    )


class VersionError(Exception):
    """Error raised when a feature is not supported in the current version"""


def check_version(base, comparator=None, service="nifi", default_version="2.0.0"):
    """
    Compares version base against either version comparator, or the version
    of the currently connected service instance.

    Since NiFi is java, it may return a version with -SNAPSHOT as part of it.
    As such, that will be stripped from either the comparator version or
    the version returned from NiFi

    Args:
        base (str): The base version for the comparison test
        comparator (optional[str]): The version to compare against
        default_version (optional[str]): The version to assume the service is
            if the check cannot be completed
        service (str): The service to test the version against, currently
            only supports NiFi

    Returns (int): -1/0/1 if base is lower/equal/newer than comparator

    Raises:
        VersionError: When a feature is not supported in the current version
    """

    def strip_version_string(version_string):
        # Reduces the string to only the major.minor.patch version
        return ".".join(version_string.split("-")[0].split(".")[:3])

    assert isinstance(base, str)
    assert comparator is None or isinstance(comparator, str)
    assert service in ["nifi", "registry"]
    ver_a = version.parse(strip_version_string(base))
    if comparator:
        ver_b = version.parse(strip_version_string(comparator))
    elif service == "registry":
        try:
            reg_ver = nipyapi.system.get_registry_version_info()
            ver_b = version.parse(strip_version_string(reg_ver))
        except Exception:  # pylint: disable=broad-exception-caught
            log.warning("Unable to get registry About version, assuming %s", default_version)
            ver_b = version.parse(default_version)
    else:
        nifi_ver = nipyapi.system.get_nifi_version_info()
        nifi_ver_str = getattr(nifi_ver, "ni_fi_version", nifi_ver)
        ver_b = version.parse(strip_version_string(nifi_ver_str))
    if ver_b > ver_a:
        return -1
    if ver_b < ver_a:
        return 1
    return 0


def validate_parameters_versioning_support(
    verify_nifi=True, verify_registry=True  # pylint: disable=unused-argument
):  # pylint: disable=unused-argument
    """
    Convenience method to check if Parameters are supported
    Args:
        verify_nifi (bool): If True, check NiFi meets the min version
        verify_registry (bool): If True, check Registry meets the min version
    """
    # NiFi 2.x/Registry 2.x support Parameter Contexts in versioned flows.
    # Legacy warnings for <1.10 (NiFi) or <0.6 (Registry) removed as we no
    # longer support those platform versions.
    return None


def extract_oidc_user_identity(token_data):
    """
    Extract user identity (UUID) from OIDC token response.

    This function decodes the JWT access token to extract the 'sub' (subject) field,
    which contains the user's unique identifier that NiFi uses for policy assignment.

    Args:
        token_data (dict): The full OAuth2 token response from service_login_oidc()
                          when called with return_token_info=True

    Returns:
        str: The user identity UUID from the token's 'sub' field

    Raises:
        ValueError: If the token cannot be decoded or doesn't contain expected fields
    """
    try:
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("No access_token found in token data")

        # JWT tokens have 3 parts separated by dots: header.payload.signature
        parts = access_token.split(".")
        if len(parts) < 2:
            raise ValueError("Invalid JWT token format")

        # Decode the payload (second part)
        payload = parts[1]
        # Add padding for base64 decoding if needed
        payload += "=" * (4 - len(payload) % 4)
        decoded_payload = base64.b64decode(payload)
        payload_json = json.loads(decoded_payload)

        # Extract the 'sub' (subject) field which contains the user UUID
        user_uuid = payload_json.get("sub")
        if not user_uuid:
            raise ValueError("No 'sub' field found in JWT token payload")

        return user_uuid

    except Exception as e:
        raise ValueError(f"Failed to extract user identity from OIDC token: {e}") from e


def validate_templates_version_support():
    """
    Validate that the current version of NiFi supports Templates API
    """
    enforce_max_ver("2", service="nifi", error_message="Templates are deprecated in NiFi 2.x")


def enforce_max_ver(max_version, bool_response=False, service="nifi", error_message=None):
    """
    Raises an error if target NiFi environment is at or above the max version
    """
    if check_version(max_version, service=service) == -1:
        if not bool_response:
            raise VersionError(
                error_message
                or "This function is not available " "in NiFi {} or above".format(max_version)
            )
        return True
    return False


def enforce_min_ver(min_version, bool_response=False, service="nifi"):
    """
    Raises an error if target NiFi environment is not minimum version.

    Args:
        min_version (str): Version to check against
        bool_response (bool): If True, will return True instead of raising error
        service (str): nifi or registry

    Returns:
        (bool) or (NotImplementedError)
    """
    if check_version(min_version, service=service) == 1:
        if not bool_response:
            raise VersionError(
                "This function is not available " "before NiFi version " + str(min_version)
            )
        return True
    return False


def infer_object_label_from_class(obj):
    """
    Returns the expected STRING label for an object class required by certain
        functions.

    Args:
        obj: The object to infer the name of

    Returns:
        str of the relevant name, or raises an AssertionError

    """
    if isinstance(obj, nipyapi.nifi.ProcessorEntity):
        return "PROCESSOR"
    if isinstance(obj, nipyapi.nifi.FunnelEntity):
        return "FUNNEL"
    if isinstance(obj, nipyapi.nifi.PortEntity):
        return obj.port_type
    if isinstance(obj, nipyapi.nifi.RemoteProcessGroupDTO):
        return "REMOTEPROCESSGROUP"
    if isinstance(obj, nipyapi.nifi.RemoteProcessGroupPortDTO):
        # get RPG summary, find id of obj in input or output list
        parent_rpg = nipyapi.canvas.get_remote_process_group(obj.group_id, True)
        if obj.id in [x.id for x in parent_rpg["input_ports"]]:
            return "REMOTE_INPUT_PORT"
        if obj.id in [x.id for x in parent_rpg["output_ports"]]:
            return "REMOTE_OUTPUT_PORT"
        raise ValueError("Remote Port not present as expected in RPG")
    raise AssertionError("Object Class not recognised for this function")


def bypass_slash_encoding(service, bypass):
    """
    Instructs the API Client to bypass encoding the '/' character

    Args:
        service (str): 'nifi' or 'registry'
        bypass (bool): True will not encode '/' in fields via API calls

    Returns:
        None

    """
    assert service in ["nifi", "registry"]
    assert isinstance(bypass, bool)
    current_config = getattr(nipyapi, service).configuration
    if bypass:
        if "/" not in current_config.safe_chars_for_path_param:
            current_config.safe_chars_for_path_param += "/"
    else:
        current_config.safe_chars_for_path_param = copy(nipyapi.config.default_safe_chars)


@contextmanager
def rest_exceptions():
    """Simple exception wrapper for Rest Exceptions"""
    try:
        yield
    except (nipyapi.nifi.rest.ApiException, nipyapi.registry.rest.ApiException) as e:
        raise ValueError(e.body) from e


def exception_handler(status_code=None, response=None):
    """Simple Function wrapper to handle HTTP Status Exceptions"""

    def func_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except (nipyapi.nifi.rest.ApiException, nipyapi.registry.rest.ApiException) as e:
                if status_code is not None and e.status == int(status_code):
                    return response
                raise ValueError(e.body) from e

        return wrapper

    return func_wrapper


def resolve_relative_paths(file_path, root_path=None):
    """
    Convert a relative path to absolute, leave absolute paths unchanged.

    Essential for SSL/TLS certificate configuration where libraries typically
    require absolute paths to avoid ambiguity about file locations.

    Args:
        file_path (str or None): File path to resolve
        root_path (str, optional): Root directory for relative path resolution.
                                  Defaults to PROJECT_ROOT_DIR if not specified.

    Returns:
        str or None: Absolute path if input was a relative path string,
                    unchanged if input was absolute path or None.

    Example:
        >>> resolve_relative_paths('certs/ca.pem', '/project')
        '/project/certs/ca.pem'
        >>> resolve_relative_paths('/etc/ssl/ca.pem')
        '/etc/ssl/ca.pem'
        >>> resolve_relative_paths(None)
        None
    """

    if file_path is None or not isinstance(file_path, str) or not file_path.strip():
        return file_path

    if os.path.isabs(file_path):
        return file_path

    # Use provided root or default to package root directory
    effective_root = root_path or os.path.dirname(nipyapi.config.PROJECT_ROOT_DIR)
    return os.path.join(effective_root, file_path)


def getenv(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Enhanced environment variable getter with None handling.

    Args:
        name (str): Environment variable name
        default (Optional[str]): Default value if variable not set

    Returns:
        Optional[str]: Environment variable value or default
    """
    val = os.getenv(name)
    return val if val is not None else default


def getenv_bool(name: str, default: Optional[bool] = None) -> Optional[bool]:
    """
    Parse environment variable as boolean using JSON-style interpretation.

    Handles common boolean environment variable patterns and uses json.loads()
    for the standard 'true'/'false' cases that most programmers understand.

    Args:
        name (str): Environment variable name
        default (Optional[bool]): Default value if variable not set

    Returns:
        Optional[bool]: Boolean value or default if not set

    Example:
        >>> os.environ['MY_FLAG'] = '0'
        >>> getenv_bool('MY_FLAG')  # False
        >>> os.environ['MY_FLAG'] = 'true'
        >>> getenv_bool('MY_FLAG')  # True
        >>> getenv_bool('UNSET_FLAG', False)  # False
    """
    val = os.getenv(name)
    if val is None:
        return default

    # Clean and normalize the value
    val_clean = val.strip().lower()

    # Handle JSON-style booleans directly
    if val_clean in ("true", "false"):
        return json.loads(val_clean)

    # Handle common falsy patterns
    if val_clean in ("0", "no", "off", "n", ""):
        return False

    # Everything else is truthy (including '1', 'yes', 'on', 'y', etc.)
    return True
