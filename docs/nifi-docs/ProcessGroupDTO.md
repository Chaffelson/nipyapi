# ProcessGroupDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the component. | [optional] 
**versioned_component_id** | **str** | The ID of the corresponding component that is under version control | [optional] 
**parent_group_id** | **str** | The id of parent process group of this component if applicable. | [optional] 
**position** | [**PositionDTO**](PositionDTO.md) | The position of this component in the UI if applicable. | [optional] 
**name** | **str** | The name of the process group. | [optional] 
**comments** | **str** | The comments for the process group. | [optional] 
**variables** | **dict(str, str)** | The variables that are configured for the Process Group. Note that this map contains only those variables that are defined on this Process Group and not any variables that are defined in the parent Process Group, etc. I.e., this Map will not contain all variables that are accessible by components in this Process Group by rather only the variables that are defined for this Process Group itself. | [optional] 
**version_control_information** | [**VersionControlInformationDTO**](VersionControlInformationDTO.md) | The Version Control information that indicates which Flow Registry, and where in the Flow Registry, this Process Group is tracking to; or null if this Process Group is not under version control | [optional] 
**running_count** | **int** | The number of running components in this process group. | [optional] 
**stopped_count** | **int** | The number of stopped components in the process group. | [optional] 
**invalid_count** | **int** | The number of invalid components in the process group. | [optional] 
**disabled_count** | **int** | The number of disabled components in the process group. | [optional] 
**active_remote_port_count** | **int** | The number of active remote ports in the process group. | [optional] 
**inactive_remote_port_count** | **int** | The number of inactive remote ports in the process group. | [optional] 
**up_to_date_count** | **int** | The number of up to date versioned process groups in the process group. | [optional] 
**locally_modified_count** | **int** | The number of locally modified versioned process groups in the process group. | [optional] 
**stale_count** | **int** | The number of stale versioned process groups in the process group. | [optional] 
**locally_modified_and_stale_count** | **int** | The number of locally modified and stale versioned process groups in the process group. | [optional] 
**sync_failure_count** | **int** | The number of versioned process groups in the process group that are unable to sync to a registry. | [optional] 
**input_port_count** | **int** | The number of input ports in the process group. | [optional] 
**output_port_count** | **int** | The number of output ports in the process group. | [optional] 
**contents** | [**FlowSnippetDTO**](FlowSnippetDTO.md) | The contents of this process group. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


