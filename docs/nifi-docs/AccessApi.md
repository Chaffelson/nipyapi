# nifi.AccessApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_access_token**](AccessApi.md#create_access_token) | **POST** /access/token | Creates a token for accessing the REST API via username/password
[**create_access_token_from_ticket**](AccessApi.md#create_access_token_from_ticket) | **POST** /access/kerberos | Creates a token for accessing the REST API via Kerberos ticket exchange / SPNEGO negotiation
[**create_download_token**](AccessApi.md#create_download_token) | **POST** /access/download-token | Creates a single use access token for downloading FlowFile content.
[**create_ui_extension_token**](AccessApi.md#create_ui_extension_token) | **POST** /access/ui-extension-token | Creates a single use access token for accessing a NiFi UI extension.
[**get_access_status**](AccessApi.md#get_access_status) | **GET** /access | Gets the status the client&#39;s access
[**get_login_config**](AccessApi.md#get_login_config) | **GET** /access/config | Retrieves the access configuration for this NiFi
[**knox_callback**](AccessApi.md#knox_callback) | **GET** /access/knox/callback | Redirect/callback URI for processing the result of the Apache Knox login sequence.
[**knox_request**](AccessApi.md#knox_request) | **GET** /access/knox/request | Initiates a request to authenticate through Apache Knox.
[**oidc_callback**](AccessApi.md#oidc_callback) | **GET** /access/oidc/callback | Redirect/callback URI for processing the result of the OpenId Connect login sequence.
[**oidc_exchange**](AccessApi.md#oidc_exchange) | **POST** /access/oidc/exchange | Retrieves a JWT following a successful login sequence using the configured OpenId Connect provider.
[**oidc_request**](AccessApi.md#oidc_request) | **GET** /access/oidc/request | Initiates a request to authenticate through the configured OpenId Connect provider.


# **create_access_token**
> str create_access_token(username=username, password=password)

Creates a token for accessing the REST API via username/password

The token returned is formatted as a JSON Web Token (JWT). The token is base64 encoded and comprised of three parts. The header, the body, and the signature. The expiration of the token is a contained within the body. The token can be used in the Authorization header in the format 'Authorization: Bearer <token>'.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()
username = 'username_example' # str |  (optional)
password = 'password_example' # str |  (optional)

try: 
    # Creates a token for accessing the REST API via username/password
    api_response = api_instance.create_access_token(username=username, password=password)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->create_access_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | [optional] 
 **password** | **str**|  | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **create_access_token_from_ticket**
> str create_access_token_from_ticket()

Creates a token for accessing the REST API via Kerberos ticket exchange / SPNEGO negotiation

The token returned is formatted as a JSON Web Token (JWT). The token is base64 encoded and comprised of three parts. The header, the body, and the signature. The expiration of the token is a contained within the body. The token can be used in the Authorization header in the format 'Authorization: Bearer <token>'.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Creates a token for accessing the REST API via Kerberos ticket exchange / SPNEGO negotiation
    api_response = api_instance.create_access_token_from_ticket()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->create_access_token_from_ticket: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **create_download_token**
> str create_download_token()

Creates a single use access token for downloading FlowFile content.

The token returned is a base64 encoded string. It is valid for a single request up to five minutes from being issued. It is used as a query parameter name 'access_token'.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Creates a single use access token for downloading FlowFile content.
    api_response = api_instance.create_download_token()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->create_download_token: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **create_ui_extension_token**
> str create_ui_extension_token()

Creates a single use access token for accessing a NiFi UI extension.

The token returned is a base64 encoded string. It is valid for a single request up to five minutes from being issued. It is used as a query parameter name 'access_token'.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Creates a single use access token for accessing a NiFi UI extension.
    api_response = api_instance.create_ui_extension_token()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->create_ui_extension_token: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_access_status**
> AccessStatusEntity get_access_status()

Gets the status the client's access

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Gets the status the client's access
    api_response = api_instance.get_access_status()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->get_access_status: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AccessStatusEntity**](AccessStatusEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **get_login_config**
> AccessConfigurationEntity get_login_config()

Retrieves the access configuration for this NiFi



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Retrieves the access configuration for this NiFi
    api_response = api_instance.get_login_config()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->get_login_config: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AccessConfigurationEntity**](AccessConfigurationEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **knox_callback**
> knox_callback()

Redirect/callback URI for processing the result of the Apache Knox login sequence.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Redirect/callback URI for processing the result of the Apache Knox login sequence.
    api_instance.knox_callback()
except ApiException as e:
    print("Exception when calling AccessApi->knox_callback: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **knox_request**
> knox_request()

Initiates a request to authenticate through Apache Knox.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Initiates a request to authenticate through Apache Knox.
    api_instance.knox_request()
except ApiException as e:
    print("Exception when calling AccessApi->knox_request: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **oidc_callback**
> oidc_callback()

Redirect/callback URI for processing the result of the OpenId Connect login sequence.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Redirect/callback URI for processing the result of the OpenId Connect login sequence.
    api_instance.oidc_callback()
except ApiException as e:
    print("Exception when calling AccessApi->oidc_callback: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **oidc_exchange**
> str oidc_exchange()

Retrieves a JWT following a successful login sequence using the configured OpenId Connect provider.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Retrieves a JWT following a successful login sequence using the configured OpenId Connect provider.
    api_response = api_instance.oidc_exchange()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->oidc_exchange: %s\n" % e)
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

# **oidc_request**
> oidc_request()

Initiates a request to authenticate through the configured OpenId Connect provider.

Note: This endpoint is subject to change as NiFi and it's REST API evolve.

### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.AccessApi()

try: 
    # Initiates a request to authenticate through the configured OpenId Connect provider.
    api_instance.oidc_request()
except ApiException as e:
    print("Exception when calling AccessApi->oidc_request: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

