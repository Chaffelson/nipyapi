# nifi.FlowApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate_controller_services**](FlowApi.md#activate_controller_services) | **PUT** /flow/process-groups/{id}/controller-services | Enable or disable Controller Services in the specified Process Group.
[**generate_client_id**](FlowApi.md#generate_client_id) | **GET** /flow/client-id | Generates a client id.
[**get_about_info**](FlowApi.md#get_about_info) | **GET** /flow/about | Retrieves details about this NiFi to put in the About dialog
[**get_action**](FlowApi.md#get_action) | **GET** /flow/history/{id} | Gets an action
[**get_banners**](FlowApi.md#get_banners) | **GET** /flow/banners | Retrieves the banners for this NiFi
[**get_buckets**](FlowApi.md#get_buckets) | **GET** /flow/registries/{id}/buckets | Gets the buckets from the specified registry for the current user
[**get_bulletin_board**](FlowApi.md#get_bulletin_board) | **GET** /flow/bulletin-board | Gets current bulletins
[**get_bulletins**](FlowApi.md#get_bulletins) | **GET** /flow/controller/bulletins | Retrieves Controller level bulletins
[**get_cluster_summary**](FlowApi.md#get_cluster_summary) | **GET** /flow/cluster/summary | The cluster summary for this NiFi
[**get_component_history**](FlowApi.md#get_component_history) | **GET** /flow/history/components/{componentId} | Gets configuration history for a component
[**get_connection_status**](FlowApi.md#get_connection_status) | **GET** /flow/connections/{id}/status | Gets status for a connection
[**get_connection_status_history**](FlowApi.md#get_connection_status_history) | **GET** /flow/connections/{id}/status/history | Gets the status history for a connection
[**get_controller_service_types**](FlowApi.md#get_controller_service_types) | **GET** /flow/controller-service-types | Retrieves the types of controller services that this NiFi supports
[**get_controller_services_from_controller**](FlowApi.md#get_controller_services_from_controller) | **GET** /flow/controller/controller-services | Gets all controller services
[**get_controller_services_from_group**](FlowApi.md#get_controller_services_from_group) | **GET** /flow/process-groups/{id}/controller-services | Gets all controller services
[**get_controller_status**](FlowApi.md#get_controller_status) | **GET** /flow/status | Gets the current status of this NiFi
[**get_current_user**](FlowApi.md#get_current_user) | **GET** /flow/current-user | Retrieves the user identity of the user making the request
[**get_flow**](FlowApi.md#get_flow) | **GET** /flow/process-groups/{id} | Gets a process group
[**get_flow_config**](FlowApi.md#get_flow_config) | **GET** /flow/config | Retrieves the configuration for this NiFi flow
[**get_flows**](FlowApi.md#get_flows) | **GET** /flow/registries/{registry-id}/buckets/{bucket-id}/flows | Gets the flows from the specified registry and bucket for the current user
[**get_input_port_status**](FlowApi.md#get_input_port_status) | **GET** /flow/input-ports/{id}/status | Gets status for an input port
[**get_output_port_status**](FlowApi.md#get_output_port_status) | **GET** /flow/output-ports/{id}/status | Gets status for an output port
[**get_prioritizers**](FlowApi.md#get_prioritizers) | **GET** /flow/prioritizers | Retrieves the types of prioritizers that this NiFi supports
[**get_process_group_status**](FlowApi.md#get_process_group_status) | **GET** /flow/process-groups/{id}/status | Gets the status for a process group
[**get_process_group_status_history**](FlowApi.md#get_process_group_status_history) | **GET** /flow/process-groups/{id}/status/history | Gets status history for a remote process group
[**get_processor_status**](FlowApi.md#get_processor_status) | **GET** /flow/processors/{id}/status | Gets status for a processor
[**get_processor_status_history**](FlowApi.md#get_processor_status_history) | **GET** /flow/processors/{id}/status/history | Gets status history for a processor
[**get_processor_types**](FlowApi.md#get_processor_types) | **GET** /flow/processor-types | Retrieves the types of processors that this NiFi supports
[**get_registries**](FlowApi.md#get_registries) | **GET** /flow/registries | Gets the listing of available registries
[**get_remote_process_group_status**](FlowApi.md#get_remote_process_group_status) | **GET** /flow/remote-process-groups/{id}/status | Gets status for a remote process group
[**get_remote_process_group_status_history**](FlowApi.md#get_remote_process_group_status_history) | **GET** /flow/remote-process-groups/{id}/status/history | Gets the status history
[**get_reporting_task_types**](FlowApi.md#get_reporting_task_types) | **GET** /flow/reporting-task-types | Retrieves the types of reporting tasks that this NiFi supports
[**get_reporting_tasks**](FlowApi.md#get_reporting_tasks) | **GET** /flow/reporting-tasks | Gets all reporting tasks
[**get_templates**](FlowApi.md#get_templates) | **GET** /flow/templates | Gets all templates
[**get_versions**](FlowApi.md#get_versions) | **GET** /flow/registries/{registry-id}/buckets/{bucket-id}/flows/{flow-id}/versions | Gets the flow versions from the specified registry and bucket for the specified flow for the current user
[**query_history**](FlowApi.md#query_history) | **GET** /flow/history | Gets configuration history
[**schedule_components**](FlowApi.md#schedule_components) | **PUT** /flow/process-groups/{id} | Schedule or unschedule components in the specified Process Group.
[**search_cluster**](FlowApi.md#search_cluster) | **GET** /flow/cluster/search-results | Searches the cluster for a node with the specified address
[**search_flow**](FlowApi.md#search_flow) | **GET** /flow/search-results | Performs a search against this NiFi using the specified search term


# **activate_controller_services**
> ActivateControllerServicesEntity activate_controller_services(id, body)

Enable or disable Controller Services in the specified Process Group.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The process group id.
body = nifi.ActivateControllerServicesEntity() # ActivateControllerServicesEntity | The request to schedule or unschedule. If the comopnents in the request are not specified, all authorized components will be considered.

try: 
    # Enable or disable Controller Services in the specified Process Group.
    api_response = api_instance.activate_controller_services(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->activate_controller_services: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 
 **body** | [**ActivateControllerServicesEntity**](ActivateControllerServicesEntity.md)| The request to schedule or unschedule. If the comopnents in the request are not specified, all authorized components will be considered. | 

### Return type

[**ActivateControllerServicesEntity**](ActivateControllerServicesEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **generate_client_id**
> str generate_client_id()

Generates a client id.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Generates a client id.
    api_response = api_instance.generate_client_id()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->generate_client_id: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_about_info**
> AboutEntity get_about_info()

Retrieves details about this NiFi to put in the About dialog



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Retrieves details about this NiFi to put in the About dialog
    api_response = api_instance.get_about_info()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_about_info: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AboutEntity**](AboutEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_action**
> ActionEntity get_action(id)

Gets an action

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The action id.

try: 
    # Gets an action
    api_response = api_instance.get_action(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The action id. | 

### Return type

[**ActionEntity**](ActionEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_banners**
> BannerEntity get_banners()

Retrieves the banners for this NiFi



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Retrieves the banners for this NiFi
    api_response = api_instance.get_banners()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_banners: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BannerEntity**](BannerEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_buckets**
> BucketsEntity get_buckets(id)

Gets the buckets from the specified registry for the current user



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The registry id.

try: 
    # Gets the buckets from the specified registry for the current user
    api_response = api_instance.get_buckets(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_buckets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The registry id. | 

### Return type

[**BucketsEntity**](BucketsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_bulletin_board**
> BulletinBoardEntity get_bulletin_board(after=after, source_name=source_name, message=message, source_id=source_id, group_id=group_id, limit=limit)

Gets current bulletins



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
after = 'after_example' # str | Includes bulletins with an id after this value. (optional)
source_name = 'source_name_example' # str | Includes bulletins originating from this sources whose name match this regular expression. (optional)
message = 'message_example' # str | Includes bulletins whose message that match this regular expression. (optional)
source_id = 'source_id_example' # str | Includes bulletins originating from this sources whose id match this regular expression. (optional)
group_id = 'group_id_example' # str | Includes bulletins originating from this sources whose group id match this regular expression. (optional)
limit = 'limit_example' # str | The number of bulletins to limit the response to. (optional)

try: 
    # Gets current bulletins
    api_response = api_instance.get_bulletin_board(after=after, source_name=source_name, message=message, source_id=source_id, group_id=group_id, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_bulletin_board: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **after** | **str**| Includes bulletins with an id after this value. | [optional] 
 **source_name** | **str**| Includes bulletins originating from this sources whose name match this regular expression. | [optional] 
 **message** | **str**| Includes bulletins whose message that match this regular expression. | [optional] 
 **source_id** | **str**| Includes bulletins originating from this sources whose id match this regular expression. | [optional] 
 **group_id** | **str**| Includes bulletins originating from this sources whose group id match this regular expression. | [optional] 
 **limit** | **str**| The number of bulletins to limit the response to. | [optional] 

### Return type

[**BulletinBoardEntity**](BulletinBoardEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_bulletins**
> ControllerBulletinsEntity get_bulletins()

Retrieves Controller level bulletins



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Retrieves Controller level bulletins
    api_response = api_instance.get_bulletins()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_bulletins: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ControllerBulletinsEntity**](ControllerBulletinsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_cluster_summary**
> ClusteSummaryEntity get_cluster_summary()

The cluster summary for this NiFi



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # The cluster summary for this NiFi
    api_response = api_instance.get_cluster_summary()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_cluster_summary: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ClusteSummaryEntity**](ClusteSummaryEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_component_history**
> ComponentHistoryEntity get_component_history(component_id)

Gets configuration history for a component

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
component_id = 'component_id_example' # str | The component id.

try: 
    # Gets configuration history for a component
    api_response = api_instance.get_component_history(component_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_component_history: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **component_id** | **str**| The component id. | 

### Return type

[**ComponentHistoryEntity**](ComponentHistoryEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_connection_status**
> ConnectionStatusEntity get_connection_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)

Gets status for a connection



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The connection id.
nodewise = false # bool | Whether or not to include the breakdown per node. Optional, defaults to false (optional) (default to false)
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where to get the status. (optional)

try: 
    # Gets status for a connection
    api_response = api_instance.get_connection_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_connection_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 
 **nodewise** | **bool**| Whether or not to include the breakdown per node. Optional, defaults to false | [optional] [default to false]
 **cluster_node_id** | **str**| The id of the node where to get the status. | [optional] 

### Return type

[**ConnectionStatusEntity**](ConnectionStatusEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_connection_status_history**
> StatusHistoryEntity get_connection_status_history(id)

Gets the status history for a connection



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The connection id.

try: 
    # Gets the status history for a connection
    api_response = api_instance.get_connection_status_history(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_connection_status_history: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The connection id. | 

### Return type

[**StatusHistoryEntity**](StatusHistoryEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_controller_service_types**
> ControllerServiceTypesEntity get_controller_service_types(service_type=service_type, service_bundle_group=service_bundle_group, service_bundle_artifact=service_bundle_artifact, service_bundle_version=service_bundle_version, bundle_group_filter=bundle_group_filter, bundle_artifact_filter=bundle_artifact_filter, type_filter=type_filter)

Retrieves the types of controller services that this NiFi supports

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
service_type = 'service_type_example' # str | If specified, will only return controller services that are compatible with this type of service. (optional)
service_bundle_group = 'service_bundle_group_example' # str | If serviceType specified, is the bundle group of the serviceType. (optional)
service_bundle_artifact = 'service_bundle_artifact_example' # str | If serviceType specified, is the bundle artifact of the serviceType. (optional)
service_bundle_version = 'service_bundle_version_example' # str | If serviceType specified, is the bundle version of the serviceType. (optional)
bundle_group_filter = 'bundle_group_filter_example' # str | If specified, will only return types that are a member of this bundle group. (optional)
bundle_artifact_filter = 'bundle_artifact_filter_example' # str | If specified, will only return types that are a member of this bundle artifact. (optional)
type_filter = 'type_filter_example' # str | If specified, will only return types whose fully qualified classname matches. (optional)

try: 
    # Retrieves the types of controller services that this NiFi supports
    api_response = api_instance.get_controller_service_types(service_type=service_type, service_bundle_group=service_bundle_group, service_bundle_artifact=service_bundle_artifact, service_bundle_version=service_bundle_version, bundle_group_filter=bundle_group_filter, bundle_artifact_filter=bundle_artifact_filter, type_filter=type_filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_controller_service_types: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_type** | **str**| If specified, will only return controller services that are compatible with this type of service. | [optional] 
 **service_bundle_group** | **str**| If serviceType specified, is the bundle group of the serviceType. | [optional] 
 **service_bundle_artifact** | **str**| If serviceType specified, is the bundle artifact of the serviceType. | [optional] 
 **service_bundle_version** | **str**| If serviceType specified, is the bundle version of the serviceType. | [optional] 
 **bundle_group_filter** | **str**| If specified, will only return types that are a member of this bundle group. | [optional] 
 **bundle_artifact_filter** | **str**| If specified, will only return types that are a member of this bundle artifact. | [optional] 
 **type_filter** | **str**| If specified, will only return types whose fully qualified classname matches. | [optional] 

### Return type

[**ControllerServiceTypesEntity**](ControllerServiceTypesEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_controller_services_from_controller**
> ControllerServicesEntity get_controller_services_from_controller()

Gets all controller services



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Gets all controller services
    api_response = api_instance.get_controller_services_from_controller()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_controller_services_from_controller: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ControllerServicesEntity**](ControllerServicesEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_controller_services_from_group**
> ControllerServicesEntity get_controller_services_from_group(id, include_ancestor_groups=include_ancestor_groups, include_descendant_groups=include_descendant_groups)

Gets all controller services



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The process group id.
include_ancestor_groups = true # bool | Whether or not to include parent/ancestory process groups (optional) (default to true)
include_descendant_groups = false # bool | Whether or not to include descendant process groups (optional) (default to false)

try: 
    # Gets all controller services
    api_response = api_instance.get_controller_services_from_group(id, include_ancestor_groups=include_ancestor_groups, include_descendant_groups=include_descendant_groups)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_controller_services_from_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 
 **include_ancestor_groups** | **bool**| Whether or not to include parent/ancestory process groups | [optional] [default to true]
 **include_descendant_groups** | **bool**| Whether or not to include descendant process groups | [optional] [default to false]

### Return type

[**ControllerServicesEntity**](ControllerServicesEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_controller_status**
> ControllerStatusEntity get_controller_status()

Gets the current status of this NiFi



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Gets the current status of this NiFi
    api_response = api_instance.get_controller_status()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_controller_status: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ControllerStatusEntity**](ControllerStatusEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_current_user**
> CurrentUserEntity get_current_user()

Retrieves the user identity of the user making the request



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Retrieves the user identity of the user making the request
    api_response = api_instance.get_current_user()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_current_user: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CurrentUserEntity**](CurrentUserEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_flow**
> ProcessGroupFlowEntity get_flow(id)

Gets a process group



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The process group id.

try: 
    # Gets a process group
    api_response = api_instance.get_flow(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_flow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 

### Return type

[**ProcessGroupFlowEntity**](ProcessGroupFlowEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_flow_config**
> FlowConfigurationEntity get_flow_config()

Retrieves the configuration for this NiFi flow



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Retrieves the configuration for this NiFi flow
    api_response = api_instance.get_flow_config()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_flow_config: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**FlowConfigurationEntity**](FlowConfigurationEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_flows**
> BucketsEntity get_flows(registry_id, bucket_id)

Gets the flows from the specified registry and bucket for the current user



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
registry_id = 'registry_id_example' # str | The registry id.
bucket_id = 'bucket_id_example' # str | The bucket id.

try: 
    # Gets the flows from the specified registry and bucket for the current user
    api_response = api_instance.get_flows(registry_id, bucket_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_flows: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_id** | **str**| The registry id. | 
 **bucket_id** | **str**| The bucket id. | 

### Return type

[**BucketsEntity**](BucketsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_input_port_status**
> PortStatusEntity get_input_port_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)

Gets status for an input port



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The input port id.
nodewise = false # bool | Whether or not to include the breakdown per node. Optional, defaults to false (optional) (default to false)
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where to get the status. (optional)

try: 
    # Gets status for an input port
    api_response = api_instance.get_input_port_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_input_port_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The input port id. | 
 **nodewise** | **bool**| Whether or not to include the breakdown per node. Optional, defaults to false | [optional] [default to false]
 **cluster_node_id** | **str**| The id of the node where to get the status. | [optional] 

### Return type

[**PortStatusEntity**](PortStatusEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_output_port_status**
> PortStatusEntity get_output_port_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)

Gets status for an output port



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The output port id.
nodewise = false # bool | Whether or not to include the breakdown per node. Optional, defaults to false (optional) (default to false)
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where to get the status. (optional)

try: 
    # Gets status for an output port
    api_response = api_instance.get_output_port_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_output_port_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The output port id. | 
 **nodewise** | **bool**| Whether or not to include the breakdown per node. Optional, defaults to false | [optional] [default to false]
 **cluster_node_id** | **str**| The id of the node where to get the status. | [optional] 

### Return type

[**PortStatusEntity**](PortStatusEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_prioritizers**
> PrioritizerTypesEntity get_prioritizers()

Retrieves the types of prioritizers that this NiFi supports

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Retrieves the types of prioritizers that this NiFi supports
    api_response = api_instance.get_prioritizers()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_prioritizers: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**PrioritizerTypesEntity**](PrioritizerTypesEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_process_group_status**
> ProcessGroupStatusEntity get_process_group_status(id, recursive=recursive, nodewise=nodewise, cluster_node_id=cluster_node_id)

Gets the status for a process group

The status for a process group includes status for all descendent components. When invoked on the root group with recursive set to true, it will return the current status of every component in the flow.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The process group id.
recursive = false # bool | Whether all descendant groups and the status of their content will be included. Optional, defaults to false (optional) (default to false)
nodewise = false # bool | Whether or not to include the breakdown per node. Optional, defaults to false (optional) (default to false)
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where to get the status. (optional)

try: 
    # Gets the status for a process group
    api_response = api_instance.get_process_group_status(id, recursive=recursive, nodewise=nodewise, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_process_group_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 
 **recursive** | **bool**| Whether all descendant groups and the status of their content will be included. Optional, defaults to false | [optional] [default to false]
 **nodewise** | **bool**| Whether or not to include the breakdown per node. Optional, defaults to false | [optional] [default to false]
 **cluster_node_id** | **str**| The id of the node where to get the status. | [optional] 

### Return type

[**ProcessGroupStatusEntity**](ProcessGroupStatusEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_process_group_status_history**
> StatusHistoryEntity get_process_group_status_history(id)

Gets status history for a remote process group



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The process group id.

try: 
    # Gets status history for a remote process group
    api_response = api_instance.get_process_group_status_history(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_process_group_status_history: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 

### Return type

[**StatusHistoryEntity**](StatusHistoryEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_processor_status**
> ProcessorStatusEntity get_processor_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)

Gets status for a processor



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The processor id.
nodewise = false # bool | Whether or not to include the breakdown per node. Optional, defaults to false (optional) (default to false)
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where to get the status. (optional)

try: 
    # Gets status for a processor
    api_response = api_instance.get_processor_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_processor_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The processor id. | 
 **nodewise** | **bool**| Whether or not to include the breakdown per node. Optional, defaults to false | [optional] [default to false]
 **cluster_node_id** | **str**| The id of the node where to get the status. | [optional] 

### Return type

[**ProcessorStatusEntity**](ProcessorStatusEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_processor_status_history**
> StatusHistoryEntity get_processor_status_history(id)

Gets status history for a processor



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The processor id.

try: 
    # Gets status history for a processor
    api_response = api_instance.get_processor_status_history(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_processor_status_history: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The processor id. | 

### Return type

[**StatusHistoryEntity**](StatusHistoryEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_processor_types**
> ProcessorTypesEntity get_processor_types(bundle_group_filter=bundle_group_filter, bundle_artifact_filter=bundle_artifact_filter, type=type)

Retrieves the types of processors that this NiFi supports

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
bundle_group_filter = 'bundle_group_filter_example' # str | If specified, will only return types that are a member of this bundle group. (optional)
bundle_artifact_filter = 'bundle_artifact_filter_example' # str | If specified, will only return types that are a member of this bundle artifact. (optional)
type = 'type_example' # str | If specified, will only return types whose fully qualified classname matches. (optional)

try: 
    # Retrieves the types of processors that this NiFi supports
    api_response = api_instance.get_processor_types(bundle_group_filter=bundle_group_filter, bundle_artifact_filter=bundle_artifact_filter, type=type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_processor_types: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bundle_group_filter** | **str**| If specified, will only return types that are a member of this bundle group. | [optional] 
 **bundle_artifact_filter** | **str**| If specified, will only return types that are a member of this bundle artifact. | [optional] 
 **type** | **str**| If specified, will only return types whose fully qualified classname matches. | [optional] 

### Return type

[**ProcessorTypesEntity**](ProcessorTypesEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_registries**
> RegistryClientsEntity get_registries()

Gets the listing of available registries



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Gets the listing of available registries
    api_response = api_instance.get_registries()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_registries: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**RegistryClientsEntity**](RegistryClientsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_remote_process_group_status**
> RemoteProcessGroupStatusEntity get_remote_process_group_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)

Gets status for a remote process group



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The remote process group id.
nodewise = false # bool | Whether or not to include the breakdown per node. Optional, defaults to false (optional) (default to false)
cluster_node_id = 'cluster_node_id_example' # str | The id of the node where to get the status. (optional)

try: 
    # Gets status for a remote process group
    api_response = api_instance.get_remote_process_group_status(id, nodewise=nodewise, cluster_node_id=cluster_node_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_remote_process_group_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The remote process group id. | 
 **nodewise** | **bool**| Whether or not to include the breakdown per node. Optional, defaults to false | [optional] [default to false]
 **cluster_node_id** | **str**| The id of the node where to get the status. | [optional] 

### Return type

[**RemoteProcessGroupStatusEntity**](RemoteProcessGroupStatusEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_remote_process_group_status_history**
> StatusHistoryEntity get_remote_process_group_status_history(id)

Gets the status history



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The remote process group id.

try: 
    # Gets the status history
    api_response = api_instance.get_remote_process_group_status_history(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_remote_process_group_status_history: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The remote process group id. | 

### Return type

[**StatusHistoryEntity**](StatusHistoryEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_reporting_task_types**
> ReportingTaskTypesEntity get_reporting_task_types(bundle_group_filter=bundle_group_filter, bundle_artifact_filter=bundle_artifact_filter, type=type)

Retrieves the types of reporting tasks that this NiFi supports

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
bundle_group_filter = 'bundle_group_filter_example' # str | If specified, will only return types that are a member of this bundle group. (optional)
bundle_artifact_filter = 'bundle_artifact_filter_example' # str | If specified, will only return types that are a member of this bundle artifact. (optional)
type = 'type_example' # str | If specified, will only return types whose fully qualified classname matches. (optional)

try: 
    # Retrieves the types of reporting tasks that this NiFi supports
    api_response = api_instance.get_reporting_task_types(bundle_group_filter=bundle_group_filter, bundle_artifact_filter=bundle_artifact_filter, type=type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_reporting_task_types: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bundle_group_filter** | **str**| If specified, will only return types that are a member of this bundle group. | [optional] 
 **bundle_artifact_filter** | **str**| If specified, will only return types that are a member of this bundle artifact. | [optional] 
 **type** | **str**| If specified, will only return types whose fully qualified classname matches. | [optional] 

### Return type

[**ReportingTaskTypesEntity**](ReportingTaskTypesEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_reporting_tasks**
> ReportingTasksEntity get_reporting_tasks()

Gets all reporting tasks



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Gets all reporting tasks
    api_response = api_instance.get_reporting_tasks()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_reporting_tasks: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ReportingTasksEntity**](ReportingTasksEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_templates**
> TemplatesEntity get_templates()

Gets all templates



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()

try: 
    # Gets all templates
    api_response = api_instance.get_templates()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_templates: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**TemplatesEntity**](TemplatesEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_versions**
> BucketsEntity get_versions(registry_id, bucket_id, flow_id)

Gets the flow versions from the specified registry and bucket for the specified flow for the current user



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
registry_id = 'registry_id_example' # str | The registry id.
bucket_id = 'bucket_id_example' # str | The bucket id.
flow_id = 'flow_id_example' # str | The flow id.

try: 
    # Gets the flow versions from the specified registry and bucket for the specified flow for the current user
    api_response = api_instance.get_versions(registry_id, bucket_id, flow_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->get_versions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_id** | **str**| The registry id. | 
 **bucket_id** | **str**| The bucket id. | 
 **flow_id** | **str**| The flow id. | 

### Return type

[**BucketsEntity**](BucketsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **query_history**
> HistoryEntity query_history(offset, count, sort_column=sort_column, sort_order=sort_order, start_date=start_date, end_date=end_date, user_identity=user_identity, source_id=source_id)

Gets configuration history

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
offset = 'offset_example' # str | The offset into the result set.
count = 'count_example' # str | The number of actions to return.
sort_column = 'sort_column_example' # str | The field to sort on. (optional)
sort_order = 'sort_order_example' # str | The direction to sort. (optional)
start_date = 'start_date_example' # str | Include actions after this date. (optional)
end_date = 'end_date_example' # str | Include actions before this date. (optional)
user_identity = 'user_identity_example' # str | Include actions performed by this user. (optional)
source_id = 'source_id_example' # str | Include actions on this component. (optional)

try: 
    # Gets configuration history
    api_response = api_instance.query_history(offset, count, sort_column=sort_column, sort_order=sort_order, start_date=start_date, end_date=end_date, user_identity=user_identity, source_id=source_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->query_history: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **str**| The offset into the result set. | 
 **count** | **str**| The number of actions to return. | 
 **sort_column** | **str**| The field to sort on. | [optional] 
 **sort_order** | **str**| The direction to sort. | [optional] 
 **start_date** | **str**| Include actions after this date. | [optional] 
 **end_date** | **str**| Include actions before this date. | [optional] 
 **user_identity** | **str**| Include actions performed by this user. | [optional] 
 **source_id** | **str**| Include actions on this component. | [optional] 

### Return type

[**HistoryEntity**](HistoryEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **schedule_components**
> ScheduleComponentsEntity schedule_components(id, body)

Schedule or unschedule components in the specified Process Group.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
id = 'id_example' # str | The process group id.
body = nifi.ScheduleComponentsEntity() # ScheduleComponentsEntity | The request to schedule or unschedule. If the comopnents in the request are not specified, all authorized components will be considered.

try: 
    # Schedule or unschedule components in the specified Process Group.
    api_response = api_instance.schedule_components(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->schedule_components: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The process group id. | 
 **body** | [**ScheduleComponentsEntity**](ScheduleComponentsEntity.md)| The request to schedule or unschedule. If the comopnents in the request are not specified, all authorized components will be considered. | 

### Return type

[**ScheduleComponentsEntity**](ScheduleComponentsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **search_cluster**
> ClusterSearchResultsEntity search_cluster(q)

Searches the cluster for a node with the specified address

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
q = 'q_example' # str | Node address to search for.

try: 
    # Searches the cluster for a node with the specified address
    api_response = api_instance.search_cluster(q)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->search_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Node address to search for. | 

### Return type

[**ClusterSearchResultsEntity**](ClusterSearchResultsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **search_flow**
> SearchResultsEntity search_flow(q=q)

Performs a search against this NiFi using the specified search term

Only search results from authorized components will be returned.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.FlowApi()
q = 'q_example' # str |  (optional)

try: 
    # Performs a search against this NiFi using the specified search term
    api_response = api_instance.search_flow(q=q)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FlowApi->search_flow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**|  | [optional] 

### Return type

[**SearchResultsEntity**](SearchResultsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

