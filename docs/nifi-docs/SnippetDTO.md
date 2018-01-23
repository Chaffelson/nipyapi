# SnippetDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the snippet. | [optional] 
**uri** | **str** | The URI of the snippet. | [optional] 
**parent_group_id** | **str** | The group id for the components in the snippet. | [optional] 
**process_groups** | [**dict(str, RevisionDTO)**](RevisionDTO.md) | The ids of the process groups in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests). | [optional] 
**remote_process_groups** | [**dict(str, RevisionDTO)**](RevisionDTO.md) | The ids of the remote process groups in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests). | [optional] 
**processors** | [**dict(str, RevisionDTO)**](RevisionDTO.md) | The ids of the processors in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests). | [optional] 
**input_ports** | [**dict(str, RevisionDTO)**](RevisionDTO.md) | The ids of the input ports in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests). | [optional] 
**output_ports** | [**dict(str, RevisionDTO)**](RevisionDTO.md) | The ids of the output ports in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests). | [optional] 
**connections** | [**dict(str, RevisionDTO)**](RevisionDTO.md) | The ids of the connections in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests). | [optional] 
**labels** | [**dict(str, RevisionDTO)**](RevisionDTO.md) | The ids of the labels in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests). | [optional] 
**funnels** | [**dict(str, RevisionDTO)**](RevisionDTO.md) | The ids of the funnels in this snippet. These ids will be populated within each response. They can be specified when creating a snippet. However, once a snippet has been created its contents cannot be modified (these ids are ignored during update requests). | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


