# ProcessGroupStatusDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the Process Group | [optional] 
**name** | **str** | The name of the Process Group | [optional] 
**stats_last_refreshed** | **str** | The time the status for the process group was last refreshed. | [optional] 
**aggregate_snapshot** | [**ProcessGroupStatusSnapshotDTO**](ProcessGroupStatusSnapshotDTO.md) | The aggregate status of all nodes in the cluster | [optional] 
**node_snapshots** | [**list[NodeProcessGroupStatusSnapshotDTO]**](NodeProcessGroupStatusSnapshotDTO.md) | The status reported by each node in the cluster. If the NiFi instance is a standalone instance, rather than a clustered instance, this value may be null. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


