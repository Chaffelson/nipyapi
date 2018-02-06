# nifi.ControllerApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_bulletin**](ControllerApi.md#create_bulletin) | **POST** /controller/bulletin | Creates a new bulletin
[**create_controller_service**](ControllerApi.md#create_controller_service) | **POST** /controller/controller-services | Creates a new controller service
[**create_registry_client**](ControllerApi.md#create_registry_client) | **POST** /controller/registry-clients | Creates a new registry client
[**create_reporting_task**](ControllerApi.md#create_reporting_task) | **POST** /controller/reporting-tasks | Creates a new reporting task
[**delete_history**](ControllerApi.md#delete_history) | **DELETE** /controller/history | Purges history
[**delete_node**](ControllerApi.md#delete_node) | **DELETE** /controller/cluster/nodes/{id} | Removes a node from the cluster
[**delete_registry_client**](ControllerApi.md#delete_registry_client) | **DELETE** /controller/registry-clients/{id} | Deletes a registry client
[**get_cluster**](ControllerApi.md#get_cluster) | **GET** /controller/cluster | Gets the contents of the cluster
[**get_controller_config**](ControllerApi.md#get_controller_config) | **GET** /controller/config | Retrieves the configuration for this NiFi Controller
[**get_node**](ControllerApi.md#get_node) | **GET** /controller/cluster/nodes/{id} | Gets a node in the cluster
[**get_registry_client**](ControllerApi.md#get_registry_client) | **GET** /controller/registry-clients/{id} | Gets a registry client
[**get_registry_clients**](ControllerApi.md#get_registry_clients) | **GET** /controller/registry-clients | Gets the listing of available registry clients
[**update_controller_config**](ControllerApi.md#update_controller_config) | **PUT** /controller/config | Retrieves the configuration for this NiFi
[**update_node**](ControllerApi.md#update_node) | **PUT** /controller/cluster/nodes/{id} | Updates a node in the cluster
[**update_registry_client**](ControllerApi.md#update_registry_client) | **PUT** /controller/registry-clients/{id} | Updates a registry client


# **create_bulletin**
> BulletinEntity create_bulletin(body)

Creates a new bulletin



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
body = nifi.BulletinEntity() # BulletinEntity | The reporting task configuration details.

try: 
    # Creates a new bulletin
    api_response = api_instance.create_bulletin(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->create_bulletin: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BulletinEntity**](BulletinEntity.md)| The reporting task configuration details. | 

### Return type

[**BulletinEntity**](BulletinEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **create_controller_service**
> ControllerServiceEntity create_controller_service(body)

Creates a new controller service



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
body = nifi.ControllerServiceEntity() # ControllerServiceEntity | The controller service configuration details.

try: 
    # Creates a new controller service
    api_response = api_instance.create_controller_service(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->create_controller_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ControllerServiceEntity**](ControllerServiceEntity.md)| The controller service configuration details. | 

### Return type

[**ControllerServiceEntity**](ControllerServiceEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **create_registry_client**
> RegistryClientEntity create_registry_client(body)

Creates a new registry client



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
body = nifi.RegistryClientEntity() # RegistryClientEntity | The registry configuration details.

try: 
    # Creates a new registry client
    api_response = api_instance.create_registry_client(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->create_registry_client: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RegistryClientEntity**](RegistryClientEntity.md)| The registry configuration details. | 

### Return type

[**RegistryClientEntity**](RegistryClientEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **create_reporting_task**
> ReportingTaskEntity create_reporting_task(body)

Creates a new reporting task



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
body = nifi.ReportingTaskEntity() # ReportingTaskEntity | The reporting task configuration details.

try: 
    # Creates a new reporting task
    api_response = api_instance.create_reporting_task(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->create_reporting_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ReportingTaskEntity**](ReportingTaskEntity.md)| The reporting task configuration details. | 

### Return type

[**ReportingTaskEntity**](ReportingTaskEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **delete_history**
> HistoryEntity delete_history(end_date)

Purges history



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
end_date = 'end_date_example' # str | Purge actions before this date/time.

try: 
    # Purges history
    api_response = api_instance.delete_history(end_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->delete_history: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **end_date** | **str**| Purge actions before this date/time. | 

### Return type

[**HistoryEntity**](HistoryEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **delete_node**
> NodeEntity delete_node(id)

Removes a node from the cluster



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
id = 'id_example' # str | The node id.

try: 
    # Removes a node from the cluster
    api_response = api_instance.delete_node(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->delete_node: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The node id. | 

### Return type

[**NodeEntity**](NodeEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **delete_registry_client**
> RegistryClientEntity delete_registry_client(id, version=version, client_id=client_id)

Deletes a registry client



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
id = 'id_example' # str | The registry id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes a registry client
    api_response = api_instance.delete_registry_client(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->delete_registry_client: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The registry id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**RegistryClientEntity**](RegistryClientEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_cluster**
> ClusterEntity get_cluster()

Gets the contents of the cluster

Returns the contents of the cluster including all nodes and their status.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()

try: 
    # Gets the contents of the cluster
    api_response = api_instance.get_cluster()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->get_cluster: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ClusterEntity**](ClusterEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_controller_config**
> ControllerConfigurationEntity get_controller_config()

Retrieves the configuration for this NiFi Controller



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()

try: 
    # Retrieves the configuration for this NiFi Controller
    api_response = api_instance.get_controller_config()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->get_controller_config: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ControllerConfigurationEntity**](ControllerConfigurationEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_node**
> NodeEntity get_node(id)

Gets a node in the cluster



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
id = 'id_example' # str | The node id.

try: 
    # Gets a node in the cluster
    api_response = api_instance.get_node(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->get_node: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The node id. | 

### Return type

[**NodeEntity**](NodeEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_registry_client**
> RegistryClientEntity get_registry_client(id)

Gets a registry client



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
id = 'id_example' # str | The registry id.

try: 
    # Gets a registry client
    api_response = api_instance.get_registry_client(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->get_registry_client: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The registry id. | 

### Return type

[**RegistryClientEntity**](RegistryClientEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_registry_clients**
> RegistryClientsEntity get_registry_clients()

Gets the listing of available registry clients



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()

try: 
    # Gets the listing of available registry clients
    api_response = api_instance.get_registry_clients()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->get_registry_clients: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**RegistryClientsEntity**](RegistryClientsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_controller_config**
> ControllerConfigurationEntity update_controller_config(body)

Retrieves the configuration for this NiFi



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
body = nifi.ControllerConfigurationEntity() # ControllerConfigurationEntity | The controller configuration.

try: 
    # Retrieves the configuration for this NiFi
    api_response = api_instance.update_controller_config(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->update_controller_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ControllerConfigurationEntity**](ControllerConfigurationEntity.md)| The controller configuration. | 

### Return type

[**ControllerConfigurationEntity**](ControllerConfigurationEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_node**
> NodeEntity update_node(id, body)

Updates a node in the cluster



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
id = 'id_example' # str | The node id.
body = nifi.NodeEntity() # NodeEntity | The node configuration. The only configuration that will be honored at this endpoint is the status.

try: 
    # Updates a node in the cluster
    api_response = api_instance.update_node(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->update_node: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The node id. | 
 **body** | [**NodeEntity**](NodeEntity.md)| The node configuration. The only configuration that will be honored at this endpoint is the status. | 

### Return type

[**NodeEntity**](NodeEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_registry_client**
> RegistryClientEntity update_registry_client(id, body)

Updates a registry client



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerApi()
id = 'id_example' # str | The registry id.
body = nifi.RegistryClientEntity() # RegistryClientEntity | The registry configuration details.

try: 
    # Updates a registry client
    api_response = api_instance.update_registry_client(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerApi->update_registry_client: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The registry id. | 
 **body** | [**RegistryClientEntity**](RegistryClientEntity.md)| The registry configuration details. | 

### Return type

[**RegistryClientEntity**](RegistryClientEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

