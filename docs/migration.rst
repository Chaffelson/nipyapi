===============
Migration Guide
===============

Upgrading from NiPyAPI 0.x/NiFi 1.x to NiPyAPI 1.x/NiFi 2.x
-------------------------------------------------------------

This guide helps you migrate existing code from NiPyAPI 0.x (targeting Apache NiFi/Registry 1.x) to NiPyAPI 1.x (targeting Apache NiFi/Registry 2.x).

.. note::
   **Breaking Changes**: This is a major version upgrade with significant breaking changes.
   Plan for code updates and testing when migrating.

.. note::
   **New in 1.x**: The **Profiles System** provides centralized configuration management.
   You can use profiles, environment variables, or direct configuration - all approaches work with the same underlying system.

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
| **Python**       | 2.7, 3.6+            | 3.9+                 |
+------------------+----------------------+----------------------+

Understanding Migration Scope
------------------------------

.. important::
   **NiPyAPI Migration ≠ NiFi Flow Migration**

   Upgrading NiPyAPI from 0.x to 1.x **does not automatically migrate your NiFi flows** from NiFi 1.x to 2.x.
   These are separate migration processes:

**What NiPyAPI 1.x Migration Covers:**

- Python client library compatibility with NiFi 2.x APIs
- Authentication and connection management
- SDK function names and parameters
- Configuration and deployment automation

**What NiFi Flow Migration Requires Separately:**

- **Processor Updates**: Many processors have new names, properties, or behaviors in NiFi 2.x
- **Controller Service Changes**: Connection pool configurations, SSL contexts, and service properties
- **Expression Language**: Some expression language functions and syntax have changed
- **Flow Structure**: Deprecated components need replacement with 2.x equivalents
- **Property Validation**: New validation rules and required properties
- **Deprecations**: Variable Registry and Templates are deprecated, use Parameters and Git versioning instead.

**How NiPyAPI 1.x Can Help Your Flow Migration:**

NiPyAPI 1.x provides powerful automation tools for flow migration tasks:

- **Flow Analysis**: Inventory processors, controller services, and configurations across environments
- **Bulk Updates**: Programmatically update processor properties and relationships
- **Version Control**: Export, modify, and import flows through NiFi Registry
- **Environment Promotion**: Move updated flows between development, staging, and production
- **Migration Scripts**: Automate repetitive flow update tasks
- **Validation Functions**: Report on invalid processors, controller services, and connections
- **Sandbox Environment**: Test different authentication mechanisms with ``make sandbox`` target
- **Parameter Management**: Manage parameters across environments

You can continue to use NiPyAPI 0.x with NiFi 1.x, and NiPyAPI 1.x with NiFi 2.x to assist with the migration process.

For NiFi-specific migration guidance, consult the `Apache NiFi Migration Guide <https://cwiki.apache.org/confluence/display/NIFI/Migrating+Deprecated+Components+and+Features+for+2.0.0>`_ and your organization's NiFi administrators.

Major Changes Summary
---------------------

**Breaking Changes - Action Required**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Function renaming**: Upstream API specification changes result in operation IDs now using suffixed names (e.g., ``update_run_status1``) and some other functions are also renamed
- **Authentication and configuration overhaul**: Significant changes to align with modern API standards and upstream API changes
- **Users must review and update authentication patterns** - legacy configuration methods will be different

**Removed Features**
~~~~~~~~~~~~~~~~~~~~

- **Templates API**: Deprecated in NiFi 2.x - use Process Groups and Git or Flow Registry instead
- **Python 2.7 Support**: EOL, dropped in favor of modern Python 3.9+
- **Legacy Authentication**: Simplified to modern bearer token approach

**NEW: Profile Management System**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Extensible file format** (YAML/JSON) with **environment variable overrides** and **sane defaults** - familiar workflow like AWS CLI
- **Intelligent authentication method detection**: OIDC, mTLS, and Basic authentication based on available configuration parameters
- **Built-in profiles** for common deployment patterns: ``single-user``, ``secure-ldap``, ``secure-mtls``, ``secure-oidc``
- **Extensible profiles** with provided ``examples/profiles.yml`` as a starting point, or create your own
- **15+ configurable parameters** (URLs, credentials, certificates, SSL settings) with environment variable overrides
- **Profile switching** with ``nipyapi.profiles.switch()`` configures endpoints, authentication, and SSL settings in single function call configurable directly or with ``NIPYAPI_PROFILE`` environment variable

