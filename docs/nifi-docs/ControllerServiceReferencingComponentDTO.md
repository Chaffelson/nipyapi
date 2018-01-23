# ControllerServiceReferencingComponentDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**group_id** | **str** | The group id for the component referencing a controller service. If this component is another controller service or a reporting task, this field is blank. | [optional] 
**id** | **str** | The id of the component referencing a controller service. | [optional] 
**name** | **str** | The name of the component referencing a controller service. | [optional] 
**type** | **str** | The type of the component referencing a controller service. | [optional] 
**state** | **str** | The scheduled state of a processor or reporting task referencing a controller service. If this component is another controller service, this field represents the controller service state. | [optional] 
**properties** | **dict(str, str)** | The properties for the component. | [optional] 
**descriptors** | [**dict(str, PropertyDescriptorDTO)**](PropertyDescriptorDTO.md) | The descriptors for the component properties. | [optional] 
**validation_errors** | **list[str]** | The validation errors for the component. | [optional] 
**reference_type** | **str** | The type of reference this is. | [optional] 
**active_thread_count** | **int** | The number of active threads for the referencing component. | [optional] 
**reference_cycle** | **bool** | If the referencing component represents a controller service, this indicates whether it has already been represented in this hierarchy. | [optional] 
**referencing_components** | [**list[ControllerServiceReferencingComponentEntity]**](ControllerServiceReferencingComponentEntity.md) | If the referencing component represents a controller service, these are the components that reference it. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


