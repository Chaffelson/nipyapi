# nifi.ReportingtasksApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**clear_state**](ReportingtasksApi.md#clear_state) | **POST** /reporting-tasks/{id}/state/clear-requests | Clears the state for a reporting task
[**get_property_descriptor**](ReportingtasksApi.md#get_property_descriptor) | **GET** /reporting-tasks/{id}/descriptors | Gets a reporting task property descriptor
[**get_reporting_task**](ReportingtasksApi.md#get_reporting_task) | **GET** /reporting-tasks/{id} | Gets a reporting task
[**get_state**](ReportingtasksApi.md#get_state) | **GET** /reporting-tasks/{id}/state | Gets the state for a reporting task
[**remove_reporting_task**](ReportingtasksApi.md#remove_reporting_task) | **DELETE** /reporting-tasks/{id} | Deletes a reporting task
[**update_reporting_task**](ReportingtasksApi.md#update_reporting_task) | **PUT** /reporting-tasks/{id} | Updates a reporting task


# **clear_state**
> ComponentStateEntity clear_state(id)

Clears the state for a reporting task



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ReportingtasksApi()
id = 'id_example' # str | The reporting task id.

try: 
    # Clears the state for a reporting task
    api_response = api_instance.clear_state(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReportingtasksApi->clear_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The reporting task id. | 

### Return type

[**ComponentStateEntity**](ComponentStateEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_property_descriptor**
> PropertyDescriptorEntity get_property_descriptor(id, property_name)

Gets a reporting task property descriptor



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ReportingtasksApi()
id = 'id_example' # str | The reporting task id.
property_name = 'property_name_example' # str | The property name.

try: 
    # Gets a reporting task property descriptor
    api_response = api_instance.get_property_descriptor(id, property_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReportingtasksApi->get_property_descriptor: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The reporting task id. | 
 **property_name** | **str**| The property name. | 

### Return type

[**PropertyDescriptorEntity**](PropertyDescriptorEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_reporting_task**
> ReportingTaskEntity get_reporting_task(id)

Gets a reporting task



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ReportingtasksApi()
id = 'id_example' # str | The reporting task id.

try: 
    # Gets a reporting task
    api_response = api_instance.get_reporting_task(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReportingtasksApi->get_reporting_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The reporting task id. | 

### Return type

[**ReportingTaskEntity**](ReportingTaskEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_state**
> ComponentStateEntity get_state(id)

Gets the state for a reporting task



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ReportingtasksApi()
id = 'id_example' # str | The reporting task id.

try: 
    # Gets the state for a reporting task
    api_response = api_instance.get_state(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReportingtasksApi->get_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The reporting task id. | 

### Return type

[**ComponentStateEntity**](ComponentStateEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_reporting_task**
> ReportingTaskEntity remove_reporting_task(id, version=version, client_id=client_id)

Deletes a reporting task



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ReportingtasksApi()
id = 'id_example' # str | The reporting task id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes a reporting task
    api_response = api_instance.remove_reporting_task(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReportingtasksApi->remove_reporting_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The reporting task id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**ReportingTaskEntity**](ReportingTaskEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_reporting_task**
> ReportingTaskEntity update_reporting_task(id, body)

Updates a reporting task



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ReportingtasksApi()
id = 'id_example' # str | The reporting task id.
body = nifi.ReportingTaskEntity() # ReportingTaskEntity | The reporting task configuration details.

try: 
    # Updates a reporting task
    api_response = api_instance.update_reporting_task(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReportingtasksApi->update_reporting_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The reporting task id. | 
 **body** | [**ReportingTaskEntity**](ReportingTaskEntity.md)| The reporting task configuration details. | 

### Return type

[**ReportingTaskEntity**](ReportingTaskEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

