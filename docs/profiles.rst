.. highlight:: python

=================================
Environment Profiles with NiPyAPI
=================================

NiPyAPI profiles provide a centralized configuration system for managing different Apache NiFi and NiFi Registry environments. This system exists because enterprise environments typically have multiple deployments (development, staging, production) that administrators and developers need to switch between when performing tasks. Instead of manually reconfiguring endpoints, certificates, and authentication for each environment, profiles let you switch between pre-configured setups with a single function call.

Quick Start
===========

**1. Start the infrastructure first:**

.. code-block:: console

    # Generate certificates and start Docker environment
    make certs
    make up NIPYAPI_PROFILE=single-user
    make wait-ready NIPYAPI_PROFILE=single-user

**2. Switch to the profile and start working:**

.. code-block:: python

    import nipyapi

    # Switch to single-user development environment
    nipyapi.profiles.switch('single-user')

    # Now all API calls use the single-user configuration
    about = nipyapi.system.get_nifi_version_info()
    flows = nipyapi.canvas.list_all_process_groups()

**Available built-in profiles:**

- ``single-user`` - HTTP Basic authentication (recommended for getting started)
- ``secure-ldap`` - LDAP authentication over TLS
- ``secure-mtls`` - Mutual TLS certificate authentication
- ``secure-oidc`` - OpenID Connect (OAuth2) authentication

Why Use Profiles?
=================

**Without profiles** (manual configuration):

.. code-block:: python

    import nipyapi
    from nipyapi import config, utils

    # Manual configuration for each environment
    config.nifi_config.username = "einstein"
    config.nifi_config.password = "password1234"
    config.nifi_config.ssl_ca_cert = "/path/to/ca.crt"
    config.registry_config.username = "einstein"
    config.registry_config.password = "password1234"
    utils.set_endpoint("https://localhost:9443/nifi-api", ssl=True, login=True)
    utils.set_endpoint("http://localhost:18080/nifi-registry-api", ssl=True, login=True)

    # Repeat for every environment...

**With profiles** (centralized configuration):

.. code-block:: python

    import nipyapi

    # Single function call configures everything
    nipyapi.profiles.switch('single-user')

    # Switch to production when ready
    nipyapi.profiles.switch('production')

Configuration Structure
=======================

Default profiles are defined in ``examples/profiles.yml`` (JSON is also supported). The structure uses a flat key-value format:

.. code-block:: yaml

    profile_name:
      # Service endpoints
      nifi_url: "https://localhost:9443/nifi-api"
      registry_url: "http://localhost:18080/nifi-registry-api"
      registry_internal_url: "http://registry-single:18080"

      # Authentication credentials
      nifi_user: "einstein"
      nifi_pass: "password1234"
      registry_user: "einstein"
      registry_pass: "password1234"

      # Shared certificate configuration (simple PKI)
      ca_path: "resources/certs/client/ca.pem"
      client_cert: "resources/certs/client/client.crt"
      client_key: "resources/certs/client/client.key"
      client_key_password: ""

      # Per-service certificate configuration (complex PKI)
      nifi_ca_path: null
      registry_ca_path: null
      nifi_client_cert: null
      registry_client_cert: null
      nifi_client_key: null
      registry_client_key: null
      nifi_client_key_password: null
      registry_client_key_password: null

      # SSL/TLS security settings
      nifi_verify_ssl: null
      registry_verify_ssl: null
      nifi_disable_host_check: null
      registry_disable_host_check: null
      suppress_ssl_warnings: null

      # Advanced settings
      nifi_proxy_identity: null

      # OIDC configuration
      oidc_token_endpoint: null
      oidc_client_id: null
      oidc_client_secret: null

**All Configuration Keys:**

Core connection settings:
  - ``nifi_url`` - NiFi API endpoint URL
  - ``registry_url`` - Registry API endpoint URL
  - ``registry_internal_url`` - Internal Registry URL for NiFi → Registry communication (used when services are on private networks like Docker where internal hostnames differ from external access)

