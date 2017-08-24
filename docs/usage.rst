=====
Usage
=====

To use Nipyapi in a project::

    import nipyapi
    nipyapi.swagger_client.configuration.host = "http://localhost:8080/nifi-api"
    con = nipyapi.swagger_client.SystemdiagnosticsApi()
    con.get_system_diagnostics()
