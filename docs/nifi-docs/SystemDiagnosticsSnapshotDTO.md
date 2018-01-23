# SystemDiagnosticsSnapshotDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_non_heap** | **str** | Total size of non heap. | [optional] 
**total_non_heap_bytes** | **int** | Total number of bytes allocated to the JVM not used for heap | [optional] 
**used_non_heap** | **str** | Amount of use non heap. | [optional] 
**used_non_heap_bytes** | **int** | Total number of bytes used by the JVM not in the heap space | [optional] 
**free_non_heap** | **str** | Amount of free non heap. | [optional] 
**free_non_heap_bytes** | **int** | Total number of free non-heap bytes available to the JVM | [optional] 
**max_non_heap** | **str** | Maximum size of non heap. | [optional] 
**max_non_heap_bytes** | **int** | The maximum number of bytes that the JVM can use for non-heap purposes | [optional] 
**non_heap_utilization** | **str** | Utilization of non heap. | [optional] 
**total_heap** | **str** | Total size of heap. | [optional] 
**total_heap_bytes** | **int** | The total number of bytes that are available for the JVM heap to use | [optional] 
**used_heap** | **str** | Amount of used heap. | [optional] 
**used_heap_bytes** | **int** | The number of bytes of JVM heap that are currently being used | [optional] 
**free_heap** | **str** | Amount of free heap. | [optional] 
**free_heap_bytes** | **int** | The number of bytes that are allocated to the JVM heap but not currently being used | [optional] 
**max_heap** | **str** | Maximum size of heap. | [optional] 
**max_heap_bytes** | **int** | The maximum number of bytes that can be used by the JVM | [optional] 
**heap_utilization** | **str** | Utilization of heap. | [optional] 
**available_processors** | **int** | Number of available processors if supported by the underlying system. | [optional] 
**processor_load_average** | **float** | The processor load average if supported by the underlying system. | [optional] 
**total_threads** | **int** | Total number of threads. | [optional] 
**daemon_threads** | **int** | Number of daemon threads. | [optional] 
**uptime** | **str** | The uptime of the Java virtual machine | [optional] 
**flow_file_repository_storage_usage** | [**StorageUsageDTO**](StorageUsageDTO.md) | The flowfile repository storage usage. | [optional] 
**content_repository_storage_usage** | [**list[StorageUsageDTO]**](StorageUsageDTO.md) | The content repository storage usage. | [optional] 
**provenance_repository_storage_usage** | [**list[StorageUsageDTO]**](StorageUsageDTO.md) | The provenance repository storage usage. | [optional] 
**garbage_collection** | [**list[GarbageCollectionDTO]**](GarbageCollectionDTO.md) | The garbage collection details. | [optional] 
**stats_last_refreshed** | **str** | When the diagnostics were generated. | [optional] 
**version_info** | [**VersionInfoDTO**](VersionInfoDTO.md) | The nifi, os, java, and build version information | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