**Enhanced Development Workflow**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Comprehensive Makefile targets** for all key development and release processes
- **End-to-end automation**: entire client generation and testing sequence from test certificates to final integration tests
- **GitHub Actions CI** with full Docker NiFi integration tests and coverage reporting
- **Sandbox Docker environment** for testing different authentication mechanisms with ``make sandbox`` target

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

Understanding the Profiles System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NiPyAPI 1.x introduces a **centralized configuration system** that eliminates the need for complex manual setup. The system revolves around two key components:

1. **Configuration File**: ``examples/profiles.yml`` (or your custom file)
2. **Python Interface**: ``nipyapi.profiles.switch('profile-name')``

**How it works:**

.. code-block:: python

    # 1. Profiles file defines your environments
    # examples/profiles.yml contains: single-user, secure-ldap, secure-mtls, secure-oidc

    # 2. Switch to any environment with one function call
    import nipyapi
    nipyapi.profiles.switch('single-user')  # Configures everything automatically

    # 3. Use NiPyAPI normally - authentication and SSL are handled
    about = nipyapi.system.get_nifi_version_info()

**Why this matters for migration:**

- **0.x approach**: 10+ lines of manual configuration per environment
- **1.x approach**: 1 line switches entire environment configuration
- **Zero code changes** needed to switch between dev/staging/production

**Understanding the Profiles System**

The profiles system was introduced to solve environment configuration complexity in 0.x. Instead of manually configuring multiple services, certificates, and authentication for each environment, profiles provide centralized configuration management through YAML files.

For complete profile configuration and usage details, see ``docs/profiles.rst``.

**Migration Strategy:**
1. Create profiles.yml defining your environments (or use ``examples/profiles.yml`` for testing)
2. Replace manual configuration blocks with ``nipyapi.profiles.switch('profile-name')`` calls
3. Test each environment switch to ensure authentication and SSL work correctly

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
     - ``NIFI_CA_CERT_PATH`` (profiles) or ``TLS_CA_CERT_PATH`` (shared)
     - **REMOVED** - Use profiles system or direct config

**Authentication Migration Strategy**

The 1.x authentication approach is **profiles-first**. Instead of manually configuring each service, define your authentication in profiles.yml and let the system handle the complexity. The old calls are still present, but the new method is intended to remove the complexity of understanding the underlying authentication mechanisms.

**Old approach (0.x) - Manual configuration**:

.. code-block:: python

    # 0.x: Complex manual setup (DO NOT USE in 1.x)
    import nipyapi
    nipyapi.config.nifi_config.ssl_ca_cert = nipyapi.config.default_ssl_context["ca_file"]
    nipyapi.utils.set_endpoint("https://localhost:8443/nifi-api", ssl=True, login=True,
                              username="nobel", password="supersecret1!")

**New approach (1.x) - Profiles-based configuration**:

.. code-block:: python

    # 1.x: Profiles handle everything automatically (RECOMMENDED)
    import nipyapi

    # For development/testing (uses examples/profiles.yml)
    nipyapi.profiles.switch('single-user')

    # For your production environment (uses custom profiles.yml)
    nipyapi.profiles.switch('production', profiles_file='/etc/nipyapi/profiles.yml')

    # Environment variables can override any profile setting
    # export NIFI_API_ENDPOINT=https://special.endpoint.com/nifi-api
    # export NIFI_USERNAME=override_user
    nipyapi.profiles.switch('single-user')  # Uses environment overrides

**Manual Configuration**:

.. code-block:: python

    # 1.x: Manual configuration still supported but more verbose
    import nipyapi
    from nipyapi import config, utils

    # HTTPS is now the default with proper certificate management
    config.nifi_config.ssl_ca_cert = "resources/certs/ca/ca.crt"

    # Establish authenticated endpoint
    utils.set_endpoint("https://localhost:9443/nifi-api", ssl=True, login=True,
                      username="einstein", password="password1234")

**What profiles.yml handles for you:**

- **Endpoints**: NiFi and Registry URLs
- **Authentication**: Username/password, certificates, OIDC tokens
- **SSL Configuration**: CA certificates, SSL verification, hostname checking, warning suppression
- **Service Integration**: NiFi → Registry proxy identity
- **Environment Flexibility**: Development vs production settings with smart SSL defaults

**Docker Environment and Testing**

We now use the ``Makefile`` to start and stop the Docker environment, with integrated profiles support.

