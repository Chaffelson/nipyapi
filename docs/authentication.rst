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
- The Makefile targets `test-su`, `test-ldap`, and `test-mtls` run the full test suite with profile-appropriate TLS and credentials via `tests/conftest.py`.

