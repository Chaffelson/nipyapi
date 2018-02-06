# nifi.FunnelApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_funnel**](FunnelApi.md#get_funnel) | **GET** /funnels/{id} | Gets a funnel
[**remove_funnel**](FunnelApi.md#remove_funnel) | **DELETE** /funnels/{id} | Deletes a funnel
[**update_funnel**](FunnelApi.md#update_funnel) | **PUT** /funnels/{id} | Updates a funnel


# **get_funnel**
> FunnelEntity get_funnel(id)

Gets a funnel



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FunnelApi()
id = 'id_example' # str | The funnel id.

try: 
    # Gets a funnel
    api_response = api_instance.get_funnel(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FunnelApi->get_funnel: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The funnel id. | 

### Return type

[**FunnelEntity**](FunnelEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **remove_funnel**
> FunnelEntity remove_funnel(id, version=version, client_id=client_id)

Deletes a funnel



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FunnelApi()
id = 'id_example' # str | The funnel id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes a funnel
    api_response = api_instance.remove_funnel(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FunnelApi->remove_funnel: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The funnel id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**FunnelEntity**](FunnelEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_funnel**
> FunnelEntity update_funnel(id, body)

Updates a funnel



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FunnelApi()
id = 'id_example' # str | The funnel id.
body = nifi.FunnelEntity() # FunnelEntity | The funnel configuration details.

try: 
    # Updates a funnel
    api_response = api_instance.update_funnel(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FunnelApi->update_funnel: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The funnel id. | 
 **body** | [**FunnelEntity**](FunnelEntity.md)| The funnel configuration details. | 

### Return type

[**FunnelEntity**](FunnelEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

