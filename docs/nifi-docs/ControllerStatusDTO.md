# ControllerStatusDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_thread_count** | **int** | The number of active threads in the NiFi. | [optional] 
**queued** | **str** | The number of flowfiles queued in the NiFi. | [optional] 
**flow_files_queued** | **int** | The number of FlowFiles queued across the entire flow | [optional] 
**bytes_queued** | **int** | The size of the FlowFiles queued across the entire flow | [optional] 
**running_count** | **int** | The number of running components in the NiFi. | [optional] 
**stopped_count** | **int** | The number of stopped components in the NiFi. | [optional] 
**invalid_count** | **int** | The number of invalid components in the NiFi. | [optional] 
**disabled_count** | **int** | The number of disabled components in the NiFi. | [optional] 
**active_remote_port_count** | **int** | The number of active remote ports in the NiFi. | [optional] 
**inactive_remote_port_count** | **int** | The number of inactive remote ports in the NiFi. | [optional] 
**up_to_date_count** | **int** | The number of up to date versioned process groups in the NiFi. | [optional] 
**locally_modified_count** | **int** | The number of locally modified versioned process groups in the NiFi. | [optional] 
**stale_count** | **int** | The number of stale versioned process groups in the NiFi. | [optional] 
**locally_modified_and_stale_count** | **int** | The number of locally modified and stale versioned process groups in the NiFi. | [optional] 
**sync_failure_count** | **int** | The number of versioned process groups in the NiFi that are unable to sync to a registry. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