Authentication credentials:
  - ``nifi_user`` / ``nifi_pass`` - NiFi Basic authentication credentials
  - ``registry_user`` / ``registry_pass`` - Registry Basic authentication credentials

Shared SSL/TLS certificates (simple PKI - convenience options where both NiFi and Registry share configuration):
  - ``ca_path`` - CA certificate bundle path (used by both services)
  - ``client_cert`` - Client certificate path (used by both services for mTLS)
  - ``client_key`` - Client private key path (used by both services for mTLS)
  - ``client_key_password`` - Private key password

Per-service SSL/TLS certificates (complex PKI):
  - ``nifi_ca_path`` / ``registry_ca_path`` - Service-specific CA certificate paths
  - ``nifi_client_cert`` / ``registry_client_cert`` - Service-specific client certificate paths
  - ``nifi_client_key`` / ``registry_client_key`` - Service-specific client key paths
  - ``nifi_client_key_password`` / ``registry_client_key_password`` - Service-specific key passwords

SSL/TLS security settings:
  - ``nifi_verify_ssl`` / ``registry_verify_ssl`` - SSL certificate verification (true/false/null). Smart defaults: true for HTTPS URLs, false for HTTP URLs
  - ``nifi_disable_host_check`` / ``registry_disable_host_check`` - Disable SSL hostname verification (true/false/null). Only applies to HTTPS connections. Default: null (secure hostname checking enabled)
  - ``suppress_ssl_warnings`` - Suppress SSL warnings for development with self-signed certificates (true/false/null)

Advanced settings:
  - ``nifi_proxy_identity`` - Identity for NiFi → Registry proxied requests

OIDC authentication:
  - ``oidc_token_endpoint`` - OAuth2 token endpoint URL
  - ``oidc_client_id`` / ``oidc_client_secret`` - OAuth2 client credentials

Profile Switching Behavior
===========================

**Authentication Method Precedence**: When multiple authentication methods are present in a profile, the system uses this priority order: **1) OIDC** (``oidc_token_endpoint``), **2) mTLS** (``client_cert`` + ``client_key``), **3) Basic Auth** (``nifi_user`` + ``nifi_pass``). To ensure predictable behavior, design profiles with only one authentication method per environment.

**Service Connection Logic**: Performing a switch to NiFi or Registry is based on whether the ``nifi_url`` or ``registry_url`` is present in the profile. You can have a profile that contains only a ``nifi_url`` and it would not attempt to authenticate to Registry.

**OIDC Authentication Note**: For OIDC profiles, the presence of an ``oidc_token_endpoint`` means that the basic credentials (``nifi_user``/``nifi_pass``) will be applied to the OIDC service rather than directly to the NiFi or Registry service.

Path Resolution
===============

SSL libraries prefer absolute paths over relative paths for certificate files. Where relative paths are provided in profiles, they will be resolved to absolute paths in the operating system. You can override the root directory for relative path resolution using the ``NIPYAPI_CERTS_ROOT_PATH`` environment variable.

Built-in Profiles
==================

single-user (Recommended for Development)
------------------------------------------

HTTP Basic authentication with HTTPS NiFi and HTTP Registry:

.. code-block:: python

    nipyapi.profiles.switch('single-user')

**Authentication method**: Basic (detected by presence of ``nifi_user`` and ``nifi_pass``)

**Required properties**:
  - ``nifi_user: einstein``
  - ``nifi_pass: password1234``
  - ``registry_user: einstein``
  - ``registry_pass: password1234``

**Additional properties used**:
  - ``nifi_url: https://localhost:9443/nifi-api``
  - ``registry_url: http://localhost:18080/nifi-registry-api``
  - ``registry_internal_url: http://registry-single:18080``
  - ``ca_path: resources/certs/client/ca.pem``
  - ``client_cert: resources/certs/client/client.crt``
  - ``client_key: resources/certs/client/client.key``
  - ``client_key_password: ""``
  - ``nifi_disable_host_check: true`` (development with self-signed certificates)
  - ``suppress_ssl_warnings: true`` (suppress warnings for development)