**Integrated Docker + Profiles Workflow**

.. code-block:: shell

   # One-command environment setup
   make certs && make up NIPYAPI_PROFILE=secure-ldap && make wait-ready NIPYAPI_PROFILE=secure-ldap

   # Python code matches the environment
   nipyapi.profiles.switch('secure-ldap')

   # Testing with the same profile
   make test NIPYAPI_PROFILE=secure-ldap

**Old commands**::

    # 0.x approach
    cd resources/docker/some_profile
    docker-compose up -d

**New commands**::

    # 1.x approach
    make up NIPYAPI_PROFILE=secure-ldap
    make wait-ready NIPYAPI_PROFILE=secure-ldap

**Development vs Production Security**

**Development (Self-signed certificates)**::

    # Quick setup for learning and testing
    make certs
    make up NIPYAPI_PROFILE=single-user
    nipyapi.profiles.switch('single-user')

    # SSL warnings are safely suppressed in development
    nipyapi.config.disable_insecure_request_warnings = True

**Production (Trusted certificates)**::

    # Use trusted CA certificates
    export TLS_CA_CERT_PATH=/etc/ssl/certs/ca-bundle.crt
    export NIFI_API_ENDPOINT=https://nifi.company.com/nifi-api
    export NIFI_USERNAME=service_account

    # SSL verification is always enabled in production
    nipyapi.profiles.switch('production')

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

Due to upstream NiFi 2.x API changes, many operation IDs now use suffixed names. **You must update your code**:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Old Method (0.x)
     - New Method (1.x)
     - Status
   * - ``update_run_status``
     - ``update_run_status1``
     - **Renamed - Action Required**
   * - ``FlowfileQueuesApi``
     - ``FlowFileQueuesApi``
     - Case change
   * - Various processor operations
     - Many now have ``1`` suffix
     - **Check your API calls**

.. important::
   **Function Renaming**: Upstream API specification changes result in operation IDs now using suffixed names.
   If you get ``AttributeError`` exceptions, check for renamed operations - many now have '1' suffix.

**Common Migration Pattern**:

.. code-block:: python

    # Before (0.x)
    api.update_run_status(processor_id, request_body)

    # After (1.x) - Note the '1' suffix
    api.update_run_status1(processor_id, request_body)

**Updated: Controller Service Management**

Old approach (0.x)::

    # 0.x pattern
    nipyapi.canvas.schedule_controller_service(service_id, scheduled=True)

New approach (1.x)::

    # 1.x pattern - uses different underlying API endpoint
    nipyapi.canvas.schedule_controller_service(service_id, scheduled=True)
    # Implementation uses ControllerServicesApi.update_run_status1()

.. Note:: Behavior of the new mthods may be the same, but you should test carefully.

Configuration Changes
~~~~~~~~~~~~~~~~~~~~~

**SSL/TLS Configuration**

NiPyAPI 1.x introduces **smart SSL defaults** and **granular SSL controls**:

**Smart SSL Defaults (NEW in 1.x)**::

    # SSL verification automatically enabled for HTTPS URLs
    nifi_url: https://nifi.company.com/nifi-api     # verify_ssl=true (automatic)
    registry_url: http://registry.company.com/      # verify_ssl=false (automatic)

**Granular SSL Controls (NEW in 1.x)**::

    # Development profile with self-signed certificates
    nifi_verify_ssl: false             # Disable SSL verification (cert + hostname) for HTTPS
    suppress_ssl_warnings: true        # Suppress urllib3 warnings for development

    # Production profile with trusted certificates
    nifi_verify_ssl: true              # Enable full SSL verification (default for HTTPS)
    suppress_ssl_warnings: false       # Show all SSL warnings

**Key SSL Behavior Changes from 0.x to 1.x:**

**1. SSL Parameter in set_endpoint()**

Old behavior (0.x)::

    # ssl=True parameter enabled SSL verification with default system behavior
    nipyapi.utils.set_endpoint("https://localhost:8443/nifi-api", ssl=True, login=True,
                              username="nobel", password="supersecret1!")
    # SSL verification was system-dependent and not granularly controlled

New behavior (1.x)::

    # ssl=True still works, but now respects granular configuration
    nipyapi.config.nifi_config.verify_ssl = True           # Explicit SSL verification control (cert + hostname)
    nipyapi.utils.set_endpoint("https://localhost:9443/nifi-api", ssl=True, login=True,
                              username="einstein", password="password1234")

