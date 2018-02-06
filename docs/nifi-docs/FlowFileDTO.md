# FlowFileDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uri** | **str** | The URI that can be used to access this FlowFile. | [optional] 
**uuid** | **str** | The FlowFile UUID. | [optional] 
**filename** | **str** | The FlowFile filename. | [optional] 
**position** | **int** | The FlowFile&#39;s position in the queue. | [optional] 
**size** | **int** | The FlowFile file size. | [optional] 
**queued_duration** | **int** | How long this FlowFile has been enqueued. | [optional] 
**lineage_duration** | **int** | Duration since the FlowFile&#39;s greatest ancestor entered the flow. | [optional] 
**cluster_node_id** | **str** | The id of the node where this FlowFile resides. | [optional] 
**cluster_node_address** | **str** | The label for the node where this FlowFile resides. | [optional] 
**attributes** | **dict(str, str)** | The FlowFile attributes. | [optional] 
**content_claim_section** | **str** | The section in which the content claim lives. | [optional] 
**content_claim_container** | **str** | The container in which the content claim lives. | [optional] 
**content_claim_identifier** | **str** | The identifier of the content claim. | [optional] 
**content_claim_offset** | **int** | The offset into the content claim where the flowfile&#39;s content begins. | [optional] 
**content_claim_file_size** | **str** | The file size of the content claim formatted. | [optional] 
**content_claim_file_size_bytes** | **int** | The file size of the content claim in bytes. | [optional] 
**penalized** | **bool** | If the FlowFile is penalized. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


