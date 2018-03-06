#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convenience utility functions for NiPyApi, not really intended for external use
"""

from __future__ import absolute_import, unicode_literals
import logging
import json
import time
import six
import ruamel.yaml
import docker
import requests
from requests.models import Response
import nipyapi

__all__ = ['dump', 'load', 'fs_read', 'fs_write', 'filter_obj',
           'wait_to_complete', 'is_endpoint_up', 'set_endpoint',
           'start_docker_containers', 'DockerContainer']

log = logging.getLogger(__name__)


def dump(obj, mode='json'):
    """
    Dumps a native datatype object to json or yaml, defaults to json

    Args:
        obj (varies): The native datatype object to serialise
        mode (str): 'json' or 'yaml', the supported export modes

    Returns (str): The serialised object

    """
    assert mode in ['json', 'yaml']
    try:
        out = json.dumps(
            obj=obj,
            sort_keys=True,
            indent=4
            # default=_json_default
        )
    except TypeError as e:
        raise e
    if mode == 'json':
        return out
    elif mode == 'yaml':
        return ruamel.yaml.safe_dump(
            json.loads(out),
            default_flow_style=False
        )
    else:
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
    assert isinstance(obj, (six.string_types, bytes))
    assert dto is None or isinstance(dto, tuple)
    # ensure object is standard json before reusing the api_client deserializer
    # safe_load from ruamel.yaml as it doesn't accidentally convert str
    # to unicode in py2. It also manages both json and yaml equally well
    # Good explanation: https://stackoverflow.com/a/16373377/4717963
    # Safe Load also helps prevent code injection
    loaded_obj = ruamel.yaml.safe_load(obj)
    if dto:
        assert dto[0] in ['nifi', 'registry']
        assert isinstance(dto[1], six.string_types)
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
        with open(str(file_path), 'w') as f:
            f.write(obj)
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
        with open(str(file_path), 'r') as f:
            return f.read()
    except IOError as e:
        raise e


def filter_obj(obj, value, key):
    """
    Implements a custom filter method because native datatypes don't have
    consistently named or located fields.

    Note that each object used by this function must be registered with
    identifier_types and identifiers in config

    Args:
        obj (varies): the NiFi or NiFi-Registry object to filter on
        value (str): the String value to look for
        key (str): the object key to filter against

    Returns: None if 0 matches, list if > 1, single Object entity if ==1

    """
    from functools import reduce
    import operator
    # Using the object class name as a lookup as they are unique within the
    # NiFi DTOs
    if isinstance(obj, list) and not obj:
        return None
    try:
        obj_class_name = obj[0].__class__.__name__
    except (TypeError, IndexError):
        raise TypeError("The passed object {0} is not a known filterable"
                        " nipyapi object".format(obj.__class__.__name__))
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
    out = [
        i for i in obj if value in
        reduce(operator.getitem, key_lookup, i.to_dict())
    ]
    # Manage our return contract
    if not out:
        return None
    elif len(out) > 1:
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
        log.debug("- Calling test_function")
        test_result = test_function(*args, **kwargs)
        log.debug("- Checking result")
        if test_result:
            log.info("- Function output evaluated to True, returning output")
            return test_result
        log.info("- Function output evaluated to False, sleeping...")
        time.sleep(delay)
    log.info("- Hit Timeout, raising TimeOut Error")
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
        log.debug("- Calling endpoint")
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            log.info("- Got 200, returning True")
            return True
        log.info("- Got status code %s, returning False",
                 response.status_code)
        return False
    except requests.ConnectionError:
        log.info("- Got ConnectionError, returning False")
        return False


def set_endpoint(endpoint_url):
    """
    EXPERIMENTAL

    Sets the endpoint when switching between instances of NiFi or other
    projects. Not tested extensively with secured instances.

    Args:
        endpoint_url (str): The URL to set as the endpoint. Autodetects the
        relevant service e.g. 'http://localhost:18080/nifi-registry-api'

    Returns (bool): True for success, False for not
    """
    log.info("Called set_endpoint with args %s", locals())
    if 'nifi-api' in endpoint_url:
        log.info("Setting NiFi endpoint to %s", endpoint_url)
        if nipyapi.config.nifi_config.api_client:
            nipyapi.config.nifi_config.api_client.host = endpoint_url
        nipyapi.config.nifi_config.host = endpoint_url
        if nipyapi.config.nifi_config.host == endpoint_url:
            return True
        return False
    elif 'registry-api' in endpoint_url:
        log.info("Setting Registry endpoint to %s", endpoint_url)
        if nipyapi.config.registry_config.api_client:
            nipyapi.config.registry_config.api_client.host = endpoint_url
        nipyapi.config.registry_config.host = endpoint_url
        if nipyapi.config.registry_config.host == endpoint_url:
            return True
        return False
    else:
        raise ValueError("Unrecognised NiFi or subproject API Endpoint")


class DockerContainer(object):
    """
    Helper class for Docker container automation without using Ansible
    """
    def __init__(self, name=None, image_name=None, image_tag=None, ports=None,
                 env=None, volumes=None, test_url=None, endpoint=None):
        self.name = name
        self.image_name = image_name
        self.image_tag = image_tag
        self.ports = ports
        self.env = env
        self.volumes = volumes
        self.test_url = test_url
        self.endpoint = endpoint

    def get_test_url_status(self):
        """
        Checks if a URL is available
        :return: status code if available, String 'ConnectionError' if not
        """
        try:
            return requests.get(self.test_url).status_code
        except requests.ConnectionError:
            return 'ConnectionError'


def start_docker_containers(docker_containers, network_name='demo'):
    """
    Deploys a list of DockerContainer's on a given network

    Args:
        docker_containers (list[DockerContainer]): list of Dockers to start
        network_name (str): The name of the Docker Bridge Network to get or
            create for the Docker Containers

    Returns: Nothing

    """
    log.info("Creating Docker client using Environment Variables")
    d_client = docker.from_env()

    for target in docker_containers:
        assert isinstance(target, DockerContainer)

    # Pull relevant Images
    log.info("Pulling relevant Docker Images")
    for image in set([(c.image_name + ':' + c.image_tag)
                      for c in docker_containers]):
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
    c_hooks = {}
    for c in docker_containers:
        log.info("Starting Container %s", c.name)
        c_hooks[c.name] = d_client.containers.run(
            image=c.image_name + ':' + c.image_tag,
            detach=True,
            network=network_name,
            hostname=c.name,
            name=c.name,
            ports=c.ports,
            environment=c.env,
            volumes=c.volumes
        )
