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
    :target: https://coveralls.io/github/Chaffelson/nipyapi?branch=master
    :alt: test coverage

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License


Features
--------

| This package provides pythonic calls for common NiFi tasks and CICD/SDLC integrations
| These are implemented by replicating the action of the same task in the GUI and surfacing the underlying NiFi Data structures and calls wherever possible, to retain UX parallelism for the user


Usage
-----
The easiest way to install NiPyApi is with pip::

    # in bash
    pip install nipyapi

Then import and use the module::

    # in python
    from nipyapi import canvas
    dir(canvas)
    > 'delete_process_group', 'get_flow', 'get_process_group_by_name', 'get_root_pg_id',
    > 'list_all_process_groups', 'process_group_status', 'schedule_process_group'
    canvas.get_root_pg_id()

    from nipyapi import templates
    dir(templates)
    > 'all_templates', 'create_template', 'delete_template', 'deploy_template',
    > 'export_template', 'get_template_by_name', 'make_pg_snippet', 'upload_template'
    templates.all_templates()

Background
----------

| For more information on Apache NiFi, please visit `https://nifi.apache.org <https://nifi.apache.org>`_
| For Documentation on this package please visit `https://nipyapi.readthedocs.io. <https://nipyapi.readthedocs.io/en/latest>`_


Version Support
---------------

| This project leverages the `nifi-python-swagger-client <https://github.com/Chaffelson/nifi-python-swagger-client>`_ to maintain version compatibility with NiFi releases
| Currently we are testing against NiFi version 1.2.x
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
