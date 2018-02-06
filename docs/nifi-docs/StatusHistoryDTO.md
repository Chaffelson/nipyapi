# StatusHistoryDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**generated** | **str** | When the status history was generated. | [optional] 
**component_details** | **dict(str, str)** | A Map of key/value pairs that describe the component that the status history belongs to | [optional] 
**field_descriptors** | [**list[StatusDescriptorDTO]**](StatusDescriptorDTO.md) | The Descriptors that provide information on each of the metrics provided in the status history | [optional] 
**aggregate_snapshots** | [**list[StatusSnapshotDTO]**](StatusSnapshotDTO.md) | A list of StatusSnapshotDTO objects that provide the actual metric values for the component. If the NiFi instance is clustered, this will represent the aggregate status across all nodes. If the NiFi instance is not clustered, this will represent the status of the entire NiFi instance. | [optional] 
**node_snapshots** | [**list[NodeStatusSnapshotsDTO]**](NodeStatusSnapshotsDTO.md) | The NodeStatusSnapshotsDTO objects that provide the actual metric values for the component, for each node. If the NiFi instance is not clustered, this value will be null. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