**2. SSL Context Configuration**

Old approach (0.x)::

    # NIFI_CA_CERT is no longer supported in 1.x
    # Use direct configuration instead
    nipyapi.config.nifi_config.ssl_ca_cert = '/path/to/ca.pem'

New approach (1.x) - Direct Configuration::

    import nipyapi
    # Direct configuration (no default_ssl_context needed)
    nipyapi.config.nifi_config.ssl_ca_cert = '/path/to/ca.pem'
    nipyapi.config.registry_config.ssl_ca_cert = '/path/to/ca.pem'  # Per-service control
    nipyapi.config.nifi_config.verify_ssl = True                   # Full SSL verification (cert + hostname)

New approach (1.x) - Profiles (Recommended)::

    # Use profiles with smart defaults - handles all SSL complexity
    nipyapi.profiles.switch('production')  # All SSL settings configured automatically

**3. SSL Configuration Complexity Reduction**

SSL configuration approach changes:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Aspect
     - 0.x Approach
     - 1.x Approach
   * - **SSL Configuration**
     - Complex: global settings + env vars + manual config
     - Simple: profiles with smart defaults
   * - **Per-Service Control**
     - Global ``global_ssl_verify`` affects both services
     - Independent ``nifi_verify_ssl`` / ``registry_verify_ssl``
   * - **Hostname Checking**
     - Global ``global_ssl_host_check`` setting
     - Integrated with ``nifi_verify_ssl`` / ``registry_verify_ssl`` (when false, hostname checking is disabled)
   * - **Certificate Management**
     - Environment variables (``NIFI_CA_CERT`` - **REMOVED**) + ``default_ssl_context``
     - Profiles with shared/per-service certificates + smart resolution
   * - **Configuration Style**
     - Manual: Set globals, env vars, then configure each service
     - Declarative: Define environment in profile, apply with one call

**4. Enhanced SSL Controls (1.x)**

**0.x approach - Global settings affecting both services:**

.. code-block:: python

    # 0.x: Global SSL settings affected both NiFi and Registry
    nipyapi.config.global_ssl_verify = True            # Applied to both services
    nipyapi.config.global_ssl_host_check = True        # Applied to both services
    nipyapi.config.disable_insecure_request_warnings = False

    # Direct certificate configuration (NIFI_CA_CERT no longer supported)
    nipyapi.config.nifi_config.ssl_ca_cert = '/path/to/ca.pem'

**1.x approach - Per-service granular control:**

.. code-block:: yaml

    # 1.x: Fine-grained per-service SSL control in profiles
    nifi_verify_ssl: true              # Independent NiFi SSL verification (cert + hostname)
    registry_verify_ssl: false         # Independent Registry SSL control (no verification)
    suppress_ssl_warnings: true        # Global warning suppression (cleaner than 0.x)

**Complexity Comparison Example:**

.. code-block:: python

    # 0.x: Complex multi-step configuration (10+ lines)
    import os
    import nipyapi

    # Step 1: Set global SSL settings
    nipyapi.config.global_ssl_verify = True
    nipyapi.config.global_ssl_host_check = False  # But this affects BOTH services!
    nipyapi.config.disable_insecure_request_warnings = True

    # Step 2: Direct configuration (NIFI_CA_CERT no longer supported)
    nipyapi.config.nifi_config.ssl_ca_cert = '/path/to/ca.pem'

    # Step 4: Manually configure each service endpoint
    nipyapi.utils.set_endpoint("https://localhost:8443/nifi-api", ssl=True, login=True)
    # Registry SSL settings? More complex configuration needed...

    # vs.

    # 1.x: Simple declarative configuration (1 line)
    nipyapi.profiles.switch('single-user')  # Everything configured automatically

**Common SSL Migration Issues and Solutions:**

**Issue: "ssl=True doesn't work like it used to"**

In 0.x, ``ssl=True`` behavior was system-dependent. In 1.x, it respects explicit configuration:

.. code-block:: python

   # 1.x: Configure SSL explicitly before calling set_endpoint
   nipyapi.config.nifi_config.verify_ssl = True
   nipyapi.config.nifi_config.ssl_ca_cert = '/path/to/ca.pem'
   nipyapi.utils.set_endpoint(url, ssl=True, login=True)

**Issue: "Self-signed certificates cause hostname errors"**

