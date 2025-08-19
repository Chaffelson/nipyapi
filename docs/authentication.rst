.. highlight:: python

=============================
Authentication with NiPyAPI 2
=============================

NiPyAPI 1.x targets Apache NiFi 2.x and NiFi Registry 2.x, which prefer secure-by-default deployments.
This page shows how to configure the client for the three common modes we test via Docker Compose profiles.

.. note::
   **Test vs Production Certificates:**
   
   Example snippets below use the NiPyAPI repository's generated test certificates (``resources/certs/``) 
   and localhost URLs for demonstration with the provided Docker profiles.
   
   **For production deployments:** Replace certificate/key/CA bundle paths with your own production 
   credentials and endpoints. The authentication patterns remain the same, only the paths and URLs change.

Prerequisites
-------------

If you want to use the provided Docker profiles, you need to:

- Generate local test certificates (if using the provided Docker profiles)::

    make certs

- Bring up a set of Docker containers for a profile and wait for readiness (examples)::

    make up NIPYAPI_AUTH_MODE=single-user && make wait-ready NIPYAPI_AUTH_MODE=single-user
    # or
    make up NIPYAPI_AUTH_MODE=secure-ldap && make wait-ready NIPYAPI_AUTH_MODE=secure-ldap
    # or
    make up NIPYAPI_AUTH_MODE=secure-mtls && make wait-ready NIPYAPI_AUTH_MODE=secure-mtls
    # or
    make up NIPYAPI_AUTH_MODE=secure-oidc && make wait-ready NIPYAPI_AUTH_MODE=secure-oidc

Environment variables
---------------------

You can optionally configure endpoints and TLS via environment variables. Standard names are
``NIFI_API_ENDPOINT`` and ``REGISTRY_API_ENDPOINT``:

.. code-block:: shell

    export NIFI_API_ENDPOINT=https://localhost:9443/nifi-api
    export REGISTRY_API_ENDPOINT=http://localhost:18080/nifi-registry-api
    # CA bundle for TLS verification (preferred over disabling verify)
    export REQUESTS_CA_BUNDLE=/path/to/ca.pem
    # Provide a CA bundle for TLS verification (preferred over disabling verify)
    export REQUESTS_CA_BUNDLE=/path/to/ca.pem
    # Optional toggles
    export NIPYAPI_VERIFY_SSL=1
    export NIPYAPI_CHECK_HOSTNAME=1

These are read at import time to seed defaults (see `nipyapi/config.py`).

For mTLS-driven test setups (and for convenience in local scripts), these additional
variables are recognized by the test harness (`tests/conftest.py`) and commonly used:

.. code-block:: shell

    export TLS_CA_CERT_PATH=/path/to/ca.pem
    # or use the standard Python variable recognized by requests/urllib3
    export REQUESTS_CA_BUNDLE=/path/to/ca.pem
    export MTLS_CLIENT_CERT=/path/to/client.crt
    export MTLS_CLIENT_KEY=/path/to/client.key
    export MTLS_CLIENT_KEY_PASSWORD=yourKeyPassword

Note: ``utils.set_endpoint(...)`` does not read these environment variables directly.
It relies on parameters you pass (endpoint, login, username/password) and any values
already set on the configuration objects (CA bundle, client cert/key). Prefer passing
the endpoint string to ``set_endpoint`` and setting credentials/certs explicitly on
``nipyapi.config``.

Recommended usage patterns
--------------------------

- Minimal env + explicit calls:

  - Optionally set ``REQUESTS_CA_BUNDLE`` (shared CA) and
    ``NIFI_API_ENDPOINT``/``REGISTRY_API_ENDPOINT`` for defaults.
  - Set credentials/certs on ``nipyapi.config``.
  - Call ``utils.set_endpoint(endpoint, ssl=True, login=...)`` for each service.

- Fully programmatic (no env):
  - Set ``config.nifi_config.ssl_ca_cert`` and/or client cert/key.
  - Set ``config.nifi_config.username/password`` (and registry equivalents) when using basic auth.
  - Call ``utils.set_endpoint(endpoint, ssl=True, login=...)`` and pass username/password if desired.

Common Setup
------------

Using the library-level configuration objects is preferred. For TLS verification, either set
``REQUESTS_CA_BUNDLE`` to your CA bundle file or set ``configuration.ssl_ca_cert`` directly.

