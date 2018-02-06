# registry.AccessApi

All URIs are relative to *http://localhost/nifi-registry-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_access_token_by_trying_all_providers**](AccessApi.md#create_access_token_by_trying_all_providers) | **POST** /access/token | Creates a token for accessing the REST API via auto-detected method of verifying client identity claim credentials
[**create_access_token_using_form_login**](AccessApi.md#create_access_token_using_form_login) | **POST** /access/token/login | Creates a token for accessing the REST API via username/password
[**create_access_token_using_identity_provider_credentials**](AccessApi.md#create_access_token_using_identity_provider_credentials) | **POST** /access/token/identity-provider | Creates a token for accessing the REST API via a custom identity provider.
[**create_access_token_using_kerberos_ticket**](AccessApi.md#create_access_token_using_kerberos_ticket) | **POST** /access/token/kerberos | Creates a token for accessing the REST API via Kerberos Service Tickets or SPNEGO Tokens (which includes Kerberos Service Tickets)
[**get_access_status**](AccessApi.md#get_access_status) | **GET** /access | Returns the current client&#39;s authenticated identity and permissions to top-level resources
[**get_identity_provider_usage_instructions**](AccessApi.md#get_identity_provider_usage_instructions) | **GET** /access/token/identity-provider/usage | Provides a description of how the currently configured identity provider expects credentials to be passed to POST /access/token/identity-provider
[**test_identity_provider_recognizes_credentials_format**](AccessApi.md#test_identity_provider_recognizes_credentials_format) | **POST** /access/token/identity-provider/test | Tests the format of the credentials against this identity provider without preforming authentication on the credentials to validate them.


# **create_access_token_by_trying_all_providers**
> str create_access_token_by_trying_all_providers()

Creates a token for accessing the REST API via auto-detected method of verifying client identity claim credentials

The token returned is formatted as a JSON Web Token (JWT). The token is base64 encoded and comprised of three parts. The header, the body, and the signature. The expiration of the token is a contained within the body. The token can be used in the Authorization header in the format 'Authorization: Bearer <token>'.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.AccessApi()

try: 
    # Creates a token for accessing the REST API via auto-detected method of verifying client identity claim credentials
    api_response = api_instance.create_access_token_by_trying_all_providers()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->create_access_token_by_trying_all_providers: %s\n" % e)
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

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **create_access_token_using_form_login**
> str create_access_token_using_form_login()

Creates a token for accessing the REST API via username/password

The user credentials must be passed in standard HTTP Basic Auth format. That is: 'Authorization: Basic <credentials>', where <credentials> is the base64 encoded value of '<username>:<password>'. The token returned is formatted as a JSON Web Token (JWT). The token is base64 encoded and comprised of three parts. The header, the body, and the signature. The expiration of the token is a contained within the body. The token can be used in the Authorization header in the format 'Authorization: Bearer <token>'.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.AccessApi()

try: 
    # Creates a token for accessing the REST API via username/password
    api_response = api_instance.create_access_token_using_form_login()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->create_access_token_using_form_login: %s\n" % e)
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

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **create_access_token_using_identity_provider_credentials**
> str create_access_token_using_identity_provider_credentials()

Creates a token for accessing the REST API via a custom identity provider.

The user credentials must be passed in a format understood by the custom identity provider, e.g., a third-party auth token in an HTTP header. The exact format of the user credentials expected by the custom identity provider can be discovered by 'GET /access/token/identity-provider/usage'. The token returned is formatted as a JSON Web Token (JWT). The token is base64 encoded and comprised of three parts. The header, the body, and the signature. The expiration of the token is a contained within the body. The token can be used in the Authorization header in the format 'Authorization: Bearer <token>'.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.AccessApi()

try: 
    # Creates a token for accessing the REST API via a custom identity provider.
    api_response = api_instance.create_access_token_using_identity_provider_credentials()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->create_access_token_using_identity_provider_credentials: %s\n" % e)
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

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **create_access_token_using_kerberos_ticket**
> str create_access_token_using_kerberos_ticket()

Creates a token for accessing the REST API via Kerberos Service Tickets or SPNEGO Tokens (which includes Kerberos Service Tickets)

The token returned is formatted as a JSON Web Token (JWT). The token is base64 encoded and comprised of three parts. The header, the body, and the signature. The expiration of the token is a contained within the body. The token can be used in the Authorization header in the format 'Authorization: Bearer <token>'.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.AccessApi()

try: 
    # Creates a token for accessing the REST API via Kerberos Service Tickets or SPNEGO Tokens (which includes Kerberos Service Tickets)
    api_response = api_instance.create_access_token_using_kerberos_ticket()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->create_access_token_using_kerberos_ticket: %s\n" % e)
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

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_access_status**
> CurrentUser get_access_status()

Returns the current client's authenticated identity and permissions to top-level resources



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.AccessApi()

try: 
    # Returns the current client's authenticated identity and permissions to top-level resources
    api_response = api_instance.get_access_status()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->get_access_status: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CurrentUser**](CurrentUser.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **get_identity_provider_usage_instructions**
> str get_identity_provider_usage_instructions()

Provides a description of how the currently configured identity provider expects credentials to be passed to POST /access/token/identity-provider



### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.AccessApi()

try: 
    # Provides a description of how the currently configured identity provider expects credentials to be passed to POST /access/token/identity-provider
    api_response = api_instance.get_identity_provider_usage_instructions()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->get_identity_provider_usage_instructions: %s\n" % e)
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

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

# **test_identity_provider_recognizes_credentials_format**
> str test_identity_provider_recognizes_credentials_format()

Tests the format of the credentials against this identity provider without preforming authentication on the credentials to validate them.

The user credentials should be passed in a format understood by the custom identity provider as defined by 'GET /access/token/identity-provider/usage'.

### Example 
```python
from __future__ import print_function
import time
import registry
from registry.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = registry.AccessApi()

try: 
    # Tests the format of the credentials against this identity provider without preforming authentication on the credentials to validate them.
    api_response = api_instance.test_identity_provider_recognizes_credentials_format()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessApi->test_identity_provider_recognizes_credentials_format: %s\n" % e)
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

[[Back to top]](#) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to README]](../registryDocs.md)

