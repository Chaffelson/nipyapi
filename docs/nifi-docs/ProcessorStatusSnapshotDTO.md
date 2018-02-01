# ProcessorStatusSnapshotDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the processor. | [optional] 
**group_id** | **str** | The id of the parent process group to which the processor belongs. | [optional] 
**name** | **str** | The name of the prcessor. | [optional] 
**type** | **str** | The type of the processor. | [optional] 
**run_status** | **str** | The state of the processor. | [optional] 
**execution_node** | **str** | Indicates the node where the process will execute. | [optional] 
**bytes_read** | **int** | The number of bytes read by this Processor in the last 5 mintues | [optional] 
**bytes_written** | **int** | The number of bytes written by this Processor in the last 5 minutes | [optional] 
**read** | **str** | The number of bytes read in the last 5 minutes. | [optional] 
**written** | **str** | The number of bytes written in the last 5 minutes. | [optional] 
**flow_files_in** | **int** | The number of FlowFiles that have been accepted in the last 5 minutes | [optional] 
**bytes_in** | **int** | The size of the FlowFiles that have been accepted in the last 5 minutes | [optional] 
**input** | **str** | The count/size of flowfiles that have been accepted in the last 5 minutes. | [optional] 
**flow_files_out** | **int** | The number of FlowFiles transferred to a Connection in the last 5 minutes | [optional] 
**bytes_out** | **int** | The size of the FlowFiles transferred to a Connection in the last 5 minutes | [optional] 
**output** | **str** | The count/size of flowfiles that have been processed in the last 5 minutes. | [optional] 
**task_count** | **int** | The number of times this Processor has run in the last 5 minutes | [optional] 
**tasks_duration_nanos** | **int** | The number of nanoseconds that this Processor has spent running in the last 5 minutes | [optional] 
**tasks** | **str** | The total number of task this connectable has completed over the last 5 minutes. | [optional] 
**tasks_duration** | **str** | The total duration of all tasks for this connectable over the last 5 minutes. | [optional] 
**active_thread_count** | **int** | The number of threads currently executing in the processor. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


