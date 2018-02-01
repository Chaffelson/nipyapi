# VersionedControllerService

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | **str** | The component&#39;s unique identifier | [optional] 
**name** | **str** | The component&#39;s name | [optional] 
**comments** | **str** | The user-supplied comments for the component | [optional] 
**position** | [**ThePositionOfAComponentOnTheGraph**](ThePositionOfAComponentOnTheGraph.md) | The component&#39;s position on the graph | [optional] 
**type** | **str** | The type of the controller service. | [optional] 
**bundle** | [**Bundle**](Bundle.md) | The details of the artifact that bundled this processor type. | [optional] 
**controller_service_apis** | [**list[ControllerServiceAPI]**](ControllerServiceAPI.md) | Lists the APIs this Controller Service implements. | [optional] 
**properties** | **dict(str, str)** | The properties of the controller service. | [optional] 
**property_descriptors** | [**dict(str, VersionedPropertyDescriptor)**](VersionedPropertyDescriptor.md) | The property descriptors for the processor. | [optional] 
**annotation_data** | **str** | The annotation for the controller service. This is how the custom UI relays configuration to the controller service. | [optional] 
**component_type** | **str** |  | [optional] 
**group_identifier** | **str** | The ID of the Process Group that this component belongs to | [optional] 

[[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to README]](../registryDocs.md)


