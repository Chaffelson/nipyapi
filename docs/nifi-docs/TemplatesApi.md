# nifi.TemplatesApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**export_template**](TemplatesApi.md#export_template) | **GET** /templates/{id}/download | Exports a template
[**remove_template**](TemplatesApi.md#remove_template) | **DELETE** /templates/{id} | Deletes a template


# **export_template**
> str export_template(id)

Exports a template



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TemplatesApi()
id = 'id_example' # str | The template id.

try: 
    # Exports a template
    api_response = api_instance.export_template(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TemplatesApi->export_template: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The template id. | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_template**
> TemplateEntity remove_template(id)

Deletes a template



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.TemplatesApi()
id = 'id_example' # str | The template id.

try: 
    # Deletes a template
    api_response = api_instance.remove_template(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TemplatesApi->remove_template: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The template id. | 

### Return type

[**TemplateEntity**](TemplateEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