0.x had system-dependent hostname checking. 1.x provides granular control:

.. code-block:: python

   # For development with self-signed certificates
   nipyapi.config.nifi_config.verify_ssl = False          # Accept self-signed certs (disables cert + hostname verification)

**Issue: "Different SSL requirements for NiFi vs Registry"**

0.x primarily supported NiFi. 1.x supports independent SSL configuration:

.. code-block:: python

   # 1.x: Independent SSL control per service
   nipyapi.config.nifi_config.verify_ssl = True           # HTTPS with trusted certs
   nipyapi.config.registry_config.verify_ssl = False      # HTTP or self-signed

**Testing Profiles**

Old commands::

    pytest tests/

New commands::

    make test NIPYAPI_PROFILE=secure-ldap
    # or
    NIPYAPI_PROFILE=secure-ldap pytest tests/

See the ``devnotes.rst`` guide for more details.

New Authentication Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~

NiPyAPI 1.x adds support for modern authentication:

**OpenID Connect (OIDC)**::

    # OAuth2 with external identity providers
    nipyapi.profiles.switch('secure-oidc')
    # Supports Keycloak, Okta, Azure AD, etc.

**Enhanced mTLS**::

    # Certificate-based authentication
    nipyapi.profiles.switch('secure-mtls')
    # Simplified certificate management

**Environment Variable Integration**::

    # Override any profile setting
    export NIFI_API_ENDPOINT=https://production.company.com/nifi-api
    export NIFI_USERNAME=production_user
    export NIFI_DISABLE_HOST_CHECK=true         # Disable hostname verification
    export NIPYAPI_SUPPRESS_SSL_WARNINGS=true   # Suppress SSL warnings
    nipyapi.profiles.switch('single-user')  # Uses overrides

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

2. **Choose Your Profiles Strategy**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Strategy A: Start with Built-in Profiles (Recommended)**

Use the provided ``examples/profiles.yml`` for immediate compatibility:

.. code-block:: python

   # Test with development Docker environment
   nipyapi.profiles.switch('single-user')

   # Validate connection
   version = nipyapi.system.get_nifi_version_info()
   print(f"Connected to NiFi {version}")

**Strategy B: Create Custom Profiles**

Create your own ``profiles.yml`` for your environments:

.. code-block:: bash

   # Copy the example as a starting point
   cp examples/profiles.yml ~/.nipyapi/profiles.yml

   # Edit for your environments
   vim ~/.nipyapi/profiles.yml

**Strategy C: Environment-Driven Configuration**

Use profiles with environment variable overrides:

.. code-block:: python

   # Code stays the same across environments
   nipyapi.profiles.switch('base-profile')

   # Environment variables control the actual connection
   # export NIFI_API_ENDPOINT=https://nifi.staging.com/nifi-api  # staging
   # export NIFI_API_ENDPOINT=https://nifi.company.com/nifi-api  # production

3. **Test Your Profile Configuration**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validate your profiles work before migrating production code:

.. code-block:: python

   import nipyapi

   # Test profile loading
   try:
       nipyapi.profiles.switch('your-profile-name')
       print("✓ Profile loaded successfully")
   except Exception as e:
       print(f"✗ Profile error: {e}")

   # Test connectivity
   try:
       version = nipyapi.system.get_nifi_version_info()
       print(f"✓ Connected to NiFi {version}")
   except Exception as e:
       print(f"✗ Connection error: {e}")

4. **Update Your Application Code**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Replace manual configuration with profile switching:**

.. code-block:: python

   # Before (0.x) - Complex setup
   import nipyapi
   nipyapi.config.nifi_config.ssl_ca_cert = "/path/to/ca.pem"
   nipyapi.utils.set_endpoint("https://nifi.com/nifi-api", ssl=True, login=True,
                             username="user", password="pass")
   # ... 10+ more configuration lines ...

   # After (1.x) - Simple profile switch
   import nipyapi
   nipyapi.profiles.switch('production')

   # Your existing business logic stays the same
   flows = nipyapi.canvas.list_all_process_groups()
   about = nipyapi.system.get_nifi_version_info()

**Fix renamed function calls:**

.. code-block:: python

   # Before (0.x)
   api.update_run_status(processor_id, request_body)

   # After (1.x) - Note the '1' suffix
   api.update_run_status1(processor_id, request_body)

5. **Update Testing Environment**
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

6. **Remove Templates Usage**
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

