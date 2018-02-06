# nifi.FlowfilequeuesApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_drop_request**](FlowfilequeuesApi.md#create_drop_request) | **POST** /flowfile-queues/{id}/drop-requests | Creates a request to drop the contents of the queue in this connection.
[**create_flow_file_listing**](FlowfilequeuesApi.md#create_flow_file_listing) | **POST** /flowfile-queues/{id}/listing-requests | Lists the contents of the queue in this connection.
[**delete_listing_request**](FlowfilequeuesApi.md#delete_listing_request) | **DELETE** /flowfile-queues/{id}/listing-requests/{listing-request-id} | Cancels and/or removes a request to list the contents of this connection.
[**download_flow_file_content**](FlowfilequeuesApi.md#download_flow_file_content) | **GET** /flowfile-queues/{id}/flowfiles/{flowfile-uuid}/content | Gets the content for a FlowFile in a Connection.
[**get_drop_request**](FlowfilequeuesApi.md#get_drop_request) | **GET** /flowfile-queues/{id}/drop-requests/{drop-request-id} | Gets the current status of a drop request for the specified connection.
[**get_flow_file**](FlowfilequeuesApi.md#get_flow_file) | **GET** /flowfile-queues/{id}/flowfiles/{flowfile-uuid} | Gets a FlowFile from a Connection.
[**get_listing_request**](FlowfilequeuesApi.md#get_listing_request) | **GET** /flowfile-queues/{id}/listing-requests/{listing-request-id} | Gets the current status of a listing request for the specified connection.
[**remove_drop_request**](FlowfilequeuesApi.md#remove_drop_request) | **DELETE** /flowfile-queues/{id}/drop-requests/{drop-request-id} | Cancels and/or removes a request to drop the contents of this connection.


# **create_drop_request**
> DropRequestEntity create_drop_request(id)

Creates a request to drop the contents of the queue in this connection.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowfilequeuesApi()
id = 'id_example' # str | The connection id.

try: 
    # Creates a request to drop the contents of the queue in this connection.
    api_response = api_instance.create_drop_request(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowfilequeuesApi->create_drop_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 

### Return type

[**DropRequestEntity**](DropRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **create_flow_file_listing**
> ListingRequestEntity create_flow_file_listing(id)

Lists the contents of the queue in this connection.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowfilequeuesApi()
id = 'id_example' # str | The connection id.

try: 
    # Lists the contents of the queue in this connection.
    api_response = api_instance.create_flow_file_listing(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowfilequeuesApi->create_flow_file_listing: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 

### Return type

[**ListingRequestEntity**](ListingRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **delete_listing_request**
> ListingRequestEntity delete_listing_request(id, listing_request_id)

Cancels and/or removes a request to list the contents of this connection.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowfilequeuesApi()
id = 'id_example' # str | The connection id.
listing_request_id = 'listing_request_id_example' # str | The listing request id.

try: 
    # Cancels and/or removes a request to list the contents of this connection.
    api_response = api_instance.delete_listing_request(id, listing_request_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowfilequeuesApi->delete_listing_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 
 **listing_request_id** | **str**| The listing request id. | 

### Return type

[**ListingRequestEntity**](ListingRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **download_flow_file_content**
> StreamingOutput download_flow_file_content(id, flowfile_uuid, client_id=client_id, cluster_node_id=cluster_node_id)

Gets the content for a FlowFile in a Connection.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowfilequeuesApi()
id = 'id_example' # str | The connection id.
flowfile_uuid = 'flowfile_uuid_example' # str | The flowfile uuid.
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where the content exists if clustered. (optional)

try: 
    # Gets the content for a FlowFile in a Connection.
    api_response = api_instance.download_flow_file_content(id, flowfile_uuid, client_id=client_id, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowfilequeuesApi->download_flow_file_content: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 
 **flowfile_uuid** | **str**| The flowfile uuid. | 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 
 **cluster_node_id** | **str**| The id of the node where the content exists if clustered. | [optional] 

### Return type

[**StreamingOutput**](StreamingOutput.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_drop_request**
> DropRequestEntity get_drop_request(id, drop_request_id)

Gets the current status of a drop request for the specified connection.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowfilequeuesApi()
id = 'id_example' # str | The connection id.
drop_request_id = 'drop_request_id_example' # str | The drop request id.

try: 
    # Gets the current status of a drop request for the specified connection.
    api_response = api_instance.get_drop_request(id, drop_request_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowfilequeuesApi->get_drop_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 
 **drop_request_id** | **str**| The drop request id. | 

### Return type

[**DropRequestEntity**](DropRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_flow_file**
> FlowFileEntity get_flow_file(id, flowfile_uuid, cluster_node_id=cluster_node_id)

Gets a FlowFile from a Connection.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowfilequeuesApi()
id = 'id_example' # str | The connection id.
flowfile_uuid = 'flowfile_uuid_example' # str | The flowfile uuid.
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where the content exists if clustered. (optional)

try: 
    # Gets a FlowFile from a Connection.
    api_response = api_instance.get_flow_file(id, flowfile_uuid, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowfilequeuesApi->get_flow_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 
 **flowfile_uuid** | **str**| The flowfile uuid. | 
 **cluster_node_id** | **str**| The id of the node where the content exists if clustered. | [optional] 

### Return type

[**FlowFileEntity**](FlowFileEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_listing_request**
> ListingRequestEntity get_listing_request(id, listing_request_id)

Gets the current status of a listing request for the specified connection.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowfilequeuesApi()
id = 'id_example' # str | The connection id.
listing_request_id = 'listing_request_id_example' # str | The listing request id.

try: 
    # Gets the current status of a listing request for the specified connection.
    api_response = api_instance.get_listing_request(id, listing_request_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowfilequeuesApi->get_listing_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 
 **listing_request_id** | **str**| The listing request id. | 

### Return type

[**ListingRequestEntity**](ListingRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **remove_drop_request**
> DropRequestEntity remove_drop_request(id, drop_request_id)

Cancels and/or removes a request to drop the contents of this connection.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowfilequeuesApi()
id = 'id_example' # str | The connection id.
drop_request_id = 'drop_request_id_example' # str | The drop request id.

try: 
    # Cancels and/or removes a request to drop the contents of this connection.
    api_response = api_instance.remove_drop_request(id, drop_request_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowfilequeuesApi->remove_drop_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 
 **drop_request_id** | **str**| The drop request id. | 

### Return type

[**DropRequestEntity**](DropRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

