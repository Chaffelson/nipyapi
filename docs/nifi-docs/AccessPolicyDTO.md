# AccessPolicyDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the component. | [optional] 
**versioned_component_id** | **str** | The ID of the corresponding component that is under version control | [optional] 
**parent_group_id** | **str** | The id of parent process group of this component if applicable. | [optional] 
**position** | [**PositionDTO**](PositionDTO.md) | The position of this component in the UI if applicable. | [optional] 
**resource** | **str** | The resource for this access policy. | [optional] 
**action** | **str** | The action associated with this access policy. | [optional] 
**component_reference** | [**ComponentReferenceEntity**](ComponentReferenceEntity.md) | Component this policy references if applicable. | [optional] 
**configurable** | **bool** | Whether this policy is configurable. | [optional] 
**users** | [**list[TenantEntity]**](TenantEntity.md) | The set of user IDs associated with this access policy. | [optional] 
**user_groups** | [**list[TenantEntity]**](TenantEntity.md) | The set of user group IDs associated with this access policy. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


