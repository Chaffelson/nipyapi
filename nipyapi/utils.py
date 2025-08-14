"""
Convenience utility functions for NiPyApi, not really intended for external use
"""

import logging
import os
import json
import io
import time
from copy import copy
from functools import reduce, wraps
import operator
from contextlib import contextmanager
from packaging import version
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
import requests
from requests.models import Response
import nipyapi
from nipyapi.config import default_string_encoding as DEF_ENCODING

__all__ = ['dump', 'load', 'fs_read', 'fs_write', 'filter_obj',
           'wait_to_complete', 'is_endpoint_up', 'set_endpoint',
           'start_docker_containers', 'DockerContainer',
           'infer_object_label_from_class', 'bypass_slash_encoding',
           'exception_handler', 'enforce_min_ver', 'check_version',
           'validate_parameters_versioning_support'
           ]

log = logging.getLogger(__name__)

try:
    import docker
    from docker.errors import ImageNotFound
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False
 



def dump(obj, mode='json'):
    """
    Dumps a native datatype object or swagger entity to json or yaml
        defaults to json

    Args:
        obj (varies): The native datatype object or swagger type to serialise
        mode (str): 'json' or 'yaml', the supported export modes

    Returns (str): The serialised object

    """
    assert mode in ['json', 'yaml']
    api_client = nipyapi.nifi.ApiClient()
    prepared_obj = api_client.sanitize_for_serialization(obj)
    if mode == 'json':
        try:
            return json.dumps(
                obj=prepared_obj,
                sort_keys=True,
                indent=4
            )
        except TypeError as e:
            raise e
    if mode == 'yaml':
        # Use 'safe' loading to prevent arbitrary code execution
        yaml = YAML(typ='safe', pure=True)
        # Force block style to avoid inline flow mappings that can break parsing
        yaml.default_flow_style = False
        # Create a StringIO object to act as the stream
        stream = StringIO()
        # Dump to the StringIO stream
        yaml.dump(prepared_obj, stream)
        # Return the contents of the stream as a string
        return stream.getvalue()
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
    yaml = YAML(typ='safe', pure=True)
    loaded_obj = yaml.load(obj)
    if dto:
        assert dto[0] in ['nifi', 'registry']
        assert isinstance(dto[1], str)
        obj_as_json = dump(loaded_obj)
        response = Response()
        response.data = obj_as_json
        if 'nifi' in dto[0]:
            return nipyapi.config.nifi_config.api_client.deserialize(
                response=response,
                response_type=dto[1]
            )
        return nipyapi.config.registry_config.api_client.deserialize(
            response=response,
            response_type=dto[1]
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
        with io.open(str(file_path), 'w', encoding=DEF_ENCODING) as f:
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
        with io.open(str(file_path), 'r', encoding=DEF_ENCODING) as f:
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
            "The passed object {0} is not a filterable nipyapi object"
            .format(obj.__class__.__name__)) from e
    # Check if this class has a registered filter in Nipyapi.config
    this_filter = nipyapi.config.registered_filters.get(obj_class_name, False)
    if not this_filter:
        registered_filters = ' '.join(nipyapi.config.registered_filters.keys())
        raise ValueError(
            "{0} is not a registered NiPyApi filterable class, registered "
            "classes are {1}".format(obj_class_name, registered_filters)
        )
    # Check if the supplied key is part of the registered filter
    key_lookup = nipyapi.config.registered_filters[obj_class_name].get(
        key, False
    )
    if not key_lookup:
        valid_keys = ' '.join(
            nipyapi.config.registered_filters[obj_class_name].keys()
        )
        raise ValueError(
            "{0} is not a registered filter method for object {1}, valid "
            "methods are {2}".format(key, obj_class_name, valid_keys)
        )
    # List comprehension using reduce to unpack the list of keys in the filter
    if greedy:
        out = [
            i for i in obj if value in
            reduce(operator.getitem, key_lookup, i.to_dict())
        ]
    else:
        out = [
            i for i in obj if
            value == reduce(operator.getitem, key_lookup, i.to_dict())
        ]
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
    log.info("Called wait_to_complete for function %s",
             test_function.__name__)
    delay = kwargs.pop('nipyapi_delay', nipyapi.config.short_retry_delay)
    max_wait = kwargs.pop('nipyapi_max_wait', nipyapi.config.short_max_wait)
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
    raise ValueError("Timed Out waiting for {0} to complete".format(
        test_function.__name__))


