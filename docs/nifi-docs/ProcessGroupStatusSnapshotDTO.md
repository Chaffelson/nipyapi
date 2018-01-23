# ProcessGroupStatusSnapshotDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the process group. | [optional] 
**name** | **str** | The name of this process group. | [optional] 
**connection_status_snapshots** | [**list[ConnectionStatusSnapshotEntity]**](ConnectionStatusSnapshotEntity.md) | The status of all conenctions in the process group. | [optional] 
**processor_status_snapshots** | [**list[ProcessorStatusSnapshotEntity]**](ProcessorStatusSnapshotEntity.md) | The status of all processors in the process group. | [optional] 
**process_group_status_snapshots** | [**list[ProcessGroupStatusSnapshotEntity]**](ProcessGroupStatusSnapshotEntity.md) | The status of all process groups in the process group. | [optional] 
**remote_process_group_status_snapshots** | [**list[RemoteProcessGroupStatusSnapshotEntity]**](RemoteProcessGroupStatusSnapshotEntity.md) | The status of all remote process groups in the process group. | [optional] 
**input_port_status_snapshots** | [**list[PortStatusSnapshotEntity]**](PortStatusSnapshotEntity.md) | The status of all input ports in the process group. | [optional] 
**output_port_status_snapshots** | [**list[PortStatusSnapshotEntity]**](PortStatusSnapshotEntity.md) | The status of all output ports in the process group. | [optional] 
**versioned_flow_state** | **str** | The current state of the Process Group, as it relates to the Versioned Flow | [optional] 
**flow_files_in** | **int** | The number of FlowFiles that have come into this ProcessGroup in the last 5 minutes | [optional] 
**bytes_in** | **int** | The number of bytes that have come into this ProcessGroup in the last 5 minutes | [optional] 
**input** | **str** | The input count/size for the process group in the last 5 minutes (pretty printed). | [optional] 
**flow_files_queued** | **int** | The number of FlowFiles that are queued up in this ProcessGroup right now | [optional] 
**bytes_queued** | **int** | The number of bytes that are queued up in this ProcessGroup right now | [optional] 
**queued** | **str** | The count/size that is queued in the the process group. | [optional] 
**queued_count** | **str** | The count that is queued for the process group. | [optional] 
**queued_size** | **str** | The size that is queued for the process group. | [optional] 
**bytes_read** | **int** | The number of bytes read by components in this ProcessGroup in the last 5 minutes | [optional] 
**read** | **str** | The number of bytes read in the last 5 minutes. | [optional] 
**bytes_written** | **int** | The number of bytes written by components in this ProcessGroup in the last 5 minutes | [optional] 
**written** | **str** | The number of bytes written in the last 5 minutes. | [optional] 
**flow_files_out** | **int** | The number of FlowFiles transferred out of this ProcessGroup in the last 5 minutes | [optional] 
**bytes_out** | **int** | The number of bytes transferred out of this ProcessGroup in the last 5 minutes | [optional] 
**output** | **str** | The output count/size for the process group in the last 5 minutes. | [optional] 
**flow_files_transferred** | **int** | The number of FlowFiles transferred in this ProcessGroup in the last 5 minutes | [optional] 
**bytes_transferred** | **int** | The number of bytes transferred in this ProcessGroup in the last 5 minutes | [optional] 
**transferred** | **str** | The count/size transferred to/from queues in the process group in the last 5 minutes. | [optional] 
**bytes_received** | **int** | The number of bytes received from external sources by components within this ProcessGroup in the last 5 minutes | [optional] 
**flow_files_received** | **int** | The number of FlowFiles received from external sources by components within this ProcessGroup in the last 5 minutes | [optional] 
**received** | **str** | The count/size sent to the process group in the last 5 minutes. | [optional] 
**bytes_sent** | **int** | The number of bytes sent to an external sink by components within this ProcessGroup in the last 5 minutes | [optional] 
**flow_files_sent** | **int** | The number of FlowFiles sent to an external sink by components within this ProcessGroup in the last 5 minutes | [optional] 
**sent** | **str** | The count/size sent from this process group in the last 5 minutes. | [optional] 
**active_thread_count** | **int** | The active thread count for this process group. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


