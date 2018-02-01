# RemoteProcessGroupStatusDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**group_id** | **str** | The unique ID of the process group that the Processor belongs to | [optional] 
**id** | **str** | The unique ID of the Processor | [optional] 
**name** | **str** | The name of the remote process group. | [optional] 
**target_uri** | **str** | The URI of the target system. | [optional] 
**transmission_status** | **str** | The transmission status of the remote process group. | [optional] 
**stats_last_refreshed** | **str** | The time the status for the process group was last refreshed. | [optional] 
**aggregate_snapshot** | [**RemoteProcessGroupStatusSnapshotDTO**](RemoteProcessGroupStatusSnapshotDTO.md) | A status snapshot that represents the aggregate stats of all nodes in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this represents the stats of the single instance. | [optional] 
**node_snapshots** | [**list[NodeRemoteProcessGroupStatusSnapshotDTO]**](NodeRemoteProcessGroupStatusSnapshotDTO.md) | A status snapshot for each node in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this may be null. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


