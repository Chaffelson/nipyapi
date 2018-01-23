# ListingRequestDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id for this listing request. | [optional] 
**uri** | **str** | The URI for future requests to this listing request. | [optional] 
**submission_time** | **str** | The timestamp when the query was submitted. | [optional] 
**last_updated** | **str** | The last time this listing request was updated. | [optional] 
**percent_completed** | **int** | The current percent complete. | [optional] 
**finished** | **bool** | Whether the query has finished. | [optional] 
**failure_reason** | **str** | The reason, if any, that this listing request failed. | [optional] 
**max_results** | **int** | The maximum number of FlowFileSummary objects to return | [optional] 
**state** | **str** | The current state of the listing request. | [optional] 
**queue_size** | [**QueueSizeDTO**](QueueSizeDTO.md) | The size of the queue | [optional] 
**flow_file_summaries** | [**list[FlowFileSummaryDTO]**](FlowFileSummaryDTO.md) | The FlowFile summaries. The summaries will be populated once the request has completed. | [optional] 
**source_running** | **bool** | Whether the source of the connection is running | [optional] 
**destination_running** | **bool** | Whether the destination of the connection is running | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


