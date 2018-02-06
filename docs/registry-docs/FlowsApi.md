# registry.FlowsApi

All URIs are relative to *http://localhost/nifi-registry-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_available_flow_fields**](FlowsApi.md#get_available_flow_fields) | **GET** /flows/fields | Retrieves the available field names that can be used for searching or sorting on flows.


# **get_available_flow_fields**
> Fields get_available_flow_fields()

Retrieves the available field names that can be used for searching or sorting on flows.



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.FlowsApi()

try: 
    # Retrieves the available field names that can be used for searching or sorting on flows.
    api_response = api_instance.get_available_flow_fields()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowsApi->get_available_flow_fields: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Fields**](Fields.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

