# nifi.SitetositeApi

All URIs are relative to *http://localhost/nifi-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_peers**](SitetositeApi.md#get_peers) | **GET** /site-to-site/peers | Returns the available Peers and its status of this NiFi
[**get_site_to_site_details**](SitetositeApi.md#get_site_to_site_details) | **GET** /site-to-site | Returns the details about this NiFi necessary to communicate via site to site


# **get_peers**
> PeersEntity get_peers()

Returns the available Peers and its status of this NiFi



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.SitetositeApi()

try: 
    # Returns the available Peers and its status of this NiFi
    api_response = api_instance.get_peers()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SitetositeApi->get_peers: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**PeersEntity**](PeersEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json, application/xml

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_site_to_site_details**
> ControllerEntity get_site_to_site_details()

Returns the details about this NiFi necessary to communicate via site to site



### Example 
```python
from __future__ import print_function
import time
import nifi
from nifi.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nifi.SitetositeApi()

try: 
    # Returns the details about this NiFi necessary to communicate via site to site
    api_response = api_instance.get_site_to_site_details()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SitetositeApi->get_site_to_site_details: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ControllerEntity**](ControllerEntity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

