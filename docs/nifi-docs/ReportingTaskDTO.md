# ReportingTaskDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the component. | [optional] 
**versioned_component_id** | **str** | The ID of the corresponding component that is under version control | [optional] 
**parent_group_id** | **str** | The id of parent process group of this component if applicable. | [optional] 
**position** | [**PositionDTO**](PositionDTO.md) | The position of this component in the UI if applicable. | [optional] 
**name** | **str** | The name of the reporting task. | [optional] 
**type** | **str** | The fully qualified type of the reporting task. | [optional] 
**bundle** | [**BundleDTO**](BundleDTO.md) | The details of the artifact that bundled this processor type. | [optional] 
**state** | **str** | The state of the reporting task. | [optional] 
**comments** | **str** | The comments of the reporting task. | [optional] 
**persists_state** | **bool** | Whether the reporting task persists state. | [optional] 
**restricted** | **bool** | Whether the reporting task requires elevated privileges. | [optional] 
**deprecated** | **bool** | Whether the reporting task has been deprecated. | [optional] 
**multiple_versions_available** | **bool** | Whether the reporting task has multiple versions available. | [optional] 
**scheduling_period** | **str** | The frequency with which to schedule the reporting task. The format of the value willd epend on the valud of the schedulingStrategy. | [optional] 
**scheduling_strategy** | **str** | The scheduling strategy that determines how the schedulingPeriod value should be interpreted. | [optional] 
**default_scheduling_period** | **dict(str, str)** | The default scheduling period for the different scheduling strategies. | [optional] 
**properties** | **dict(str, str)** | The properties of the reporting task. | [optional] 
**descriptors** | [**dict(str, PropertyDescriptorDTO)**](PropertyDescriptorDTO.md) | The descriptors for the reporting tasks properties. | [optional] 
**custom_ui_url** | **str** | The URL for the custom configuration UI for the reporting task. | [optional] 
**annotation_data** | **str** | The annotation data for the repoting task. This is how the custom UI relays configuration to the reporting task. | [optional] 
**validation_errors** | **list[str]** | Gets the validation errors from the reporting task. These validation errors represent the problems with the reporting task that must be resolved before it can be scheduled to run. | [optional] 
**active_thread_count** | **int** | The number of active threads for the reporting task. | [optional] 
**extension_missing** | **bool** | Whether the underlying extension is missing. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