**Use case**: Development, testing, learning NiPyAPI

secure-ldap
-----------

LDAP authentication over TLS for both services:

.. code-block:: python

    nipyapi.profiles.switch('secure-ldap')

**Authentication method**: Basic (detected by presence of ``nifi_user`` and ``nifi_pass``)

**Required properties**:
  - ``nifi_user: einstein``
  - ``nifi_pass: password``
  - ``registry_user: einstein``
  - ``registry_pass: password``

**Additional properties used**:
  - ``nifi_url: https://localhost:9444/nifi-api``
  - ``registry_url: https://localhost:18444/nifi-registry-api``
  - ``registry_internal_url: https://registry-ldap:18443``
  - ``ca_path: resources/certs/client/ca.pem``
  - ``client_cert: resources/certs/client/client.crt``
  - ``client_key: resources/certs/client/client.key``
  - ``client_key_password: ""``
  - ``nifi_proxy_identity: C=US, O=NiPyAPI, CN=nifi``

**Use case**: Enterprise LDAP authentication testing

**Note**: Although both ``single-user`` and ``secure-ldap`` profiles use Basic authentication (detected by ``nifi_user``/``nifi_pass``), they are separate profiles because they use different Docker container configurations with different authentication providers. The ``single-user`` profile uses NiFi's built-in single-user authentication, while ``secure-ldap`` uses LDAP authentication backend.

secure-mtls
-----------

Mutual TLS certificate authentication:

.. code-block:: python

    nipyapi.profiles.switch('secure-mtls')

**Authentication method**: mTLS (detected by presence of ``client_cert`` and ``client_key``)

**Required properties**:
  - ``client_cert: resources/certs/client/client.crt``
  - ``client_key: resources/certs/client/client.key``

**Optional properties**:
  - ``client_key_password: ""``

**Additional properties used**:
  - ``nifi_url: https://localhost:9445/nifi-api``
  - ``registry_url: https://localhost:18445/nifi-registry-api``
  - ``registry_internal_url: https://registry-mtls:18443``
  - ``ca_path: resources/certs/client/ca.pem``
  - ``nifi_proxy_identity: C=US, O=NiPyAPI, CN=nifi``

**Use case**: High-security environments, certificate-based authentication

secure-oidc
-----------

OpenID Connect (OAuth2) authentication:

.. code-block:: python

    nipyapi.profiles.switch('secure-oidc')

**Authentication method**: OIDC (detected by presence of ``oidc_token_endpoint``)

**Required properties**:
  - ``oidc_token_endpoint: http://localhost:8080/realms/nipyapi/protocol/openid-connect/token``
  - ``oidc_client_id: nipyapi-client``
  - ``oidc_client_secret: nipyapi-secret``
  - ``nifi_user: einstein``
  - ``nifi_pass: password1234``

**Additional properties used**:
  - ``nifi_url: https://localhost:9446/nifi-api``
  - ``registry_url: http://localhost:18446/nifi-registry-api``
  - ``registry_internal_url: http://registry-oidc:18080``
  - ``registry_user: einstein``
  - ``registry_pass: password1234``
  - ``ca_path: resources/certs/client/ca.pem``
  - ``client_cert: resources/certs/client/client.crt``
  - ``client_key: resources/certs/client/client.key``
  - ``client_key_password: ""``

**Use case**: Modern OAuth2 integration, external identity providers

Environment Variable Overrides
===============================

Any profile configuration can be overridden with environment variables:

