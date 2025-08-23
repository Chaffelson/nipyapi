===============
Migration Guide
===============

Upgrading from NiPyAPI 0.x/NiFi 1.x to NiPyAPI 1.x/NiFi 2.x
-------------------------------------------------------------

This guide helps you migrate existing code from NiPyAPI 0.x (targeting Apache NiFi/Registry 1.x) to NiPyAPI 1.x (targeting Apache NiFi/Registry 2.x).

.. note::
   **Breaking Changes**: This is a major version upgrade with significant breaking changes.
   Plan for code updates and testing when migrating.

Version Overview
----------------

+------------------+----------------------+----------------------+
| Component        | Old Version (0.x)    | New Version (1.x)    |
+==================+======================+======================+
| **NiPyAPI**      | 0.x                  | 1.x                  |
+------------------+----------------------+----------------------+
| **Apache NiFi**  | 1.x (tested: 1.28.1)| 2.x (tested: 2.5.0)   |
+------------------+----------------------+----------------------+
| **NiFi Registry**| 0.x, 1.x             | 2.x (tested: 2.5.0)  |
+------------------+----------------------+----------------------+
| **Python**       | 2.7, 3.6+           | 3.9+                  |
+------------------+----------------------+----------------------+

Major Changes Summary
---------------------

**Removed Features**
~~~~~~~~~~~~~~~~~~~~

- **Templates API**: Deprecated in NiFi 2.x
- **Python 2.7 Support**: EOL, dropped in favor of modern Python 3.9+
- **Legacy Authentication**: Simplified to modern bearer token approach

**Updated APIs**
~~~~~~~~~~~~~~~~

- **Client Generation**: Now uses OpenAPI 3.x specs with swagger-codegen v3
- **Authentication**: Bearer token-based authentication replacing custom token handling
- **Renamed Operations**: Updated to match upstream NiFi 2.x naming (e.g., ``update_run_status1``)

**Enhanced Features**
~~~~~~~~~~~~~~~~~~~~~

- **Docker Profiles**: Streamlined LDAP, mTLS, and single-user configurations
- **Security**: Enhanced certificate management and authentication flows
- **Documentation**: Completely restructured with individual API pages
- **Build System**: Modern Python packaging with ``pyproject.toml`` and ``Makefile``

Breaking Changes
----------------

Authentication and Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Environment Variables**

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Old (0.x)
     - New (1.x)
     - Notes
   * - ``test_default = True`` (in conftest.py)
     - ``NIPYAPI_PROFILE``
     - Environment variable replaces file editing
   * - ``NIFI_CA_CERT``
     - ``config.nifi_config.ssl_ca_cert``
     - Programmatic configuration preferred

**Authentication Setup**

Old approach (0.x)::

    import nipyapi

    # Default endpoints were HTTP
    # nifi_config.host = "http://localhost:8080/nifi-api"  (default)
    # registry_config.host = "http://localhost:18080/nifi-registry-api"  (default)

    # For secure endpoints, manual SSL context setup was required
    nipyapi.config.nifi_config.ssl_ca_cert = nipyapi.config.default_ssl_context["ca_file"]
    nipyapi.utils.set_endpoint("https://localhost:8443/nifi-api", ssl=True, login=True,
                              username="nobel", password="supersecret1!")

New approach (1.x)::

    import nipyapi
    from nipyapi import config, utils

    # HTTPS is now the default with proper certificate management
    config.nifi_config.ssl_ca_cert = "resources/certs/ca/ca.crt"

    # Establish authenticated endpoint
    utils.set_endpoint("https://localhost:9443/nifi-api", ssl=True, login=True,
                      username="einstein", password="password1234")

**Docker Environment**

We now use the ``Makefile`` to start and stop the Docker environment, and the profiles do not conflict.

Old commands::

    # 0.x approach
    cd resources/docker/some_profile
    docker-compose up -d

New commands::

    # 1.x approach
    make up NIPYAPI_PROFILE=secure-ldap
    make wait-ready NIPYAPI_PROFILE=secure-ldap

API Changes
~~~~~~~~~~~

**Removed: Templates**

Old code (0.x)::

    import nipyapi.templates
    templates = nipyapi.templates.list_all_templates()

