=====
Usage
=====

Examples
--------

To use Nipyapi in a project::

    # in Bash
    pip install nipyapi

    # in Python
    import nipyapi

To fetch the NiFi system's diagnostics::

    from nipyapi import system
    system.get_system_diagnostics()

To fetch the NiFi system's root Process Group ID::

    from nipyapi import canvas
    canvas.get_root_pg_id()

Configuration
-------------

Further configuration parameters for the Nifi and Registry may be found in nipyapi.config::

    from nipyapi import config
    config.nifi_config.host = 'http://localhost:8080/nifi-api'
