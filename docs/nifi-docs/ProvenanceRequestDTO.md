# ProvenanceRequestDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**search_terms** | **dict(str, str)** | The search terms used to perform the search. | [optional] 
**cluster_node_id** | **str** | The id of the node in the cluster where this provenance originated. | [optional] 
**start_date** | **str** | The earliest event time to include in the query. | [optional] 
**end_date** | **str** | The latest event time to include in the query. | [optional] 
**minimum_file_size** | **str** | The minimum file size to include in the query. | [optional] 
**maximum_file_size** | **str** | The maximum file size to include in the query. | [optional] 
**max_results** | **int** | The maximum number of results to include. | [optional] 
**summarize** | **bool** | Whether or not to summarize provenance events returned. This property is false by default. | [optional] 
**incremental_results** | **bool** | Whether or not incremental results are returned. If false, provenance events are only returned once the query completes. This property is true by default. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


