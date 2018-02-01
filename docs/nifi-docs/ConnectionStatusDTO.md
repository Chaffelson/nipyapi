# ConnectionStatusDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the connection | [optional] 
**group_id** | **str** | The ID of the Process Group that the connection belongs to | [optional] 
**name** | **str** | The name of the connection | [optional] 
**stats_last_refreshed** | **str** | The timestamp of when the stats were last refreshed | [optional] 
**source_id** | **str** | The ID of the source component | [optional] 
**source_name** | **str** | The name of the source component | [optional] 
**destination_id** | **str** | The ID of the destination component | [optional] 
**destination_name** | **str** | The name of the destination component | [optional] 
**aggregate_snapshot** | [**ConnectionStatusSnapshotDTO**](ConnectionStatusSnapshotDTO.md) | The status snapshot that represents the aggregate stats of the cluster | [optional] 
**node_snapshots** | [**list[NodeConnectionStatusSnapshotDTO]**](NodeConnectionStatusSnapshotDTO.md) | A list of status snapshots for each node | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


