# NodeDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** | The id of the node. | [optional] 
**address** | **str** | The node&#39;s host/ip address. | [optional] 
**api_port** | **int** | The port the node is listening for API requests. | [optional] 
**status** | **str** | The node&#39;s status. | [optional] 
**heartbeat** | **str** | the time of the nodes&#39;s last heartbeat. | [optional] 
**connection_requested** | **str** | The time of the node&#39;s last connection request. | [optional] 
**roles** | **list[str]** | The roles of this node. | [optional] 
**active_thread_count** | **int** | The active threads for the NiFi on the node. | [optional] 
**queued** | **str** | The queue the NiFi on the node. | [optional] 
**events** | [**list[NodeEventDTO]**](NodeEventDTO.md) | The node&#39;s events. | [optional] 
**node_start_time** | **str** | The time at which this Node was last refreshed. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


