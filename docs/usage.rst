=====
Usage
=====

To use Nipyapi in a project::

    import nypiapi


To retrieve the system diagonostics::

    import nipyapi
    system = nipyapi.System()
    system.get_system_diagnostics()

To print the root Process Group ID::

    import nipyapi
    canvas = nipyapi.Canvas()
    canvas.get_root_pg_id()
