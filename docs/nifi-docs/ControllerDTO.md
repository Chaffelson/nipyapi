# ControllerDTO

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The id of the NiFi. | [optional] 
**name** | **str** | The name of the NiFi. | [optional] 
**comments** | **str** | The comments for the NiFi. | [optional] 
**running_count** | **int** | The number of running components in the NiFi. | [optional] 
**stopped_count** | **int** | The number of stopped components in the NiFi. | [optional] 
**invalid_count** | **int** | The number of invalid components in the NiFi. | [optional] 
**disabled_count** | **int** | The number of disabled components in the NiFi. | [optional] 
**active_remote_port_count** | **int** | The number of active remote ports contained in the NiFi. | [optional] 
**inactive_remote_port_count** | **int** | The number of inactive remote ports contained in the NiFi. | [optional] 
**input_port_count** | **int** | The number of input ports contained in the NiFi. | [optional] 
**output_port_count** | **int** | The number of output ports in the NiFi. | [optional] 
**remote_site_listening_port** | **int** | The Socket Port on which this instance is listening for Remote Transfers of Flow Files. If this instance is not configured to receive Flow Files from remote instances, this will be null. | [optional] 
**remote_site_http_listening_port** | **int** | The HTTP(S) Port on which this instance is listening for Remote Transfers of Flow Files. If this instance is not configured to receive Flow Files from remote instances, this will be null. | [optional] 
**site_to_site_secure** | **bool** | Indicates whether or not Site-to-Site communications with this instance is secure (2-way authentication). | [optional] 
**instance_id** | **str** | If clustered, the id of the Cluster Manager, otherwise the id of the NiFi. | [optional] 
**input_ports** | [**list[PortDTO]**](PortDTO.md) | The input ports available to send data to for the NiFi. | [optional] 
**output_ports** | [**list[PortDTO]**](PortDTO.md) | The output ports available to received data from the NiFi. | [optional] 

[[Back to Model list]](../nifiDocs.md#documentation-for-models) [[Back to API list]](../nifiDocs.md#documentation-for-api-endpoints) [[Back to README]](../nifiDocs.md)


