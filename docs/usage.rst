=====
Usage
=====

To use Nipyapi in a project::

    # in Bash
    pip install nipyapi

    # in Python
    import nipyapi

To fetch the NiFi system's diagnostics::

    import nipyapi
    system = nipyapi.System(host='http://localhost:8080/nifi-api')
    system.get_system_diagnostics()

To fetch the NiFi system's root Process Group ID::

    import nipyapi
    nipyapi.Canvas().get_root_pg_id()

Configuration
-------------

Further configuration parameters for the swagger_client may be found in swagger_client.configuration::

    import nipyapi
    nipyapi.swagger_client.configuration.host = 'http://localhost:8080/nifi-api'
