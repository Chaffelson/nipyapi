=======
NiPyApi
=======

Nifi-Python-Api: A convenient Python wrapper for the Apache NiFi Rest API

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

| This package provides pythonic calls for common NiFi tasks and CICD/SDLC integrations - you might call it Flow Development LifeCycle
| These are implemented by replicating the action of the same task in the GUI and surfacing the underlying NiFi Data structures and calls wherever possible, to retain UX parallelism for the user

Functionality Highlights:
 - Full native Python rest client for NiFi and NiFi-Registry
 - CRUD wrappers for common task areas like Processor Groups, Processors, Templates, Registry Clients, Registry Buckets, Registry Flows, etc.
 - Convenience functions for inventory tasks, such as recursively retrieving the entire canvas, or a flat list of all Process Groups
 - Docker Compose configurations for testing and deployment
 - Limited support for scheduling components
 - A scripted deployment of an interactive environment for testing and demonstration purposes

Coming soon:
 - Secured environment support is not currently implemented, but it is planned to be done very soon
 - Support for complex scheduling requests, such as stopping a large flow and waiting for all Processors to be halted
 - Support for edge cases during Versioning changes, such as Reverting a flow containing live data

Usage
-----
The easiest way to install NiPyApi is with pip::

    # in bash
    pip install nipyapi

Then import a module and execute tasks::

    # in python
    from nipyapi import config
    config.nifi_config.host = 'http://localhost:8080/nifi-api'
    from nipyapi.canvas import get_root_pg_id
    get_root_pg_id()
    >'4d5dcf9a-015e-1000-097e-e505ed0f7fd2'

You can also use the demo to create an interactive console showing a few of the features::

    # in python
    from nipyapi import config
    config.nifi_config.host = 'http://localhost:8080/nifi-api'
    config.registry_config.host = 'http://localhost:18080/nifi-registry-api'
    from nipyapi.demo.console import *

You can also pull the repository from Github and use or contribute to the latest features, check out the `Contribution Guide <https://github.com/Chaffelson/nipyapi/blob/master/docs/contributing.rst>`_ for more info.

Background
----------

| For more information on Apache NiFi, please visit `https://nifi.apache.org <https://nifi.apache.org>`_
| For Documentation on this package please visit `https://nipyapi.readthedocs.io. <https://nipyapi.readthedocs.io/en/latest>`_


Version Support
---------------

| This project leverages the `nifi-python-swagger-client <https://github.com/Chaffelson/nifi-python-swagger-client>`_ to maintain version compatibility with NiFi releases
| Currently we are testing against NiFi version 1.2 - 1.5, and NiFi-Registry version 0.1.0
| If you require a different version please raise an `issue <https://github.com/Chaffelson/nipyapi/issues>`_

Requirements
------------

Python 2.7 or 3.6 supported, though other versions may work


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Inspired by the equivalent Java client maintained over at
`hermannpencole/nifi-config <https://github.com/hermannpencole/nifi-config>`_

The swagger 2.0 compliant client auto-generated using the
`Swagger Codegen <https://github.com/swagger-api/swagger-codegen>`_ project,
and then cleaned / bugfixed by the authors
