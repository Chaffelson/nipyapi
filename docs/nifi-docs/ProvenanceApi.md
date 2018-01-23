# nifi.ProvenanceApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_lineage**](ProvenanceApi.md#delete_lineage) | **DELETE** /provenance/lineage/{id} | Deletes a lineage query
[**delete_provenance**](ProvenanceApi.md#delete_provenance) | **DELETE** /provenance/{id} | Deletes a provenance query
[**get_lineage**](ProvenanceApi.md#get_lineage) | **GET** /provenance/lineage/{id} | Gets a lineage query
[**get_provenance**](ProvenanceApi.md#get_provenance) | **GET** /provenance/{id} | Gets a provenance query
[**get_search_options**](ProvenanceApi.md#get_search_options) | **GET** /provenance/search-options | Gets the searchable attributes for provenance events
[**submit_lineage_request**](ProvenanceApi.md#submit_lineage_request) | **POST** /provenance/lineage | Submits a lineage query
[**submit_provenance_request**](ProvenanceApi.md#submit_provenance_request) | **POST** /provenance | Submits a provenance query


# **delete_lineage**
> LineageEntity delete_lineage(id, cluster_node_id=cluster_node_id)

Deletes a lineage query



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProvenanceApi()
id = 'id_example' # str | The id of the lineage query.
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where this query exists if clustered. (optional)

try: 
    # Deletes a lineage query
    api_response = api_instance.delete_lineage(id, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProvenanceApi->delete_lineage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the lineage query. | 
 **cluster_node_id** | **str**| The id of the node where this query exists if clustered. | [optional] 

### Return type

[**LineageEntity**](LineageEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_provenance**
> ProvenanceEntity delete_provenance(id, cluster_node_id=cluster_node_id)

Deletes a provenance query



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProvenanceApi()
id = 'id_example' # str | The id of the provenance query.
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where this query exists if clustered. (optional)

try: 
    # Deletes a provenance query
    api_response = api_instance.delete_provenance(id, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProvenanceApi->delete_provenance: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the provenance query. | 
 **cluster_node_id** | **str**| The id of the node where this query exists if clustered. | [optional] 

### Return type

[**ProvenanceEntity**](ProvenanceEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_lineage**
> LineageEntity get_lineage(id, cluster_node_id=cluster_node_id)

Gets a lineage query



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProvenanceApi()
id = 'id_example' # str | The id of the lineage query.
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where this query exists if clustered. (optional)

try: 
    # Gets a lineage query
    api_response = api_instance.get_lineage(id, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProvenanceApi->get_lineage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the lineage query. | 
 **cluster_node_id** | **str**| The id of the node where this query exists if clustered. | [optional] 

### Return type

[**LineageEntity**](LineageEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_provenance**
> ProvenanceEntity get_provenance(id, cluster_node_id=cluster_node_id, summarize=summarize, incremental_results=incremental_results)

Gets a provenance query



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProvenanceApi()
id = 'id_example' # str | The id of the provenance query.
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where this query exists if clustered. (optional)
summarize = false # bool | Whether or not incremental results are returned. If false, provenance events are only returned once the query completes. This property is true by default. (optional) (default to false)
incremental_results = true # bool | Whether or not to summarize provenance events returned. This property is false by default. (optional) (default to true)

try: 
    # Gets a provenance query
    api_response = api_instance.get_provenance(id, cluster_node_id=cluster_node_id, summarize=summarize, incremental_results=incremental_results)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProvenanceApi->get_provenance: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the provenance query. | 
 **cluster_node_id** | **str**| The id of the node where this query exists if clustered. | [optional] 
 **summarize** | **bool**| Whether or not incremental results are returned. If false, provenance events are only returned once the query completes. This property is true by default. | [optional] [default to false]
 **incremental_results** | **bool**| Whether or not to summarize provenance events returned. This property is false by default. | [optional] [default to true]

### Return type

[**ProvenanceEntity**](ProvenanceEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_search_options**
> ProvenanceOptionsEntity get_search_options()

Gets the searchable attributes for provenance events



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProvenanceApi()

try: 
    # Gets the searchable attributes for provenance events
    api_response = api_instance.get_search_options()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProvenanceApi->get_search_options: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ProvenanceOptionsEntity**](ProvenanceOptionsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_lineage_request**
> LineageEntity submit_lineage_request(body)

Submits a lineage query

Lineage queries may be long running so this endpoint submits a request. The response will include the current state of the query. If the request is not completed the URI in the response can be used at a later time to get the updated state of the query. Once the query has completed the lineage request should be deleted by the client who originally submitted it.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProvenanceApi()
body = nifi.LineageEntity() # LineageEntity | The lineage query details.

try: 
    # Submits a lineage query
    api_response = api_instance.submit_lineage_request(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProvenanceApi->submit_lineage_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**LineageEntity**](LineageEntity.md)| The lineage query details. | 

### Return type

[**LineageEntity**](LineageEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_provenance_request**
> ProvenanceEntity submit_provenance_request(body)

Submits a provenance query

Provenance queries may be long running so this endpoint submits a request. The response will include the current state of the query. If the request is not completed the URI in the response can be used at a later time to get the updated state of the query. Once the query has completed the provenance request should be deleted by the client who originally submitted it.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.ProvenanceApi()
body = nifi.ProvenanceEntity() # ProvenanceEntity | The provenance query details.

try: 
    # Submits a provenance query
    api_response = api_instance.submit_provenance_request(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProvenanceApi->submit_provenance_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProvenanceEntity**](ProvenanceEntity.md)| The provenance query details. | 

### Return type

[**ProvenanceEntity**](ProvenanceEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

