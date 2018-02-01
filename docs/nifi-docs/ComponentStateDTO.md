# ComponentStateDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**component_id** | **str** | The component identifier. | [optional] 
**state_description** | **str** | Description of the state this component persists. | [optional] 
**cluster_state** | [**StateMapDTO**](StateMapDTO.md) | The cluster state for this component, or null if this NiFi is a standalone instance. | [optional] 
**local_state** | [**StateMapDTO**](StateMapDTO.md) | The local state for this component. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


