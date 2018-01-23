# ProvenanceResultsDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provenance_events** | [**list[ProvenanceEventDTO]**](ProvenanceEventDTO.md) | The provenance events that matched the search criteria. | [optional] 
**total** | **str** | The total number of results formatted. | [optional] 
**total_count** | **int** | The total number of results. | [optional] 
**generated** | **str** | Then the search was performed. | [optional] 
**oldest_event** | **str** | The oldest event available in the provenance repository. | [optional] 
**time_offset** | **int** | The time offset of the server that&#39;s used for event time. | [optional] 
**errors** | **list[str]** | Any errors that occurred while performing the provenance request. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


