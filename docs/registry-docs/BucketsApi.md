# registry.BucketsApi

All URIs are relative to *http://localhost/nifi-registry-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_bucket**](BucketsApi.md#create_bucket) | **POST** /buckets | Creates a bucket
[**delete_bucket**](BucketsApi.md#delete_bucket) | **DELETE** /buckets/{bucketId} | Deletes a bucket along with all objects stored in the bucket
[**get_available_bucket_fields**](BucketsApi.md#get_available_bucket_fields) | **GET** /buckets/fields | Retrieves field names for searching or sorting on buckets.
[**get_bucket**](BucketsApi.md#get_bucket) | **GET** /buckets/{bucketId} | Gets a bucket
[**get_buckets**](BucketsApi.md#get_buckets) | **GET** /buckets | Gets all buckets
[**update_bucket**](BucketsApi.md#update_bucket) | **PUT** /buckets/{bucketId} | Updates a bucket


# **create_bucket**
> Bucket create_bucket(body=body)

Creates a bucket



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketsApi()
body = registry.Bucket() # Bucket | The bucket to create (optional)

try: 
    # Creates a bucket
    api_response = api_instance.create_bucket(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->create_bucket: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Bucket**](Bucket.md)| The bucket to create | [optional] 

### Return type

[**Bucket**](Bucket.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **delete_bucket**
> Bucket delete_bucket(bucket_id)

Deletes a bucket along with all objects stored in the bucket



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier

try: 
    # Deletes a bucket along with all objects stored in the bucket
    api_response = api_instance.delete_bucket(bucket_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->delete_bucket: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 

### Return type

[**Bucket**](Bucket.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_available_bucket_fields**
> Fields get_available_bucket_fields()

Retrieves field names for searching or sorting on buckets.



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketsApi()

try: 
    # Retrieves field names for searching or sorting on buckets.
    api_response = api_instance.get_available_bucket_fields()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->get_available_bucket_fields: %s\n" % e)
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

# **get_bucket**
> Bucket get_bucket(bucket_id)

Gets a bucket



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier

try: 
    # Gets a bucket
    api_response = api_instance.get_bucket(bucket_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->get_bucket: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 

### Return type

[**Bucket**](Bucket.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_buckets**
> list[Bucket] get_buckets()

Gets all buckets

The returned list will include only buckets for which the user is authorized.If the user is not authorized for any buckets, this returns an empty list.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketsApi()

try: 
    # Gets all buckets
    api_response = api_instance.get_buckets()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->get_buckets: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Bucket]**](Bucket.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **update_bucket**
> Bucket update_bucket(bucket_id, body=body)

Updates a bucket



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
body = registry.Bucket() # Bucket | The updated bucket (optional)

try: 
    # Updates a bucket
    api_response = api_instance.update_bucket(bucket_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->update_bucket: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **body** | [**Bucket**](Bucket.md)| The updated bucket | [optional] 

### Return type

[**Bucket**](Bucket.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

