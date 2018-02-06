# RemoteProcessGroupDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the component. | [optional] 
**versioned_component_id** | **str** | The ID of the corresponding component that is under version control | [optional] 
**parent_group_id** | **str** | The id of parent process group of this component if applicable. | [optional] 
**position** | [**PositionDTO**](PositionDTO.md) | The position of this component in the UI if applicable. | [optional] 
**target_uri** | **str** | The target URI of the remote process group. If target uri is not set, but uris are set, then returns the first url in the urls. If neither target uri nor uris are set, then returns null. | [optional] 
**target_uris** | **str** | The target URI of the remote process group. If target uris is not set but target uri is set, then returns a collection containing the single target uri. If neither target uris nor uris are set, then returns null. | [optional] 
**target_secure** | **bool** | Whether the target is running securely. | [optional] 
**name** | **str** | The name of the remote process group. | [optional] 
**comments** | **str** | The comments for the remote process group. | [optional] 
**communications_timeout** | **str** | The time period used for the timeout when communicating with the target. | [optional] 
**yield_duration** | **str** | When yielding, this amount of time must elapse before the remote process group is scheduled again. | [optional] 
**transport_protocol** | **str** |  | [optional] 
**local_network_interface** | **str** | The local network interface to send/receive data. If not specified, any local address is used. If clustered, all nodes must have an interface with this identifier. | [optional] 
**proxy_host** | **str** |  | [optional] 
**proxy_port** | **int** |  | [optional] 
**proxy_user** | **str** |  | [optional] 
**proxy_password** | **str** |  | [optional] 
**authorization_issues** | **list[str]** | Any remote authorization issues for the remote process group. | [optional] 
**validation_errors** | **list[str]** | The validation errors for the remote process group. These validation errors represent the problems with the remote process group that must be resolved before it can transmit. | [optional] 
**transmitting** | **bool** | Whether the remote process group is actively transmitting. | [optional] 
**input_port_count** | **int** | The number of remote input ports currently available on the target. | [optional] 
**output_port_count** | **int** | The number of remote output ports currently available on the target. | [optional] 
**active_remote_input_port_count** | **int** | The number of active remote input ports. | [optional] 
**inactive_remote_input_port_count** | **int** | The number of inactive remote input ports. | [optional] 
**active_remote_output_port_count** | **int** | The number of active remote output ports. | [optional] 
**inactive_remote_output_port_count** | **int** | The number of inactive remote output ports. | [optional] 
**flow_refreshed** | **str** | The timestamp when this remote process group was last refreshed. | [optional] 
**contents** | [**RemoteProcessGroupContentsDTO**](RemoteProcessGroupContentsDTO.md) | The contents of the remote process group. Will contain available input/output ports. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


