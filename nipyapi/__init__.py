"""
NiPyAPI: A convenient Python wrapper for the Apache NiFi Rest API
"""

import importlib

__author__ = """Daniel Chaffelson"""
__email__ = "chaffelson@gmail.com"
try:
    # Generated during build by setuptools_scm
    from ._version import version as __version__  # type: ignore
except ImportError:  # pragma: no cover - version file not present in editable contexts
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _pkg_version

    try:
        __version__ = _pkg_version("nipyapi")
    except PackageNotFoundError:  # package metadata not available (e.g., source checkout)
        __version__ = "0.0.0+unknown"
__all__ = [
    "canvas",
    "system",
    "config",
    "nifi",
    "registry",
    "versioning",
    "utils",
    "security",
    "parameters",
    "profiles",
    "layout",
    "extensions",
]

for sub_module in __all__:
    importlib.import_module("nipyapi." + sub_module)
