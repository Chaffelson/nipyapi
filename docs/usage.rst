=====
Usage
=====

To use Nipyapi in a project::

    import nypiapi


To do a simple test connection and retrieve the system diagonostics::

    from nipyapi import swagger_client
    swagger_client.configuration.host = "http://localhost:8080/nifi-api"
    con = swagger_client.SystemdiagnosticsApi()
    con.get_system_diagnostics()
