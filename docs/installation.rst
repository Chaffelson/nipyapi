.. highlight:: shell

============
Installation
============

Requirements
------------

- **Python**: 3.9 or higher
- **Apache NiFi**: 2.0.0 or higher (for target NiFi instances)
- **Apache NiFi Registry**: 2.0.0 or higher (optional, for local versioning features)
- **Docker Desktop**: Optional, for local development and testing with provided profiles

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

Next Steps
----------

**Option 1: Quick Test with Docker (Recommended for New Users)**

If you have Docker Desktop, you can test with our provided environment:

.. code-block:: console

    # Clone repository for Docker profiles
    $ git clone https://github.com/Chaffelson/nipyapi.git
    $ cd nipyapi

    # Start test environment
    $ make certs && make up NIPYAPI_PROFILE=single-user && make wait-ready NIPYAPI_PROFILE=single-user

Then test the connection:

.. code-block:: python

    import nipyapi

    # Use built-in profile (no manual configuration needed)
    nipyapi.profiles.switch('single-user')

    # Test connection
    try:
        version = nipyapi.system.get_nifi_version_info()
        print(f"✓ Connected to NiFi {version}")
    except Exception as e:
        print(f"✗ Connection failed: {e}")

**Option 2: Connect to Your Existing NiFi**

If you have NiFi already running, create a custom profile:

.. code-block:: python

    import nipyapi

    # Create custom profile configuration
    custom_config = {
        'nifi_url': 'https://your-nifi.com/nifi-api',  # NiFi 2.x typically uses HTTPS
        'nifi_user': 'your_username',
        'nifi_pass': 'your_password',
        'nifi_verify_ssl': True
    }

    # Test connection
    try:
        # Manual configuration (advanced)
        nipyapi.config.nifi_config.host = custom_config['nifi_url']
        nipyapi.utils.set_endpoint(custom_config['nifi_url'], ssl=True, login=True,
                                  username=custom_config['nifi_user'],
                                  password=custom_config['nifi_pass'])

        version = nipyapi.system.get_nifi_version_info()
        print(f"✓ Connected to NiFi {version}")
    except Exception as e:
        print(f"✗ Connection failed: {e}")

**Learn More**

For complete configuration options and authentication methods:

- **Profiles System**: See ``docs/profiles.rst`` for centralized configuration management
- **Authentication**: See ``docs/security.rst`` for all supported authentication methods
- **Migration**: See ``docs/migration.rst`` if upgrading from NiPyAPI 0.x
- **Quick Start**: See ``README.rst`` for step-by-step setup instructions


.. include:: nipyapi-docs/dependencies.rst

.. _Github repo: https://github.com/Chaffelson/nipyapi
