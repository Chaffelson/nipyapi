# AffectedComponentDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**process_group_id** | **str** | The UUID of the Process Group that this component is in | [optional] 
**id** | **str** | The UUID of this component | [optional] 
**reference_type** | **str** | The type of this component | [optional] 
**name** | **str** | The name of this component. | [optional] 
**state** | **str** | The scheduled state of a processor or reporting task referencing a controller service. If this component is another controller service, this field represents the controller service state. | [optional] 
**active_thread_count** | **int** | The number of active threads for the referencing component. | [optional] 
**validation_errors** | **list[str]** | The validation errors for the component. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


