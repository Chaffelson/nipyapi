# VariableRegistryUpdateRequestDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_id** | **str** | The unique ID of this request. | [optional] 
**process_group_id** | **str** | The unique ID of the Process Group that the variable registry belongs to | [optional] 
**uri** | **str** | The URI for future requests to this drop request. | [optional] 
**submission_time** | **str** | The time at which this request was submitted. | [optional] 
**last_updated** | **str** | The last time this request was updated. | [optional] 
**complete** | **bool** | Whether or not this request has completed | [optional] 
**failure_reason** | **str** | An explanation of why this request failed, or null if this request has not failed | [optional] 
**update_steps** | [**list[VariableRegistryUpdateStepDTO]**](VariableRegistryUpdateStepDTO.md) | The steps that are required in order to complete the request, along with the status of each | [optional] 
**affected_components** | [**list[AffectedComponentEntity]**](AffectedComponentEntity.md) | A set of all components that will be affected if the value of this variable is changed | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


