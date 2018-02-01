# PortStatusSnapshotDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the port. | [optional] 
**group_id** | **str** | The id of the parent process group of the port. | [optional] 
**name** | **str** | The name of the port. | [optional] 
**active_thread_count** | **int** | The active thread count for the port. | [optional] 
**flow_files_in** | **int** | The number of FlowFiles that have been accepted in the last 5 minutes. | [optional] 
**bytes_in** | **int** | The size of hte FlowFiles that have been accepted in the last 5 minutes. | [optional] 
**input** | **str** | The count/size of flowfiles that have been accepted in the last 5 minutes. | [optional] 
**flow_files_out** | **int** | The number of FlowFiles that have been processed in the last 5 minutes. | [optional] 
**bytes_out** | **int** | The number of bytes that have been processed in the last 5 minutes. | [optional] 
**output** | **str** | The count/size of flowfiles that have been processed in the last 5 minutes. | [optional] 
**transmitting** | **bool** | Whether the port has incoming or outgoing connections to a remote NiFi. | [optional] 
**run_status** | **str** | The run status of the port. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


