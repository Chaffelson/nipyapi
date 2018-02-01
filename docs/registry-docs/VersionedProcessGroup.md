# VersionedProcessGroup

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | **str** | The component&#39;s unique identifier | [optional] 
**name** | **str** | The component&#39;s name | [optional] 
**comments** | **str** | The user-supplied comments for the component | [optional] 
**position** | [**ThePositionOfAComponentOnTheGraph**](ThePositionOfAComponentOnTheGraph.md) | The component&#39;s position on the graph | [optional] 
**process_groups** | [**list[VersionedProcessGroup]**](VersionedProcessGroup.md) | The child Process Groups | [optional] 
**remote_process_groups** | [**list[VersionedRemoteProcessGroup]**](VersionedRemoteProcessGroup.md) | The Remote Process Groups | [optional] 
**processors** | [**list[VersionedProcessor]**](VersionedProcessor.md) | The Processors | [optional] 
**input_ports** | [**list[VersionedPort]**](VersionedPort.md) | The Input Ports | [optional] 
**output_ports** | [**list[VersionedPort]**](VersionedPort.md) | The Output Ports | [optional] 
**connections** | [**list[VersionedConnection]**](VersionedConnection.md) | The Connections | [optional] 
**labels** | [**list[VersionedLabel]**](VersionedLabel.md) | The Labels | [optional] 
**funnels** | [**list[VersionedFunnel]**](VersionedFunnel.md) | The Funnels | [optional] 
**controller_services** | [**list[VersionedControllerService]**](VersionedControllerService.md) | The Controller Services | [optional] 
**versioned_flow_coordinates** | [**VersionedFlowCoordinates**](VersionedFlowCoordinates.md) | The coordinates where the remote flow is stored, or null if the Process Group is not directly under Version Control | [optional] 
**variables** | **dict(str, str)** | The Variables in the Variable Registry for this Process Group (not including any ancestor or descendant Process Groups) | [optional] 
**component_type** | **str** |  | [optional] 
**group_identifier** | **str** | The ID of the Process Group that this component belongs to | [optional] 

[[Back to Model list]](../registryDocs.md#documentation-for-models) [[Back to API list]](../registryDocs.md#documentation-for-api-endpoints) [[Back to README]](../registryDocs.md)


