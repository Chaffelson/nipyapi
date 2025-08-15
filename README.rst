==============
|nipy| NiPyApi
==============

.. |nipy| image:: https://image.ibb.co/f0FRs0/nipy.png
    :height: 28px

Nifi-Python-Api: A rich Apache NiFi Python Client SDK

.. image:: https://img.shields.io/pypi/v/nipyapi.svg
        :target: https://pypi.python.org/pypi/nipyapi
        :alt: Release Status

.. image:: https://readthedocs.org/projects/nipyapi/badge/?version=latest
        :target: https://nipyapi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Chaffelson/nipyapi/shield.svg
     :target: https://pyup.io/repos/github/Chaffelson/nipyapi/
     :alt: Python Updates

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License


Features
--------

**Three layers of Python support for working with Apache NiFi:**
 - Top-level examples (see `examples/` in the repo)
 - Mid-level Client SDK for typical complex tasks
 - Low-level Client SDKs for the full API implementation of NiFi and selected sub-projects

**Functionality Highlights:**
 - Detailed documentation of the full SDK at all levels
 - CRUD wrappers for common task areas like Processor Groups, Processors, Templates, Registry Clients, Registry Buckets, Registry Flows, etc.
 - Convenience functions for inventory tasks, such as recursively retrieving the entire canvas, or a flat list of all Process Groups
 - Support for scheduling and purging flows, controller services, and connections
 - Support for fetching and updating Variable Registries
 - Support for import/export of Versioned Flows from NiFi-Registry
 - Docker Compose profiles for testing and development


Please see the `issue <https://github.com/Chaffelson/nipyapi/issues>`_ register for more information on current development.

Quick Start
-----------

| The mid-level functionality is in *nipyapi.canvas / nipyapi.security / nipyapi.parameters / nipyapi.versioning*
| You can access the entire API using the low-level SDKs in *nipyapi.nifi / nipyapi.registry*

The easiest way to install NiPyApi is with pip::

    # in bash
    pip install nipyapi
    
    # for local development with linting/testing tools
    pip install -e ".[dev]"

You can set the config for your endpoints in the central config file::

    # in python
    import nipyapi
    nipyapi.config.nifi_config.host = 'https://localhost:9443/nifi-api'
    # NiFi Registry 2.x commonly runs HTTPS (e.g., 18443). Adjust per your profile.
    nipyapi.config.registry_config.host = 'https://localhost:18443/nifi-registry-api'

Then import a module and execute tasks::

    nipyapi.canvas.get_root_pg_id()
    >'4d5dcf9a-015e-1000-097e-e505ed0f7fd2'

Use Docker Compose profiles in `resources/docker/compose.yml` for local testing. See `docs/contributing.rst` for profile-based testing instructions.

Please check out the `Contribution Guide <https://github.com/Chaffelson/nipyapi/blob/master/docs/contributing.rst>`_ if you are interested in contributing to the feature set.

Background and Documentation
----------------------------

| For more information on Apache NiFi, please visit `https://nifi.apache.org <https://nifi.apache.org>`_
| For Documentation on this package please visit `https://nipyapi.readthedocs.io. <https://nipyapi.readthedocs.io/en/latest>`_


NiFi Version Support
--------------------

| NiPyAPI 1.x targets Apache NiFi 2.x and NiFi Registry 2.x.
| If you want to work with NiFi 1.x, please use the 0.x branch.
| If you find a version compatibility problem please raise an `issue <https://github.com/Chaffelson/nipyapi/issues>`_

Python Support
--------------

| Python 3.9-12 supported, though other versions may work.
| Python2 is no longer supported as of the NiPyAPI 1.0 release, please use the 0.x branch for Python2 projects.
| OSX M1 chips are known to have had various issues with Requests and Certificates.

| Tests are run locally against upstream Apache NiFi and NiFi Registry Docker images via Docker Compose profiles (Docker Desktop).
| Developed on macOS 14+ and Windows 10.
| Outside of the standard Python modules, runtime uses requests/urllib3, ruamel.yaml, and PySocks. Demos and Docker management have been removed from the client; use Docker Compose profiles in resources/docker instead.
