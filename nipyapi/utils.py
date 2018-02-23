#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INTERNAL USE
Convenience utility functions for NiPyApi
"""

from __future__ import absolute_import, unicode_literals
import json
import time
import six
import ruamel.yaml
from requests.models import Response
import nipyapi


# Python 2.7 doesn't have Py3.3+ Error codes, but they're more readable
if six.PY2:
    FileNotFoundError = IOError
    PermissionError = IOError


def dump(obj, mode='json'):
    """
    Dumps a serialisable object to json or yaml, defaults to json
    :param obj: object to serialise
    :param mode: Str; 'json' or 'yaml
    :return: the serialised object
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
        raise ValueError("Invalid dump Mode specified ({0})"
                         .format(mode))


def load(obj, dto=None):
    """
    Loads a serialised object back into native datatypes, and optionally
    imports it back into the native NiFi DTO
    :param obj: serialised object to load
    :param dto: Optional (Str, Str)
    Tuple of nifi model service as a string 'nifi' or 'registry', and the class
    name to load into
    :return:
    """
    assert isinstance(obj, (six.string_types, bytes))
    assert dto is None or isinstance(dto, tuple)
    # ensure object is standard json before reusing the api_client deserializer
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
    # safe_load from ruamel.yaml as it doesn't accidentally convert str
    # to unicode in py2. It also manages both json and yaml equally well
    # Good explanation: https://stackoverflow.com/a/16373377/4717963
    return loaded_obj


def fs_write(obj, file_path):
    """
    Convenience function to write a object to a file path
    :param obj: Writable object, like a String
    :param file_path: String path to the file for writing
    :return: The Object that was written
    """
    try:
        with open(str(file_path), 'w') as f:
            f.write(obj)
        return obj
    except TypeError as e:
        raise e


def fs_read(file_path):
    """
    Convenience function to read contents from a file
    :param file_path: String path to the file for reading
    :return: The contents of the file
    """
    try:
        with open(str(file_path), 'r') as f:
            return f.read()
    except (FileNotFoundError, PermissionError) as e:
        raise e


def filter_obj(obj, value, key):
    """
    Implements a custom filter method because Objects returned by the API
    don't have consistently named identifiers.
    Note that each class must be registered with the identifiers to be used
    :param obj: the NiFi or NiFi-Registry object to filter on
    :param value: the String value to look for
    :param key: the String of the object key to filter against
    :return: None if 0 matches, list if > 1, single Object entity if ==1
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
        raise TypeError("The passed object ({0}) is not a known filterable"
                        " nipyapi object".format(obj.__class__.__name__))
    # Check if this class has a registered filter in Nipyapi.config
    this_filter = nipyapi.config.registered_filters.get(obj_class_name, False)
    if not this_filter:
        registered_filters = ' '.join(nipyapi.config.registered_filters.keys())
        raise ValueError(
            "({0}) is not a registered NiPyApi filterable class, registered "
            "classes are ({1})".format(obj_class_name, registered_filters)
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
            "({0}) is not a registered filter method for object ({1}), valid "
            "methods are ({2})".format(key, obj_class_name, valid_keys)
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
    Implements a basic retry loop for a given test function
    :param test_function: Function returning a Bool once a state is reached
    :param args: any args to pass to the test function
    :param kwargs: any kwargs to pass to the test function
    :return: Bool of success or not
    """
    timeout = time.time() + nipyapi.config.retry_max_wait
    while time.time() < timeout:
        test_result = test_function(*args, **kwargs)
        if test_result:
            return test_result
        time.sleep(nipyapi.config.retry_delay)
    return False
