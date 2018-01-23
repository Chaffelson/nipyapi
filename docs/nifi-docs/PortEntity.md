# PortEntity

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**revision** | [**RevisionDTO**](RevisionDTO.md) | The revision for this request/response. The revision is required for any mutable flow requests and is included in all responses. | [optional] 
**id** | **str** | The id of the component. | [optional] 
**uri** | **str** | The URI for futures requests to the component. | [optional] 
**position** | [**PositionDTO**](PositionDTO.md) | The position of this component in the UI if applicable. | [optional] 
**permissions** | [**PermissionsDTO**](PermissionsDTO.md) | The permissions for this component. | [optional] 
**bulletins** | [**list[BulletinEntity]**](BulletinEntity.md) | The bulletins for this component. | [optional] 
**component** | [**PortDTO**](PortDTO.md) |  | [optional] 
**status** | [**PortStatusDTO**](PortStatusDTO.md) | The status of the port. | [optional] 
**port_type** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


