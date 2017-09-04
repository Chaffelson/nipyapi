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
    canvas = nipyapi.Canvas()
    canvas.get_root_pg_id()
