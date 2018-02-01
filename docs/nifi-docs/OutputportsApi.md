# nifi.OutputportsApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_output_port**](OutputportsApi.md#get_output_port) | **GET** /output-ports/{id} | Gets an output port
[**remove_output_port**](OutputportsApi.md#remove_output_port) | **DELETE** /output-ports/{id} | Deletes an output port
[**update_output_port**](OutputportsApi.md#update_output_port) | **PUT** /output-ports/{id} | Updates an output port


# **get_output_port**
> PortEntity get_output_port(id)

Gets an output port



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.OutputportsApi()
id = 'id_example' # str | The output port id.

try: 
    # Gets an output port
    api_response = api_instance.get_output_port(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OutputportsApi->get_output_port: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The output port id. | 

### Return type

[**PortEntity**](PortEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **remove_output_port**
> PortEntity remove_output_port(id, version=version, client_id=client_id)

Deletes an output port



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.OutputportsApi()
id = 'id_example' # str | The output port id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes an output port
    api_response = api_instance.remove_output_port(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OutputportsApi->remove_output_port: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The output port id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**PortEntity**](PortEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_output_port**
> PortEntity update_output_port(id, body)

Updates an output port



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.OutputportsApi()
id = 'id_example' # str | The output port id.
body = nifi.PortEntity() # PortEntity | The output port configuration details.

try: 
    # Updates an output port
    api_response = api_instance.update_output_port(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OutputportsApi->update_output_port: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The output port id. | 
 **body** | [**PortEntity**](PortEntity.md)| The output port configuration details. | 

### Return type

[**PortEntity**](PortEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

