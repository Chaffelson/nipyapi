# registry.BucketFlowsApi

All URIs are relative to *http://localhost/nifi-registry-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_flow**](BucketFlowsApi.md#create_flow) | **POST** /buckets/{bucketId}/flows | Creates a flow
[**create_flow_version**](BucketFlowsApi.md#create_flow_version) | **POST** /buckets/{bucketId}/flows/{flowId}/versions | Creates the next version of a flow
[**delete_flow**](BucketFlowsApi.md#delete_flow) | **DELETE** /buckets/{bucketId}/flows/{flowId} | Deletes a flow.
[**get_flow**](BucketFlowsApi.md#get_flow) | **GET** /buckets/{bucketId}/flows/{flowId} | Gets a flow
[**get_flow_version**](BucketFlowsApi.md#get_flow_version) | **GET** /buckets/{bucketId}/flows/{flowId}/versions/{versionNumber} | Gets the given version of a flow
[**get_flow_versions**](BucketFlowsApi.md#get_flow_versions) | **GET** /buckets/{bucketId}/flows/{flowId}/versions | Gets summary information for all versions of a flow. Versions are ordered newest-&gt;oldest.
[**get_flows**](BucketFlowsApi.md#get_flows) | **GET** /buckets/{bucketId}/flows | Gets all flows in the given bucket
[**get_latest_flow_version**](BucketFlowsApi.md#get_latest_flow_version) | **GET** /buckets/{bucketId}/flows/{flowId}/versions/latest | Get the latest version of a flow
[**get_latest_flow_version_metadata**](BucketFlowsApi.md#get_latest_flow_version_metadata) | **GET** /buckets/{bucketId}/flows/{flowId}/versions/latest/metadata | Get the metadata for the latest version of a flow
[**update_flow**](BucketFlowsApi.md#update_flow) | **PUT** /buckets/{bucketId}/flows/{flowId} | Updates a flow


# **create_flow**
> VersionedFlow create_flow(bucket_id, body=body)

Creates a flow

The flow id is created by the server and populated in the returned entity.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
body = registry.VersionedFlow() # VersionedFlow | The details of the flow to create. (optional)

try: 
    # Creates a flow
    api_response = api_instance.create_flow(bucket_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->create_flow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **body** | [**VersionedFlow**](VersionedFlow.md)| The details of the flow to create. | [optional] 

### Return type

[**VersionedFlow**](VersionedFlow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **create_flow_version**
> VersionedFlowSnapshot create_flow_version(bucket_id, flow_id, body=body)

Creates the next version of a flow

The version number is created by the server and populated in the returned entity.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
flow_id = 'flow_id_example' # str | The flow identifier
body = registry.VersionedFlowSnapshot() # VersionedFlowSnapshot | The new versioned flow snapshot. (optional)

try: 
    # Creates the next version of a flow
    api_response = api_instance.create_flow_version(bucket_id, flow_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->create_flow_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **flow_id** | **str**| The flow identifier | 
 **body** | [**VersionedFlowSnapshot**](VersionedFlowSnapshot.md)| The new versioned flow snapshot. | [optional] 

### Return type

[**VersionedFlowSnapshot**](VersionedFlowSnapshot.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **delete_flow**
> VersionedFlow delete_flow(bucket_id, flow_id)

Deletes a flow.



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
flow_id = 'flow_id_example' # str | The flow identifier

try: 
    # Deletes a flow.
    api_response = api_instance.delete_flow(bucket_id, flow_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->delete_flow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **flow_id** | **str**| The flow identifier | 

### Return type

[**VersionedFlow**](VersionedFlow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_flow**
> VersionedFlow get_flow(bucket_id, flow_id)

Gets a flow



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
flow_id = 'flow_id_example' # str | The flow identifier

try: 
    # Gets a flow
    api_response = api_instance.get_flow(bucket_id, flow_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->get_flow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **flow_id** | **str**| The flow identifier | 

### Return type

[**VersionedFlow**](VersionedFlow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_flow_version**
> VersionedFlowSnapshot get_flow_version(bucket_id, flow_id, version_number)

Gets the given version of a flow



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
flow_id = 'flow_id_example' # str | The flow identifier
version_number = 56 # int | The version number

try: 
    # Gets the given version of a flow
    api_response = api_instance.get_flow_version(bucket_id, flow_id, version_number)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->get_flow_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **flow_id** | **str**| The flow identifier | 
 **version_number** | **int**| The version number | 

### Return type

[**VersionedFlowSnapshot**](VersionedFlowSnapshot.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_flow_versions**
> list[VersionedFlowSnapshotMetadata] get_flow_versions(bucket_id, flow_id)

Gets summary information for all versions of a flow. Versions are ordered newest->oldest.



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
flow_id = 'flow_id_example' # str | The flow identifier

try: 
    # Gets summary information for all versions of a flow. Versions are ordered newest->oldest.
    api_response = api_instance.get_flow_versions(bucket_id, flow_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->get_flow_versions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **flow_id** | **str**| The flow identifier | 

### Return type

[**list[VersionedFlowSnapshotMetadata]**](VersionedFlowSnapshotMetadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_flows**
> list[VersionedFlow] get_flows(bucket_id)

Gets all flows in the given bucket



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier

try: 
    # Gets all flows in the given bucket
    api_response = api_instance.get_flows(bucket_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->get_flows: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 

### Return type

[**list[VersionedFlow]**](VersionedFlow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_latest_flow_version**
> VersionedFlowSnapshot get_latest_flow_version(bucket_id, flow_id)

Get the latest version of a flow



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
flow_id = 'flow_id_example' # str | The flow identifier

try: 
    # Get the latest version of a flow
    api_response = api_instance.get_latest_flow_version(bucket_id, flow_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->get_latest_flow_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **flow_id** | **str**| The flow identifier | 

### Return type

[**VersionedFlowSnapshot**](VersionedFlowSnapshot.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_latest_flow_version_metadata**
> VersionedFlowSnapshotMetadata get_latest_flow_version_metadata(bucket_id, flow_id)

Get the metadata for the latest version of a flow



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
flow_id = 'flow_id_example' # str | The flow identifier

try: 
    # Get the metadata for the latest version of a flow
    api_response = api_instance.get_latest_flow_version_metadata(bucket_id, flow_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->get_latest_flow_version_metadata: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **flow_id** | **str**| The flow identifier | 

### Return type

[**VersionedFlowSnapshotMetadata**](VersionedFlowSnapshotMetadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **update_flow**
> VersionedFlow update_flow(bucket_id, flow_id, body=body)

Updates a flow



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.BucketFlowsApi()
bucket_id = 'bucket_id_example' # str | The bucket identifier
flow_id = 'flow_id_example' # str | The flow identifier
body = registry.VersionedFlow() # VersionedFlow | The updated flow (optional)

try: 
    # Updates a flow
    api_response = api_instance.update_flow(bucket_id, flow_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketFlowsApi->update_flow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bucket_id** | **str**| The bucket identifier | 
 **flow_id** | **str**| The flow identifier | 
 **body** | [**VersionedFlow**](VersionedFlow.md)| The updated flow | [optional] 

### Return type

[**VersionedFlow**](VersionedFlow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

