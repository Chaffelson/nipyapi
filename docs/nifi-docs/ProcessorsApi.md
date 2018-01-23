# nifi.ProcessorsApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**clear_state**](ProcessorsApi.md#clear_state) | **POST** /processors/{id}/state/clear-requests | Clears the state for a processor
[**delete_processor**](ProcessorsApi.md#delete_processor) | **DELETE** /processors/{id} | Deletes a processor
[**get_processor**](ProcessorsApi.md#get_processor) | **GET** /processors/{id} | Gets a processor
[**get_property_descriptor**](ProcessorsApi.md#get_property_descriptor) | **GET** /processors/{id}/descriptors | Gets the descriptor for a processor property
[**get_state**](ProcessorsApi.md#get_state) | **GET** /processors/{id}/state | Gets the state for a processor
[**update_processor**](ProcessorsApi.md#update_processor) | **PUT** /processors/{id} | Updates a processor


# **clear_state**
> ComponentStateEntity clear_state(id)

Clears the state for a processor



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProcessorsApi()
id = 'id_example' # str | The processor id.

try: 
    # Clears the state for a processor
    api_response = api_instance.clear_state(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessorsApi->clear_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The processor id. | 

### Return type

[**ComponentStateEntity**](ComponentStateEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_processor**
> ProcessorEntity delete_processor(id, version=version, client_id=client_id)

Deletes a processor



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProcessorsApi()
id = 'id_example' # str | The processor id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes a processor
    api_response = api_instance.delete_processor(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessorsApi->delete_processor: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The processor id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**ProcessorEntity**](ProcessorEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_processor**
> ProcessorEntity get_processor(id)

Gets a processor



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProcessorsApi()
id = 'id_example' # str | The processor id.

try: 
    # Gets a processor
    api_response = api_instance.get_processor(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessorsApi->get_processor: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The processor id. | 

### Return type

[**ProcessorEntity**](ProcessorEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_property_descriptor**
> PropertyDescriptorEntity get_property_descriptor(id, property_name, client_id=client_id)

Gets the descriptor for a processor property



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProcessorsApi()
id = 'id_example' # str | The processor id.
property_name = 'property_name_example' # str | The property name.
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Gets the descriptor for a processor property
    api_response = api_instance.get_property_descriptor(id, property_name, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessorsApi->get_property_descriptor: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The processor id. | 
 **property_name** | **str**| The property name. | 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

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

Gets the state for a processor



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProcessorsApi()
id = 'id_example' # str | The processor id.

try: 
    # Gets the state for a processor
    api_response = api_instance.get_state(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessorsApi->get_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The processor id. | 

### Return type

[**ComponentStateEntity**](ComponentStateEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_processor**
> ProcessorEntity update_processor(id, body)

Updates a processor



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProcessorsApi()
id = 'id_example' # str | The processor id.
body = nifi.ProcessorEntity() # ProcessorEntity | The processor configuration details.

try: 
    # Updates a processor
    api_response = api_instance.update_processor(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProcessorsApi->update_processor: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The processor id. | 
 **body** | [**ProcessorEntity**](ProcessorEntity.md)| The processor configuration details. | 

### Return type

[**ProcessorEntity**](ProcessorEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

