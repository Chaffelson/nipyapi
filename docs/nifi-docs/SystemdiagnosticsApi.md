# nifi.SystemdiagnosticsApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_system_diagnostics**](SystemdiagnosticsApi.md#get_system_diagnostics) | **GET** /system-diagnostics | Gets the diagnostics for the system NiFi is running on


# **get_system_diagnostics**
> SystemDiagnosticsEntity get_system_diagnostics(nodewise=nodewise, cluster_node_id=cluster_node_id)

Gets the diagnostics for the system NiFi is running on



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.SystemdiagnosticsApi()
nodewise = false # bool | Whether or not to include the breakdown per node. Optional, defaults to false (optional) (default to false)
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where to get the status. (optional)

try: 
    # Gets the diagnostics for the system NiFi is running on
    api_response = api_instance.get_system_diagnostics(nodewise=nodewise, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemdiagnosticsApi->get_system_diagnostics: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **nodewise** | **bool**| Whether or not to include the breakdown per node. Optional, defaults to false | [optional] [default to false]
 **cluster_node_id** | **str**| The id of the node where to get the status. | [optional] 

### Return type

[**SystemDiagnosticsEntity**](SystemDiagnosticsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

