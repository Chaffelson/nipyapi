.. highlight:: python

=======================
Security with NiPyAPI 2
=======================

NiPyAPI 1.x targets Apache NiFi 2.x and NiFi Registry 2.x, which prefer secure-by-default deployments.
This page covers authentication methods, SSL/TLS configuration, certificate management, and security practices
for both development and production environments.

.. note::
   **Quick Environment Switching:**

   For simplified workflow-focused configuration management, see `Environment Profiles <profiles.html>`_.
   Profiles provide a centralized way to switch between development, testing, and production environments
   with a single function call. This page focuses on the underlying technical authentication mechanisms.

.. note::
   **Test vs Production Certificates:**

   Example snippets below use the NiPyAPI repository's generated test certificates (``resources/certs/``)
   and localhost URLs for demonstration with the provided Docker profiles.

   **For production deployments:** Replace certificate/key/CA bundle paths with your own production
   credentials and endpoints. The authentication patterns remain largely the same, only the paths and URLs change.

Development vs Production Security
==================================

Understanding the security model differences between development and production environments is crucial for proper NiPyAPI usage.

Development Environment Security
--------------------------------

**Self-Signed Certificate Infrastructure**

The NiPyAPI development environment uses self-signed certificates generated via ``make certs``:

- **Root CA**: ``resources/certs/ca/ca.crt`` - Custom certificate authority for all test certificates
- **Server Certificates**: Generated with proper Subject Alternative Names (SANs) for localhost, container names
- **Client Certificates**: ``resources/certs/client/client.crt`` - For mTLS authentication testing
- **Unified Trust**: All certificates signed by the same root CA for simplified testing

**SSL Warning Suppression**

Development environments deliberately disable SSL verification warnings:

.. code-block:: python

    # In development/testing code
    nipyapi.config.disable_insecure_request_warnings = True

**Why this is safe in development:**

- Certificates are **properly signed** by our controlled root CA
- **Subject Alternative Names** correctly match hostnames (localhost, container names)
- **Trust chain is valid** - only the root CA is self-signed
- **Controlled environment** - no risk of man-in-the-middle attacks
- **Consistent test results** - eliminates noise from certificate warnings

**Why warnings are suppressed:**

SSL libraries correctly identify the root CA as "self-signed" and issue warnings, even though:

- The certificate chain is cryptographically valid
- Hostname verification passes
- The certificates provide real security within the controlled environment

Production Environment Security
-------------------------------

**Enterprise PKI Integration**

Production deployments should use certificates from trusted certificate authorities:

- **Commercial CAs** (DigiCert, Let's Encrypt, etc.)
- **Enterprise PKI** (internal certificate authorities)
- **Cloud Provider CAs** (AWS Certificate Manager, Azure Key Vault, etc.)

**SSL Verification Best Practices**

.. code-block:: python

    # In production code - NEVER disable SSL verification
    nipyapi.config.nifi_config.verify_ssl = True
    nipyapi.config.registry_config.verify_ssl = True

    # Use proper CA bundles
    nipyapi.config.nifi_config.ssl_ca_cert = "/etc/ssl/certs/ca-bundle.crt"
    nipyapi.config.registry_config.ssl_ca_cert = "/etc/ssl/certs/ca-bundle.crt"

**Security Configuration Guidelines**

1. **Never disable SSL verification** in production
2. **Use proper certificate validation** with trusted CAs
3. **Rotate certificates regularly** according to your security policy
4. **Monitor certificate expiration** and automate renewal
5. **Use least privilege access** for service accounts
6. **Audit authentication events** and API access

Certificate Generation and Management
=====================================

**Development Certificate Generation**

The NiPyAPI repository includes scripts for generating development certificates::

    # Generate complete certificate infrastructure
    make certs

    # Manual generation (if needed)
    ./resources/certs/gen_certs.sh

**Certificate Structure**

Generated certificates include:

- **ca/ca.crt** - Root certificate authority (self-signed)
- **ca/ca.key** - Root CA private key
- **nifi/keystore.p12** - NiFi server certificate (PKCS#12)
- **registry/keystore.p12** - Registry server certificate (PKCS#12)
- **client/client.crt** - Client certificate for mTLS (PEM)
- **client/client.key** - Client private key for mTLS (PEM)
- **client/client.p12** - Client certificate for browser import (PKCS#12)
- **truststore/truststore.p12** - Java truststore with root CA

**Production Certificate Requirements**

For production deployments:

1. **Obtain certificates from trusted CAs**
2. **Include proper Subject Alternative Names** for all hostnames/IPs
3. **Use appropriate key lengths** (2048-bit RSA minimum, 256-bit ECDSA preferred)
4. **Implement certificate lifecycle management**
5. **Store private keys securely** (HSM, encrypted storage)

Prerequisites
=============

If you want to use the provided Docker profiles, you need to:

- Generate local test certificates (if using the provided Docker profiles)::

    make certs

- Bring up a set of Docker containers for a profile and wait for readiness (examples)::

    make up NIPYAPI_PROFILE=single-user && make wait-ready NIPYAPI_PROFILE=single-user
    # or
    make up NIPYAPI_PROFILE=secure-ldap && make wait-ready NIPYAPI_PROFILE=secure-ldap
    # or
    make up NIPYAPI_PROFILE=secure-mtls && make wait-ready NIPYAPI_PROFILE=secure-mtls
    # or
    make up NIPYAPI_PROFILE=secure-oidc && make wait-ready NIPYAPI_PROFILE=secure-oidc

Environment variables
=====================

Environment variables provide a way to override profile configurations or configure NiPyAPI directly.

.. important::
   **Recommended Approach**: Use the **Profiles System** (``nipyapi.profiles.switch()``) for configuration management.

   The profiles system supports multiple configuration sources:

   - **YAML/JSON files**: ``examples/profiles.yml`` or custom profile files
   - **Environment variables**: Override any profile setting (e.g., ``NIFI_API_ENDPOINT``, ``NIFI_USERNAME``)
   - **Programmatic overrides**: Direct configuration object manipulation

   All approaches use the same profiles system under the hood and provide automatic authentication
   method detection. Environment variables are a **valid and supported** way to use profiles,
   especially useful for CI/CD and containerized deployments.

For complete environment variable documentation including profiles system integration, see `Environment Profiles <profiles.html>`_.

**Core Configuration Variables**

These variables are read at import time to seed defaults (see ``nipyapi/config.py``):

.. code-block:: shell

    # Service endpoints (used by both profiles and direct configuration)
    export NIFI_API_ENDPOINT=https://localhost:9443/nifi-api
    export REGISTRY_API_ENDPOINT=http://localhost:18080/nifi-registry-api

    # SSL configuration (current)
    export REQUESTS_CA_BUNDLE=/path/to/ca.pem                    # Standard Python/requests CA bundle
    export TLS_CA_CERT_PATH=/path/to/ca.pem                      # Shared CA for both NiFi and Registry
    export NIPYAPI_VERIFY_SSL=1                                  # Global SSL verification toggle
    export NIPYAPI_CHECK_HOSTNAME=1                              # Hostname verification toggle

.. note::
   **Environment Variable Changes**

   **Variables with name changes:**

   - ``NIFI_CA_CERT`` → **Renamed** to ``NIFI_CA_CERT_PATH`` (profiles) or use ``TLS_CA_CERT_PATH`` (shared)
   - ``REGISTRY_CA_CERT`` → **Renamed** to ``REGISTRY_CA_CERT_PATH`` (profiles) or use ``TLS_CA_CERT_PATH`` (shared)

   **Variables moved to profiles system:**

   These variables still work the same way but are now managed through the profiles system:

   - ``NIFI_CLIENT_CERT`` → Now handled via profiles system (same variable name)
   - ``NIFI_CLIENT_KEY`` → Now handled via profiles system (same variable name)
   - ``REGISTRY_CLIENT_CERT`` → Now handled via profiles system (same variable name)
   - ``REGISTRY_CLIENT_KEY`` → Now handled via profiles system (same variable name)

   **Migration**: For CA certificates, update variable names. For client certificates, no changes needed - the same environment variables work but are now processed through the profiles system instead of direct configuration.

**Profile System Variables**

When using the profiles system, these variables can override any profile configuration:

.. code-block:: shell

    # Profiles system configuration
    export NIPYAPI_PROFILES_FILE=/path/to/custom/profiles.yml    # Custom profiles file location

    # Authentication overrides (see profiles.rst for complete list)
    export NIFI_USERNAME=production_user
    export NIFI_PASSWORD=production_password
    export TLS_CA_CERT_PATH=/path/to/ca.pem
    export MTLS_CLIENT_CERT=/path/to/client.crt
    export MTLS_CLIENT_KEY=/path/to/client.key

**Direct Configuration**

For programmatic configuration:

.. code-block:: python

    # Modern approach: Set configuration directly (NiPyAPI 1.x)
    import nipyapi
    from nipyapi import config

    # Configure endpoints
    config.nifi_config.host = "https://nifi.company.com/nifi-api"
    config.registry_config.host = "https://registry.company.com/nifi-registry-api"

    # Configure SSL certificates
    config.nifi_config.ssl_ca_cert = "/path/to/ca.pem"
    config.nifi_config.cert_file = "/path/to/client.crt"  # For mTLS
    config.nifi_config.key_file = "/path/to/client.key"   # For mTLS

    # Configure authentication
    config.nifi_config.username = "user"
    config.nifi_config.password = "password"

    # Establish connection
    nipyapi.utils.set_endpoint(config.nifi_config.host, ssl=True, login=True)

.. note::
   **Recommendation**: Use the profiles system instead of manual configuration for better maintainability and environment management.

Registry vs NiFi Authentication Requirements
===========================================

**Important:** NiFi Registry and NiFi have different authentication requirements depending on their deployment mode:

**NiFi Registry Authentication:**

- **HTTP Deployments** (``http://...``): **No authentication required**. Registry allows unauthenticated API access for development and testing environments.
- **HTTPS Deployments** (``https://...``): **Authentication required** via username/password or client certificates.

**NiFi Authentication:**

- **All Deployments**: **Authentication always required** when using secure connection methods (``ssl=True`` or ``https://`` URLs).

**Practical Implications:**

.. code-block:: python

    # Registry HTTP - No authentication needed
    nipyapi.config.registry_config.host = "http://localhost:18080/nifi-registry-api"
    # Can immediately make API calls without login

    # Registry HTTPS - Authentication required
    nipyapi.config.registry_config.host = "https://localhost:18443/nifi-registry-api"
    nipyapi.security.service_login("registry", username="user", password="pass")

    # NiFi - Authentication required for secure connections
    nipyapi.config.nifi_config.host = "https://localhost:9443/nifi-api"
    nipyapi.security.service_login("nifi", username="user", password="pass")

.. note::
   The profiles system and ``set_endpoint()`` function automatically handle these authentication differences. When using Registry over HTTP, no login attempt will be made even if ``login=True`` is specified.

Authentication Methods
======================

NiPyAPI provides several approaches for configuring authentication and SSL/TLS, from high-level profiles to low-level configuration.

**Option A: Profiles System (recommended for most users)**

The profiles system provides centralized configuration management for different environments:

.. code-block:: python

    import nipyapi

    # Switch to pre-configured profile
    nipyapi.profiles.switch('single-user')      # Development environment
    nipyapi.profiles.switch('secure-ldap')      # LDAP authentication
    nipyapi.profiles.switch('secure-mtls')      # Certificate authentication
    nipyapi.profiles.switch('secure-oidc')      # OAuth2/OIDC authentication

    # Custom profiles file
    nipyapi.profiles.switch('production', profiles_file='/etc/nipyapi/profiles.yml')

For complete profiles documentation, see `Environment Profiles <profiles.html>`_.

**Option B: Environment Variables (simple overrides)**

Environment variables can override any profile configuration or provide direct configuration:

.. code-block:: shell

    # Set CA bundle for both services via standard environment variable
    export REQUESTS_CA_BUNDLE=/path/to/ca.pem

    # Override profile settings
    export NIFI_API_ENDPOINT=https://production.company.com/nifi-api
    export NIFI_USERNAME=service_account

**Option C: Convenience Functions (manual configuration)**

.. code-block:: python

    import nipyapi

    # Set CA certificate for both NiFi and Registry services at once
    nipyapi.security.set_shared_ca_cert("/path/to/ca.pem")

    # Reset connections to apply SSL changes
    nipyapi.security.reset_service_connections()

**Option D: Per-Service Configuration**

.. code-block:: python

    import nipyapi

    # Explicit per-service config (when services use different CAs)
    nipyapi.config.nifi_config.ssl_ca_cert = "/path/to/nifi-ca.pem"
    nipyapi.config.registry_config.ssl_ca_cert = "/path/to/registry-ca.pem"

    # Reset connections to apply changes
    nipyapi.security.reset_service_connections()


Single-user (basic auth)
------------------------

Default ports (Docker profile): NiFi ``https://localhost:9443/nifi-api``; Registry ``http://localhost:18080/nifi-registry-api``.

.. code-block:: python

    from nipyapi import config, utils

    # Basic auth credentials (Docker profile defaults)
    config.nifi_config.username = "einstein"
    config.nifi_config.password = "password1234"  # single-user default
    # Note: Registry HTTP credentials not needed (unauthenticated access)

    # Establish sessions using legacy set_endpoint command instead of new profiles.switch() system.
    utils.set_endpoint("https://localhost:9443/nifi-api", ssl=True, login=True)
    utils.set_endpoint("http://localhost:18080/nifi-registry-api", ssl=False, login=False)  # HTTP Registry - no auth needed


Secure LDAP (basic auth over TLS)
---------------------------------

Default ports (Docker profile): NiFi ``https://localhost:9444/nifi-api``; Registry ``https://localhost:18444/nifi-registry-api``.

.. code-block:: python

    from nipyapi import config, utils

    config.nifi_config.username = "einstein"
    config.nifi_config.password = "password"
    config.registry_config.username = "einstein"
    config.registry_config.password = "password"

    utils.set_endpoint("https://localhost:9444/nifi-api", ssl=True, login=True)
    utils.set_endpoint("https://localhost:18444/nifi-registry-api", ssl=True, login=True)


Secure mTLS (client certificate)
--------------------------------

Default ports (Docker profile): NiFi ``https://localhost:9445/nifi-api``; Registry ``https://localhost:18445/nifi-registry-api``.

.. code-block:: python

    from nipyapi import config, utils

    # Set client cert and key (PEM)
    # For NiPyAPI test environment: "resources/certs/client/client.crt" and "resources/certs/client/client.key"
    # For production: replace with your own client certificate paths
    config.nifi_config.cert_file = "/path/to/client.crt"
    config.nifi_config.key_file = "/path/to/client.key"
    # If your key is encrypted, set key password via MTLS_CLIENT_KEY_PASSWORD env or programmatically
    # Reuse for Registry if using the same client identity
    config.registry_config.cert_file = config.nifi_config.cert_file
    config.registry_config.key_file = config.nifi_config.key_file
    # CA bundle for both services (or per-service as above)
    # For NiPyAPI test environment: "resources/certs/ca/ca.crt"
    # For production: replace with your own CA bundle path
    config.nifi_config.ssl_ca_cert = "/path/to/ca.pem"
    config.registry_config.ssl_ca_cert = "/path/to/ca.pem"

    # Establish endpoints without token login (mTLS provides auth)
    utils.set_endpoint("https://localhost:9445/nifi-api", ssl=True, login=False)
    utils.set_endpoint("https://localhost:18445/nifi-registry-api", ssl=True, login=False)


Browser Certificate Import (mTLS Web UI Access)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For mTLS web UI access, you must import the client certificate into your browser **before** visiting the NiFi/Registry URLs.

**Using NiPyAPI test certificates:** The NiPyAPI Docker environment generates a browser-compatible PKCS#12 certificate at:
``resources/certs/client/client.p12`` (password: ``changeit``)

**Using production certificates:** Convert your client certificate and key to PKCS#12 format for browser import as required:

.. code-block:: shell

    openssl pkcs12 -export -in /path/to/client.crt -inkey /path/to/client.key -out client.p12

**Chrome/Edge:**

1. Settings → Privacy & Security → Security → **Manage certificates**
2. **Personal** tab → **Import** → Browse to your ``.p12`` file
3. Enter your certificate password (``changeit`` for NiPyAPI test certs)
4. ✓ Check "Mark this key as exportable" → **Next** → **Finish**

**Firefox:**

1. Settings → Privacy & Security → Certificates → **View Certificates**
2. **Your Certificates** tab → **Import** → Select your ``.p12`` file
3. Enter your certificate password (``changeit`` for NiPyAPI test certs)

**Safari:**

1. Double-click your ``.p12`` file
2. **Keychain Access** opens → Choose **"login"** keychain → Enter your certificate password (``changeit`` for NiPyAPI test certs)
3. Right-click imported certificate → **Get Info** → **Trust** → **Always Trust**

**After Import:**

Visit https://localhost:9445/nifi or https://localhost:18445/nifi-registry and your browser
will prompt to select the "client" certificate. The certificate subject ``CN=user1`` is
pre-configured with admin access in the Docker environment.

**Safari Keychain Authentication:**

After selecting the certificate, Safari will prompt for your macOS user/admin password to access
the keychain. You have two options:

- **"Allow"** - Enter password each time you access the NiFi/Registry site
- **"Always Allow"** - Grant permanent access (no password prompt on subsequent visits)

Choose based on your security requirements and company policy. For development environments,
"Always Allow" provides convenience. For production access, consider the security implications
of storing keychain access permissions.

OpenID Connect (OIDC)
---------------------

OIDC provides modern OAuth2-based authentication for NiFi using external identity providers like Keycloak, Okta, or Azure AD. Both browser-based and programmatic access are supported.

**Default ports (Docker profile):** NiFi ``https://localhost:9446/nifi-api``; Registry ``http://localhost:18446/nifi-registry-api``.

**Server-Side Configuration**

The Docker profile includes a pre-configured Keycloak instance with:

- **Realm:** ``nipyapi``
- **Client ID:** ``nipyapi-client``
- **Client Secret:** ``nipyapi-secret``
- **Test User:** ``einstein@example.com`` / ``password1234``
- **Admin Console:** http://localhost:8080/admin (admin/password)

**Browser Authentication**

For browser-based access:

1. Visit https://localhost:9446/nifi
2. You'll be redirected to Keycloak login
3. Login with ``einstein`` / ``password1234``
4. You'll be redirected back to NiFi with initial access

**Programmatic Authentication (Multi-Step Setup)**

.. important::
   **One-Time Manual Setup Required:**

   Programmatic OIDC access requires a one-time manual setup due to NiFi's security architecture.
   The OAuth2 password flow creates a separate application identity that needs admin policies.
   So the initial admin identity (einstein) manually authorizes the OIDC application identity (a UUID), which then bootstraps policies for both identities.

**Step 1: Initial Discovery**

Use the sandbox script to discover your OIDC application UUID::

    make sandbox NIPYAPI_PROFILE=secure-oidc

Note: This leverages the comprehensive example script ``examples/sandbox.py`` which demonstrates robust JWT token parsing to extract the OIDC application UUID.

This will attempt OAuth2 authentication and display the required manual steps, including a unique UUID like ``2a670050-ff88-41d6-a01f-d32ed7e90e09``.

**Step 2: Manual Policy Configuration**

.. note::
    The script will print these instructions in the console along with the generated UUID.

1. Open your browser and navigate to the NiFi UI (https://localhost:9446/nifi)
2. Login via OIDC with your credentials (``einstein`` / ``password1234``)
3. Go to **Settings → Users** (hamburger menu → Settings)
4. Click **"Add User"** and create a new user with the exact OIDC application UUID displayed in Step 1
5. Go to **Settings → Policies**
6. Grant these policies to the OIDC application UUID:

   - **"view the user interface"** (view access)
   - **"view users"** (view access)
   - **"view policies"** (view access)
   - **"modify policies"** (modify access)

.. note::
   These are the minimum policies required for programmatic access. You can add more policies as needed.
   The bootstrap script will grant the remaining policies automatically if you run it.

.. note::
   **User Creation Required**: You must create the user (Step 4) before assigning policies (Step 6).
   The OIDC application UUID is dynamically generated and the user won't exist until you create it manually.

**Step 3: Retry Setup**

Simply re-run the same sandbox command to now complete the bootstrap::

    make sandbox NIPYAPI_PROFILE=secure-oidc

**Programmatic Access After Setup**

After setup, programmatic access works seamlessly using the profiles system:

.. code-block:: python

    import nipyapi

    # Use the secure-oidc profile (handles all OIDC configuration automatically)
    nipyapi.profiles.switch('secure-oidc')

    # All API calls now work with full admin privileges
    about_info = nipyapi.nifi.FlowApi().get_about_info()
    current_user = nipyapi.nifi.FlowApi().get_current_user()
    flows = nipyapi.canvas.list_all_process_groups()

**Manual OIDC Configuration**

For direct programmatic control:

.. code-block:: python

    import nipyapi

    # Manual OAuth2 password flow configuration
    nipyapi.security.service_login_oidc(
        service='nifi',
        username='einstein',
        password='password1234',
        oidc_token_endpoint='http://localhost:8080/realms/nipyapi/protocol/openid-connect/token',
        client_id='nipyapi-client',
        client_secret='nipyapi-secret'
    )

    # API calls work the same way
    about_info = nipyapi.nifi.FlowApi().get_about_info()
    current_user = nipyapi.nifi.FlowApi().get_current_user()

**Why This Setup is Required**

NiFi's OIDC implementation creates different identities for different authentication flows:

- **Browser authentication**: Uses the configured user claim (e.g., ``einstein@example.com``)
- **OAuth2 password flow**: Uses the JWT token's 'sub' field as the user identity (a UUID like ``51c482de-649c-4951-ae1e-50075aa8340b``)

The OAuth2 application identity is dynamically generated by the OIDC provider and doesn't exist in NiFi's user registry until manually created. This is why both user creation and policy assignment are required.

.. tip::
   **Automated Bootstrap**: The sandbox script automatically handles policy assignment for both identities:
   the browser user (``einstein@example.com``) AND the OAuth2 application identity. This ensures
   both browser and programmatic access work seamlessly after the one-time manual setup.

**Troubleshooting OIDC**

**Problem**: "No applicable policies could be found" errors after manual setup

**Solution**: Ensure both user creation AND policy assignment steps were completed:

1. Verify the user exists: **Settings → Users** → Search for your UUID
2. Verify policies assigned: **Settings → Policies** → Check each required policy contains your UUID
3. Clear browser cache and retry authentication

**Problem**: "Untrusted proxy identity" errors in Registry

**Solution**: This indicates NiFi → Registry communication issues. Verify:

1. Registry is accessible: ``curl http://localhost:18446/nifi-registry-api/about``
2. NiFi is using the correct URL for the Registry client in your environment
3. Registry authentication works independently
4. Registry proxy user policies are configured (handled automatically by sandbox script)

**Problem**: Manual setup seems to work but programmatic access still fails

**Solution**: The setup affects only new authentications. Clear any cached API clients:

.. code-block:: python

    import nipyapi
    nipyapi.config.nifi_config.api_client = None  # Clear cached client
    # Retry authentication

**General Debugging**

For complex connectivity or authentication issues, especially with Registry, scripts can help identify specific blockers:

Use the sandbox script and test suite to validate Registry connectivity and troubleshoot configuration issues:

.. code-block:: shell

    # Test complete Registry integration
    make sandbox NIPYAPI_PROFILE=secure-ldap
    make test NIPYAPI_PROFILE=secure-ldap

Quick connection checks
=======================

After configuring endpoints and credentials/certificates as above, you can verify connectivity without
needing any policy bootstrap using lightweight version probes:

.. code-block:: python

    from nipyapi import system
    # Should return NiFi version info (object or version string)
    print(system.get_nifi_version_info())
    # Should return a non-empty version string for Registry
    print(system.get_registry_version_info())


NiFi Registry Client SSL Configuration
======================================

Understanding SSL trust relationships is important when configuring NiFi Registry clients for flow version control. NiFi and Registry can interact through implicit trust (shared CA) or explicit SSL Context Services.

Implicit Trust (Shared Root CA)
--------------------------------

When NiFi and Registry share a common root certificate authority, they automatically trust each other through NiFi's global SSL configuration:

**How it works:**
- When Registry Client's `ssl-context-service` property is `null`, NiFi falls back to global SSL configuration
- NiFi's global truststore (configured via environment variables) contains the shared root CA
- Registry's certificate is signed by the same root CA
- NiFi automatically trusts Registry connections through this fallback mechanism
- Registry Client components work immediately without explicit SSL Context Services

**Benefits:**
- Simplified configuration and reduced complexity
- No additional SSL Context Services required
- Automatic trust relationship establishment
- Lower operational overhead

**Example: Simple Registry Client (implicit trust)**::

    # No SSL Context Service needed - uses NiFi's global SSL configuration
    registry_client = nipyapi.versioning.ensure_registry_client(
        name='my_registry_client',
        uri='https://registry.example.com/nifi-registry-api',
        description='Registry Client using implicit SSL trust'
    )

Explicit SSL Context Services
-----------------------------

When NiFi and Registry have different certificate authorities or specific PKI requirements, explicit SSL Context Services provide per-component SSL configuration:

**When required:**
- **Different certificate authorities** (NiFi and Registry use different root CAs)
- **Enterprise PKI integration** (complex trust hierarchies, intermediate CAs)
- **Component-specific certificates** (different keystores per Registry Client)
- **Granular security policies** (different SSL requirements per component)
- **Cloud platform requirements** (e.g., Cloudera DataHub NiFi implementations)

**Example: Explicit SSL Context Service**::

    # Create SSL Context Service for specific PKI requirements
    ssl_context = nipyapi.security.ensure_ssl_context(
        name='registry_ssl_context',
        parent_pg=parent_pg,
        keystore_file='/path/to/specific/keystore.p12',
        keystore_password='password',
        truststore_file='/path/to/specific/truststore.p12',
        truststore_password='password'
    )

    # Registry Client with explicit SSL Context
    registry_client = nipyapi.versioning.ensure_registry_client(
        name='secure_registry_client',
        uri='https://secure-registry.example.com/nifi-registry-api',
        description='Registry Client with explicit SSL Context',
        ssl_context_service=ssl_context
    )

NiPyAPI Testing Implementation
------------------------------

The NiPyAPI test infrastructure uses the **implicit trust** approach:

- All test certificates share a common root CA (``resources/certs/ca/ca.crt``)
- NiFi containers are configured with global truststore containing the shared CA
- Registry Clients work automatically without SSL Context Services
- Simplified test setup and maintenance

This approach is suitable for development, testing, and deployments where certificate management is centralized. Enterprise deployments with complex PKI requirements may require explicit SSL Context Services.

Security Module Organization
=============================

Understanding where to find different types of security functionality:

**nipyapi.security** - Taking Security Actions
-----------------------------------------------

The security module performs active security operations:

- **Authentication functions**: ``service_login_oidc()``, ``set_service_auth_token()``
- **SSL configuration**: ``set_shared_ca_cert()``, ``set_service_ssl_context()``, ``reset_service_connections()``
- **Security bootstrapping**: Policy creation, user setup, admin access management
- **Trust management**: Certificate verification, SSL context services

*Use this module when you need to perform security operations or configure authentication.*

**nipyapi.profiles** - Configuration Management
------------------------------------------------

The profiles module handles configuration definitions and validation:

- **Environment switching**: ``switch()`` function for changing between environments
- **Configuration validation**: Ensuring certificate paths exist, URLs are valid
- **Environment variable mapping**: How ``NIFI_API_ENDPOINT`` maps to internal config
- **Profile definitions**: Built-in and custom profile management

*Use this module when you want to switch environments or manage configuration centrally.*

**nipyapi.utils** - Supporting Utilities
-----------------------------------------

The utils module provides supporting functions:

- **Path resolution**: Converting relative certificate paths to absolute paths
- **Endpoint management**: Lower-level endpoint configuration functions
- **Data transformation**: Helper functions for security-related data handling

*Use this module when you need utility functions for path handling and data transformation.*
