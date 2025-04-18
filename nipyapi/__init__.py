"""
NiPyAPI: A convenient Python wrapper for the Apache NiFi Rest API
"""

import importlib

__author__ = """Daniel Chaffelson"""
__email__ = 'chaffelson@gmail.com'
__version__ = '0.22.0'
__all__ = ['canvas', 'system', 'templates', 'config', 'nifi', 'registry',
           'versioning', 'demo', 'utils', 'security', 'parameters']

for sub_module in __all__:
    importlib.import_module('nipyapi.' + sub_module)
