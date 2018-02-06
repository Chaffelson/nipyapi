# ConnectionEntity

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**revision** | [**RevisionDTO**](RevisionDTO.md) | The revision for this request/response. The revision is required for any mutable flow requests and is included in all responses. | [optional] 
**id** | **str** | The id of the component. | [optional] 
**uri** | **str** | The URI for futures requests to the component. | [optional] 
**position** | [**PositionDTO**](PositionDTO.md) | The position of this component in the UI if applicable. | [optional] 
**permissions** | [**PermissionsDTO**](PermissionsDTO.md) | The permissions for this component. | [optional] 
**bulletins** | [**list[BulletinEntity]**](BulletinEntity.md) | The bulletins for this component. | [optional] 
**component** | [**ConnectionDTO**](ConnectionDTO.md) |  | [optional] 
**status** | [**ConnectionStatusDTO**](ConnectionStatusDTO.md) | The status of the connection. | [optional] 
**bends** | [**list[PositionDTO]**](PositionDTO.md) | The bend points on the connection. | [optional] 
**label_index** | **int** | The index of the bend point where to place the connection label. | [optional] 
**getz_index** | **int** | The z index of the connection. | [optional] 
**source_id** | **str** | The identifier of the source of this connection. | [optional] 
**source_group_id** | **str** | The identifier of the group of the source of this connection. | [optional] 
**source_type** | **str** | The type of component the source connectable is. | 
**destination_id** | **str** | The identifier of the destination of this connection. | [optional] 
**destination_group_id** | **str** | The identifier of the group of the destination of this connection. | [optional] 
**destination_type** | **str** | The type of component the destination connectable is. | 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


