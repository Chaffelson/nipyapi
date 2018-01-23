# VersionedFlowUpdateRequestDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_id** | **str** | The unique ID of this request. | [optional] 
**process_group_id** | **str** | The unique ID of the Process Group that the variable registry belongs to | [optional] 
**uri** | **str** | The URI for future requests to this drop request. | [optional] 
**last_updated** | **str** | The last time this request was updated. | [optional] 
**complete** | **bool** | Whether or not this request has completed | [optional] 
**failure_reason** | **str** | An explanation of why this request failed, or null if this request has not failed | [optional] 
**percent_completed** | **int** | The percentage complete for the request, between 0 and 100 | [optional] 
**state** | **str** | The state of the request | [optional] 
**version_control_information** | [**VersionControlInformationDTO**](VersionControlInformationDTO.md) | The VersionControlInformation that describes where the Versioned Flow is located; this may not be populated until the request is completed. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


