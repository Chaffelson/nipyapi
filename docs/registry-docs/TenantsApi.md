# registry.TenantsApi

All URIs are relative to *http://localhost/nifi-registry-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_user**](TenantsApi.md#create_user) | **POST** /tenants/users | Creates a user
[**create_user_group**](TenantsApi.md#create_user_group) | **POST** /tenants/user-groups | Creates a user group
[**get_user**](TenantsApi.md#get_user) | **GET** /tenants/users/{id} | Gets a user
[**get_user_group**](TenantsApi.md#get_user_group) | **GET** /tenants/user-groups/{id} | Gets a user group
[**get_user_groups**](TenantsApi.md#get_user_groups) | **GET** /tenants/user-groups | Gets all user groups
[**get_users**](TenantsApi.md#get_users) | **GET** /tenants/users | Gets all users
[**remove_user**](TenantsApi.md#remove_user) | **DELETE** /tenants/users/{id} | Deletes a user
[**remove_user_group**](TenantsApi.md#remove_user_group) | **DELETE** /tenants/user-groups/{id} | Deletes a user group
[**update_user**](TenantsApi.md#update_user) | **PUT** /tenants/users/{id} | Updates a user
[**update_user_group**](TenantsApi.md#update_user_group) | **PUT** /tenants/user-groups/{id} | Updates a user group


# **create_user**
> User create_user(body)

Creates a user

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()
body = registry.User() # User | The user configuration details.

try: 
    # Creates a user
    api_response = api_instance.create_user(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->create_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**User**](User.md)| The user configuration details. | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **create_user_group**
> UserGroup create_user_group(body)

Creates a user group

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()
body = registry.UserGroup() # UserGroup | The user group configuration details.

try: 
    # Creates a user group
    api_response = api_instance.create_user_group(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->create_user_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserGroup**](UserGroup.md)| The user group configuration details. | 

### Return type

[**UserGroup**](UserGroup.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_user**
> User get_user(id)

Gets a user

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()
id = 'id_example' # str | The user id.

try: 
    # Gets a user
    api_response = api_instance.get_user(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->get_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user id. | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_user_group**
> UserGroup get_user_group(id)

Gets a user group

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()
id = 'id_example' # str | The user group id.

try: 
    # Gets a user group
    api_response = api_instance.get_user_group(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->get_user_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user group id. | 

### Return type

[**UserGroup**](UserGroup.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_user_groups**
> list[UserGroup] get_user_groups()

Gets all user groups

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()

try: 
    # Gets all user groups
    api_response = api_instance.get_user_groups()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->get_user_groups: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[UserGroup]**](UserGroup.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_users**
> list[User] get_users()

Gets all users

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()

try: 
    # Gets all users
    api_response = api_instance.get_users()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->get_users: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[User]**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **remove_user**
> User remove_user(id)

Deletes a user

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()
id = 'id_example' # str | The user id.

try: 
    # Deletes a user
    api_response = api_instance.remove_user(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->remove_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user id. | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **remove_user_group**
> UserGroup remove_user_group(id)

Deletes a user group

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()
id = 'id_example' # str | The user group id.

try: 
    # Deletes a user group
    api_response = api_instance.remove_user_group(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->remove_user_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user group id. | 

### Return type

[**UserGroup**](UserGroup.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **update_user**
> User update_user(id, body)

Updates a user

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()
id = 'id_example' # str | The user id.
body = registry.User() # User | The user configuration details.

try: 
    # Updates a user
    api_response = api_instance.update_user(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->update_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user id. | 
 **body** | [**User**](User.md)| The user configuration details. | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **update_user_group**
> UserGroup update_user_group(id, body)

Updates a user group

Note: This endpoint is subject to change as NiFi and its REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.TenantsApi()
id = 'id_example' # str | The user group id.
body = registry.UserGroup() # UserGroup | The user group configuration details.

try: 
    # Updates a user group
    api_response = api_instance.update_user_group(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->update_user_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user group id. | 
 **body** | [**UserGroup**](UserGroup.md)| The user group configuration details. | 

### Return type

[**UserGroup**](UserGroup.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

