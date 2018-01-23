# PortDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the component. | [optional] 
**versioned_component_id** | **str** | The ID of the corresponding component that is under version control | [optional] 
**parent_group_id** | **str** | The id of parent process group of this component if applicable. | [optional] 
**position** | [**PositionDTO**](PositionDTO.md) | The position of this component in the UI if applicable. | [optional] 
**name** | **str** | The name of the port. | [optional] 
**comments** | **str** | The comments for the port. | [optional] 
**state** | **str** | The state of the port. | [optional] 
**type** | **str** | The type of port. | [optional] 
**transmitting** | **bool** | Whether the port has incoming or output connections to a remote NiFi. This is only applicable when the port is running in the root group. | [optional] 
**concurrently_schedulable_task_count** | **int** | The number of tasks that should be concurrently scheduled for the port. | [optional] 
**user_access_control** | **list[str]** | The users that are allowed to access the port. | [optional] 
**group_access_control** | **list[str]** | The user groups that are allowed to access the port. | [optional] 
**validation_errors** | **list[str]** | Gets the validation errors from this port. These validation errors represent the problems with the port that must be resolved before it can be started. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


