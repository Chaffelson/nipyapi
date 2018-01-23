# VersionedRemoteGroupPort

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | **str** | The component&#39;s unique identifier | [optional] 
**name** | **str** | The component&#39;s name | [optional] 
**comments** | **str** | The user-supplied comments for the component | [optional] 
**position** | [**ThePositionOfAComponentOnTheGraph**](ThePositionOfAComponentOnTheGraph.md) | The component&#39;s position on the graph | [optional] 
**remote_group_id** | **str** | The id of the remote process group that the port resides in. | [optional] 
**concurrently_schedulable_task_count** | **int** | The number of task that may transmit flowfiles to the target port concurrently. | [optional] 
**use_compression** | **bool** | Whether the flowfiles are compressed when sent to the target port. | [optional] 
**batch_size** | [**BatchSize**](BatchSize.md) | The batch settings for data transmission. | [optional] 
**component_type** | **str** |  | [optional] 
**target_id** | **str** | The ID of the port on the target NiFi instance | [optional] 
**group_identifier** | **str** | The ID of the Process Group that this component belongs to | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