.. code-block:: shell

    # Override service endpoints
    export NIFI_API_ENDPOINT=https://production.example.com/nifi-api
    export REGISTRY_API_ENDPOINT=https://registry.production.example.com/nifi-registry-api

    # Override credentials
    export NIFI_USERNAME=production_user
    export NIFI_PASSWORD=production_password
    export REGISTRY_USERNAME=production_user
    export REGISTRY_PASSWORD=production_password

    # Override certificates
    export TLS_CA_CERT_PATH=/etc/ssl/certs/production-ca.pem
    export MTLS_CLIENT_CERT=/etc/ssl/certs/client.crt
    export MTLS_CLIENT_KEY=/etc/ssl/private/client.key
    export MTLS_CLIENT_KEY_PASSWORD=key_password

    # Override SSL verification
    export NIFI_VERIFY_SSL=true
    export REGISTRY_VERIFY_SSL=true

    # Override OIDC configuration
    export OIDC_TOKEN_ENDPOINT=https://sso.company.com/auth/realms/company/protocol/openid-connect/token
    export OIDC_CLIENT_ID=nipyapi-production
    export OIDC_CLIENT_SECRET=production_secret

**Environment variable mapping (from profiles.py):**

URLs and credentials:
  - ``NIFI_API_ENDPOINT`` → ``nifi_url``
  - ``REGISTRY_API_ENDPOINT`` → ``registry_url``
  - ``NIFI_USERNAME`` → ``nifi_user``
  - ``NIFI_PASSWORD`` → ``nifi_pass``
  - ``REGISTRY_USERNAME`` → ``registry_user``
  - ``REGISTRY_PASSWORD`` → ``registry_pass``

Basic certificate paths:
  - ``TLS_CA_CERT_PATH`` → ``ca_path``
  - ``MTLS_CLIENT_CERT`` → ``client_cert``
  - ``MTLS_CLIENT_KEY`` → ``client_key``
  - ``MTLS_CLIENT_KEY_PASSWORD`` → ``client_key_password``

SSL/TLS security settings:
  - ``NIFI_VERIFY_SSL`` → ``nifi_verify_ssl``
  - ``REGISTRY_VERIFY_SSL`` → ``registry_verify_ssl``
  - ``NIFI_DISABLE_HOST_CHECK`` → ``nifi_disable_host_check``
  - ``REGISTRY_DISABLE_HOST_CHECK`` → ``registry_disable_host_check``
  - ``NIPYAPI_SUPPRESS_SSL_WARNINGS`` → ``suppress_ssl_warnings``

Advanced settings:
  - ``NIFI_PROXY_IDENTITY`` → ``nifi_proxy_identity``

OIDC configuration:
  - ``OIDC_TOKEN_ENDPOINT`` → ``oidc_token_endpoint``
  - ``OIDC_CLIENT_ID`` → ``oidc_client_id``
  - ``OIDC_CLIENT_SECRET`` → ``oidc_client_secret``

Per-service certificate overrides (complex PKI):
  - ``NIFI_CA_CERT_PATH`` → ``nifi_ca_path``
  - ``REGISTRY_CA_CERT_PATH`` → ``registry_ca_path``
  - ``NIFI_CLIENT_CERT`` → ``nifi_client_cert``
  - ``REGISTRY_CLIENT_CERT`` → ``registry_client_cert``
  - ``NIFI_CLIENT_KEY`` → ``nifi_client_key``
  - ``REGISTRY_CLIENT_KEY`` → ``registry_client_key``
  - ``NIFI_CLIENT_KEY_PASSWORD`` → ``nifi_client_key_password``
  - ``REGISTRY_CLIENT_KEY_PASSWORD`` → ``registry_client_key_password``

Path resolution:
  - ``NIPYAPI_CERTS_ROOT_PATH`` → Custom root directory for relative path resolution

Profiles system:
  - ``NIPYAPI_PROFILES_FILE`` → Custom profiles file path (overrides default examples/profiles.yml)

Creating Custom Profiles
=========================

You have several options for creating custom profiles:

**Option 1: Modify or extend examples/profiles.yml**

.. code-block:: yaml

    my-production:
      # Service endpoints
      nifi_url: "https://nifi.company.com/nifi-api"
      registry_url: "https://registry.company.com/nifi-registry-api"
      registry_internal_url: "https://registry.company.com/nifi-registry-api"

      # Authentication credentials
      nifi_user: "service_account"
      nifi_pass: "secure_password"
      registry_user: "service_account"
      registry_pass: "secure_password"

      # SSL settings
      nifi_verify_ssl: true
      registry_verify_ssl: true
      ca_path: "/etc/ssl/company-ca.pem"

