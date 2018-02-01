# nifi.VersionsApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_version_control_request**](VersionsApi.md#create_version_control_request) | **POST** /versions/active-requests | Creates a request so that a Process Group can be placed under Version Control or have its Version Control configuration changed. Creating this request will prevent any other threads from simultaneously saving local changes to Version Control. It will not, however, actually save the local flow to the Flow Registry. A POST to /versions/process-groups/{id} should be used to initiate saving of the local flow to the Flow Registry.
[**delete_revert_request**](VersionsApi.md#delete_revert_request) | **DELETE** /versions/revert-requests/{id} | Deletes the Revert Request with the given ID. After a request is created via a POST to /versions/revert-requests/process-groups/{id}, it is expected that the client will properly clean up the request by DELETE&#39;ing it, once the Revert process has completed. If the request is deleted before the request completes, then the Revert request will finish the step that it is currently performing and then will cancel any subsequent steps.
[**delete_update_request**](VersionsApi.md#delete_update_request) | **DELETE** /versions/update-requests/{id} | Deletes the Update Request with the given ID. After a request is created via a POST to /versions/update-requests/process-groups/{id}, it is expected that the client will properly clean up the request by DELETE&#39;ing it, once the Update process has completed. If the request is deleted before the request completes, then the Update request will finish the step that it is currently performing and then will cancel any subsequent steps.
[**delete_version_control_request**](VersionsApi.md#delete_version_control_request) | **DELETE** /versions/active-requests/{id} | Deletes the Version Control Request with the given ID. This will allow other threads to save flows to the Flow Registry. See also the documentation for POSTing to /versions/active-requests for information regarding why this is done.
[**get_revert_request**](VersionsApi.md#get_revert_request) | **GET** /versions/revert-requests/{id} | Returns the Revert Request with the given ID. Once a Revert Request has been created by performing a POST to /versions/revert-requests/process-groups/{id}, that request can subsequently be retrieved via this endpoint, and the request that is fetched will contain the updated state, such as percent complete, the current state of the request, and any failures.
[**get_update_request**](VersionsApi.md#get_update_request) | **GET** /versions/update-requests/{id} | Returns the Update Request with the given ID. Once an Update Request has been created by performing a POST to /versions/update-requests/process-groups/{id}, that request can subsequently be retrieved via this endpoint, and the request that is fetched will contain the updated state, such as percent complete, the current state of the request, and any failures.
[**get_version_information**](VersionsApi.md#get_version_information) | **GET** /versions/process-groups/{id} | Gets the Version Control information for a process group
[**initiate_revert_flow_version**](VersionsApi.md#initiate_revert_flow_version) | **POST** /versions/revert-requests/process-groups/{id} | For a Process Group that is already under Version Control, this will initiate the action of reverting any local changes that have been made to the Process Group since it was last synchronized with the Flow Registry. This will result in the flow matching the Versioned Flow that exists in the Flow Registry. This can be a lengthy process, as it will stop any Processors and disable any Controller Services necessary to perform the action and then restart them. As a result, the endpoint will immediately return a VersionedFlowUpdateRequestEntity, and the process of updating the flow will occur asynchronously in the background. The client may then periodically poll the status of the request by issuing a GET request to /versions/revert-requests/{requestId}. Once the request is completed, the client is expected to issue a DELETE request to /versions/revert-requests/{requestId}.
[**initiate_version_control_update**](VersionsApi.md#initiate_version_control_update) | **POST** /versions/update-requests/process-groups/{id} | For a Process Group that is already under Version Control, this will initiate the action of changing from a specific version of the flow in the Flow Registry to a different version of the flow. This can be a lengthy process, as it will stop any Processors and disable any Controller Services necessary to perform the action and then restart them. As a result, the endpoint will immediately return a VersionedFlowUpdateRequestEntity, and the process of updating the flow will occur asynchronously in the background. The client may then periodically poll the status of the request by issuing a GET request to /versions/update-requests/{requestId}. Once the request is completed, the client is expected to issue a DELETE request to /versions/update-requests/{requestId}.
[**save_to_flow_registry**](VersionsApi.md#save_to_flow_registry) | **POST** /versions/process-groups/{id} | Begins version controlling the Process Group with the given ID or commits changes to the Versioned Flow, depending on if the provided VersionControlInformation includes a flowId
[**stop_version_control**](VersionsApi.md#stop_version_control) | **DELETE** /versions/process-groups/{id} | Stops version controlling the Process Group with the given ID. The Process Group will no longer track to any Versioned Flow.
[**update_flow_version**](VersionsApi.md#update_flow_version) | **PUT** /versions/process-groups/{id} | For a Process Group that is already under Version Control, this will update the version of the flow to a different version. This endpoint expects that the given snapshot will not modify any Processor that is currently running or any Controller Service that is enabled.
[**update_version_control_request**](VersionsApi.md#update_version_control_request) | **PUT** /versions/active-requests/{id} | Updates the request with the given ID


# **create_version_control_request**
> str create_version_control_request(body)

Creates a request so that a Process Group can be placed under Version Control or have its Version Control configuration changed. Creating this request will prevent any other threads from simultaneously saving local changes to Version Control. It will not, however, actually save the local flow to the Flow Registry. A POST to /versions/process-groups/{id} should be used to initiate saving of the local flow to the Flow Registry.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
body = nifi.CreateActiveRequestEntity() # CreateActiveRequestEntity | The versioned flow details.

try: 
    # Creates a request so that a Process Group can be placed under Version Control or have its Version Control configuration changed. Creating this request will prevent any other threads from simultaneously saving local changes to Version Control. It will not, however, actually save the local flow to the Flow Registry. A POST to /versions/process-groups/{id} should be used to initiate saving of the local flow to the Flow Registry.
    api_response = api_instance.create_version_control_request(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->create_version_control_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateActiveRequestEntity**](CreateActiveRequestEntity.md)| The versioned flow details. | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **delete_revert_request**
> VersionedFlowUpdateRequestEntity delete_revert_request(id)

Deletes the Revert Request with the given ID. After a request is created via a POST to /versions/revert-requests/process-groups/{id}, it is expected that the client will properly clean up the request by DELETE'ing it, once the Revert process has completed. If the request is deleted before the request completes, then the Revert request will finish the step that it is currently performing and then will cancel any subsequent steps.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The ID of the Revert Request

try: 
    # Deletes the Revert Request with the given ID. After a request is created via a POST to /versions/revert-requests/process-groups/{id}, it is expected that the client will properly clean up the request by DELETE'ing it, once the Revert process has completed. If the request is deleted before the request completes, then the Revert request will finish the step that it is currently performing and then will cancel any subsequent steps.
    api_response = api_instance.delete_revert_request(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->delete_revert_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the Revert Request | 

### Return type

[**VersionedFlowUpdateRequestEntity**](VersionedFlowUpdateRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **delete_update_request**
> VersionedFlowUpdateRequestEntity delete_update_request(id)

Deletes the Update Request with the given ID. After a request is created via a POST to /versions/update-requests/process-groups/{id}, it is expected that the client will properly clean up the request by DELETE'ing it, once the Update process has completed. If the request is deleted before the request completes, then the Update request will finish the step that it is currently performing and then will cancel any subsequent steps.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The ID of the Update Request

try: 
    # Deletes the Update Request with the given ID. After a request is created via a POST to /versions/update-requests/process-groups/{id}, it is expected that the client will properly clean up the request by DELETE'ing it, once the Update process has completed. If the request is deleted before the request completes, then the Update request will finish the step that it is currently performing and then will cancel any subsequent steps.
    api_response = api_instance.delete_update_request(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->delete_update_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the Update Request | 

### Return type

[**VersionedFlowUpdateRequestEntity**](VersionedFlowUpdateRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **delete_version_control_request**
> delete_version_control_request(id)

Deletes the Version Control Request with the given ID. This will allow other threads to save flows to the Flow Registry. See also the documentation for POSTing to /versions/active-requests for information regarding why this is done.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The request ID.

try: 
    # Deletes the Version Control Request with the given ID. This will allow other threads to save flows to the Flow Registry. See also the documentation for POSTing to /versions/active-requests for information regarding why this is done.
    api_instance.delete_version_control_request(id)
except ApiException as e:
    print("Exception when calling VersionsApi->delete_version_control_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The request ID. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_revert_request**
> VersionedFlowUpdateRequestEntity get_revert_request(id)

Returns the Revert Request with the given ID. Once a Revert Request has been created by performing a POST to /versions/revert-requests/process-groups/{id}, that request can subsequently be retrieved via this endpoint, and the request that is fetched will contain the updated state, such as percent complete, the current state of the request, and any failures.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The ID of the Revert Request

try: 
    # Returns the Revert Request with the given ID. Once a Revert Request has been created by performing a POST to /versions/revert-requests/process-groups/{id}, that request can subsequently be retrieved via this endpoint, and the request that is fetched will contain the updated state, such as percent complete, the current state of the request, and any failures.
    api_response = api_instance.get_revert_request(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->get_revert_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the Revert Request | 

### Return type

[**VersionedFlowUpdateRequestEntity**](VersionedFlowUpdateRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_update_request**
> VersionedFlowUpdateRequestEntity get_update_request(id)

Returns the Update Request with the given ID. Once an Update Request has been created by performing a POST to /versions/update-requests/process-groups/{id}, that request can subsequently be retrieved via this endpoint, and the request that is fetched will contain the updated state, such as percent complete, the current state of the request, and any failures.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The ID of the Update Request

try: 
    # Returns the Update Request with the given ID. Once an Update Request has been created by performing a POST to /versions/update-requests/process-groups/{id}, that request can subsequently be retrieved via this endpoint, and the request that is fetched will contain the updated state, such as percent complete, the current state of the request, and any failures.
    api_response = api_instance.get_update_request(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->get_update_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the Update Request | 

### Return type

[**VersionedFlowUpdateRequestEntity**](VersionedFlowUpdateRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_version_information**
> VersionControlInformationEntity get_version_information(id)

Gets the Version Control information for a process group

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The process group id.

try: 
    # Gets the Version Control information for a process group
    api_response = api_instance.get_version_information(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->get_version_information: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 

### Return type

[**VersionControlInformationEntity**](VersionControlInformationEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **initiate_revert_flow_version**
> VersionedFlowUpdateRequestEntity initiate_revert_flow_version(id, body)

For a Process Group that is already under Version Control, this will initiate the action of reverting any local changes that have been made to the Process Group since it was last synchronized with the Flow Registry. This will result in the flow matching the Versioned Flow that exists in the Flow Registry. This can be a lengthy process, as it will stop any Processors and disable any Controller Services necessary to perform the action and then restart them. As a result, the endpoint will immediately return a VersionedFlowUpdateRequestEntity, and the process of updating the flow will occur asynchronously in the background. The client may then periodically poll the status of the request by issuing a GET request to /versions/revert-requests/{requestId}. Once the request is completed, the client is expected to issue a DELETE request to /versions/revert-requests/{requestId}.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The process group id.
body = nifi.VersionControlInformationEntity() # VersionControlInformationEntity | The controller service configuration details.

try: 
    # For a Process Group that is already under Version Control, this will initiate the action of reverting any local changes that have been made to the Process Group since it was last synchronized with the Flow Registry. This will result in the flow matching the Versioned Flow that exists in the Flow Registry. This can be a lengthy process, as it will stop any Processors and disable any Controller Services necessary to perform the action and then restart them. As a result, the endpoint will immediately return a VersionedFlowUpdateRequestEntity, and the process of updating the flow will occur asynchronously in the background. The client may then periodically poll the status of the request by issuing a GET request to /versions/revert-requests/{requestId}. Once the request is completed, the client is expected to issue a DELETE request to /versions/revert-requests/{requestId}.
    api_response = api_instance.initiate_revert_flow_version(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->initiate_revert_flow_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 
 **body** | [**VersionControlInformationEntity**](VersionControlInformationEntity.md)| The controller service configuration details. | 

### Return type

[**VersionedFlowUpdateRequestEntity**](VersionedFlowUpdateRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **initiate_version_control_update**
> VersionedFlowUpdateRequestEntity initiate_version_control_update(id, body)

For a Process Group that is already under Version Control, this will initiate the action of changing from a specific version of the flow in the Flow Registry to a different version of the flow. This can be a lengthy process, as it will stop any Processors and disable any Controller Services necessary to perform the action and then restart them. As a result, the endpoint will immediately return a VersionedFlowUpdateRequestEntity, and the process of updating the flow will occur asynchronously in the background. The client may then periodically poll the status of the request by issuing a GET request to /versions/update-requests/{requestId}. Once the request is completed, the client is expected to issue a DELETE request to /versions/update-requests/{requestId}.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The process group id.
body = nifi.VersionControlInformationEntity() # VersionControlInformationEntity | The controller service configuration details.

try: 
    # For a Process Group that is already under Version Control, this will initiate the action of changing from a specific version of the flow in the Flow Registry to a different version of the flow. This can be a lengthy process, as it will stop any Processors and disable any Controller Services necessary to perform the action and then restart them. As a result, the endpoint will immediately return a VersionedFlowUpdateRequestEntity, and the process of updating the flow will occur asynchronously in the background. The client may then periodically poll the status of the request by issuing a GET request to /versions/update-requests/{requestId}. Once the request is completed, the client is expected to issue a DELETE request to /versions/update-requests/{requestId}.
    api_response = api_instance.initiate_version_control_update(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->initiate_version_control_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 
 **body** | [**VersionControlInformationEntity**](VersionControlInformationEntity.md)| The controller service configuration details. | 

### Return type

[**VersionedFlowUpdateRequestEntity**](VersionedFlowUpdateRequestEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **save_to_flow_registry**
> VersionControlInformationEntity save_to_flow_registry(id, body)

Begins version controlling the Process Group with the given ID or commits changes to the Versioned Flow, depending on if the provided VersionControlInformation includes a flowId

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The process group id.
body = nifi.StartVersionControlRequestEntity() # StartVersionControlRequestEntity | The versioned flow details.

try: 
    # Begins version controlling the Process Group with the given ID or commits changes to the Versioned Flow, depending on if the provided VersionControlInformation includes a flowId
    api_response = api_instance.save_to_flow_registry(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->save_to_flow_registry: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 
 **body** | [**StartVersionControlRequestEntity**](StartVersionControlRequestEntity.md)| The versioned flow details. | 

### Return type

[**VersionControlInformationEntity**](VersionControlInformationEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **stop_version_control**
> VersionControlInformationEntity stop_version_control(id, version=version, client_id=client_id)

Stops version controlling the Process Group with the given ID. The Process Group will no longer track to any Versioned Flow.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The process group id.
version = 'version_example' # str | The version is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, a new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Stops version controlling the Process Group with the given ID. The Process Group will no longer track to any Versioned Flow.
    api_response = api_instance.stop_version_control(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->stop_version_control: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 
 **version** | **str**| The version is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, a new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**VersionControlInformationEntity**](VersionControlInformationEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_flow_version**
> VersionControlInformationEntity update_flow_version(id, body)

For a Process Group that is already under Version Control, this will update the version of the flow to a different version. This endpoint expects that the given snapshot will not modify any Processor that is currently running or any Controller Service that is enabled.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The process group id.
body = nifi.VersionedFlowSnapshotEntity() # VersionedFlowSnapshotEntity | The controller service configuration details.

try: 
    # For a Process Group that is already under Version Control, this will update the version of the flow to a different version. This endpoint expects that the given snapshot will not modify any Processor that is currently running or any Controller Service that is enabled.
    api_response = api_instance.update_flow_version(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->update_flow_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 
 **body** | [**VersionedFlowSnapshotEntity**](VersionedFlowSnapshotEntity.md)| The controller service configuration details. | 

### Return type

[**VersionControlInformationEntity**](VersionControlInformationEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_version_control_request**
> VersionControlInformationEntity update_version_control_request(id, body)

Updates the request with the given ID

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.VersionsApi()
id = 'id_example' # str | The request ID.
body = nifi.VersionControlComponentMappingEntity() # VersionControlComponentMappingEntity | The version control component mapping.

try: 
    # Updates the request with the given ID
    api_response = api_instance.update_version_control_request(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsApi->update_version_control_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The request ID. | 
 **body** | [**VersionControlComponentMappingEntity**](VersionControlComponentMappingEntity.md)| The version control component mapping. | 

### Return type

[**VersionControlInformationEntity**](VersionControlInformationEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

