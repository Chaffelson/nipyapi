Examples and Tutorials
======================

Example scripts demonstrating NiPyApi functionality can be found in the
`examples/ directory <https://github.com/Chaffelson/nipyapi/tree/master/examples>`_
of the source repository.

Available Examples
------------------

* **fdlc.py**: Flow Development Life Cycle examples

Playground Environment
---------------------

For quick experimentation, use the playground make target to set up a ready-to-use environment:

.. code-block:: console

    $ make playground NIPYAPI_AUTH_MODE=single-user     # Recommended - simple setup
    $ make playground NIPYAPI_AUTH_MODE=secure-ldap     # LDAP authentication  
    $ make playground NIPYAPI_AUTH_MODE=secure-mtls     # Certificate authentication (advanced)

The playground automatically creates:

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

