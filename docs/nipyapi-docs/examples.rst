Examples and Tutorials
======================

Example scripts demonstrating NiPyApi functionality can be found in the
`examples/ directory <https://github.com/Chaffelson/nipyapi/tree/master/examples>`_
of the source repository.

Available Examples
------------------

* **fdlc.py**: **Flow Development Life Cycle (FDLC)** - A comprehensive example demonstrating enterprise NiFi development workflow using NiFi Registry for version control. Shows the complete cycle: DEV environment flow creation → PROD environment deployment → iterative development → production updates. Includes multi-environment authentication, flow versioning, and Registry integration patterns.

* **sandbox.py**: **Multi-Profile Authentication Demo** - Interactive script showcasing all NiPyAPI authentication methods (single-user, LDAP, mTLS, OIDC) with real Docker environments. Demonstrates SSL/TLS configuration, security bootstrapping, Registry client setup, and sample object creation. Perfect for learning authentication patterns and testing different security configurations.

* **profiles.yml**: **Configuration Templates** - Complete YAML configuration file with working profiles for all supported authentication methods. Includes detailed comments explaining certificate paths, environment variable overrides, and per-service vs shared certificate configurations. Use as a starting template for your own deployments.

Quick Start
-----------

**New to NiPyAPI?** Start with the sandbox environment:

.. code-block:: console

    $ make sandbox NIPYAPI_PROFILE=single-user
    $ python examples/sandbox.py single-user

**Ready for enterprise patterns?** Try the FDLC workflow:

.. code-block:: console

    $ python examples/fdlc.py

**Need authentication setup?** Copy and customize ``profiles.yml`` for your environment.

Sandbox Environment
-------------------

For quick experimentation, use the sandbox make target to set up a ready-to-use environment:

.. code-block:: console

    $ make sandbox NIPYAPI_PROFILE=single-user     # Recommended - simple setup
    $ make sandbox NIPYAPI_PROFILE=secure-ldap     # LDAP authentication
    $ make sandbox NIPYAPI_PROFILE=secure-mtls     # Certificate authentication (advanced)

The sandbox automatically creates:

* Properly configured authentication and SSL
* Sample registry client and bucket
* Simple demo flow ready for experimentation
* All necessary security bootstrapping

When finished experimenting:

.. code-block:: console

    $ make down  # Clean up Docker containers

.. note::
   These are standalone Python scripts, not importable modules.
   Run them directly with Python after setting up your environment.

