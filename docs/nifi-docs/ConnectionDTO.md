# ConnectionDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the component. | [optional] 
**versioned_component_id** | **str** | The ID of the corresponding component that is under version control | [optional] 
**parent_group_id** | **str** | The id of parent process group of this component if applicable. | [optional] 
**position** | [**PositionDTO**](PositionDTO.md) | The position of this component in the UI if applicable. | [optional] 
**source** | [**ConnectableDTO**](ConnectableDTO.md) | The source of the connection. | [optional] 
**destination** | [**ConnectableDTO**](ConnectableDTO.md) | The destination of the connection. | [optional] 
**name** | **str** | The name of the connection. | [optional] 
**label_index** | **int** | The index of the bend point where to place the connection label. | [optional] 
**getz_index** | **int** | The z index of the connection. | [optional] 
**selected_relationships** | **list[str]** | The selected relationship that comprise the connection. | [optional] 
**available_relationships** | **list[str]** | The relationships that the source of the connection currently supports. | [optional] 
**back_pressure_object_threshold** | **int** | The object count threshold for determining when back pressure is applied. Updating this value is a passive change in the sense that it won&#39;t impact whether existing files over the limit are affected but it does help feeder processors to stop pushing too much into this work queue. | [optional] 
**back_pressure_data_size_threshold** | **str** | The object data size threshold for determining when back pressure is applied. Updating this value is a passive change in the sense that it won&#39;t impact whether existing files over the limit are affected but it does help feeder processors to stop pushing too much into this work queue. | [optional] 
**flow_file_expiration** | **str** | The amount of time a flow file may be in the flow before it will be automatically aged out of the flow. Once a flow file reaches this age it will be terminated from the flow the next time a processor attempts to start work on it. | [optional] 
**prioritizers** | **list[str]** | The comparators used to prioritize the queue. | [optional] 
**bends** | [**list[PositionDTO]**](PositionDTO.md) | The bend points on the connection. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


