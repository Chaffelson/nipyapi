# nifi.SnippetsApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_snippet**](SnippetsApi.md#create_snippet) | **POST** /snippets | Creates a snippet. The snippet will be automatically discarded if not used in a subsequent request after 1 minute.
[**delete_snippet**](SnippetsApi.md#delete_snippet) | **DELETE** /snippets/{id} | Deletes the components in a snippet and discards the snippet
[**update_snippet**](SnippetsApi.md#update_snippet) | **PUT** /snippets/{id} | Move&#39;s the components in this Snippet into a new Process Group and discards the snippet


# **create_snippet**
> SnippetEntity create_snippet(body)

Creates a snippet. The snippet will be automatically discarded if not used in a subsequent request after 1 minute.



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.SnippetsApi()
body = nifi.SnippetEntity() # SnippetEntity | The snippet configuration details.

try: 
    # Creates a snippet. The snippet will be automatically discarded if not used in a subsequent request after 1 minute.
    api_response = api_instance.create_snippet(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SnippetsApi->create_snippet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SnippetEntity**](SnippetEntity.md)| The snippet configuration details. | 

### Return type

[**SnippetEntity**](SnippetEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **delete_snippet**
> SnippetEntity delete_snippet(id)

Deletes the components in a snippet and discards the snippet



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.SnippetsApi()
id = 'id_example' # str | The snippet id.

try: 
    # Deletes the components in a snippet and discards the snippet
    api_response = api_instance.delete_snippet(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SnippetsApi->delete_snippet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The snippet id. | 

### Return type

[**SnippetEntity**](SnippetEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_snippet**
> SnippetEntity update_snippet(id, body)

Move's the components in this Snippet into a new Process Group and discards the snippet



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.SnippetsApi()
id = 'id_example' # str | The snippet id.
body = nifi.SnippetEntity() # SnippetEntity | The snippet configuration details.

try: 
    # Move's the components in this Snippet into a new Process Group and discards the snippet
    api_response = api_instance.update_snippet(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SnippetsApi->update_snippet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The snippet id. | 
 **body** | [**SnippetEntity**](SnippetEntity.md)| The snippet configuration details. | 

### Return type

[**SnippetEntity**](SnippetEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

