# registry.PoliciesApi

All URIs are relative to *http://localhost/nifi-registry-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_access_policy**](PoliciesApi.md#create_access_policy) | **POST** /policies | Creates an access policy
[**get_access_policies**](PoliciesApi.md#get_access_policies) | **GET** /policies | Gets all access policies
[**get_access_policy**](PoliciesApi.md#get_access_policy) | **GET** /policies/{id} | Gets an access policy
[**get_access_policy_for_resource**](PoliciesApi.md#get_access_policy_for_resource) | **GET** /policies/{action}/{resource} | Gets an access policy for the specified action and resource
[**get_resources**](PoliciesApi.md#get_resources) | **GET** /policies/resources | Gets the available resources that support access/authorization policies
[**remove_access_policy**](PoliciesApi.md#remove_access_policy) | **DELETE** /policies/{id} | Deletes an access policy
[**update_access_policy**](PoliciesApi.md#update_access_policy) | **PUT** /policies/{id} | Updates a access policy


# **create_access_policy**
> AccessPolicy create_access_policy(body)

Creates an access policy



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.PoliciesApi()
body = registry.AccessPolicy() # AccessPolicy | The access policy configuration details.

try: 
    # Creates an access policy
    api_response = api_instance.create_access_policy(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoliciesApi->create_access_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AccessPolicy**](AccessPolicy.md)| The access policy configuration details. | 

### Return type

[**AccessPolicy**](AccessPolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_access_policies**
> list[AccessPolicy] get_access_policies()

Gets all access policies



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.PoliciesApi()

try: 
    # Gets all access policies
    api_response = api_instance.get_access_policies()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoliciesApi->get_access_policies: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[AccessPolicy]**](AccessPolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_access_policy**
> AccessPolicy get_access_policy(id)

Gets an access policy



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.PoliciesApi()
id = 'id_example' # str | The access policy id.

try: 
    # Gets an access policy
    api_response = api_instance.get_access_policy(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoliciesApi->get_access_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The access policy id. | 

### Return type

[**AccessPolicy**](AccessPolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_access_policy_for_resource**
> AccessPolicy get_access_policy_for_resource(action, resource)

Gets an access policy for the specified action and resource

Will return the effective policy if no specific policy exists for the specified action and resource. Must have Read permissions to the policy with the desired action and resource. Permissions for the policy that is returned will be indicated in the response. If the client does not have permissions to that policy, the response will not include the policy and the permissions in the response will be marked accordingly. If the client does not have permissions to the policy of the desired action and resource a 403 response will be returned.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.PoliciesApi()
action = 'action_example' # str | The request action.
resource = 'resource_example' # str | The resource of the policy.

try: 
    # Gets an access policy for the specified action and resource
    api_response = api_instance.get_access_policy_for_resource(action, resource)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoliciesApi->get_access_policy_for_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **action** | **str**| The request action. | 
 **resource** | **str**| The resource of the policy. | 

### Return type

[**AccessPolicy**](AccessPolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_resources**
> list[Resource] get_resources()

Gets the available resources that support access/authorization policies



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.PoliciesApi()

try: 
    # Gets the available resources that support access/authorization policies
    api_response = api_instance.get_resources()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoliciesApi->get_resources: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Resource]**](Resource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **remove_access_policy**
> AccessPolicy remove_access_policy(id)

Deletes an access policy



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.PoliciesApi()
id = 'id_example' # str | The access policy id.

try: 
    # Deletes an access policy
    api_response = api_instance.remove_access_policy(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoliciesApi->remove_access_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The access policy id. | 

### Return type

[**AccessPolicy**](AccessPolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **update_access_policy**
> AccessPolicy update_access_policy(id, body)

Updates a access policy



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.PoliciesApi()
id = 'id_example' # str | The access policy id.
body = registry.AccessPolicy() # AccessPolicy | The access policy configuration details.

try: 
    # Updates a access policy
    api_response = api_instance.update_access_policy(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoliciesApi->update_access_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The access policy id. | 
 **body** | [**AccessPolicy**](AccessPolicy.md)| The access policy configuration details. | 

### Return type

[**AccessPolicy**](AccessPolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

