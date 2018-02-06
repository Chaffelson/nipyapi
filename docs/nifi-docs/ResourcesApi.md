# nifi.ResourcesApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_resources**](ResourcesApi.md#get_resources) | **GET** /resources | Gets the available resources that support access/authorization policies


# **get_resources**
> ResourcesEntity get_resources()

Gets the available resources that support access/authorization policies



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ResourcesApi()

try: 
    # Gets the available resources that support access/authorization policies
    api_response = api_instance.get_resources()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResourcesApi->get_resources: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ResourcesEntity**](ResourcesEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

