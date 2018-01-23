# ControllerServiceDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the component. | [optional] 
**versioned_component_id** | **str** | The ID of the corresponding component that is under version control | [optional] 
**parent_group_id** | **str** | The id of parent process group of this component if applicable. | [optional] 
**position** | [**PositionDTO**](PositionDTO.md) | The position of this component in the UI if applicable. | [optional] 
**name** | **str** | The name of the controller service. | [optional] 
**type** | **str** | The type of the controller service. | [optional] 
**bundle** | [**BundleDTO**](BundleDTO.md) | The details of the artifact that bundled this processor type. | [optional] 
**controller_service_apis** | [**list[ControllerServiceApiDTO]**](ControllerServiceApiDTO.md) | Lists the APIs this Controller Service implements. | [optional] 
**comments** | **str** | The comments for the controller service. | [optional] 
**state** | **str** | The state of the controller service. | [optional] 
**persists_state** | **bool** | Whether the controller service persists state. | [optional] 
**restricted** | **bool** | Whether the controller service requires elevated privileges. | [optional] 
**deprecated** | **bool** | Whether the ontroller service has been deprecated. | [optional] 
**multiple_versions_available** | **bool** | Whether the controller service has multiple versions available. | [optional] 
**properties** | **dict(str, str)** | The properties of the controller service. | [optional] 
**descriptors** | [**dict(str, PropertyDescriptorDTO)**](PropertyDescriptorDTO.md) | The descriptors for the controller service properties. | [optional] 
**custom_ui_url** | **str** | The URL for the controller services custom configuration UI if applicable. | [optional] 
**annotation_data** | **str** | The annotation for the controller service. This is how the custom UI relays configuration to the controller service. | [optional] 
**referencing_components** | [**list[ControllerServiceReferencingComponentEntity]**](ControllerServiceReferencingComponentEntity.md) | All components referencing this controller service. | [optional] 
**validation_errors** | **list[str]** | The validation errors from the controller service. These validation errors represent the problems with the controller service that must be resolved before it can be enabled. | [optional] 
**extension_missing** | **bool** | Whether the underlying extension is missing. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


