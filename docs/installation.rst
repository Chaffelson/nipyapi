.. highlight:: shell

============
Installation
============

Requirements
------------

- **Python**: 3.9 or higher
- **Apache NiFi**: 2.0.0 or higher (for target NiFi instances)
- **Apache NiFi Registry**: 2.0.0 or higher (optional, for local versioning features)

Stable Release
--------------

To install NiPyAPI from PyPI, run this command in your terminal:

.. code-block:: console

    $ pip install nipyapi

This is the preferred method to install NiPyAPI, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: https://packaging.python.org/tutorials/installing-packages/

Virtual Environment (Recommended)
----------------------------------

It's recommended to install NiPyAPI in a virtual environment to avoid conflicts:

.. code-block:: console

    $ python -m venv nipyapi-env
    $ source nipyapi-env/bin/activate  # On Windows: nipyapi-env\Scripts\activate
    $ pip install nipyapi

Development Installation
------------------------

To install NiPyAPI for development or to get the latest features:

.. code-block:: console

    # Clone the repository
    $ git clone https://github.com/Chaffelson/nipyapi.git
    $ cd nipyapi
    
    # Install in development mode with all dependencies
    $ pip install -e ".[dev,docs]"

Or to get the latest development version directly:

.. code-block:: console

    $ pip install git+https://github.com/Chaffelson/nipyapi.git@main

From Source Archive
-------------------

You can download and install from a source archive:

.. code-block:: console

    # Download the latest source
    $ curl -OL https://github.com/Chaffelson/nipyapi/tarball/main
    $ tar -xzf main
    $ cd Chaffelson-nipyapi-*
    
    # Install using pip (recommended)
    $ pip install .
    
    # Or build and install manually
    $ python -m build
    $ pip install dist/*.whl

Verify Installation
-------------------

To verify that NiPyAPI is installed correctly:

.. code-block:: console

    $ python -c "import nipyapi; print(f'NiPyAPI {nipyapi.__version__} installed successfully')"

For a quick connection test (requires running NiFi):

.. code-block:: python

    import nipyapi
    
    # Configure for your NiFi instance, see docs/authentication.rst for more details
    nipyapi.config.nifi_config.host = 'http://localhost:8080/nifi-api'
    
    # Test connection
    try:
        version = nipyapi.system.get_nifi_version_info()
        print(f"Connected to NiFi {version.ni_fi_version}")
    except Exception as e:
        print(f"Connection failed: {e}")


.. include:: nipyapi-docs/dependencies.rst

.. _Github repo: https://github.com/Chaffelson/nipyapi
