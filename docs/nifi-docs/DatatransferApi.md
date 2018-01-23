# nifi.DatatransferApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**commit_input_port_transaction**](DatatransferApi.md#commit_input_port_transaction) | **DELETE** /data-transfer/input-ports/{portId}/transactions/{transactionId} | Commit or cancel the specified transaction
[**commit_output_port_transaction**](DatatransferApi.md#commit_output_port_transaction) | **DELETE** /data-transfer/output-ports/{portId}/transactions/{transactionId} | Commit or cancel the specified transaction
[**create_port_transaction**](DatatransferApi.md#create_port_transaction) | **POST** /data-transfer/{portType}/{portId}/transactions | Create a transaction to the specified output port or input port
[**extend_input_port_transaction_ttl**](DatatransferApi.md#extend_input_port_transaction_ttl) | **PUT** /data-transfer/input-ports/{portId}/transactions/{transactionId} | Extend transaction TTL
[**extend_output_port_transaction_ttl**](DatatransferApi.md#extend_output_port_transaction_ttl) | **PUT** /data-transfer/output-ports/{portId}/transactions/{transactionId} | Extend transaction TTL
[**receive_flow_files**](DatatransferApi.md#receive_flow_files) | **POST** /data-transfer/input-ports/{portId}/transactions/{transactionId}/flow-files | Transfer flow files to the input port
[**transfer_flow_files**](DatatransferApi.md#transfer_flow_files) | **GET** /data-transfer/output-ports/{portId}/transactions/{transactionId}/flow-files | Transfer flow files from the output port


# **commit_input_port_transaction**
> TransactionResultEntity commit_input_port_transaction(response_code, port_id, transaction_id)

Commit or cancel the specified transaction



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.DatatransferApi()
response_code = 56 # int | The response code. Available values are BAD_CHECKSUM(19), CONFIRM_TRANSACTION(12) or CANCEL_TRANSACTION(15).
port_id = 'port_id_example' # str | The input port id.
transaction_id = 'transaction_id_example' # str | The transaction id.

try: 
    # Commit or cancel the specified transaction
    api_response = api_instance.commit_input_port_transaction(response_code, port_id, transaction_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatatransferApi->commit_input_port_transaction: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **response_code** | **int**| The response code. Available values are BAD_CHECKSUM(19), CONFIRM_TRANSACTION(12) or CANCEL_TRANSACTION(15). | 
 **port_id** | **str**| The input port id. | 
 **transaction_id** | **str**| The transaction id. | 

### Return type

[**TransactionResultEntity**](TransactionResultEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **commit_output_port_transaction**
> TransactionResultEntity commit_output_port_transaction(response_code, checksum, port_id, transaction_id)

Commit or cancel the specified transaction



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.DatatransferApi()
response_code = 56 # int | The response code. Available values are CONFIRM_TRANSACTION(12) or CANCEL_TRANSACTION(15).
checksum = 'checksum_example' # str | A checksum calculated at client side using CRC32 to check flow file content integrity. It must match with the value calculated at server side.
port_id = 'port_id_example' # str | The output port id.
transaction_id = 'transaction_id_example' # str | The transaction id.

try: 
    # Commit or cancel the specified transaction
    api_response = api_instance.commit_output_port_transaction(response_code, checksum, port_id, transaction_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatatransferApi->commit_output_port_transaction: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **response_code** | **int**| The response code. Available values are CONFIRM_TRANSACTION(12) or CANCEL_TRANSACTION(15). | 
 **checksum** | **str**| A checksum calculated at client side using CRC32 to check flow file content integrity. It must match with the value calculated at server side. | 
 **port_id** | **str**| The output port id. | 
 **transaction_id** | **str**| The transaction id. | 

### Return type

[**TransactionResultEntity**](TransactionResultEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_port_transaction**
> TransactionResultEntity create_port_transaction(port_type, port_id)

Create a transaction to the specified output port or input port



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.DatatransferApi()
port_type = 'port_type_example' # str | The port type.
port_id = 'port_id_example' # str | 

try: 
    # Create a transaction to the specified output port or input port
    api_response = api_instance.create_port_transaction(port_type, port_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatatransferApi->create_port_transaction: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_type** | **str**| The port type. | 
 **port_id** | **str**|  | 

### Return type

[**TransactionResultEntity**](TransactionResultEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **extend_input_port_transaction_ttl**
> TransactionResultEntity extend_input_port_transaction_ttl(port_id, transaction_id)

Extend transaction TTL



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.DatatransferApi()
port_id = 'port_id_example' # str | 
transaction_id = 'transaction_id_example' # str | 

try: 
    # Extend transaction TTL
    api_response = api_instance.extend_input_port_transaction_ttl(port_id, transaction_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatatransferApi->extend_input_port_transaction_ttl: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**|  | 
 **transaction_id** | **str**|  | 

### Return type

[**TransactionResultEntity**](TransactionResultEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **extend_output_port_transaction_ttl**
> TransactionResultEntity extend_output_port_transaction_ttl(port_id, transaction_id)

Extend transaction TTL



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.DatatransferApi()
port_id = 'port_id_example' # str | 
transaction_id = 'transaction_id_example' # str | 

try: 
    # Extend transaction TTL
    api_response = api_instance.extend_output_port_transaction_ttl(port_id, transaction_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatatransferApi->extend_output_port_transaction_ttl: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**|  | 
 **transaction_id** | **str**|  | 

### Return type

[**TransactionResultEntity**](TransactionResultEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **receive_flow_files**
> str receive_flow_files(port_id, transaction_id)

Transfer flow files to the input port



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.DatatransferApi()
port_id = 'port_id_example' # str | The input port id.
transaction_id = 'transaction_id_example' # str | 

try: 
    # Transfer flow files to the input port
    api_response = api_instance.receive_flow_files(port_id, transaction_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatatransferApi->receive_flow_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**| The input port id. | 
 **transaction_id** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **transfer_flow_files**
> StreamingOutput transfer_flow_files(port_id, transaction_id)

Transfer flow files from the output port



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.DatatransferApi()
port_id = 'port_id_example' # str | The output port id.
transaction_id = 'transaction_id_example' # str | 

try: 
    # Transfer flow files from the output port
    api_response = api_instance.transfer_flow_files(port_id, transaction_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatatransferApi->transfer_flow_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**| The output port id. | 
 **transaction_id** | **str**|  | 

### Return type

[**StreamingOutput**](StreamingOutput.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/octet-stream

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