.. Note:: An example of using NiFi Registry is provided in ``examples/fdlc.py``


7. **Update Configuration and Ports**
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

   nipyapi.profiles.switch('production')

**Issue: Operation Not Found**

.. code-block:: text

   AttributeError: 'ProcessGroupsApi' object has no attribute 'update_run_status'

**Solution**: Check for renamed operations (many now have '1' suffix):

.. code-block:: python

   # Old: update_run_status
   # New: update_run_status1

.. important::
   **Function Renaming**: This is the most common migration issue. Upstream API specification changes result in operation IDs now using suffixed names. If you get AttributeError exceptions, check for renamed operations.

**Systematic approach to find renamed functions:**

.. code-block:: python

   # Use dir() to find available methods
   import nipyapi
   api = nipyapi.nifi.ProcessGroupsApi()
   methods = [m for m in dir(api) if 'update' in m.lower()]
   print(methods)  # Will show: ['update_run_status1', ...]

   # Or check the API documentation
   help(api.update_run_status1)

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

.. Note:: You can find examples of using the boostrap functions in ``examples/sandbox.py``

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

.. Important:: Reversing the DN will not work, as it's an exact match.

**Issue: OIDC Authentication Setup**

.. code-block:: text

   No applicable policies could be found
   Untrusted proxy identity

**Solution**: OIDC requires one-time manual setup due to NiFi's security architecture:

.. code-block:: shell

   # 1. Use sandbox to discover your OIDC application UUID
   make sandbox NIPYAPI_PROFILE=secure-oidc

   # 2. Follow the printed instructions to create the user and assign policies in NiFi UI
   # 3. Re-run sandbox to complete bootstrap
   make sandbox NIPYAPI_PROFILE=secure-oidc

See the ``security.rst`` guide for detailed OIDC setup instructions, or follow the sandbox.

Quick Migration Checklist
--------------------------

☐ **Update dependencies**: ``nipyapi>=1.0,<2.0``

☐ **Choose migration approach**:
   - ✅ **Recommended**: Use profiles (``nipyapi.profiles.switch('single-user')``)
   - **Manual**: Direct programmatic configuration (more control)

☐ **Test with Docker environment**:
   - ``make certs && make up NIPYAPI_PROFILE=single-user`` for development
   - ``make test NIPYAPI_PROFILE=single-user`` to validate

☐ **Handle breaking changes**:
   - Replace ``update_run_status`` with ``update_run_status1`` (check all API calls)
   - Remove templates usage → use Registry flows
   - Remove variable registry usage → use Parameters
   - Replace invalid Processors/Controller Services → use replacement components
   - Update certificate paths (``demo/keys/`` → ``resources/certs/``)
   - Update default ports (8080 → 9443 for NiFi, credentials: nobel → einstein)

☐ **Migrate SSL configuration**:
   - Replace ``nipyapi.config.default_ssl_context`` pattern with profile configuration
   - Update ``ssl=True`` usage to explicitly configure ``verify_ssl`` per service
   - Replace ``NIFI_CA_CERT`` environment variables (**REMOVED**) with ``NIFI_CA_CERT_PATH`` (profiles), ``TLS_CA_CERT_PATH`` (shared), ``REQUESTS_CA_BUNDLE`` (standard), or direct config
   - For self-signed certificates, set ``verify_ssl: false`` (disables both cert and hostname verification)
   - Configure per-service SSL settings for NiFi and Registry independently
   - Use profiles for centralized SSL management (recommended)

☐ **Production deployment**:
   - Set environment variables or Profiles for credentials/endpoints
   - Use trusted certificates (not self-signed)
   - Enable SSL verification (default in production profiles)

Testing Your Migration
-----------------------

1. **Start Simple**: Begin with single-user profile testing
2. **Incremental Migration**: Migrate one authentication mode at a time
3. **Integration Testing**: Use ``make test NIPYAPI_PROFILE=single-user`` for comprehensive validation
4. **Docker Environment**: Test with provided Docker profiles before production

For additional support:

- **Examples**: See ``examples/fdlc.py`` for modern patterns
- **Sandbox**: Use ``make sandbox NIPYAPI_PROFILE=single-user`` for experimentation
- **Documentation**: Updated profiles guide at ``docs/profiles.rst`` and security guide at ``docs/security.rst``
- **Issues**: Please raise an issue on `GitHub <https://github.com/Chaffelson/nipyapi/issues>`_ if you encounter any problems.