def is_endpoint_up(endpoint_url):
    """
    Tests if a URL is available for requests

    Args:
        endpoint_url (str): The URL to test

    Returns (bool): True for a 200 response, False for not

    """
    log.info("Called is_endpoint_up with args %s", locals())
    try:
        response = requests.get(
            endpoint_url,
            timeout=nipyapi.config.short_max_wait
        )
        if response.status_code:
            if response.status_code == 200:
                log.info("Got 200 response from endpoint, returning True")
                return True
            log.info("Got status code %s from endpoint, returning False",
                     response.status_code)
        return False
    except (requests.ConnectionError, requests.exceptions.SSLError) as e:
        log.info("Got Error of type %s with details %s", type(e), str(e))
        if 'SSLError' in str(type(e)):
            log.info("Got OpenSSL error, port is probably up but needs Cert")
            return True
        log.info("Got ConnectionError, returning False")
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
    if 'nifi-api' in endpoint_url:
        configuration = nipyapi.config.nifi_config
        service = 'nifi'
    elif 'registry-api' in endpoint_url:
        configuration = nipyapi.config.registry_config
        service = 'registry'
    else:
        raise ValueError("Endpoint not recognised")

    log.info("Setting %s endpoint to %s", service, endpoint_url)
    if configuration.api_client:
        nipyapi.security.service_logout(service)
        configuration.api_client = None

    # remove any trailing slash to avoid hard to spot errors
    configuration.host = endpoint_url.rstrip('/')

    # Respect preconfigured CA only; environment integration should be handled by callers
    shared_ca = getattr(configuration, 'ssl_ca_cert', None)
    if shared_ca and login:
        # For username/password (one-way TLS) flows, prefer CA bundle over any pre-set SSLContext
        configuration.ssl_context = None
        # Recreate API client to pick up new CA
        configuration.api_client = None

    # Set up SSL context if using HTTPS
    if ssl and 'https://' in endpoint_url:
        if login:
            # For one-way TLS with username/password, rely on ssl_ca_cert and verify_ssl
            # Avoid setting a custom SSLContext here
            nipyapi.security.service_login(
                service, username=username, password=password
            )
        else:
            # mTLS auth with client certificates; prefer preconfigured values
            nipyapi.security.set_service_ssl_context(
                service=service,
                ca_file=shared_ca or nipyapi.config.default_ssl_context['ca_file'],
                client_cert_file=getattr(configuration, 'cert_file', None) or nipyapi.config.default_ssl_context['client_cert_file'],
                client_key_file=getattr(configuration, 'key_file', None) or nipyapi.config.default_ssl_context['client_key_file'],
                client_key_password=getattr(configuration, 'key_password', None) or nipyapi.config.default_ssl_context['client_key_password']
            )

    # One-time supported-version enforcement: check once using existing helper.
    try:
        enforce_min_ver('2', service=service)
    except Exception as e:
        # Do not block connection for unreachable About in secured setups; log instead
        log.debug("Version check skipped or failed for %s: %s", service, e)

    return True


# pylint: disable=R0913,R0902,R0917
class DockerContainer():
    """
    Helper class for Docker container automation without using Ansible
    """
    def __init__(self, name=None, image_name=None, image_tag=None, ports=None,
                 env=None, volumes=None, test_url=None, endpoint=None):
        if not DOCKER_AVAILABLE:
            raise ImportError(
                "The 'docker' package is required for this class. "
                "Please install nipyapi with the 'demo' extra: "
                "pip install nipyapi[demo]"
            )
        self.name = name
        self.image_name = image_name
        self.image_tag = image_tag
        self.ports = ports
        self.env = env
        self.volumes = volumes
        self.test_url = test_url
        self.endpoint = endpoint
        self.container = None

    def get_test_url_status(self):
        """
        Checks if a URL is available
        :return: status code if available, String 'ConnectionError' if not
        """
        try:
            return requests.get(self.test_url, timeout=10).status_code
        except requests.ConnectionError:
            return 'ConnectionError'
        except requests.Timeout:
            return 'Timeout'

    def set_container(self, container):
        """Set the container object"""
        self.container = container

    def get_container(self):
        """Fetch the container object"""
        return self.container


# pylint: disable=W0703,R1718
def start_docker_containers(docker_containers, network_name='demo'):
    """
    Deploys a list of DockerContainer's on a given network

    Args:
        docker_containers (list[DockerContainer]): list of Dockers to start
        network_name (str): The name of the Docker Bridge Network to get or
            create for the Docker Containers

    Returns: Nothing

    """
    if not DOCKER_AVAILABLE:
        raise ImportError(
            "The 'docker' package is required for this function. "
            "Please install nipyapi with the 'demo' extra: "
            "pip install nipyapi[demo]"
        )

    log.info("Creating Docker client using Environment Variables")
    d_client = docker.from_env()

    # Test if Docker Service is available
    try:
        d_client.version()
    except Exception as e:
        raise EnvironmentError("Docker Service not found") from e

    for target in docker_containers:
        assert isinstance(target, DockerContainer)

    # Pull relevant Images
    log.info("Pulling relevant Docker Images if needed")
    for image in set([(c.image_name + ':' + c.image_tag)
                      for c in docker_containers]):
        log.info("Checking image %s", image)
        try:
            d_client.images.get(image)
            log.info("Using local image for %s", image)
        except ImageNotFound:
            log.info("Pulling %s", image)
            d_client.images.pull(image)

    # Clear previous containers
    log.info("Clearing previous containers for this demo")
    d_clear_list = [li for li in d_client.containers.list(all=True)
                    if li.name in [i.name for i in docker_containers]]
    for c in d_clear_list:
        log.info("Removing old container %s", c.name)
        c.remove(force=True)

    # Deploy/Get Network
    log.info("Getting Docker bridge network")
    d_n_list = [li for li in d_client.networks.list()
                if network_name in li.name]
    if not d_n_list:
        d_network = d_client.networks.create(
            name=network_name,
            driver='bridge',
            check_duplicate=True
        )
    elif len(d_n_list) > 1:
        raise EnvironmentError("Too many test networks found")
    else:
        d_network = d_n_list[0]
    log.info("Using Docker network: %s", d_network.name)

    # Deploy Containers
    log.info("Starting relevant Docker Containers")
    for c in docker_containers:
        log.info("Starting Container %s", c.name)
        c.set_container(d_client.containers.run(
            image=c.image_name + ':' + c.image_tag,
            detach=True,
            network=network_name,
            hostname=c.name,
            name=c.name,
            ports=c.ports,
            environment=c.env,
            volumes=c.volumes,
            auto_remove=True
        ))


