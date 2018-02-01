# DocumentedTypeDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The fully qualified name of the type. | [optional] 
**bundle** | [**BundleDTO**](BundleDTO.md) | The details of the artifact that bundled this type. | [optional] 
**controller_service_apis** | [**list[ControllerServiceApiDTO]**](ControllerServiceApiDTO.md) | If this type represents a ControllerService, this lists the APIs it implements. | [optional] 
**description** | **str** | The description of the type. | [optional] 
**usage_restriction** | **str** | The description of why the usage of this component is restricted. | [optional] 
**deprecation_reason** | **str** | The description of why the usage of this component is restricted. | [optional] 
**tags** | **list[str]** | The tags associated with this type. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