Migration strategy::

    # Templates are deprecated in NiFi 2.x
    # Use Process Groups and Flow Registry instead:
    import nipyapi.canvas
    import nipyapi.versioning

    # Create reusable flows in Registry
    flow = nipyapi.versioning.save_flow_ver(process_group, registry_client, bucket)

**Updated: Operation Names**

Some operation IDs have changed to match NiFi 2.x:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Old Method (0.x)
     - New Method (1.x)
     - Status
   * - ``update_run_status``
     - ``update_run_status1``
     - Renamed
   * - ``FlowfileQueuesApi``
     - ``FlowFileQueuesApi``
     - Case change

**Updated: Controller Service Management**

Old approach (0.x)::

    # 0.x pattern
    nipyapi.canvas.schedule_controller_service(service_id, scheduled=True)

New approach (1.x)::

    # 1.x pattern - uses different underlying API endpoint
    nipyapi.canvas.schedule_controller_service(service_id, scheduled=True)
    # Implementation uses ControllerServicesApi.update_run_status1()

Configuration Changes
~~~~~~~~~~~~~~~~~~~~~

**SSL/TLS Configuration**

Old approach (0.x)::

    import os
    # Only applied to NiFi, not Registry
    os.environ['NIFI_CA_CERT'] = '/path/to/ca.pem'

New approach (1.x)::

    import nipyapi
    # Now applies to both NiFi and Registry
    nipyapi.config.nifi_config.ssl_ca_cert = '/path/to/ca.pem'
    nipyapi.config.registry_config.ssl_ca_cert = '/path/to/ca.pem'

**Testing Profiles**

Old commands::

    pytest tests/

New commands::

    make test NIPYAPI_PROFILE=secure-ldap
    # or
    NIPYAPI_PROFILE=secure-ldap pytest tests/

See the ``devnotes.rst`` guide for more details.

Migration Steps
---------------

1. **Update Dependencies**
~~~~~~~~~~~~~~~~~~~~~~~~~~

Update your ``requirements.txt`` or ``pyproject.toml``:

.. code-block:: text

   # Old
   nipyapi>=0.22,<1.0

   # New
   nipyapi>=1.0,<2.0

2. **Update Authentication Code**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The 0.x approach used hardcoded SSL context and different default endpoints:

.. code-block:: python

   # 0.x approach (with default_ssl_context)
   import nipyapi
   # Used demo/keys/ certificates and HTTP by default
   nipyapi.utils.set_endpoint("http://localhost:8080/nifi-api")

   # 0.x with SSL (manual cert paths)
   nipyapi.config.nifi_config.ssl_ca_cert = nipyapi.config.default_ssl_context["ca_file"]
   nipyapi.utils.set_endpoint("https://localhost:8443/nifi-api", ssl=True, login=True,
                             username="nobel", password="supersecret1!")

   # 1.x preferred approach
   import nipyapi
   from nipyapi import config, utils

   # New certificate structure and HTTPS by default
   config.nifi_config.ssl_ca_cert = 'resources/certs/ca/ca.crt'
   utils.set_endpoint("https://localhost:9443/nifi-api", ssl=True, login=True,
                     username="einstein", password="password1234")

See the ``authentication.rst`` guide for more details.

3. **Update Testing Environment**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The 0.x testing used hardcoded boolean flags in ``conftest.py``, not environment variables:

.. code-block:: python

   # 0.x approach (edit conftest.py)
   # In tests/conftest.py:
   test_default = True   # Test against default endpoints
   test_ldap = False     # Enable LDAP testing
   test_mtls = False     # Enable mTLS testing

   # Then run tests directly
   pytest tests/

The 1.x approach uses environment-driven profiles:

.. code-block:: shell

   # 1.x approach (environment-driven)
   make up NIPYAPI_PROFILE=secure-ldap
   make wait-ready NIPYAPI_PROFILE=secure-ldap
   make test NIPYAPI_PROFILE=secure-ldap

See the ``devnotes.rst`` guide for more details.

4. **Remove Templates Usage**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replace template-based workflows with Process Groups and Registry:

