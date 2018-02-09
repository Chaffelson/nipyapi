#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INTERNAL USE
Convenience utility functions for NiPyApi
"""

from __future__ import absolute_import, unicode_literals
import json
import importlib
from six import PY2
from ruamel.yaml import safe_load, safe_dump
from ruamel.yaml.reader import YAMLStreamError
from ruamel.yaml.representer import RepresenterError
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


def dump(obj, mode='json'):
    """
    return a sorted encoded string of the given object in the given format
    with no round-trip data loss or translation
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
        try:
            return safe_dump(
                data=obj,
                allow_unicode=True,
                default_flow_style=False
            )
        except RepresenterError as e:
            raise e
    else:
        raise ValueError("Invalid dump Mode specified ({0})"
                         .format(mode))


def _rehydrate_dto(mod_def, obj_name, data):
    """
    Safely? reconstructs the native DTO from a deserialised object
    :param m_name: String of the module name the DTO lives in, e.g
    nipyapi.registry.models
    :param obj_name: String name of the class to be rehydrated, e.g.
    VersionedProcessGroup. Must exist in the module passed
    :param data: the data structure that matches the object passed
    :return: The rehydrated DTO of the passed object
    """
    import inspect
    # Get a list of all valid classes defined in the given module
    valid_class_defs = dict(inspect.getmembers(mod_def, inspect.isclass))
    # Test if the passed object is a locally defined class
    if obj_name in valid_class_defs.keys():
        # Fetch the class definition
        c_def = getattr(mod_def, obj_name)
        # Instantiate the class
        c_obj = c_def.__new__(c_def)
        # use the native loaders to unpack the data as built-in python types
        c_obj.__init__(**data)
        # Iterate through the pre-defined swagger types looking for more work
        for param in c_def.swagger_types.keys():
            # If the param has been defined with some data
            if c_obj.__getattribute__(param):
                # grab the swagger type definition and parse it
                param_def = c_def.swagger_types[param]
                # if the swagger type is a list of objects
                if 'list[' in param_def:
                    # Extract the name of the object in the list
                    sub_c_name = param_def[
                        param_def.find("[")+1:param_def.find("]")
                        ]
                    # Extract the base types as a list of data objects
                    raw_list = c_obj.__getattribute__(param)
                    # replace the param with a list of rehydrated objects
                    c_obj.__setattr__(
                        param,
                        [_rehydrate_dto(
                            mod_def, sub_c_name, li
                        ) for li in raw_list]
                    )
                # If a single instance of a defined class in this module
                if param_def in valid_class_defs.keys():
                    # copying the pattern above for readability
                    sub_c_name = param_def
                    # get the base type object
                    raw_obj = c_obj.__getattribute__(param)
                    # Run the rehydrator as a single instance
                    c_obj.__setattr__(
                        param, _rehydrate_dto(mod_def, sub_c_name, raw_obj)
                    )
                # If the swagger type is a dict
                if 'dict(str, ' in param_def:
                    # Extract the key, value definition from the swagger type
                    sub_k_def, sub_v_def = param_def[
                        param_def.find("(") + 1:param_def.find(
                            ")")].rsplit(', ', 1)
                    # Extract the base dict data
                    raw_obj = c_obj.__getattribute__(param)
                    # Reconstruct with the swagger defined types
                    c_obj.__setattr__(
                        param,
                        {
                            _rehydrate_dto(mod_def, sub_k_def, k):
                                _rehydrate_dto(mod_def, sub_v_def, v)
                            for k, v in raw_obj.items()
                        }
                    )
        # Return the updated object to the parent call
        return c_obj
    # Base types should be handled fine by the built-in constructor
    # But we'll force type just to be pedantic
    elif obj_name == 'str':
        return str(data)
    elif obj_name == 'int':
        return int(data)
    else:
        raise TypeError("Object ({0}) is not recognised as a valid Swagger"
                        "Type, or Class defined in ({1})"
                        .format(obj_name, mod_def.__name__))


def load(obj, dto=None):
    """
    return a decoded object from a yaml/json string
    :param obj: String to be decoded
    :param dto: the DTO we are reconstituting, if necessary
    :return: Decoded object of native types, probably nested dicts and lists
    """
    try:
        # safe_load from ruamel.yaml as it doesn't accidentally convert str
        # to unicode in py2. It also manages both json and yaml equally well
        # Good explanation: https://stackoverflow.com/a/16373377/4717963
        loaded_obj = safe_load(obj)
    except YAMLStreamError as e:
        raise e
    if dto:
        try:
            module_name, class_name = dto
            module_definition = importlib.import_module(module_name)
            out = _rehydrate_dto(module_definition, class_name, loaded_obj)
            return out
        except ImportError as e:
            raise e
    else:
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
