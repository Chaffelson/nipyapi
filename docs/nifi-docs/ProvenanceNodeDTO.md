# ProvenanceNodeDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the node. | [optional] 
**flow_file_uuid** | **str** | The uuid of the flowfile associated with the provenance event. | [optional] 
**parent_uuids** | **list[str]** | The uuid of the parent flowfiles of the provenance event. | [optional] 
**child_uuids** | **list[str]** | The uuid of the childrent flowfiles of the provenance event. | [optional] 
**cluster_node_identifier** | **str** | The identifier of the node that this event/flowfile originated from. | [optional] 
**type** | **str** | The type of the node. | [optional] 
**event_type** | **str** | If the type is EVENT, this is the type of event. | [optional] 
**millis** | **int** | The timestamp of the node in milliseconds. | [optional] 
**timestamp** | **str** | The timestamp of the node formatted. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


