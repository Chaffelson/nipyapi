# nifi.PoliciesApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_access_policy**](PoliciesApi.md#create_access_policy) | **POST** /policies | Creates an access policy
[**get_access_policy**](PoliciesApi.md#get_access_policy) | **GET** /policies/{id} | Gets an access policy
[**get_access_policy_for_resource**](PoliciesApi.md#get_access_policy_for_resource) | **GET** /policies/{action}/{resource} | Gets an access policy for the specified action and resource
[**remove_access_policy**](PoliciesApi.md#remove_access_policy) | **DELETE** /policies/{id} | Deletes an access policy
[**update_access_policy**](PoliciesApi.md#update_access_policy) | **PUT** /policies/{id} | Updates a access policy


# **create_access_policy**
> AccessPolicyEntity create_access_policy(body)

Creates an access policy



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.PoliciesApi()
body = nifi.AccessPolicyEntity() # AccessPolicyEntity | The access policy configuration details.

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
 **body** | [**AccessPolicyEntity**](AccessPolicyEntity.md)| The access policy configuration details. | 

### Return type

[**AccessPolicyEntity**](AccessPolicyEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_access_policy**
> AccessPolicyEntity get_access_policy(id)

Gets an access policy



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.PoliciesApi()
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

[**AccessPolicyEntity**](AccessPolicyEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_access_policy_for_resource**
> AccessPolicyEntity get_access_policy_for_resource(action, resource)

Gets an access policy for the specified action and resource

Will return the effective policy if no component specific policy exists for the specified action and resource. Must have Read permissions to the policy with the desired action and resource. Permissions for the policy that is returned will be indicated in the response. This means the client could be authorized to get the policy for a given component but the effective policy may be inherited from an ancestor Process Group. If the client does not have permissions to that policy, the response will not include the policy and the permissions in the response will be marked accordingly. If the client does not have permissions to the policy of the desired action and resource a 403 response will be returned.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.PoliciesApi()
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

[**AccessPolicyEntity**](AccessPolicyEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_access_policy**
> AccessPolicyEntity remove_access_policy(id, version=version, client_id=client_id)

Deletes an access policy



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.PoliciesApi()
id = 'id_example' # str | The access policy id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes an access policy
    api_response = api_instance.remove_access_policy(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoliciesApi->remove_access_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The access policy id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**AccessPolicyEntity**](AccessPolicyEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_access_policy**
> AccessPolicyEntity update_access_policy(id, body)

Updates a access policy



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.PoliciesApi()
id = 'id_example' # str | The access policy id.
body = nifi.AccessPolicyEntity() # AccessPolicyEntity | The access policy configuration details.

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
 **body** | [**AccessPolicyEntity**](AccessPolicyEntity.md)| The access policy configuration details. | 

### Return type

[**AccessPolicyEntity**](AccessPolicyEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

