=====
Usage
=====

Examples
--------

To use Nipyapi in a project::

    # in Bash
    pip install nipyapi

    # in Python
    # To change default nifi port, see Configuration section below
    import nipyapi
    

To fetch the NiFi system's diagnostics::

    from nipyapi import system
    system.get_system_diagnostics()

To fetch the NiFi system's root Process Group ID::

    from nipyapi import canvas
    canvas.get_root_pg_id()

Configuration
-------------

Further configuration parameters for the swagger_client may be found in swagger_client.configuration::

    import nipyapi
    from nipyapi import config
    config.swagger_config.host = 'http://localhost:8080/nifi-api'
