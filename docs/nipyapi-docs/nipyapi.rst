Demos
=====

These modules leverage functionality within the rest of the Package to demonstrate various capabilities

.. toctree::
   :maxdepth: 2

   nipyapi.demo

Client SDK modules
==================

These wrapper modules contain collections of convenience functions for daily operations of your NiFi and NiFi-Registry environment.
They wrap and surface underlying data structures and calls to the full SDK swagger clients which are also included in the package.

Canvas
------

.. automodule:: nipyapi.canvas
    :members:
    :undoc-members:
    :show-inheritance:

Config
------

.. automodule:: nipyapi.config
    :members:
    :undoc-members:
    :show-inheritance:

Parameters
----------

.. automodule:: nipyapi.parameters
    :members:
    :undoc-members:
    :show-inheritance:

Security
--------

.. automodule:: nipyapi.security
    :members:
    :undoc-members:
    :show-inheritance:

System
------

.. automodule:: nipyapi.system
    :members:
    :undoc-members:
    :show-inheritance:

Templates
---------

.. automodule:: nipyapi.templates
    :members:
    :undoc-members:
    :show-inheritance:

Utils
-----

.. automodule:: nipyapi.utils
    :members:
    :undoc-members:
    :show-inheritance:

Versioning
----------

.. automodule:: nipyapi.versioning
    :members:
    :undoc-members:
    :show-inheritance:


Swagger Client SDKs
===================

These sub-packages are full swagger clients to the NiFi and NiFi-Registry APIs and may be used directly, or wrapped into the NiPyApi SDK convenience functions

.. toctree::
   :maxdepth: 3

   nipyapi.nifi
   nipyapi.registry
