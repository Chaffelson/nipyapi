#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INTERNAL USE
Convenience utility functions for NiPyApi
"""

from __future__ import absolute_import, unicode_literals
import json
from six import PY2
from ruamel.yaml import safe_load
from ruamel.yaml.reader import YAMLStreamError
from nipyapi import config

# Python 2.7 doesn't have Py3.3+ Error codes, but they're more readable
if PY2:
    FileNotFoundError = IOError
    PermissionError = IOError


def _json_default(obj):
    """
    # This tells the json dumper to look for the to_dict() method on objects
    :param obj: object being dumped
    :return: native dict repr of the object, if it exists, TypeError if not
    """
    try:
        return obj.to_dict()
    except AttributeError:
        raise TypeError("Expected Object({0}) to have swagger defined"
                        " to_dict() method".format(type(obj)))


def dump(obj, mode=None):
    """
    return an encoded string of the given object in the given format
    :param obj: Object to be encoded, expected to be a native API object
    :param mode: String of 'json' or 'yaml'
    :return: String of the encoded object
    """
    if mode == 'json':
        try:
            return json.dumps(
                obj=obj,
                sort_keys=True,
                indent=4,
                default=_json_default
            )
        except TypeError as e:
            raise e
    elif mode == 'yaml':
        raise TypeError("({0})) export/import not yet implemented"
                        .format(mode))
    else:
        raise ValueError("Invalid dump Mode specified ({0})"
                         .format(mode))


def load(obj):
    """
    return a decoded object from a yaml/json string
    :param obj: String to be decoded
    :return: Decoded object of native types, probably nested dicts and lists
    """
    try:
        # safe_load from ruamel.yaml as it doesn't accidentally convert str
        # to unicode in py2. It also manages both json and yaml equally well
        # Good explanation: https://stackoverflow.com/a/16373377/4717963
        return safe_load(obj)
    except YAMLStreamError as e:
        raise e


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
    this_filter = config.registered_filters.get(obj_class_name, False)
    if not this_filter:
        registered_filters = ' '.join(config.registered_filters.keys())
        raise ValueError(
            "({0}) is not a registered NiPyApi filterable class, registered "
            "classes are ({1})".format(obj_class_name, registered_filters)
        )
    # Check if the supplied key is part of the registered filter
    key_lookup = config.registered_filters[obj_class_name].get(key, False)
    if not key_lookup:
        valid_keys = ' '.join(config.registered_filters[obj_class_name].keys())
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