**Option 2: Create your own profile file**

You can configure a custom profiles file location using multiple methods:

*Method 2a: Environment Variable (Global)*

.. code-block:: shell

    export NIPYAPI_PROFILES_FILE=/home/user/.nipyapi/profiles.yml

*Method 2b: Config Override (Programmatic)*

.. code-block:: python

    import nipyapi
    nipyapi.config.default_profiles_file = '/home/user/.nipyapi/profiles.yml'
    nipyapi.profiles.switch('production')  # Uses custom file

*Method 2c: Per-Call Override (Explicit)*

.. code-block:: python

    import nipyapi
    # Point to custom profile file location
    nipyapi.profiles.switch('my-production', profiles_file='/home/user/.nipyapi/profiles.yml')

**Profiles File Resolution Order**

The system resolves the profiles file path in this priority order:

1. **Explicit parameter**: ``profiles_file`` argument to ``switch()``
2. **Environment variable**: ``NIPYAPI_PROFILES_FILE``
3. **Config default**: ``nipyapi.config.default_profiles_file`` (defaults to ``examples/profiles.yml``)

**Sparse Profile Definitions**

You don't have to specify values that are otherwise null unless required for that given authentication method. **Smart SSL defaults** are automatically applied:

- ``verify_ssl``: Defaults to ``true`` for HTTPS URLs, ``false`` for HTTP URLs
- ``disable_host_check``: Defaults to ``null`` (secure hostname checking), forced to ``null`` for HTTP URLs (not applicable)
- ``suppress_ssl_warnings``: Defaults to ``null`` (show warnings)

.. code-block:: yaml

    my-staging:
      # Only specify what differs from defaults
      nifi_url: "https://nifi.staging.company.com/nifi-api"
      registry_url: "https://registry.staging.company.com/nifi-registry-api"
      nifi_user: "staging_user"
      nifi_pass: "staging_password"
      # All other values use system defaults

**Alternative: Direct Client Configuration**

You don't have to use profiles. You can also directly configure the NiPyAPI client using ``nipyapi.config`` and ``nipyapi.utils.set_endpoint()`` as shown in earlier examples.

Integration with Examples
=========================

The NiPyAPI example scripts use profiles for simplified setup:

**FDLC (Flow Development Life Cycle)**

The FDLC example demonstrates enterprise flow development workflows using ``single-user`` (development) and ``secure-ldap`` (production) profiles:

.. code-block:: console

    # Interactive mode (recommended)
    python -i examples/fdlc.py
    >>> step_1_setup_environments()
    >>> step_2_create_dev_flow()
    >>> # ... continue with remaining steps

    # Auto run (complete demo)
    python examples/fdlc.py --auto

Demonstrates flow version management across environments using profile switching.

**Sandbox Environment**

.. code-block:: console

    $ make sandbox NIPYAPI_PROFILE=single-user

Creates a complete development environment with sample data using the specified profile.

Profile API Reference
=====================

**nipyapi.profiles.switch(profile_name, profiles_file=None)**

Switch to a named profile.

:param profile_name: Name of the profile to switch to
:type profile_name: str
:param profiles_file: Path to profiles file. Resolution order: 1) Explicit parameter, 2) NIPYAPI_PROFILES_FILE env var, 3) nipyapi.config.default_profiles_file
:type profiles_file: str or None
:raises ValueError: If profile is not found or configuration is invalid

.. code-block:: python

    # Switch to named profile
    nipyapi.profiles.switch('single-user')

    # Switch using custom profiles file
    nipyapi.profiles.switch('production', profiles_file='/home/user/.nipyapi/profiles.yml')

Cross-References
================

**For technical authentication details:** See `Security with NiPyAPI <security.html>`_

**For API reference:** See `API Reference <nipyapi-docs/api_reference.html>`_

**For examples:** See `Examples and Tutorials <nipyapi-docs/examples.html>`_
