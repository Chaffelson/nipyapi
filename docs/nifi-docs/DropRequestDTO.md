# DropRequestDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id for this drop request. | [optional] 
**uri** | **str** | The URI for future requests to this drop request. | [optional] 
**submission_time** | **str** | The timestamp when the query was submitted. | [optional] 
**last_updated** | **str** | The last time this drop request was updated. | [optional] 
**percent_completed** | **int** | The current percent complete. | [optional] 
**finished** | **bool** | Whether the query has finished. | [optional] 
**failure_reason** | **str** | The reason, if any, that this drop request failed. | [optional] 
**current_count** | **int** | The number of flow files currently queued. | [optional] 
**current_size** | **int** | The size of flow files currently queued in bytes. | [optional] 
**current** | **str** | The count and size of flow files currently queued. | [optional] 
**original_count** | **int** | The number of flow files to be dropped as a result of this request. | [optional] 
**original_size** | **int** | The size of flow files to be dropped as a result of this request in bytes. | [optional] 
**original** | **str** | The count and size of flow files to be dropped as a result of this request. | [optional] 
**dropped_count** | **int** | The number of flow files that have been dropped thus far. | [optional] 
**dropped_size** | **int** | The size of flow files that have been dropped thus far in bytes. | [optional] 
**dropped** | **str** | The count and size of flow files that have been dropped thus far. | [optional] 
**state** | **str** | The current state of the drop request. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


