# nifi.TenantsApi

All URIs are relative to *http://localhost/nifi-api*

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
[**search_tenants**](TenantsApi.md#search_tenants) | **GET** /tenants/search-results | Searches for a tenant with the specified identity
[**update_user**](TenantsApi.md#update_user) | **PUT** /tenants/users/{id} | Updates a user
[**update_user_group**](TenantsApi.md#update_user_group) | **PUT** /tenants/user-groups/{id} | Updates a user group


# **create_user**
> UserEntity create_user(body)

Creates a user

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()
body = nifi.UserEntity() # UserEntity | The user configuration details.

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
 **body** | [**UserEntity**](UserEntity.md)| The user configuration details. | 

### Return type

[**UserEntity**](UserEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **create_user_group**
> UserGroupEntity create_user_group(body)

Creates a user group

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()
body = nifi.UserGroupEntity() # UserGroupEntity | The user group configuration details.

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
 **body** | [**UserGroupEntity**](UserGroupEntity.md)| The user group configuration details. | 

### Return type

[**UserGroupEntity**](UserGroupEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_user**
> UserEntity get_user(id)

Gets a user

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()
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

[**UserEntity**](UserEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_user_group**
> UserGroupEntity get_user_group(id)

Gets a user group

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()
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

[**UserGroupEntity**](UserGroupEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_user_groups**
> UserGroupsEntity get_user_groups()

Gets all user groups

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()

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

[**UserGroupsEntity**](UserGroupsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_users**
> UsersEntity get_users()

Gets all users

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()

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

[**UsersEntity**](UsersEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **remove_user**
> UserEntity remove_user(id, version=version, client_id=client_id)

Deletes a user

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()
id = 'id_example' # str | The user id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes a user
    api_response = api_instance.remove_user(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->remove_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**UserEntity**](UserEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **remove_user_group**
> UserGroupEntity remove_user_group(id, version=version, client_id=client_id)

Deletes a user group

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()
id = 'id_example' # str | The user group id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes a user group
    api_response = api_instance.remove_user_group(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->remove_user_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user group id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**UserGroupEntity**](UserGroupEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **search_tenants**
> TenantsEntity search_tenants(q)

Searches for a tenant with the specified identity

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()
q = 'q_example' # str | Identity to search for.

try: 
    # Searches for a tenant with the specified identity
    api_response = api_instance.search_tenants(q)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TenantsApi->search_tenants: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Identity to search for. | 

### Return type

[**TenantsEntity**](TenantsEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_user**
> UserEntity update_user(id, body)

Updates a user

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()
id = 'id_example' # str | The user id.
body = nifi.UserEntity() # UserEntity | The user configuration details.

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
 **body** | [**UserEntity**](UserEntity.md)| The user configuration details. | 

### Return type

[**UserEntity**](UserEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_user_group**
> UserGroupEntity update_user_group(id, body)

Updates a user group

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TenantsApi()
id = 'id_example' # str | The user group id.
body = nifi.UserGroupEntity() # UserGroupEntity | The user group configuration details.

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
 **body** | [**UserGroupEntity**](UserGroupEntity.md)| The user group configuration details. | 

### Return type

[**UserGroupEntity**](UserGroupEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

