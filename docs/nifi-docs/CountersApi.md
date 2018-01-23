# nifi.CountersApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_counters**](CountersApi.md#get_counters) | **GET** /counters | Gets the current counters for this NiFi
[**update_counter**](CountersApi.md#update_counter) | **PUT** /counters/{id} | Updates the specified counter. This will reset the counter value to 0


# **get_counters**
> CountersEntity get_counters(nodewise=nodewise, cluster_node_id=cluster_node_id)

Gets the current counters for this NiFi

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.CountersApi()
nodewise = false # bool | Whether or not to include the breakdown per node. Optional, defaults to false (optional) (default to false)
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where to get the status. (optional)

try: 
    # Gets the current counters for this NiFi
    api_response = api_instance.get_counters(nodewise=nodewise, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CountersApi->get_counters: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **nodewise** | **bool**| Whether or not to include the breakdown per node. Optional, defaults to false | [optional] [default to false]
 **cluster_node_id** | **str**| The id of the node where to get the status. | [optional] 

### Return type

[**CountersEntity**](CountersEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_counter**
> CounterEntity update_counter(id)

Updates the specified counter. This will reset the counter value to 0

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.CountersApi()
id = 'id_example' # str | The id of the counter.

try: 
    # Updates the specified counter. This will reset the counter value to 0
    api_response = api_instance.update_counter(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CountersApi->update_counter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the counter. | 

### Return type

[**CounterEntity**](CounterEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

