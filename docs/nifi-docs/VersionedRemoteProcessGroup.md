# VersionedRemoteProcessGroup

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | **str** | The component&#39;s unique identifier | [optional] 
**name** | **str** | The component&#39;s name | [optional] 
**comments** | **str** | The user-supplied comments for the component | [optional] 
**position** | [**ThePositionOfAComponentOnTheGraph**](ThePositionOfAComponentOnTheGraph.md) | The component&#39;s position on the graph | [optional] 
**target_uri** | **str** | The target URI of the remote process group. If target uri is not set, but uris are set, then returns the first url in the urls. If neither target uri nor uris are set, then returns null. | [optional] 
**target_uris** | **str** | The target URI of the remote process group. If target uris is not set but target uri is set, then returns the single target uri. If neither target uris nor target uri is set, then returns null. | [optional] 
**communications_timeout** | **str** | The time period used for the timeout when communicating with the target. | [optional] 
**yield_duration** | **str** | When yielding, this amount of time must elapse before the remote process group is scheduled again. | [optional] 
**transport_protocol** | **str** | The Transport Protocol that is used for Site-to-Site communications | [optional] 
**local_network_interface** | **str** | The local network interface to send/receive data. If not specified, any local address is used. If clustered, all nodes must have an interface with this identifier. | [optional] 
**proxy_host** | **str** |  | [optional] 
**proxy_port** | **int** |  | [optional] 
**proxy_user** | **str** |  | [optional] 
**input_ports** | [**list[VersionedRemoteGroupPort]**](VersionedRemoteGroupPort.md) | A Set of Input Ports that can be connected to, in order to send data to the remote NiFi instance | [optional] 
**output_ports** | [**list[VersionedRemoteGroupPort]**](VersionedRemoteGroupPort.md) | A Set of Output Ports that can be connected to, in order to pull data from the remote NiFi instance | [optional] 
**component_type** | **str** |  | [optional] 
**group_identifier** | **str** | The ID of the Process Group that this component belongs to | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


