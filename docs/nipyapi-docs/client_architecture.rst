Client Architecture
===================

Understanding how NiPyApi clients are structured and how to use them effectively.

Client Layers
-------------

NiPyApi provides multiple layers of abstraction:

**Core Modules** (High-level): :doc:`core_modules` - Convenient Python functions for common operations

**Generated APIs** (Low-level): :doc:`nifi_apis/index` and :doc:`registry_apis/index` - Direct REST API access

**Models**: :doc:`nifi_models/index` and :doc:`registry_models/index` - Data structures used by APIs

Generated API Structure
-----------------------

Each generated API class provides two methods for every operation:

**Base Methods** (e.g., ``copy()``)
  Return response data directly. Use these for most operations.

**HTTP Info Methods** (e.g., ``copy_with_http_info()``)
  Return detailed response including status code and headers.
  Use when you need HTTP metadata or error details.

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

   import nipyapi

   # High-level approach (recommended for most users)
   process_groups = nipyapi.canvas.list_all_process_groups()

   # Low-level API approach
   api_instance = nipyapi.nifi.ProcessGroupsApi()
   
   # Get just the data
   flow = api_instance.get_flow('root')
   
   # Get data + HTTP details
   flow, status, headers = api_instance.get_flow_with_http_info('root')
   print(f"HTTP Status: {status}")

Callback Functions
------------------

The generated clients support callback functions for asynchronous operations:

.. code-block:: python

   def my_callback(response):
       print(f"Response received: {response}")

   # Use callback for async-style processing
   api_instance.get_flow('root', callback=my_callback)

**Note**: Callbacks are inherited from the original Swagger-generated client.
They maintain backwards compatibility but are not commonly used.

Error Handling
--------------

APIs can raise exceptions on HTTP errors:

.. code-block:: python

   from nipyapi.nifi.rest import ApiException

   try:
       flow = api_instance.get_flow('invalid-id')
   except ApiException as e:
       print(f"API Error: {e.status} - {e.reason}")

Model Cross-References
----------------------

API documentation includes clickable links to model classes.
Click any model type (e.g., :class:`~nipyapi.nifi.models.ProcessGroupEntity`) to jump to its detailed documentation.

