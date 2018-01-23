# nifi.ControllerservicesApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**clear_state**](ControllerservicesApi.md#clear_state) | **POST** /controller-services/{id}/state/clear-requests | Clears the state for a controller service
[**get_controller_service**](ControllerservicesApi.md#get_controller_service) | **GET** /controller-services/{id} | Gets a controller service
[**get_controller_service_references**](ControllerservicesApi.md#get_controller_service_references) | **GET** /controller-services/{id}/references | Gets a controller service
[**get_property_descriptor**](ControllerservicesApi.md#get_property_descriptor) | **GET** /controller-services/{id}/descriptors | Gets a controller service property descriptor
[**get_state**](ControllerservicesApi.md#get_state) | **GET** /controller-services/{id}/state | Gets the state for a controller service
[**remove_controller_service**](ControllerservicesApi.md#remove_controller_service) | **DELETE** /controller-services/{id} | Deletes a controller service
[**update_controller_service**](ControllerservicesApi.md#update_controller_service) | **PUT** /controller-services/{id} | Updates a controller service
[**update_controller_service_references**](ControllerservicesApi.md#update_controller_service_references) | **PUT** /controller-services/{id}/references | Updates a controller services references


# **clear_state**
> ComponentStateEntity clear_state(id)

Clears the state for a controller service



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerservicesApi()
id = 'id_example' # str | The controller service id.

try: 
    # Clears the state for a controller service
    api_response = api_instance.clear_state(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerservicesApi->clear_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The controller service id. | 

### Return type

[**ComponentStateEntity**](ComponentStateEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_controller_service**
> ControllerServiceEntity get_controller_service(id)

Gets a controller service



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerservicesApi()
id = 'id_example' # str | The controller service id.

try: 
    # Gets a controller service
    api_response = api_instance.get_controller_service(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerservicesApi->get_controller_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The controller service id. | 

### Return type

[**ControllerServiceEntity**](ControllerServiceEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_controller_service_references**
> ControllerServiceReferencingComponentsEntity get_controller_service_references(id)

Gets a controller service



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerservicesApi()
id = 'id_example' # str | The controller service id.

try: 
    # Gets a controller service
    api_response = api_instance.get_controller_service_references(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerservicesApi->get_controller_service_references: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The controller service id. | 

### Return type

[**ControllerServiceReferencingComponentsEntity**](ControllerServiceReferencingComponentsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_property_descriptor**
> PropertyDescriptorEntity get_property_descriptor(id, property_name)

Gets a controller service property descriptor



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerservicesApi()
id = 'id_example' # str | The controller service id.
property_name = 'property_name_example' # str | The property name to return the descriptor for.

try: 
    # Gets a controller service property descriptor
    api_response = api_instance.get_property_descriptor(id, property_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerservicesApi->get_property_descriptor: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The controller service id. | 
 **property_name** | **str**| The property name to return the descriptor for. | 

### Return type

[**PropertyDescriptorEntity**](PropertyDescriptorEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_state**
> ComponentStateEntity get_state(id)

Gets the state for a controller service



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerservicesApi()
id = 'id_example' # str | The controller service id.

try: 
    # Gets the state for a controller service
    api_response = api_instance.get_state(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerservicesApi->get_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The controller service id. | 

### Return type

[**ComponentStateEntity**](ComponentStateEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_controller_service**
> ControllerServiceEntity remove_controller_service(id, version=version, client_id=client_id)

Deletes a controller service



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerservicesApi()
id = 'id_example' # str | The controller service id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes a controller service
    api_response = api_instance.remove_controller_service(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerservicesApi->remove_controller_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The controller service id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**ControllerServiceEntity**](ControllerServiceEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_controller_service**
> ControllerServiceEntity update_controller_service(id, body)

Updates a controller service



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerservicesApi()
id = 'id_example' # str | The controller service id.
body = nifi.ControllerServiceEntity() # ControllerServiceEntity | The controller service configuration details.

try: 
    # Updates a controller service
    api_response = api_instance.update_controller_service(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerservicesApi->update_controller_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The controller service id. | 
 **body** | [**ControllerServiceEntity**](ControllerServiceEntity.md)| The controller service configuration details. | 

### Return type

[**ControllerServiceEntity**](ControllerServiceEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_controller_service_references**
> ControllerServiceReferencingComponentsEntity update_controller_service_references(id, body)

Updates a controller services references



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ControllerservicesApi()
id = 'id_example' # str | The controller service id.
body = nifi.UpdateControllerServiceReferenceRequestEntity() # UpdateControllerServiceReferenceRequestEntity | The controller service request update request.

try: 
    # Updates a controller services references
    api_response = api_instance.update_controller_service_references(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ControllerservicesApi->update_controller_service_references: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The controller service id. | 
 **body** | [**UpdateControllerServiceReferenceRequestEntity**](UpdateControllerServiceReferenceRequestEntity.md)| The controller service request update request. | 

### Return type

[**ControllerServiceReferencingComponentsEntity**](ControllerServiceReferencingComponentsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