class VersionError(Exception):
    """Error raised when a feature is not supported in the current version"""


def check_version(base, comparator=None, service='nifi',
                  default_version='2.0.0'):
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
        return '.'.join(version_string.split('-')[0].split('.')[:3])

    assert isinstance(base, str)
    assert comparator is None or isinstance(comparator, str)
    assert service in ['nifi', 'registry']
    ver_a = version.parse(strip_version_string(base))
    if comparator:
        ver_b = version.parse(strip_version_string(comparator))
    elif service == 'registry':
        try:
            reg_ver = nipyapi.system.get_registry_version_info()
            ver_b = version.parse(strip_version_string(reg_ver))
        except Exception:
            log.warning(
                "Unable to get registry About version, assuming %s",
                default_version)
            ver_b = version.parse(default_version)
    else:
        nifi_ver = nipyapi.system.get_nifi_version_info()
        nifi_ver_str = getattr(nifi_ver, 'ni_fi_version', nifi_ver)
        ver_b = version.parse(strip_version_string(nifi_ver_str))
    if ver_b > ver_a:
        return -1
    if ver_b < ver_a:
        return 1
    return 0


def validate_parameters_versioning_support(verify_nifi=True,
                                           verify_registry=True):
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


def validate_templates_version_support():
    """
    Validate that the current version of NiFi supports Templates API
    """
    enforce_max_ver('2', service='nifi', error_message="Templates are deprecated in NiFi 2.x")


def enforce_max_ver(max_version, bool_response=False, service='nifi', error_message=None):
    """
    Raises an error if target NiFi environment is at or above the max version
    """
    if check_version(max_version, service=service) == -1:
        if not bool_response:
            raise VersionError(error_message or "This function is not available "
                               "in NiFi {} or above".format(max_version))
        return True
    return False


def enforce_min_ver(min_version, bool_response=False, service='nifi'):
    """
    Raises an error if target NiFi environment is not minimum version
    Args:
        min_version (str): Version to check against
        bool_response (bool): If True, will return True instead of
         raising error
     service: nifi or registry

    Returns:
        (bool) or (NotImplementedError)
    """
    if check_version(min_version, service=service) == 1:
        if not bool_response:
            raise VersionError(
                "This function is not available "
                "before NiFi version " + str(min_version))
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
        return 'PROCESSOR'
    if isinstance(obj, nipyapi.nifi.FunnelEntity):
        return 'FUNNEL'
    if isinstance(obj, nipyapi.nifi.PortEntity):
        return obj.port_type
    if isinstance(obj, nipyapi.nifi.RemoteProcessGroupDTO):
        return 'REMOTEPROCESSGROUP'
    if isinstance(obj, nipyapi.nifi.RemoteProcessGroupPortDTO):
        # get RPG summary, find id of obj in input or output list
        parent_rpg = nipyapi.canvas.get_remote_process_group(
            obj.group_id, True)
        if obj.id in [x.id for x in parent_rpg['input_ports']]:
            return 'REMOTE_INPUT_PORT'
        if obj.id in [x.id for x in parent_rpg['output_ports']]:
            return 'REMOTE_OUTPUT_PORT'
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
    assert service in ['nifi', 'registry']
    assert isinstance(bypass, bool)
    current_config = getattr(nipyapi, service).configuration
    if bypass:
        if '/' not in current_config.safe_chars_for_path_param:
            current_config.safe_chars_for_path_param += '/'
    else:
        current_config.safe_chars_for_path_param = \
            copy(nipyapi.config.default_safe_chars)


@contextmanager
def rest_exceptions():
    """Simple exception wrapper for Rest Exceptions"""
    try:
        yield
    except (nipyapi.nifi.rest.ApiException,
            nipyapi.registry.rest.ApiException) as e:
        raise ValueError(e.body) from e


def exception_handler(status_code=None, response=None):
    """Simple Function wrapper to handle HTTP Status Exceptions"""
    def func_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except (nipyapi.nifi.rest.ApiException,
                    nipyapi.registry.rest.ApiException) as e:
                if status_code is not None and e.status == int(status_code):
                    return response
                raise ValueError(e.body) from e
        return wrapper
    return func_wrapper