.. code-block:: python

    import os
    import nipyapi
    from nipyapi import utils

    # Option A: via env for both services
    # For NiPyAPI test environment: "resources/certs/ca/ca.crt"
    # For production: use your own CA bundle path
    os.environ["REQUESTS_CA_BUNDLE"] = "/path/to/ca.pem"

    # Option B: explicit per-service config
    nipyapi.config.nifi_config.ssl_ca_cert = "/path/to/ca.pem"
    nipyapi.config.registry_config.ssl_ca_cert = "/path/to/ca.pem"


Single-user (basic auth)
------------------------

Default ports (Docker profile): NiFi ``https://localhost:9443/nifi-api``; Registry ``http://localhost:18080/nifi-registry-api``.

.. code-block:: python

    from nipyapi import config, utils

    # Basic auth credentials (Docker profile defaults)
    config.nifi_config.username = "einstein"
    config.nifi_config.password = "password1234"  # single-user default
    config.registry_config.username = "einstein"
    config.registry_config.password = "password1234"  # single-user default

    # Establish sessions (uses credentials already set on config)
    utils.set_endpoint("https://localhost:9443/nifi-api", ssl=True, login=True)
    utils.set_endpoint("http://localhost:18080/nifi-registry-api", ssl=True, login=True)


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

**Using production certificates:** Convert your client certificate and key to PKCS#12 format for browser import:

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

**Step 1: Initial Discovery**

Use the sandbox script to discover your OIDC application UUID::

    make sandbox NIPYAPI_AUTH_MODE=secure-oidc

Note: This leverages the comprehensive example script ``examples/sandbox.py`` which demonstrates robust JWT token parsing to extract the OIDC application UUID.

This will attempt OAuth2 authentication and display the required manual steps, including a unique UUID like ``2a670050-ff88-41d6-a01f-d32ed7e90e09``.

**Step 2: Manual Policy Configuration**

1. Open your browser and navigate to the NiFi UI (https://localhost:9446/nifi)
2. Login via OIDC with your credentials (``einstein`` / ``password1234``)
3. Go to **Settings → Users** (hamburger menu → Settings)
4. Click **"Add User"** and create a new user with the exact OIDC application UUID displayed in Step 1
5. Go to **Settings → Policies**
6. Grant these policies to the OIDC application UUID:
   
   - **"view the user interface"** (view + modify access)
   - **"view users"** (view access)
   - **"view policies"** (view access)
   - **"modify policies"** (modify access)

.. note::
   These are the minimum policies required for programmatic access. You can add more policies as needed.
   The bootstrap script will grant the remaining policies automatically if you run it.

.. note::
   **User Creation Required**: You must create the user (Step 4) before assigning policies (Step 6). 
   The OIDC application UUID is dynamically generated and won't exist until you create it manually.

**Step 3: Retry Setup**

Simply re-run the same sandbox command to now complete the bootstrap::

    make sandbox NIPYAPI_AUTH_MODE=secure-oidc

**Programmatic Access After Setup**

After setup, programmatic access works seamlessly:

.. code-block:: python

    import nipyapi
    
    # Authenticate via OAuth2 password flow
    nipyapi.security.service_login_oidc(
        service='nifi',
        username='einstein',
        password='password1234',
        oidc_token_endpoint='http://localhost:8080/realms/nipyapi/protocol/openid-connect/token',
        client_id='nipyapi-client',
        client_secret='nipyapi-secret'
    )
    
    # All API calls now work with full admin privileges
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

Quick connection checks
-----------------------

After configuring endpoints and credentials/certificates as above, you can verify connectivity without
needing any policy bootstrap using lightweight version probes:

.. code-block:: python

    from nipyapi import system
    # Should return NiFi version info (object or version string)
    print(system.get_nifi_version_info())
    # Should return a non-empty version string for Registry
    print(system.get_registry_version_info())


Notes
-----

- Prefer setting CA bundles and client certs programmatically rather than via environment variables in application code.
- The Makefile targets `test-su`, `test-ldap`, `test-mtls`, and `test-oidc` run the full test suite with profile-appropriate TLS and credentials via `tests/conftest.py`.
- For OIDC profiles, test infrastructure automatically handles token acquisition via the built-in token helper.

