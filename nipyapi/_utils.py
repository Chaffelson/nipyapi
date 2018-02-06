#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INTERNAL USE
Convenience utility functions for NiPyApi
"""

from __future__ import absolute_import, unicode_literals
import json
from ruamel.yaml import safe_load
from ruamel.yaml.reader import YAMLStreamError

# Python 2.7 doesn't have Py3.3+ Error codes, but they're more readable
try:
    import FileNotFoundError
    import PermissionError
except ImportError:
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
                        "to_dict() method".format(type(obj)))


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
        except ValueError as e:
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
    except FileNotFoundError as e:
        raise e
