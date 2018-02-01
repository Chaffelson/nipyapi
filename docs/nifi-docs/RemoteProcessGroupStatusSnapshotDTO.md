# RemoteProcessGroupStatusSnapshotDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the remote process group. | [optional] 
**group_id** | **str** | The id of the parent process group the remote process group resides in. | [optional] 
**name** | **str** | The name of the remote process group. | [optional] 
**target_uri** | **str** | The URI of the target system. | [optional] 
**transmission_status** | **str** | The transmission status of the remote process group. | [optional] 
**active_thread_count** | **int** | The number of active threads for the remote process group. | [optional] 
**flow_files_sent** | **int** | The number of FlowFiles sent to the remote process group in the last 5 minutes. | [optional] 
**bytes_sent** | **int** | The size of the FlowFiles sent to the remote process group in the last 5 minutes. | [optional] 
**sent** | **str** | The count/size of the flowfiles sent to the remote process group in the last 5 minutes. | [optional] 
**flow_files_received** | **int** | The number of FlowFiles received from the remote process group in the last 5 minutes. | [optional] 
**bytes_received** | **int** | The size of the FlowFiles received from the remote process group in the last 5 minutes. | [optional] 
**received** | **str** | The count/size of the flowfiles received from the remote process group in the last 5 minutes. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