.. code-block:: python

   # Before (0.x) - Templates
   import nipyapi.templates
   template = nipyapi.templates.upload_template('flow.xml')
   nipyapi.templates.deploy_template(pg_id, template.id)

   # After (1.x) - Registry Flows
   import nipyapi.versioning
   # Save flow to registry
   flow_ver = nipyapi.versioning.save_flow_ver(pg, registry_client, bucket)
   # Deploy to other environments
   deployed_pg = nipyapi.versioning.deploy_flow_version(
       parent_pg_id, registry_client.id, bucket.identifier, flow_ver.flow.identifier
   )

5. **Update Configuration and Ports**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Key configuration changes between NiPyAPI 0.x and 1.x:

.. list-table::
   :header-rows: 1
   :widths: 25 35 35

   * - Component
     - 0.x (NiFi 1.x)
     - 1.x (NiFi 2.x)
   * - **Default NiFi**
     - ``http://localhost:8080/nifi-api``
     - ``https://localhost:9443/nifi-api``
   * - **Default Registry**
     - ``http://localhost:18080/nifi-registry-api``
     - ``http://localhost:18080/nifi-registry-api``
   * - **Test Credentials**
     - ``nobel/supersecret1!`` (default)
     - ``einstein/password1234`` (single-user)
   * - **LDAP Credentials**
     - ``nobel/password``
     - ``einstein/password``
   * - **Certificate Location**
     - ``demo/keys/`` (localhost-ts.pem)
     - ``resources/certs/`` (ca.crt)
   * - **Docker Test Ports**
     - Default: 8443, LDAP: 9443
     - Single: 9443, LDAP: 9444, mTLS: 9445

Common Migration Issues
-----------------------

**Issue: SSL Certificate Errors**

.. code-block:: text

   SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed

**Solution**: Ensure mounted and presented certificates are valid. Then configure CA certificate properly:

.. code-block:: python

   nipyapi.config.nifi_config.ssl_ca_cert = 'resources/certs/ca/ca.crt'

See the ``authentication.rst`` guide for more details.

**Issue: Authentication Failures**

.. code-block:: text

   Unauthorized: No valid authentication

**Solution**: Use proper authentication flow:

.. code-block:: python

   utils.set_endpoint(url, ssl=True, login=True, username='user', password='pass')

**Issue: Operation Not Found**

.. code-block:: text

   AttributeError: 'ProcessGroupsApi' object has no attribute 'update_run_status'

**Solution**: Check for renamed operations (many now have '1' suffix):

.. code-block:: python

   # Old: update_run_status
   # New: update_run_status1

**Issue: Authorization Failures After Authentication**

.. code-block:: text

   No applicable policies could be found
   Forbidden: Access is denied due to insufficient permissions

Note: NiFi 2.x is more strict by default about Authentication and Authorization.

**Solution**: Bootstrap security policies for secure profiles:

.. code-block:: python

   # For NiFi operations
   nipyapi.security.bootstrap_security_policies(service='nifi')

   # For Registry operations (with proxy identity)
   nipyapi.security.bootstrap_security_policies(
       service='registry',
       nifi_proxy_identity='C=US, O=NiPyAPI, CN=nifi'
   )

**Issue: Registry Proxy Identity Not Authorized**

.. code-block:: text

   Untrusted proxy
   Unable to list buckets: access denied

**Solution**: Ensure Registry proxy configuration is set up:

.. code-block:: python

   # Registry must trust NiFi as a proxy
   nipyapi.security.bootstrap_security_policies(
       service='registry',
       nifi_proxy_identity='C=US, O=NiPyAPI, CN=nifi'
   )

The proxy identity must match the NiFi certificate subject DN when using secure profiles.

Testing Your Migration
-----------------------

1. **Start Simple**: Begin with single-user profile testing
2. **Incremental Migration**: Migrate one authentication mode at a time
3. **Integration Testing**: Use ``make test-all`` for comprehensive validation
4. **Docker Environment**: Test with provided Docker profiles before production

For additional support:

- **Examples**: See ``examples/fdlc.py`` for modern patterns
- **sandbox**: Use ``make sandbox NIPYAPI_PROFILE=single-user`` for experimentation
- **Documentation**: Updated authentication guide at ``docs/authentication.rst``
- **Issues**: Please raise an issue on `GitHub <https://github.com/Chaffelson/nipyapi/issues>`_ if you encounter any problems.
