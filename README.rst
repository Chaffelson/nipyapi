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

.. image:: https://codecov.io/gh/Chaffelson/nipyapi/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/Chaffelson/nipyapi
        :alt: Coverage Status

.. image:: https://pyup.io/repos/github/Chaffelson/nipyapi/shield.svg
     :target: https://pyup.io/repos/github/Chaffelson/nipyapi/
     :alt: Python Updates

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License


Features
--------

**Multiple interfaces for working with Apache NiFi:**
 - **Command-Line Interface**: Shell access for scripting and CI/CD pipelines (``pip install nipyapi[cli]``)
 - **Mid-level Client SDK**: Python functions for typical complex tasks
 - **Low-level Client SDKs**: Full API implementation of NiFi and NiFi Registry
 - **Examples**: Ready-to-use scripts in the `examples directory <examples/>`_

**Functionality Highlights:**
 - **CI/CD Operations**: Purpose-built commands for flow deployment pipelines (``nipyapi.ci``)
 - **Profiles System**: One-command environment switching with ``nipyapi.profiles.switch('single-user')`` (see `profiles documentation <docs/profiles.rst>`_)
 - **Modern Authentication**: Built-in support for Basic Auth, mTLS, OIDC/OAuth2, and LDAP
 - **Environment Management**: YAML/JSON configuration with environment variable overrides
 - **CRUD wrappers** for common task areas like Processor Groups, Processors, Clients, Buckets, Flows, etc.
 - **Convenience functions** for inventory tasks, such as recursively retrieving the entire canvas, or a flat list of all Process Groups
 - **Support for scheduling and purging** flows, controller services, and connections
 - **Support for import/export** of Versioned Flows from various sources
 - **Integrated Docker workflow** with Makefile automation and profile-based testing


Please see the `issue <https://github.com/Chaffelson/nipyapi/issues>`_ register for more information on current development.

Quick Start
-----------

| **Python SDK**: Mid-level functions in *nipyapi.canvas / nipyapi.security / nipyapi.parameters / nipyapi.versioning*
| **CLI**: Shell commands via ``nipyapi <module> <function>`` (requires ``pip install nipyapi[cli]``)
| **Low-level**: Full API access via *nipyapi.nifi / nipyapi.registry*

You need a running NiFi instance to connect to. Choose the approach that fits your situation:

**Path A: Quick Start with Docker (Recommended for New Users)**

.. Note:: You will need to have Docker Desktop installed and running to use the Docker profiles.

Use our provided Docker environment for immediate testing::

    # Clone the repository (includes Docker profiles and Makefile)
    git clone https://github.com/Chaffelson/nipyapi.git
    cd nipyapi

    # Install NiPyAPI in development mode
    pip install -e ".[dev]"

    # Start complete NiFi environment (this may take a few minutes)
    make certs && make up NIPYAPI_PROFILE=single-user && make wait-ready NIPYAPI_PROFILE=single-user

    # Test the connection
    python3 -c "
    import nipyapi
    nipyapi.profiles.switch('single-user')
    version = nipyapi.system.get_nifi_version_info()
    print(f'✓ Connected to NiFi {version}')
    "

**Path B: Connect to Your Existing NiFi**

If you already have NiFi running, install and configure::

    # Install NiPyAPI
    pip install nipyapi

    # Create your own profiles.yml
    mkdir -p ~/.nipyapi
    cat > ~/.nipyapi/profiles.yml << EOF
    my-nifi:
      nifi_url: https://your-nifi-host.com/nifi-api
      registry_url: http://your-registry-host.com/nifi-registry-api
      nifi_user: your_username
      nifi_pass: your_password
      nifi_verify_ssl: true
    EOF

    # Test your custom profile
    python3 -c "
    import nipyapi
    nipyapi.config.default_profiles_file = '~/.nipyapi/profiles.yml'
    nipyapi.profiles.switch('my-nifi')
    version = nipyapi.system.get_nifi_version_info()
    print(f'✓ Connected to NiFi {version}')
    "

**Path C: Manual Configuration (Advanced)**

For advanced use cases without profiles::

    # Install NiPyAPI
    pip install nipyapi

    # Configure in Python code
    import nipyapi
    from nipyapi import config, utils

    # Configure endpoints
    config.nifi_config.host = 'https://your-nifi-host.com/nifi-api'
    config.registry_config.host = 'http://your-registry-host.com/nifi-registry-api'

    # Configure authentication
    utils.set_endpoint(config.nifi_config.host, ssl=True, login=True,
                       username='your_username', password='your_password')

**Next Steps: Start Using NiPyAPI**

