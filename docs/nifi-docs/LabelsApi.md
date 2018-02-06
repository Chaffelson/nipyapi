# nifi.LabelsApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_label**](LabelsApi.md#get_label) | **GET** /labels/{id} | Gets a label
[**remove_label**](LabelsApi.md#remove_label) | **DELETE** /labels/{id} | Deletes a label
[**update_label**](LabelsApi.md#update_label) | **PUT** /labels/{id} | Updates a label


# **get_label**
> LabelEntity get_label(id)

Gets a label



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.LabelsApi()
id = 'id_example' # str | The label id.

try: 
    # Gets a label
    api_response = api_instance.get_label(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LabelsApi->get_label: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The label id. | 

### Return type

[**LabelEntity**](LabelEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **remove_label**
> LabelEntity remove_label(id, version=version, client_id=client_id)

Deletes a label



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.LabelsApi()
id = 'id_example' # str | The label id.
version = 'version_example' # str | The revision is used to verify the client is working with the latest version of the flow. (optional)
client_id = 'client_id_example' # str | If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. (optional)

try: 
    # Deletes a label
    api_response = api_instance.remove_label(id, version=version, client_id=client_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LabelsApi->remove_label: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The label id. | 
 **version** | **str**| The revision is used to verify the client is working with the latest version of the flow. | [optional] 
 **client_id** | **str**| If the client id is not specified, new one will be generated. This value (whether specified or generated) is included in the response. | [optional] 

### Return type

[**LabelEntity**](LabelEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

# **update_label**
> LabelEntity update_label(id, body)

Updates a label



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.LabelsApi()
id = 'id_example' # str | The label id.
body = nifi.LabelEntity() # LabelEntity | The label configuration details.

try: 
    # Updates a label
    api_response = api_instance.update_label(id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LabelsApi->update_label: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The label id. | 
 **body** | [**LabelEntity**](LabelEntity.md)| The label configuration details. | 

### Return type

[**LabelEntity**](LabelEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to README]](../nifiDocs.md)

