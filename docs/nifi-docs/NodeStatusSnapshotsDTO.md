# NodeStatusSnapshotsDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** | The id of the node. | [optional] 
**address** | **str** | The node&#39;s host/ip address. | [optional] 
**api_port** | **int** | The port the node is listening for API requests. | [optional] 
**status_snapshots** | [**list[StatusSnapshotDTO]**](StatusSnapshotDTO.md) | A list of StatusSnapshotDTO objects that provide the actual metric values for the component for this node. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


