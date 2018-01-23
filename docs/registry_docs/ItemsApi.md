# registry.ItemsApi

All URIs are relative to *http://localhost/nifi-registry-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_available_bucket_item_fields**](ItemsApi.md#get_available_bucket_item_fields) | **GET** /items/fields | Retrieves the available field names for searching or sorting on bucket items.
[**get_items**](ItemsApi.md#get_items) | **GET** /items | Get items across all buckets
[**get_items_in_bucket**](ItemsApi.md#get_items_in_bucket) | **GET** /items/{bucketId} | Gets items of the given bucket


# **get_available_bucket_item_fields**
> Fields get_available_bucket_item_fields()

Retrieves the available field names for searching or sorting on bucket items.



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.ItemsApi()

try: 
    # Retrieves the available field names for searching or sorting on bucket items.
    api_response = api_instance.get_available_bucket_item_fields()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ItemsApi->get_available_bucket_item_fields: %s\n" % e)
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_items**
> list[BucketItem] get_items()

Get items across all buckets

The returned items will include only items from buckets for which the user is authorized. If the user is not authorized to any buckets, an empty list will be returned.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.ItemsApi()

try: 
    # Get items across all buckets
    api_response = api_instance.get_items()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ItemsApi->get_items: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[BucketItem]**](BucketItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_items_in_bucket**
> list[BucketItem] get_items_in_bucket(bucket_id)

Gets items of the given bucket



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.ItemsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier

try: 
    # Gets items of the given bucket
    api_response = api_instance.get_items_in_bucket(bucket_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ItemsApi->get_items_in_bucket: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 

### Return type

[**list[BucketItem]**](BucketItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

