# InstantiateTemplateRequestEntity

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**origin_x** | **float** | The x coordinate of the origin of the bounding box where the new components will be placed. | [optional] 
**origin_y** | **float** | The y coordinate of the origin of the bounding box where the new components will be placed. | [optional] 
**template_id** | **str** | The identifier of the template. | [optional] 
**encoding_version** | **str** | The encoding version of the flow snippet. If not specified, this is automatically populated by the node receiving the user request. If the snippet is specified, the version will be the latest. If the snippet is not specified, the version will come from the underlying template. These details need to be replicated throughout the cluster to ensure consistency. | [optional] 
**snippet** | [**FlowSnippetDTO**](FlowSnippetDTO.md) | A flow snippet of the template contents. If not specified, this is automatically populated by the node receiving the user request. These details need to be replicated throughout the cluster to ensure consistency. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


