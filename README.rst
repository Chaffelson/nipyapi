=======
NiPyApi
=======

Nifi-Python-Api: A rich Apache NiFi Python Client SDK

.. image:: https://img.shields.io/pypi/v/nipyapi.svg
        :target: https://pypi.python.org/pypi/nipyapi
        :alt: Release Status

.. image:: https://img.shields.io/travis/Chaffelson/nipyapi.svg
        :target: https://travis-ci.org/Chaffelson/nipyapi
        :alt: Build Status

.. image:: https://readthedocs.org/projects/nipyapi/badge/?version=latest
        :target: https://nipyapi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Chaffelson/nipyapi/shield.svg
     :target: https://pyup.io/repos/github/Chaffelson/nipyapi/
     :alt: Python Updates

.. image:: https://coveralls.io/repos/github/Chaffelson/nipyapi/badge.svg?branch=master
    :target: https://coveralls.io/github/Chaffelson/nipyapi?branch=master&service=github
    :alt: test coverage

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License


Features
--------

**Three layers of Python support for working with Apache NiFi:**
 - High-level Demos and example scripts
 - Mid-level Client SDK for typical complex tasks
 - Low-level Client SDKs for the full API implementation of NiFi and selected sub-projects

**Functionality Highlights:**
 - Detailed documentation of the full SDK at all levels
 - CRUD wrappers for common task areas like Processor Groups, Processors, Templates, Registry Clients, Registry Buckets, Registry Flows, etc.
 - Convenience functions for inventory tasks, such as recursively retrieving the entire canvas, or a flat list of all Process Groups
 - Support for scheduling and purging flows
 - Support for fetching and updating Variable Registries
 - Support for import/export of Versioned Flows from NiFi-Registry
 - Docker Compose configurations for testing and deployment
 - A scripted deployment of an interactive environment, and a secured configuration, for testing and demonstration purposes

**Coming soon:**
 - Support for edge cases during Versioning changes, such as Reverting a flow containing live data
 - Support for Mnemonic component naming and path resolution
 - Rich configuration differential support

Please see the `issue <https://github.com/Chaffelson/nipyapi/issues>`_ register for more information on current development.

Quick Start
-----------
The easiest way to install NiPyApi is with pip::

    # in bash
    pip install nipyapi

Then import a module and execute tasks::

    # in python
    import nipyapi
    nipyapi.config.nifi_config.host = 'http://localhost:8080/nifi-api'
    nipyapi.canvas.get_root_pg_id()
    >'4d5dcf9a-015e-1000-097e-e505ed0f7fd2'

You can also use the demo to create an interactive console showing many features::

    # in python
    import nipyapi
    nipyapi.config.nifi_config.host = 'http://localhost:8080/nifi-api'
    nipyapi.config.registry_config.host = 'http://localhost:18080/nifi-registry-api'
    from nipyapi.demo.console import *

| There are several scripts to produce demo environments in *nipyapi.demo.**
| The mid-level functionality is in *nipyapi.canvas / nipyapi.security / nipyapi.templates / nipyapi.versioning*
| You can access the entire API using the low-level SDKs in *nipyapi.nifi / nipyapi.registry*

Please check out the `Contribution Guide <https://github.com/Chaffelson/nipyapi/blob/master/docs/contributing.rst>`_ if you are interested in contributing to the feature set.

Background and Documentation
----------------------------

| For more information on Apache NiFi, please visit `https://nifi.apache.org <https://nifi.apache.org>`_
| For Documentation on this package please visit `https://nipyapi.readthedocs.io. <https://nipyapi.readthedocs.io/en/latest>`_


NiFi Version Support
--------------------

| Currently we are testing against NiFi versions 1.1.2 - 1.5.0, and NiFi-Registry version 0.1.0.
| If you find a version compatibility problem please raise an `issue <https://github.com/Chaffelson/nipyapi/issues>`_

Python Requirements
-------------------

| Python 2.7 or 3.6 supported, though other versions may work.
| Outside of the standard Python modules, we make use of lxml, DeepDiff and ruamel.yaml
