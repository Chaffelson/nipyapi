# ProcessGroupFlowDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the component. | [optional] 
**uri** | **str** | The URI for futures requests to the component. | [optional] 
**parent_group_id** | **str** | The id of parent process group of this component if applicable. | [optional] 
**breadcrumb** | [**FlowBreadcrumbEntity**](FlowBreadcrumbEntity.md) | The breadcrumb of the process group. | [optional] 
**flow** | [**FlowDTO**](FlowDTO.md) | The flow structure starting at this Process Group. | [optional] 
**last_refreshed** | **str** | The time the flow for the process group was last refreshed. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


