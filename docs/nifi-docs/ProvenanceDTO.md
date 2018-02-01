# ProvenanceDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the provenance query. | [optional] 
**uri** | **str** | The URI for this query. Used for obtaining/deleting the request at a later time | [optional] 
**submission_time** | **str** | The timestamp when the query was submitted. | [optional] 
**expiration** | **str** | The timestamp when the query will expire. | [optional] 
**percent_completed** | **int** | The current percent complete. | [optional] 
**finished** | **bool** | Whether the query has finished. | [optional] 
**request** | [**ProvenanceRequestDTO**](ProvenanceRequestDTO.md) | The provenance request. | [optional] 
**results** | [**ProvenanceResultsDTO**](ProvenanceResultsDTO.md) | The provenance results. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