Once your environment is set up, you can start using NiPyAPI::

    import nipyapi

    # If using profiles (Paths A or B)
    nipyapi.profiles.switch('single-user')  # or your custom profile name

    # Basic operations
    root_pg_id = nipyapi.canvas.get_root_pg_id()
    version = nipyapi.system.get_nifi_version_info()
    process_groups = nipyapi.canvas.list_all_process_groups()

    print(f"Connected to NiFi {version}")
    print(f"Root Process Group: {root_pg_id}")
    print(f"Found {len(process_groups)} process groups")

**Command-Line Interface:**

For shell scripting, CI/CD pipelines, and agentic workflows, install the CLI extras::

    pip install "nipyapi[cli]"

    # Set connection via environment variables
    export NIFI_API_ENDPOINT=https://your-nifi-host.com/nifi-api
    export NIFI_USERNAME=your_username
    export NIFI_PASSWORD=your_password

    # Or use a profile
    nipyapi --profile single-user system get_nifi_version_info

    # CI/CD operations
    nipyapi ci deploy_flow --bucket flows --flow my-flow
    nipyapi ci start_flow --process_group_id <id>
    nipyapi ci get_status --process_group_id <id>

See ``docs/cli.rst`` for the complete CLI reference and ``docs/ci.rst`` for CI/CD pipeline examples.
See the companion repository `nipyapi-actions <https://github.com/Chaffelson/nipyapi-actions>`_ for GitHub Actions and GitLab CI examples and support.

**Built-in Docker Profiles:**

When using Path A (Docker), these profiles are available:

- ``single-user`` - HTTP Basic authentication (easiest to start with)
- ``secure-ldap`` - LDAP authentication over TLS
- ``secure-mtls`` - Mutual TLS certificate authentication
- ``secure-oidc`` - OpenID Connect (OAuth2) authentication

See ``docs/profiles.rst`` for complete profiles documentation and ``docs/migration.rst`` for upgrading from 0.x.

**Examples and Advanced Usage:**

- **Flow Development Lifecycle**: See ``examples/fdlc.py`` for multi-environment workflow patterns
- **Interactive Sandbox**: Run ``make sandbox NIPYAPI_PROFILE=single-user`` for experimentation (requires Docker setup)
- **Custom Profiles**: Create your own ``profiles.yml`` for production environments
- **Environment Variables**: Override any setting with ``NIFI_API_ENDPOINT``, ``NIFI_USERNAME``, etc.
- **Testing Different Auth Methods**: Use ``make up NIPYAPI_PROFILE=secure-ldap`` to try LDAP authentication

Please check out the `Contribution Guide <https://github.com/Chaffelson/nipyapi/blob/main/docs/contributing.rst>`_ if you are interested in contributing to the feature set.

Background and Documentation
----------------------------

| For more information on **Apache NiFi**, please visit `https://nifi.apache.org <https://nifi.apache.org>`_
| For **complete NiPyAPI documentation**, please visit `https://nipyapi.readthedocs.io <https://nipyapi.readthedocs.io/en/latest>`_
| For **CLI and CI/CD usage**, see ``docs/cli.rst`` and ``docs/ci.rst``
| For **profiles and authentication**, see ``docs/profiles.rst`` and ``docs/security.rst``
| For **migration from 0.x to 1.x**, see ``docs/migration.rst`` in the repository


NiFi Version Support
--------------------

| **NiPyAPI 1.x targets Apache NiFi 2.x and NiFi Registry 2.x** (tested against 2.7.2).
| **For NiFi 1.x compatibility**, please use NiPyAPI 0.x branch or pin nipyapi < 1.0.0.
| **Breaking changes** exist between 0.x and 1.x - see ``docs/migration.rst`` for upgrade guidance.
| **Docker profiles require Docker Desktop** with sufficient memory (recommend 4GB+ for NiFi).
| If you find a version compatibility problem please raise an `issue <https://github.com/Chaffelson/nipyapi/issues>`_

Python Support
--------------

| **Python 3.9-12 supported**, though other versions may work.
| **Python2 is no longer supported** as of the NiPyAPI 1.0 release, please use the 0.x branch for Python2 projects.
| OSX M1 chips have been known to have had various issues with Requests and Certificates, as did Python 3.10.

| Tests are run against **upstream Apache NiFi and NiFi Registry Docker images** via integrated Makefile automation.
| **Profile-driven testing** supports single-user, LDAP, mTLS, and OIDC authentication modes.
| Developed on **macOS 14+ and Windows 10**.
| **Runtime dependencies**: requests/urllib3, PyYAML, PySocks. CLI extras add google-fire.
| **Development tools**: Comprehensive Makefile with ``make up``, ``make test``, ``make sandbox`` targets.
