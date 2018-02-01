# ProcessorConfigDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | **dict(str, str)** | The properties for the processor. Properties whose value is not set will only contain the property name. | [optional] 
**descriptors** | [**dict(str, PropertyDescriptorDTO)**](PropertyDescriptorDTO.md) | Descriptors for the processor&#39;s properties. | [optional] 
**scheduling_period** | **str** | The frequency with which to schedule the processor. The format of the value will depend on th value of schedulingStrategy. | [optional] 
**scheduling_strategy** | **str** | Indcates whether the prcessor should be scheduled to run in event or timer driven mode. | [optional] 
**execution_node** | **str** | Indicates the node where the process will execute. | [optional] 
**penalty_duration** | **str** | The amout of time that is used when the process penalizes a flowfile. | [optional] 
**yield_duration** | **str** | The amount of time that must elapse before this processor is scheduled again after yielding. | [optional] 
**bulletin_level** | **str** | The level at which the processor will report bulletins. | [optional] 
**run_duration_millis** | **int** | The run duration for the processor in milliseconds. | [optional] 
**concurrently_schedulable_task_count** | **int** | The number of tasks that should be concurrently schedule for the processor. If the processor doesn&#39;t allow parallol processing then any positive input will be ignored. | [optional] 
**auto_terminated_relationships** | **list[str]** | The names of all relationships that cause a flow file to be terminated if the relationship is not connected elsewhere. This property differs from the &#39;isAutoTerminate&#39; property of the RelationshipDTO in that the RelationshipDTO is meant to depict the current configuration, whereas this property can be set in a DTO when updating a Processor in order to change which Relationships should be auto-terminated. | [optional] 
**comments** | **str** | The comments for the processor. | [optional] 
**custom_ui_url** | **str** | The URL for the processor&#39;s custom configuration UI if applicable. | [optional] 
**loss_tolerant** | **bool** | Whether the processor is loss tolerant. | [optional] 
**annotation_data** | **str** | The annotation data for the processor used to relay configuration between a custom UI and the procesosr. | [optional] 
**default_concurrent_tasks** | **dict(str, str)** | Maps default values for concurrent tasks for each applicable scheduling strategy. | [optional] 
**default_scheduling_period** | **dict(str, str)** | Maps default values for scheduling period for each applicable scheduling strategy. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


