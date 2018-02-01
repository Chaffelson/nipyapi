# ProcessorStatusDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**group_id** | **str** | The unique ID of the process group that the Processor belongs to | [optional] 
**id** | **str** | The unique ID of the Processor | [optional] 
**name** | **str** | The name of the Processor | [optional] 
**type** | **str** | The type of the Processor | [optional] 
**run_status** | **str** | The run status of the Processor | [optional] 
**stats_last_refreshed** | **str** | The timestamp of when the stats were last refreshed | [optional] 
**aggregate_snapshot** | [**ProcessorStatusSnapshotDTO**](ProcessorStatusSnapshotDTO.md) | A status snapshot that represents the aggregate stats of all nodes in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this represents the stats of the single instance. | [optional] 
**node_snapshots** | [**list[NodeProcessorStatusSnapshotDTO]**](NodeProcessorStatusSnapshotDTO.md) | A status snapshot for each node in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this may be null. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


