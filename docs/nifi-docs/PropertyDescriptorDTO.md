# PropertyDescriptorDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name for the property. | [optional] 
**display_name** | **str** | The human readable name for the property. | [optional] 
**description** | **str** | The description for the property. Used to relay additional details to a user or provide a mechanism of documenting intent. | [optional] 
**default_value** | **str** | The default value for the property. | [optional] 
**allowable_values** | [**list[AllowableValueEntity]**](AllowableValueEntity.md) | Allowable values for the property. If empty then the allowed values are not constrained. | [optional] 
**required** | **bool** | Whether the property is required. | [optional] 
**sensitive** | **bool** | Whether the property is sensitive and protected whenever stored or represented. | [optional] 
**dynamic** | **bool** | Whether the property is dynamic (user-defined). | [optional] 
**supports_el** | **bool** | Whether the property supports expression language. | [optional] 
**identifies_controller_service** | **str** | If the property identifies a controller service this returns the fully qualified type. | [optional] 
**identifies_controller_service_bundle** | [**BundleDTO**](BundleDTO.md) | If the property identifies a controller service this returns the bundle of the type, null otherwise. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


