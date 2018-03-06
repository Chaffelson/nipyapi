Console
-------

Importing this module will run a script which populates the NiFi canvas with a
Process Group containing a processor, and creates a sequence of Versioned
Flow Objects from it, along with a Template and various export versions.

This is intended to give the user a base set of objects to explore the API.

Usage::

    from nipyapi.demo.console import *

Secured Connection
------------------

Importing this module will pull recent Docker containers from Dockerhub, deploy
them in a secured configuration, and prepare the environment for access via
TLS in NiFi-Registry's case, and public LDAP username/password for NiFi.

This is intended to give the user an example of a secured environment.
May be combined with the Console to produce a secured environment with demo
objects.

Usage::

    from nipyapi.demo.secured_connection import *


bbende How Do I Deploy My Flow
------------------------------

An incomplete version of BBende's excellent demo.
It currently deploys some Docker NiFi and Registry instances.
