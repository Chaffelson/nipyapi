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
    "ci",  # CI/CD operations: deploy, start, stop, cleanup flows
    "canvas",  # Process groups, processors, connections, scheduling
    "versioning",  # Flow import/export, registry operations
    "security",  # Authentication, users, policies
    "parameters",  # Parameter contexts and values
    "profiles",  # Profile switching and configuration
    "layout",  # Canvas positioning, flow structure analysis
    "system",  # System info, cluster status
    "bulletins",  # Bulletin retrieval, filtering, clearing
    "extensions",  # NiFi extensions (NARs) management
    "utils",  # File ops, retries, wait patterns, filtering
    "config",  # Endpoint configuration, API clients
    "nifi",  # Low-level NiFi API (generated - do not modify)
    "registry",  # Low-level Registry API (generated - do not modify)
]

for sub_module in __all__:
    importlib.import_module("nipyapi." + sub_module)
