## Documentation for NiFi API Endpoints

All URIs are relative to *http://localhost/nifi-api*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AccessApi* | [**create_access_token**](nifi-docs/AccessApi.md#create_access_token) | **POST** /access/token | Creates a token for accessing the REST API via username/password
*AccessApi* | [**create_access_token_from_ticket**](nifi-docs/AccessApi.md#create_access_token_from_ticket) | **POST** /access/kerberos | Creates a token for accessing the REST API via Kerberos ticket exchange / SPNEGO negotiation
*AccessApi* | [**create_download_token**](nifi-docs/AccessApi.md#create_download_token) | **POST** /access/download-token | Creates a single use access token for downloading FlowFile content.
*AccessApi* | [**create_ui_extension_token**](nifi-docs/AccessApi.md#create_ui_extension_token) | **POST** /access/ui-extension-token | Creates a single use access token for accessing a NiFi UI extension.
*AccessApi* | [**get_access_status**](nifi-docs/AccessApi.md#get_access_status) | **GET** /access | Gets the status the client&#39;s access
*AccessApi* | [**get_login_config**](nifi-docs/AccessApi.md#get_login_config) | **GET** /access/config | Retrieves the access configuration for this NiFi
*AccessApi* | [**knox_callback**](nifi-docs/AccessApi.md#knox_callback) | **GET** /access/knox/callback | Redirect/callback URI for processing the result of the Apache Knox login sequence.
*AccessApi* | [**knox_request**](nifi-docs/AccessApi.md#knox_request) | **GET** /access/knox/request | Initiates a request to authenticate through Apache Knox.
*AccessApi* | [**oidc_callback**](nifi-docs/AccessApi.md#oidc_callback) | **GET** /access/oidc/callback | Redirect/callback URI for processing the result of the OpenId Connect login sequence.
*AccessApi* | [**oidc_exchange**](nifi-docs/AccessApi.md#oidc_exchange) | **POST** /access/oidc/exchange | Retrieves a JWT following a successful login sequence using the configured OpenId Connect provider.
*AccessApi* | [**oidc_request**](nifi-docs/AccessApi.md#oidc_request) | **GET** /access/oidc/request | Initiates a request to authenticate through the configured OpenId Connect provider.
*ConnectionsApi* | [**delete_connection**](nifi-docs/ConnectionsApi.md#delete_connection) | **DELETE** /connections/{id} | Deletes a connection
*ConnectionsApi* | [**get_connection**](nifi-docs/ConnectionsApi.md#get_connection) | **GET** /connections/{id} | Gets a connection
*ConnectionsApi* | [**update_connection**](nifi-docs/ConnectionsApi.md#update_connection) | **PUT** /connections/{id} | Updates a connection
*ControllerApi* | [**create_bulletin**](nifi-docs/ControllerApi.md#create_bulletin) | **POST** /controller/bulletin | Creates a new bulletin
*ControllerApi* | [**create_controller_service**](nifi-docs/ControllerApi.md#create_controller_service) | **POST** /controller/controller-services | Creates a new controller service
*ControllerApi* | [**create_registry_client**](nifi-docs/ControllerApi.md#create_registry_client) | **POST** /controller/registry-clients | Creates a new registry client
*ControllerApi* | [**create_reporting_task**](nifi-docs/ControllerApi.md#create_reporting_task) | **POST** /controller/reporting-tasks | Creates a new reporting task
*ControllerApi* | [**delete_history**](nifi-docs/ControllerApi.md#delete_history) | **DELETE** /controller/history | Purges history
*ControllerApi* | [**delete_node**](nifi-docs/ControllerApi.md#delete_node) | **DELETE** /controller/cluster/nodes/{id} | Removes a node from the cluster
*ControllerApi* | [**delete_registry_client**](nifi-docs/ControllerApi.md#delete_registry_client) | **DELETE** /controller/registry-clients/{id} | Deletes a registry client
*ControllerApi* | [**get_cluster**](nifi-docs/ControllerApi.md#get_cluster) | **GET** /controller/cluster | Gets the contents of the cluster
*ControllerApi* | [**get_controller_config**](nifi-docs/ControllerApi.md#get_controller_config) | **GET** /controller/config | Retrieves the configuration for this NiFi Controller
*ControllerApi* | [**get_node**](nifi-docs/ControllerApi.md#get_node) | **GET** /controller/cluster/nodes/{id} | Gets a node in the cluster
*ControllerApi* | [**get_registry_client**](nifi-docs/ControllerApi.md#get_registry_client) | **GET** /controller/registry-clients/{id} | Gets a registry client
*ControllerApi* | [**get_registry_clients**](nifi-docs/ControllerApi.md#get_registry_clients) | **GET** /controller/registry-clients | Gets the listing of available registry clients
*ControllerApi* | [**update_controller_config**](nifi-docs/ControllerApi.md#update_controller_config) | **PUT** /controller/config | Retrieves the configuration for this NiFi
*ControllerApi* | [**update_node**](nifi-docs/ControllerApi.md#update_node) | **PUT** /controller/cluster/nodes/{id} | Updates a node in the cluster
*ControllerApi* | [**update_registry_client**](nifi-docs/ControllerApi.md#update_registry_client) | **PUT** /controller/registry-clients/{id} | Updates a registry client
*ControllerservicesApi* | [**clear_state**](nifi-docs/ControllerservicesApi.md#clear_state) | **POST** /controller-services/{id}/state/clear-requests | Clears the state for a controller service
*ControllerservicesApi* | [**get_controller_service**](nifi-docs/ControllerservicesApi.md#get_controller_service) | **GET** /controller-services/{id} | Gets a controller service
*ControllerservicesApi* | [**get_controller_service_references**](nifi-docs/ControllerservicesApi.md#get_controller_service_references) | **GET** /controller-services/{id}/references | Gets a controller service
*ControllerservicesApi* | [**get_property_descriptor**](nifi-docs/ControllerservicesApi.md#get_property_descriptor) | **GET** /controller-services/{id}/descriptors | Gets a controller service property descriptor
*ControllerservicesApi* | [**get_state**](nifi-docs/ControllerservicesApi.md#get_state) | **GET** /controller-services/{id}/state | Gets the state for a controller service
*ControllerservicesApi* | [**remove_controller_service**](nifi-docs/ControllerservicesApi.md#remove_controller_service) | **DELETE** /controller-services/{id} | Deletes a controller service
*ControllerservicesApi* | [**update_controller_service**](nifi-docs/ControllerservicesApi.md#update_controller_service) | **PUT** /controller-services/{id} | Updates a controller service
*ControllerservicesApi* | [**update_controller_service_references**](nifi-docs/ControllerservicesApi.md#update_controller_service_references) | **PUT** /controller-services/{id}/references | Updates a controller services references
*CountersApi* | [**get_counters**](nifi-docs/CountersApi.md#get_counters) | **GET** /counters | Gets the current counters for this NiFi
*CountersApi* | [**update_counter**](nifi-docs/CountersApi.md#update_counter) | **PUT** /counters/{id} | Updates the specified counter. This will reset the counter value to 0
*DatatransferApi* | [**commit_input_port_transaction**](nifi-docs/DatatransferApi.md#commit_input_port_transaction) | **DELETE** /data-transfer/input-ports/{portId}/transactions/{transactionId} | Commit or cancel the specified transaction
*DatatransferApi* | [**commit_output_port_transaction**](nifi-docs/DatatransferApi.md#commit_output_port_transaction) | **DELETE** /data-transfer/output-ports/{portId}/transactions/{transactionId} | Commit or cancel the specified transaction
*DatatransferApi* | [**create_port_transaction**](nifi-docs/DatatransferApi.md#create_port_transaction) | **POST** /data-transfer/{portType}/{portId}/transactions | Create a transaction to the specified output port or input port
*DatatransferApi* | [**extend_input_port_transaction_ttl**](nifi-docs/DatatransferApi.md#extend_input_port_transaction_ttl) | **PUT** /data-transfer/input-ports/{portId}/transactions/{transactionId} | Extend transaction TTL
*DatatransferApi* | [**extend_output_port_transaction_ttl**](nifi-docs/DatatransferApi.md#extend_output_port_transaction_ttl) | **PUT** /data-transfer/output-ports/{portId}/transactions/{transactionId} | Extend transaction TTL
*DatatransferApi* | [**receive_flow_files**](nifi-docs/DatatransferApi.md#receive_flow_files) | **POST** /data-transfer/input-ports/{portId}/transactions/{transactionId}/flow-files | Transfer flow files to the input port
*DatatransferApi* | [**transfer_flow_files**](nifi-docs/DatatransferApi.md#transfer_flow_files) | **GET** /data-transfer/output-ports/{portId}/transactions/{transactionId}/flow-files | Transfer flow files from the output port
*FlowApi* | [**activate_controller_services**](nifi-docs/FlowApi.md#activate_controller_services) | **PUT** /flow/process-groups/{id}/controller-services | Enable or disable Controller Services in the specified Process Group.
*FlowApi* | [**generate_client_id**](nifi-docs/FlowApi.md#generate_client_id) | **GET** /flow/client-id | Generates a client id.
*FlowApi* | [**get_about_info**](nifi-docs/FlowApi.md#get_about_info) | **GET** /flow/about | Retrieves details about this NiFi to put in the About dialog
*FlowApi* | [**get_action**](nifi-docs/FlowApi.md#get_action) | **GET** /flow/history/{id} | Gets an action
*FlowApi* | [**get_banners**](nifi-docs/FlowApi.md#get_banners) | **GET** /flow/banners | Retrieves the banners for this NiFi
*FlowApi* | [**get_buckets**](nifi-docs/FlowApi.md#get_buckets) | **GET** /flow/registries/{id}/buckets | Gets the buckets from the specified registry for the current user
*FlowApi* | [**get_bulletin_board**](nifi-docs/FlowApi.md#get_bulletin_board) | **GET** /flow/bulletin-board | Gets current bulletins
*FlowApi* | [**get_bulletins**](nifi-docs/FlowApi.md#get_bulletins) | **GET** /flow/controller/bulletins | Retrieves Controller level bulletins
*FlowApi* | [**get_cluster_summary**](nifi-docs/FlowApi.md#get_cluster_summary) | **GET** /flow/cluster/summary | The cluster summary for this NiFi
*FlowApi* | [**get_component_history**](nifi-docs/FlowApi.md#get_component_history) | **GET** /flow/history/components/{componentId} | Gets configuration history for a component
*FlowApi* | [**get_connection_status**](nifi-docs/FlowApi.md#get_connection_status) | **GET** /flow/connections/{id}/status | Gets status for a connection
*FlowApi* | [**get_connection_status_history**](nifi-docs/FlowApi.md#get_connection_status_history) | **GET** /flow/connections/{id}/status/history | Gets the status history for a connection
*FlowApi* | [**get_controller_service_types**](nifi-docs/FlowApi.md#get_controller_service_types) | **GET** /flow/controller-service-types | Retrieves the types of controller services that this NiFi supports
*FlowApi* | [**get_controller_services_from_controller**](nifi-docs/FlowApi.md#get_controller_services_from_controller) | **GET** /flow/controller/controller-services | Gets all controller services
*FlowApi* | [**get_controller_services_from_group**](nifi-docs/FlowApi.md#get_controller_services_from_group) | **GET** /flow/process-groups/{id}/controller-services | Gets all controller services
*FlowApi* | [**get_controller_status**](nifi-docs/FlowApi.md#get_controller_status) | **GET** /flow/status | Gets the current status of this NiFi
*FlowApi* | [**get_current_user**](nifi-docs/FlowApi.md#get_current_user) | **GET** /flow/current-user | Retrieves the user identity of the user making the request
*FlowApi* | [**get_flow**](nifi-docs/FlowApi.md#get_flow) | **GET** /flow/process-groups/{id} | Gets a process group
*FlowApi* | [**get_flow_config**](nifi-docs/FlowApi.md#get_flow_config) | **GET** /flow/config | Retrieves the configuration for this NiFi flow
*FlowApi* | [**get_flows**](nifi-docs/FlowApi.md#get_flows) | **GET** /flow/registries/{registry-id}/buckets/{bucket-id}/flows | Gets the flows from the specified registry and bucket for the current user
*FlowApi* | [**get_input_port_status**](nifi-docs/FlowApi.md#get_input_port_status) | **GET** /flow/input-ports/{id}/status | Gets status for an input port
*FlowApi* | [**get_output_port_status**](nifi-docs/FlowApi.md#get_output_port_status) | **GET** /flow/output-ports/{id}/status | Gets status for an output port
*FlowApi* | [**get_prioritizers**](nifi-docs/FlowApi.md#get_prioritizers) | **GET** /flow/prioritizers | Retrieves the types of prioritizers that this NiFi supports
*FlowApi* | [**get_process_group_status**](nifi-docs/FlowApi.md#get_process_group_status) | **GET** /flow/process-groups/{id}/status | Gets the status for a process group
*FlowApi* | [**get_process_group_status_history**](nifi-docs/FlowApi.md#get_process_group_status_history) | **GET** /flow/process-groups/{id}/status/history | Gets status history for a remote process group
*FlowApi* | [**get_processor_status**](nifi-docs/FlowApi.md#get_processor_status) | **GET** /flow/processors/{id}/status | Gets status for a processor
*FlowApi* | [**get_processor_status_history**](nifi-docs/FlowApi.md#get_processor_status_history) | **GET** /flow/processors/{id}/status/history | Gets status history for a processor
*FlowApi* | [**get_processor_types**](nifi-docs/FlowApi.md#get_processor_types) | **GET** /flow/processor-types | Retrieves the types of processors that this NiFi supports
*FlowApi* | [**get_registries**](nifi-docs/FlowApi.md#get_registries) | **GET** /flow/registries | Gets the listing of available registries
*FlowApi* | [**get_remote_process_group_status**](nifi-docs/FlowApi.md#get_remote_process_group_status) | **GET** /flow/remote-process-groups/{id}/status | Gets status for a remote process group
*FlowApi* | [**get_remote_process_group_status_history**](nifi-docs/FlowApi.md#get_remote_process_group_status_history) | **GET** /flow/remote-process-groups/{id}/status/history | Gets the status history
*FlowApi* | [**get_reporting_task_types**](nifi-docs/FlowApi.md#get_reporting_task_types) | **GET** /flow/reporting-task-types | Retrieves the types of reporting tasks that this NiFi supports
*FlowApi* | [**get_reporting_tasks**](nifi-docs/FlowApi.md#get_reporting_tasks) | **GET** /flow/reporting-tasks | Gets all reporting tasks
*FlowApi* | [**get_templates**](nifi-docs/FlowApi.md#get_templates) | **GET** /flow/templates | Gets all templates
*FlowApi* | [**get_versions**](nifi-docs/FlowApi.md#get_versions) | **GET** /flow/registries/{registry-id}/buckets/{bucket-id}/flows/{flow-id}/versions | Gets the flow versions from the specified registry and bucket for the specified flow for the current user
*FlowApi* | [**query_history**](nifi-docs/FlowApi.md#query_history) | **GET** /flow/history | Gets configuration history
*FlowApi* | [**schedule_components**](nifi-docs/FlowApi.md#schedule_components) | **PUT** /flow/process-groups/{id} | Schedule or unschedule components in the specified Process Group.
*FlowApi* | [**search_cluster**](nifi-docs/FlowApi.md#search_cluster) | **GET** /flow/cluster/search-results | Searches the cluster for a node with the specified address
*FlowApi* | [**search_flow**](nifi-docs/FlowApi.md#search_flow) | **GET** /flow/search-results | Performs a search against this NiFi using the specified search term
*FlowfilequeuesApi* | [**create_drop_request**](nifi-docs/FlowfilequeuesApi.md#create_drop_request) | **POST** /flowfile-queues/{id}/drop-requests | Creates a request to drop the contents of the queue in this connection.
*FlowfilequeuesApi* | [**create_flow_file_listing**](nifi-docs/FlowfilequeuesApi.md#create_flow_file_listing) | **POST** /flowfile-queues/{id}/listing-requests | Lists the contents of the queue in this connection.
*FlowfilequeuesApi* | [**delete_listing_request**](nifi-docs/FlowfilequeuesApi.md#delete_listing_request) | **DELETE** /flowfile-queues/{id}/listing-requests/{listing-request-id} | Cancels and/or removes a request to list the contents of this connection.
*FlowfilequeuesApi* | [**download_flow_file_content**](nifi-docs/FlowfilequeuesApi.md#download_flow_file_content) | **GET** /flowfile-queues/{id}/flowfiles/{flowfile-uuid}/content | Gets the content for a FlowFile in a Connection.
*FlowfilequeuesApi* | [**get_drop_request**](nifi-docs/FlowfilequeuesApi.md#get_drop_request) | **GET** /flowfile-queues/{id}/drop-requests/{drop-request-id} | Gets the current status of a drop request for the specified connection.
*FlowfilequeuesApi* | [**get_flow_file**](nifi-docs/FlowfilequeuesApi.md#get_flow_file) | **GET** /flowfile-queues/{id}/flowfiles/{flowfile-uuid} | Gets a FlowFile from a Connection.
*FlowfilequeuesApi* | [**get_listing_request**](nifi-docs/FlowfilequeuesApi.md#get_listing_request) | **GET** /flowfile-queues/{id}/listing-requests/{listing-request-id} | Gets the current status of a listing request for the specified connection.
*FlowfilequeuesApi* | [**remove_drop_request**](nifi-docs/FlowfilequeuesApi.md#remove_drop_request) | **DELETE** /flowfile-queues/{id}/drop-requests/{drop-request-id} | Cancels and/or removes a request to drop the contents of this connection.
*FunnelApi* | [**get_funnel**](nifi-docs/FunnelApi.md#get_funnel) | **GET** /funnels/{id} | Gets a funnel
*FunnelApi* | [**remove_funnel**](nifi-docs/FunnelApi.md#remove_funnel) | **DELETE** /funnels/{id} | Deletes a funnel
*FunnelApi* | [**update_funnel**](nifi-docs/FunnelApi.md#update_funnel) | **PUT** /funnels/{id} | Updates a funnel
*InputportsApi* | [**get_input_port**](nifi-docs/InputportsApi.md#get_input_port) | **GET** /input-ports/{id} | Gets an input port
*InputportsApi* | [**remove_input_port**](nifi-docs/InputportsApi.md#remove_input_port) | **DELETE** /input-ports/{id} | Deletes an input port
*InputportsApi* | [**update_input_port**](nifi-docs/InputportsApi.md#update_input_port) | **PUT** /input-ports/{id} | Updates an input port
*LabelsApi* | [**get_label**](nifi-docs/LabelsApi.md#get_label) | **GET** /labels/{id} | Gets a label
*LabelsApi* | [**remove_label**](nifi-docs/LabelsApi.md#remove_label) | **DELETE** /labels/{id} | Deletes a label
*LabelsApi* | [**update_label**](nifi-docs/LabelsApi.md#update_label) | **PUT** /labels/{id} | Updates a label
*OutputportsApi* | [**get_output_port**](nifi-docs/OutputportsApi.md#get_output_port) | **GET** /output-ports/{id} | Gets an output port
*OutputportsApi* | [**remove_output_port**](nifi-docs/OutputportsApi.md#remove_output_port) | **DELETE** /output-ports/{id} | Deletes an output port
*OutputportsApi* | [**update_output_port**](nifi-docs/OutputportsApi.md#update_output_port) | **PUT** /output-ports/{id} | Updates an output port
*PoliciesApi* | [**create_access_policy**](nifi-docs/PoliciesApi.md#create_access_policy) | **POST** /policies | Creates an access policy
*PoliciesApi* | [**get_access_policy**](nifi-docs/PoliciesApi.md#get_access_policy) | **GET** /policies/{id} | Gets an access policy
*PoliciesApi* | [**get_access_policy_for_resource**](nifi-docs/PoliciesApi.md#get_access_policy_for_resource) | **GET** /policies/{action}/{resource} | Gets an access policy for the specified action and resource
*PoliciesApi* | [**remove_access_policy**](nifi-docs/PoliciesApi.md#remove_access_policy) | **DELETE** /policies/{id} | Deletes an access policy
*PoliciesApi* | [**update_access_policy**](nifi-docs/PoliciesApi.md#update_access_policy) | **PUT** /policies/{id} | Updates a access policy
*ProcessgroupsApi* | [**copy_snippet**](nifi-docs/ProcessgroupsApi.md#copy_snippet) | **POST** /process-groups/{id}/snippet-instance | Copies a snippet and discards it.
*ProcessgroupsApi* | [**create_connection**](nifi-docs/ProcessgroupsApi.md#create_connection) | **POST** /process-groups/{id}/connections | Creates a connection
*ProcessgroupsApi* | [**create_controller_service**](nifi-docs/ProcessgroupsApi.md#create_controller_service) | **POST** /process-groups/{id}/controller-services | Creates a new controller service
*ProcessgroupsApi* | [**create_funnel**](nifi-docs/ProcessgroupsApi.md#create_funnel) | **POST** /process-groups/{id}/funnels | Creates a funnel
*ProcessgroupsApi* | [**create_input_port**](nifi-docs/ProcessgroupsApi.md#create_input_port) | **POST** /process-groups/{id}/input-ports | Creates an input port
*ProcessgroupsApi* | [**create_label**](nifi-docs/ProcessgroupsApi.md#create_label) | **POST** /process-groups/{id}/labels | Creates a label
*ProcessgroupsApi* | [**create_output_port**](nifi-docs/ProcessgroupsApi.md#create_output_port) | **POST** /process-groups/{id}/output-ports | Creates an output port
*ProcessgroupsApi* | [**create_process_group**](nifi-docs/ProcessgroupsApi.md#create_process_group) | **POST** /process-groups/{id}/process-groups | Creates a process group
*ProcessgroupsApi* | [**create_processor**](nifi-docs/ProcessgroupsApi.md#create_processor) | **POST** /process-groups/{id}/processors | Creates a new processor
*ProcessgroupsApi* | [**create_remote_process_group**](nifi-docs/ProcessgroupsApi.md#create_remote_process_group) | **POST** /process-groups/{id}/remote-process-groups | Creates a new process group
*ProcessgroupsApi* | [**create_template**](nifi-docs/ProcessgroupsApi.md#create_template) | **POST** /process-groups/{id}/templates | Creates a template and discards the specified snippet.
*ProcessgroupsApi* | [**delete_variable_registry_update_request**](nifi-docs/ProcessgroupsApi.md#delete_variable_registry_update_request) | **DELETE** /process-groups/{groupId}/variable-registry/update-requests/{updateId} | Deletes an update request for a process group&#39;s variable registry. If the request is not yet complete, it will automatically be cancelled.
*ProcessgroupsApi* | [**get_connections**](nifi-docs/ProcessgroupsApi.md#get_connections) | **GET** /process-groups/{id}/connections | Gets all connections
*ProcessgroupsApi* | [**get_funnels**](nifi-docs/ProcessgroupsApi.md#get_funnels) | **GET** /process-groups/{id}/funnels | Gets all funnels
*ProcessgroupsApi* | [**get_input_ports**](nifi-docs/ProcessgroupsApi.md#get_input_ports) | **GET** /process-groups/{id}/input-ports | Gets all input ports
*ProcessgroupsApi* | [**get_labels**](nifi-docs/ProcessgroupsApi.md#get_labels) | **GET** /process-groups/{id}/labels | Gets all labels
*ProcessgroupsApi* | [**get_local_modifications**](nifi-docs/ProcessgroupsApi.md#get_local_modifications) | **GET** /process-groups/{id}/local-modifications | Gets a list of local modifications to the Process Group since it was last synchronized with the Flow Registry
*ProcessgroupsApi* | [**get_output_ports**](nifi-docs/ProcessgroupsApi.md#get_output_ports) | **GET** /process-groups/{id}/output-ports | Gets all output ports
*ProcessgroupsApi* | [**get_process_group**](nifi-docs/ProcessgroupsApi.md#get_process_group) | **GET** /process-groups/{id} | Gets a process group
*ProcessgroupsApi* | [**get_process_groups**](nifi-docs/ProcessgroupsApi.md#get_process_groups) | **GET** /process-groups/{id}/process-groups | Gets all process groups
*ProcessgroupsApi* | [**get_processors**](nifi-docs/ProcessgroupsApi.md#get_processors) | **GET** /process-groups/{id}/processors | Gets all processors
*ProcessgroupsApi* | [**get_remote_process_groups**](nifi-docs/ProcessgroupsApi.md#get_remote_process_groups) | **GET** /process-groups/{id}/remote-process-groups | Gets all remote process groups
*ProcessgroupsApi* | [**get_variable_registry**](nifi-docs/ProcessgroupsApi.md#get_variable_registry) | **GET** /process-groups/{id}/variable-registry | Gets a process group&#39;s variable registry
*ProcessgroupsApi* | [**get_variable_registry_update_request**](nifi-docs/ProcessgroupsApi.md#get_variable_registry_update_request) | **GET** /process-groups/{groupId}/variable-registry/update-requests/{updateId} | Gets a process group&#39;s variable registry
*ProcessgroupsApi* | [**import_template**](nifi-docs/ProcessgroupsApi.md#import_template) | **POST** /process-groups/{id}/templates/import | Imports a template
*ProcessgroupsApi* | [**instantiate_template**](nifi-docs/ProcessgroupsApi.md#instantiate_template) | **POST** /process-groups/{id}/template-instance | Instantiates a template
*ProcessgroupsApi* | [**remove_process_group**](nifi-docs/ProcessgroupsApi.md#remove_process_group) | **DELETE** /process-groups/{id} | Deletes a process group
*ProcessgroupsApi* | [**submit_update_variable_registry_request**](nifi-docs/ProcessgroupsApi.md#submit_update_variable_registry_request) | **POST** /process-groups/{id}/variable-registry/update-requests | Submits a request to update a process group&#39;s variable registry
*ProcessgroupsApi* | [**update_process_group**](nifi-docs/ProcessgroupsApi.md#update_process_group) | **PUT** /process-groups/{id} | Updates a process group
*ProcessgroupsApi* | [**update_variable_registry**](nifi-docs/ProcessgroupsApi.md#update_variable_registry) | **PUT** /process-groups/{id}/variable-registry | Updates the contents of a Process Group&#39;s variable Registry
*ProcessgroupsApi* | [**upload_template**](nifi-docs/ProcessgroupsApi.md#upload_template) | **POST** /process-groups/{id}/templates/upload | Uploads a template
*ProcessorsApi* | [**clear_state**](nifi-docs/ProcessorsApi.md#clear_state) | **POST** /processors/{id}/state/clear-requests | Clears the state for a processor
*ProcessorsApi* | [**delete_processor**](nifi-docs/ProcessorsApi.md#delete_processor) | **DELETE** /processors/{id} | Deletes a processor
*ProcessorsApi* | [**get_processor**](nifi-docs/ProcessorsApi.md#get_processor) | **GET** /processors/{id} | Gets a processor
*ProcessorsApi* | [**get_property_descriptor**](nifi-docs/ProcessorsApi.md#get_property_descriptor) | **GET** /processors/{id}/descriptors | Gets the descriptor for a processor property
*ProcessorsApi* | [**get_state**](nifi-docs/ProcessorsApi.md#get_state) | **GET** /processors/{id}/state | Gets the state for a processor
*ProcessorsApi* | [**update_processor**](nifi-docs/ProcessorsApi.md#update_processor) | **PUT** /processors/{id} | Updates a processor
*ProvenanceApi* | [**delete_lineage**](nifi-docs/ProvenanceApi.md#delete_lineage) | **DELETE** /provenance/lineage/{id} | Deletes a lineage query
*ProvenanceApi* | [**delete_provenance**](nifi-docs/ProvenanceApi.md#delete_provenance) | **DELETE** /provenance/{id} | Deletes a provenance query
*ProvenanceApi* | [**get_lineage**](nifi-docs/ProvenanceApi.md#get_lineage) | **GET** /provenance/lineage/{id} | Gets a lineage query
*ProvenanceApi* | [**get_provenance**](nifi-docs/ProvenanceApi.md#get_provenance) | **GET** /provenance/{id} | Gets a provenance query
*ProvenanceApi* | [**get_search_options**](nifi-docs/ProvenanceApi.md#get_search_options) | **GET** /provenance/search-options | Gets the searchable attributes for provenance events
*ProvenanceApi* | [**submit_lineage_request**](nifi-docs/ProvenanceApi.md#submit_lineage_request) | **POST** /provenance/lineage | Submits a lineage query
*ProvenanceApi* | [**submit_provenance_request**](nifi-docs/ProvenanceApi.md#submit_provenance_request) | **POST** /provenance | Submits a provenance query
*ProvenanceeventsApi* | [**get_input_content**](nifi-docs/ProvenanceeventsApi.md#get_input_content) | **GET** /provenance-events/{id}/content/input | Gets the input content for a provenance event
*ProvenanceeventsApi* | [**get_output_content**](nifi-docs/ProvenanceeventsApi.md#get_output_content) | **GET** /provenance-events/{id}/content/output | Gets the output content for a provenance event
*ProvenanceeventsApi* | [**get_provenance_event**](nifi-docs/ProvenanceeventsApi.md#get_provenance_event) | **GET** /provenance-events/{id} | Gets a provenance event
*ProvenanceeventsApi* | [**submit_replay**](nifi-docs/ProvenanceeventsApi.md#submit_replay) | **POST** /provenance-events/replays | Replays content from a provenance event
*RemoteprocessgroupsApi* | [**get_remote_process_group**](nifi-docs/RemoteprocessgroupsApi.md#get_remote_process_group) | **GET** /remote-process-groups/{id} | Gets a remote process group
*RemoteprocessgroupsApi* | [**remove_remote_process_group**](nifi-docs/RemoteprocessgroupsApi.md#remove_remote_process_group) | **DELETE** /remote-process-groups/{id} | Deletes a remote process group
*RemoteprocessgroupsApi* | [**update_remote_process_group**](nifi-docs/RemoteprocessgroupsApi.md#update_remote_process_group) | **PUT** /remote-process-groups/{id} | Updates a remote process group
*RemoteprocessgroupsApi* | [**update_remote_process_group_input_port**](nifi-docs/RemoteprocessgroupsApi.md#update_remote_process_group_input_port) | **PUT** /remote-process-groups/{id}/input-ports/{port-id} | Updates a remote port
*RemoteprocessgroupsApi* | [**update_remote_process_group_output_port**](nifi-docs/RemoteprocessgroupsApi.md#update_remote_process_group_output_port) | **PUT** /remote-process-groups/{id}/output-ports/{port-id} | Updates a remote port
*ReportingtasksApi* | [**clear_state**](nifi-docs/ReportingtasksApi.md#clear_state) | **POST** /reporting-tasks/{id}/state/clear-requests | Clears the state for a reporting task
*ReportingtasksApi* | [**get_property_descriptor**](nifi-docs/ReportingtasksApi.md#get_property_descriptor) | **GET** /reporting-tasks/{id}/descriptors | Gets a reporting task property descriptor
*ReportingtasksApi* | [**get_reporting_task**](nifi-docs/ReportingtasksApi.md#get_reporting_task) | **GET** /reporting-tasks/{id} | Gets a reporting task
*ReportingtasksApi* | [**get_state**](nifi-docs/ReportingtasksApi.md#get_state) | **GET** /reporting-tasks/{id}/state | Gets the state for a reporting task
*ReportingtasksApi* | [**remove_reporting_task**](nifi-docs/ReportingtasksApi.md#remove_reporting_task) | **DELETE** /reporting-tasks/{id} | Deletes a reporting task
*ReportingtasksApi* | [**update_reporting_task**](nifi-docs/ReportingtasksApi.md#update_reporting_task) | **PUT** /reporting-tasks/{id} | Updates a reporting task
*ResourcesApi* | [**get_resources**](nifi-docs/ResourcesApi.md#get_resources) | **GET** /resources | Gets the available resources that support access/authorization policies
*SitetositeApi* | [**get_peers**](nifi-docs/SitetositeApi.md#get_peers) | **GET** /site-to-site/peers | Returns the available Peers and its status of this NiFi
*SitetositeApi* | [**get_site_to_site_details**](nifi-docs/SitetositeApi.md#get_site_to_site_details) | **GET** /site-to-site | Returns the details about this NiFi necessary to communicate via site to site
*SnippetsApi* | [**create_snippet**](nifi-docs/SnippetsApi.md#create_snippet) | **POST** /snippets | Creates a snippet. The snippet will be automatically discarded if not used in a subsequent request after 1 minute.
*SnippetsApi* | [**delete_snippet**](nifi-docs/SnippetsApi.md#delete_snippet) | **DELETE** /snippets/{id} | Deletes the components in a snippet and discards the snippet
*SnippetsApi* | [**update_snippet**](nifi-docs/SnippetsApi.md#update_snippet) | **PUT** /snippets/{id} | Move&#39;s the components in this Snippet into a new Process Group and discards the snippet
*SystemdiagnosticsApi* | [**get_system_diagnostics**](nifi-docs/SystemdiagnosticsApi.md#get_system_diagnostics) | **GET** /system-diagnostics | Gets the diagnostics for the system NiFi is running on
*TemplatesApi* | [**export_template**](nifi-docs/TemplatesApi.md#export_template) | **GET** /templates/{id}/download | Exports a template
*TemplatesApi* | [**remove_template**](nifi-docs/TemplatesApi.md#remove_template) | **DELETE** /templates/{id} | Deletes a template
*TenantsApi* | [**create_user**](nifi-docs/TenantsApi.md#create_user) | **POST** /tenants/users | Creates a user
*TenantsApi* | [**create_user_group**](nifi-docs/TenantsApi.md#create_user_group) | **POST** /tenants/user-groups | Creates a user group
*TenantsApi* | [**get_user**](nifi-docs/TenantsApi.md#get_user) | **GET** /tenants/users/{id} | Gets a user
*TenantsApi* | [**get_user_group**](nifi-docs/TenantsApi.md#get_user_group) | **GET** /tenants/user-groups/{id} | Gets a user group
*TenantsApi* | [**get_user_groups**](nifi-docs/TenantsApi.md#get_user_groups) | **GET** /tenants/user-groups | Gets all user groups
*TenantsApi* | [**get_users**](nifi-docs/TenantsApi.md#get_users) | **GET** /tenants/users | Gets all users
*TenantsApi* | [**remove_user**](nifi-docs/TenantsApi.md#remove_user) | **DELETE** /tenants/users/{id} | Deletes a user
*TenantsApi* | [**remove_user_group**](nifi-docs/TenantsApi.md#remove_user_group) | **DELETE** /tenants/user-groups/{id} | Deletes a user group
*TenantsApi* | [**search_tenants**](nifi-docs/TenantsApi.md#search_tenants) | **GET** /tenants/search-results | Searches for a tenant with the specified identity
*TenantsApi* | [**update_user**](nifi-docs/TenantsApi.md#update_user) | **PUT** /tenants/users/{id} | Updates a user
*TenantsApi* | [**update_user_group**](nifi-docs/TenantsApi.md#update_user_group) | **PUT** /tenants/user-groups/{id} | Updates a user group
*VersionsApi* | [**create_version_control_request**](nifi-docs/VersionsApi.md#create_version_control_request) | **POST** /versions/active-requests | Creates a request so that a Process Group can be placed under Version Control or have its Version Control configuration changed. Creating this request will prevent any other threads from simultaneously saving local changes to Version Control. It will not, however, actually save the local flow to the Flow Registry. A POST to /versions/process-groups/{id} should be used to initiate saving of the local flow to the Flow Registry.
*VersionsApi* | [**delete_revert_request**](nifi-docs/VersionsApi.md#delete_revert_request) | **DELETE** /versions/revert-requests/{id} | Deletes the Revert Request with the given ID. After a request is created via a POST to /versions/revert-requests/process-groups/{id}, it is expected that the client will properly clean up the request by DELETE&#39;ing it, once the Revert process has completed. If the request is deleted before the request completes, then the Revert request will finish the step that it is currently performing and then will cancel any subsequent steps.
*VersionsApi* | [**delete_update_request**](nifi-docs/VersionsApi.md#delete_update_request) | **DELETE** /versions/update-requests/{id} | Deletes the Update Request with the given ID. After a request is created via a POST to /versions/update-requests/process-groups/{id}, it is expected that the client will properly clean up the request by DELETE&#39;ing it, once the Update process has completed. If the request is deleted before the request completes, then the Update request will finish the step that it is currently performing and then will cancel any subsequent steps.
*VersionsApi* | [**delete_version_control_request**](nifi-docs/VersionsApi.md#delete_version_control_request) | **DELETE** /versions/active-requests/{id} | Deletes the Version Control Request with the given ID. This will allow other threads to save flows to the Flow Registry. See also the documentation for POSTing to /versions/active-requests for information regarding why this is done.
*VersionsApi* | [**get_revert_request**](nifi-docs/VersionsApi.md#get_revert_request) | **GET** /versions/revert-requests/{id} | Returns the Revert Request with the given ID. Once a Revert Request has been created by performing a POST to /versions/revert-requests/process-groups/{id}, that request can subsequently be retrieved via this endpoint, and the request that is fetched will contain the updated state, such as percent complete, the current state of the request, and any failures.
*VersionsApi* | [**get_update_request**](nifi-docs/VersionsApi.md#get_update_request) | **GET** /versions/update-requests/{id} | Returns the Update Request with the given ID. Once an Update Request has been created by performing a POST to /versions/update-requests/process-groups/{id}, that request can subsequently be retrieved via this endpoint, and the request that is fetched will contain the updated state, such as percent complete, the current state of the request, and any failures.
*VersionsApi* | [**get_version_information**](nifi-docs/VersionsApi.md#get_version_information) | **GET** /versions/process-groups/{id} | Gets the Version Control information for a process group
*VersionsApi* | [**initiate_revert_flow_version**](nifi-docs/VersionsApi.md#initiate_revert_flow_version) | **POST** /versions/revert-requests/process-groups/{id} | For a Process Group that is already under Version Control, this will initiate the action of reverting any local changes that have been made to the Process Group since it was last synchronized with the Flow Registry. This will result in the flow matching the Versioned Flow that exists in the Flow Registry. This can be a lengthy process, as it will stop any Processors and disable any Controller Services necessary to perform the action and then restart them. As a result, the endpoint will immediately return a VersionedFlowUpdateRequestEntity, and the process of updating the flow will occur asynchronously in the background. The client may then periodically poll the status of the request by issuing a GET request to /versions/revert-requests/{requestId}. Once the request is completed, the client is expected to issue a DELETE request to /versions/revert-requests/{requestId}.
*VersionsApi* | [**initiate_version_control_update**](nifi-docs/VersionsApi.md#initiate_version_control_update) | **POST** /versions/update-requests/process-groups/{id} | For a Process Group that is already under Version Control, this will initiate the action of changing from a specific version of the flow in the Flow Registry to a different version of the flow. This can be a lengthy process, as it will stop any Processors and disable any Controller Services necessary to perform the action and then restart them. As a result, the endpoint will immediately return a VersionedFlowUpdateRequestEntity, and the process of updating the flow will occur asynchronously in the background. The client may then periodically poll the status of the request by issuing a GET request to /versions/update-requests/{requestId}. Once the request is completed, the client is expected to issue a DELETE request to /versions/update-requests/{requestId}.
*VersionsApi* | [**save_to_flow_registry**](nifi-docs/VersionsApi.md#save_to_flow_registry) | **POST** /versions/process-groups/{id} | Begins version controlling the Process Group with the given ID or commits changes to the Versioned Flow, depending on if the provided VersionControlInformation includes a flowId
*VersionsApi* | [**stop_version_control**](nifi-docs/VersionsApi.md#stop_version_control) | **DELETE** /versions/process-groups/{id} | Stops version controlling the Process Group with the given ID. The Process Group will no longer track to any Versioned Flow.
*VersionsApi* | [**update_flow_version**](nifi-docs/VersionsApi.md#update_flow_version) | **PUT** /versions/process-groups/{id} | For a Process Group that is already under Version Control, this will update the version of the flow to a different version. This endpoint expects that the given snapshot will not modify any Processor that is currently running or any Controller Service that is enabled.
*VersionsApi* | [**update_version_control_request**](nifi-docs/VersionsApi.md#update_version_control_request) | **PUT** /versions/active-requests/{id} | Updates the request with the given ID


## Documentation For Models

 - [AboutDTO](nifi-docs/AboutDTO.md)
 - [AboutEntity](nifi-docs/AboutEntity.md)
 - [AccessConfigurationDTO](nifi-docs/AccessConfigurationDTO.md)
 - [AccessConfigurationEntity](nifi-docs/AccessConfigurationEntity.md)
 - [AccessPolicyDTO](nifi-docs/AccessPolicyDTO.md)
 - [AccessPolicyEntity](nifi-docs/AccessPolicyEntity.md)
 - [AccessPolicySummaryDTO](nifi-docs/AccessPolicySummaryDTO.md)
 - [AccessPolicySummaryEntity](nifi-docs/AccessPolicySummaryEntity.md)
 - [AccessStatusDTO](nifi-docs/AccessStatusDTO.md)
 - [AccessStatusEntity](nifi-docs/AccessStatusEntity.md)
 - [ActionDTO](nifi-docs/ActionDTO.md)
 - [ActionDetailsDTO](nifi-docs/ActionDetailsDTO.md)
 - [ActionEntity](nifi-docs/ActionEntity.md)
 - [ActivateControllerServicesEntity](nifi-docs/ActivateControllerServicesEntity.md)
 - [AffectedComponentDTO](nifi-docs/AffectedComponentDTO.md)
 - [AffectedComponentEntity](nifi-docs/AffectedComponentEntity.md)
 - [AllowableValueDTO](nifi-docs/AllowableValueDTO.md)
 - [AllowableValueEntity](nifi-docs/AllowableValueEntity.md)
 - [AttributeDTO](nifi-docs/AttributeDTO.md)
 - [BannerDTO](nifi-docs/BannerDTO.md)
 - [BannerEntity](nifi-docs/BannerEntity.md)
 - [BatchSettingsDTO](nifi-docs/BatchSettingsDTO.md)
 - [BatchSize](nifi-docs/BatchSize.md)
 - [Bucket](nifi-docs/Bucket.md)
 - [BucketDTO](nifi-docs/BucketDTO.md)
 - [BucketEntity](nifi-docs/BucketEntity.md)
 - [BucketsEntity](nifi-docs/BucketsEntity.md)
 - [BulletinBoardDTO](nifi-docs/BulletinBoardDTO.md)
 - [BulletinBoardEntity](nifi-docs/BulletinBoardEntity.md)
 - [BulletinDTO](nifi-docs/BulletinDTO.md)
 - [BulletinEntity](nifi-docs/BulletinEntity.md)
 - [Bundle](nifi-docs/Bundle.md)
 - [BundleDTO](nifi-docs/BundleDTO.md)
 - [ClusteSummaryEntity](nifi-docs/ClusteSummaryEntity.md)
 - [ClusterDTO](nifi-docs/ClusterDTO.md)
 - [ClusterEntity](nifi-docs/ClusterEntity.md)
 - [ClusterSearchResultsEntity](nifi-docs/ClusterSearchResultsEntity.md)
 - [ClusterSummaryDTO](nifi-docs/ClusterSummaryDTO.md)
 - [ComponentDetailsDTO](nifi-docs/ComponentDetailsDTO.md)
 - [ComponentDifferenceDTO](nifi-docs/ComponentDifferenceDTO.md)
 - [ComponentHistoryDTO](nifi-docs/ComponentHistoryDTO.md)
 - [ComponentHistoryEntity](nifi-docs/ComponentHistoryEntity.md)
 - [ComponentReferenceDTO](nifi-docs/ComponentReferenceDTO.md)
 - [ComponentReferenceEntity](nifi-docs/ComponentReferenceEntity.md)
 - [ComponentSearchResultDTO](nifi-docs/ComponentSearchResultDTO.md)
 - [ComponentStateDTO](nifi-docs/ComponentStateDTO.md)
 - [ComponentStateEntity](nifi-docs/ComponentStateEntity.md)
 - [ConnectableComponent](nifi-docs/ConnectableComponent.md)
 - [ConnectableDTO](nifi-docs/ConnectableDTO.md)
 - [ConnectionDTO](nifi-docs/ConnectionDTO.md)
 - [ConnectionEntity](nifi-docs/ConnectionEntity.md)
 - [ConnectionStatusDTO](nifi-docs/ConnectionStatusDTO.md)
 - [ConnectionStatusEntity](nifi-docs/ConnectionStatusEntity.md)
 - [ConnectionStatusSnapshotDTO](nifi-docs/ConnectionStatusSnapshotDTO.md)
 - [ConnectionStatusSnapshotEntity](nifi-docs/ConnectionStatusSnapshotEntity.md)
 - [ConnectionsEntity](nifi-docs/ConnectionsEntity.md)
 - [ControllerBulletinsEntity](nifi-docs/ControllerBulletinsEntity.md)
 - [ControllerConfigurationDTO](nifi-docs/ControllerConfigurationDTO.md)
 - [ControllerConfigurationEntity](nifi-docs/ControllerConfigurationEntity.md)
 - [ControllerDTO](nifi-docs/ControllerDTO.md)
 - [ControllerEntity](nifi-docs/ControllerEntity.md)
 - [ControllerServiceAPI](nifi-docs/ControllerServiceAPI.md)
 - [ControllerServiceApiDTO](nifi-docs/ControllerServiceApiDTO.md)
 - [ControllerServiceDTO](nifi-docs/ControllerServiceDTO.md)
 - [ControllerServiceEntity](nifi-docs/ControllerServiceEntity.md)
 - [ControllerServiceReferencingComponentDTO](nifi-docs/ControllerServiceReferencingComponentDTO.md)
 - [ControllerServiceReferencingComponentEntity](nifi-docs/ControllerServiceReferencingComponentEntity.md)
 - [ControllerServiceReferencingComponentsEntity](nifi-docs/ControllerServiceReferencingComponentsEntity.md)
 - [ControllerServiceTypesEntity](nifi-docs/ControllerServiceTypesEntity.md)
 - [ControllerServicesEntity](nifi-docs/ControllerServicesEntity.md)
 - [ControllerStatusDTO](nifi-docs/ControllerStatusDTO.md)
 - [ControllerStatusEntity](nifi-docs/ControllerStatusEntity.md)
 - [CopySnippetRequestEntity](nifi-docs/CopySnippetRequestEntity.md)
 - [CounterDTO](nifi-docs/CounterDTO.md)
 - [CounterEntity](nifi-docs/CounterEntity.md)
 - [CountersDTO](nifi-docs/CountersDTO.md)
 - [CountersEntity](nifi-docs/CountersEntity.md)
 - [CountersSnapshotDTO](nifi-docs/CountersSnapshotDTO.md)
 - [CreateActiveRequestEntity](nifi-docs/CreateActiveRequestEntity.md)
 - [CreateTemplateRequestEntity](nifi-docs/CreateTemplateRequestEntity.md)
 - [CurrentUserEntity](nifi-docs/CurrentUserEntity.md)
 - [DifferenceDTO](nifi-docs/DifferenceDTO.md)
 - [DimensionsDTO](nifi-docs/DimensionsDTO.md)
 - [DocumentedTypeDTO](nifi-docs/DocumentedTypeDTO.md)
 - [DropRequestDTO](nifi-docs/DropRequestDTO.md)
 - [DropRequestEntity](nifi-docs/DropRequestEntity.md)
 - [FlowBreadcrumbDTO](nifi-docs/FlowBreadcrumbDTO.md)
 - [FlowBreadcrumbEntity](nifi-docs/FlowBreadcrumbEntity.md)
 - [FlowComparisonEntity](nifi-docs/FlowComparisonEntity.md)
 - [FlowConfigurationDTO](nifi-docs/FlowConfigurationDTO.md)
 - [FlowConfigurationEntity](nifi-docs/FlowConfigurationEntity.md)
 - [FlowDTO](nifi-docs/FlowDTO.md)
 - [FlowEntity](nifi-docs/FlowEntity.md)
 - [FlowFileDTO](nifi-docs/FlowFileDTO.md)
 - [FlowFileEntity](nifi-docs/FlowFileEntity.md)
 - [FlowFileSummaryDTO](nifi-docs/FlowFileSummaryDTO.md)
 - [FlowSnippetDTO](nifi-docs/FlowSnippetDTO.md)
 - [FunnelDTO](nifi-docs/FunnelDTO.md)
 - [FunnelEntity](nifi-docs/FunnelEntity.md)
 - [FunnelsEntity](nifi-docs/FunnelsEntity.md)
 - [GarbageCollectionDTO](nifi-docs/GarbageCollectionDTO.md)
 - [HistoryDTO](nifi-docs/HistoryDTO.md)
 - [HistoryEntity](nifi-docs/HistoryEntity.md)
 - [InputPortsEntity](nifi-docs/InputPortsEntity.md)
 - [InstantiateTemplateRequestEntity](nifi-docs/InstantiateTemplateRequestEntity.md)
 - [LabelDTO](nifi-docs/LabelDTO.md)
 - [LabelEntity](nifi-docs/LabelEntity.md)
 - [LabelsEntity](nifi-docs/LabelsEntity.md)
 - [LineageDTO](nifi-docs/LineageDTO.md)
 - [LineageEntity](nifi-docs/LineageEntity.md)
 - [LineageRequestDTO](nifi-docs/LineageRequestDTO.md)
 - [LineageResultsDTO](nifi-docs/LineageResultsDTO.md)
 - [Link](nifi-docs/Link.md)
 - [ListingRequestDTO](nifi-docs/ListingRequestDTO.md)
 - [ListingRequestEntity](nifi-docs/ListingRequestEntity.md)
 - [NodeConnectionStatusSnapshotDTO](nifi-docs/NodeConnectionStatusSnapshotDTO.md)
 - [NodeCountersSnapshotDTO](nifi-docs/NodeCountersSnapshotDTO.md)
 - [NodeDTO](nifi-docs/NodeDTO.md)
 - [NodeEntity](nifi-docs/NodeEntity.md)
 - [NodeEventDTO](nifi-docs/NodeEventDTO.md)
 - [NodePortStatusSnapshotDTO](nifi-docs/NodePortStatusSnapshotDTO.md)
 - [NodeProcessGroupStatusSnapshotDTO](nifi-docs/NodeProcessGroupStatusSnapshotDTO.md)
 - [NodeProcessorStatusSnapshotDTO](nifi-docs/NodeProcessorStatusSnapshotDTO.md)
 - [NodeRemoteProcessGroupStatusSnapshotDTO](nifi-docs/NodeRemoteProcessGroupStatusSnapshotDTO.md)
 - [NodeSearchResultDTO](nifi-docs/NodeSearchResultDTO.md)
 - [NodeStatusSnapshotsDTO](nifi-docs/NodeStatusSnapshotsDTO.md)
 - [NodeSystemDiagnosticsSnapshotDTO](nifi-docs/NodeSystemDiagnosticsSnapshotDTO.md)
 - [OutputPortsEntity](nifi-docs/OutputPortsEntity.md)
 - [PeerDTO](nifi-docs/PeerDTO.md)
 - [PeersEntity](nifi-docs/PeersEntity.md)
 - [Permissions](nifi-docs/Permissions.md)
 - [PermissionsDTO](nifi-docs/PermissionsDTO.md)
 - [PortDTO](nifi-docs/PortDTO.md)
 - [PortEntity](nifi-docs/PortEntity.md)
 - [PortStatusDTO](nifi-docs/PortStatusDTO.md)
 - [PortStatusEntity](nifi-docs/PortStatusEntity.md)
 - [PortStatusSnapshotDTO](nifi-docs/PortStatusSnapshotDTO.md)
 - [PortStatusSnapshotEntity](nifi-docs/PortStatusSnapshotEntity.md)
 - [PositionDTO](nifi-docs/PositionDTO.md)
 - [PreviousValueDTO](nifi-docs/PreviousValueDTO.md)
 - [PrioritizerTypesEntity](nifi-docs/PrioritizerTypesEntity.md)
 - [ProcessGroupDTO](nifi-docs/ProcessGroupDTO.md)
 - [ProcessGroupEntity](nifi-docs/ProcessGroupEntity.md)
 - [ProcessGroupFlowDTO](nifi-docs/ProcessGroupFlowDTO.md)
 - [ProcessGroupFlowEntity](nifi-docs/ProcessGroupFlowEntity.md)
 - [ProcessGroupStatusDTO](nifi-docs/ProcessGroupStatusDTO.md)
 - [ProcessGroupStatusEntity](nifi-docs/ProcessGroupStatusEntity.md)
 - [ProcessGroupStatusSnapshotDTO](nifi-docs/ProcessGroupStatusSnapshotDTO.md)
 - [ProcessGroupStatusSnapshotEntity](nifi-docs/ProcessGroupStatusSnapshotEntity.md)
 - [ProcessGroupsEntity](nifi-docs/ProcessGroupsEntity.md)
 - [ProcessorConfigDTO](nifi-docs/ProcessorConfigDTO.md)
 - [ProcessorDTO](nifi-docs/ProcessorDTO.md)
 - [ProcessorEntity](nifi-docs/ProcessorEntity.md)
 - [ProcessorStatusDTO](nifi-docs/ProcessorStatusDTO.md)
 - [ProcessorStatusEntity](nifi-docs/ProcessorStatusEntity.md)
 - [ProcessorStatusSnapshotDTO](nifi-docs/ProcessorStatusSnapshotDTO.md)
 - [ProcessorStatusSnapshotEntity](nifi-docs/ProcessorStatusSnapshotEntity.md)
 - [ProcessorTypesEntity](nifi-docs/ProcessorTypesEntity.md)
 - [ProcessorsEntity](nifi-docs/ProcessorsEntity.md)
 - [PropertyDescriptorDTO](nifi-docs/PropertyDescriptorDTO.md)
 - [PropertyDescriptorEntity](nifi-docs/PropertyDescriptorEntity.md)
 - [PropertyHistoryDTO](nifi-docs/PropertyHistoryDTO.md)
 - [ProvenanceDTO](nifi-docs/ProvenanceDTO.md)
 - [ProvenanceEntity](nifi-docs/ProvenanceEntity.md)
 - [ProvenanceEventDTO](nifi-docs/ProvenanceEventDTO.md)
 - [ProvenanceEventEntity](nifi-docs/ProvenanceEventEntity.md)
 - [ProvenanceLinkDTO](nifi-docs/ProvenanceLinkDTO.md)
 - [ProvenanceNodeDTO](nifi-docs/ProvenanceNodeDTO.md)
 - [ProvenanceOptionsDTO](nifi-docs/ProvenanceOptionsDTO.md)
 - [ProvenanceOptionsEntity](nifi-docs/ProvenanceOptionsEntity.md)
 - [ProvenanceRequestDTO](nifi-docs/ProvenanceRequestDTO.md)
 - [ProvenanceResultsDTO](nifi-docs/ProvenanceResultsDTO.md)
 - [ProvenanceSearchableFieldDTO](nifi-docs/ProvenanceSearchableFieldDTO.md)
 - [QueueSizeDTO](nifi-docs/QueueSizeDTO.md)
 - [RegistryClientEntity](nifi-docs/RegistryClientEntity.md)
 - [RegistryClientsEntity](nifi-docs/RegistryClientsEntity.md)
 - [RegistryDTO](nifi-docs/RegistryDTO.md)
 - [RelationshipDTO](nifi-docs/RelationshipDTO.md)
 - [RemoteProcessGroupContentsDTO](nifi-docs/RemoteProcessGroupContentsDTO.md)
 - [RemoteProcessGroupDTO](nifi-docs/RemoteProcessGroupDTO.md)
 - [RemoteProcessGroupEntity](nifi-docs/RemoteProcessGroupEntity.md)
 - [RemoteProcessGroupPortDTO](nifi-docs/RemoteProcessGroupPortDTO.md)
 - [RemoteProcessGroupPortEntity](nifi-docs/RemoteProcessGroupPortEntity.md)
 - [RemoteProcessGroupStatusDTO](nifi-docs/RemoteProcessGroupStatusDTO.md)
 - [RemoteProcessGroupStatusEntity](nifi-docs/RemoteProcessGroupStatusEntity.md)
 - [RemoteProcessGroupStatusSnapshotDTO](nifi-docs/RemoteProcessGroupStatusSnapshotDTO.md)
 - [RemoteProcessGroupStatusSnapshotEntity](nifi-docs/RemoteProcessGroupStatusSnapshotEntity.md)
 - [RemoteProcessGroupsEntity](nifi-docs/RemoteProcessGroupsEntity.md)
 - [ReportingTaskDTO](nifi-docs/ReportingTaskDTO.md)
 - [ReportingTaskEntity](nifi-docs/ReportingTaskEntity.md)
 - [ReportingTaskTypesEntity](nifi-docs/ReportingTaskTypesEntity.md)
 - [ReportingTasksEntity](nifi-docs/ReportingTasksEntity.md)
 - [ResourceDTO](nifi-docs/ResourceDTO.md)
 - [ResourcesEntity](nifi-docs/ResourcesEntity.md)
 - [RevisionDTO](nifi-docs/RevisionDTO.md)
 - [ScheduleComponentsEntity](nifi-docs/ScheduleComponentsEntity.md)
 - [SearchResultsDTO](nifi-docs/SearchResultsDTO.md)
 - [SearchResultsEntity](nifi-docs/SearchResultsEntity.md)
 - [SnippetDTO](nifi-docs/SnippetDTO.md)
 - [SnippetEntity](nifi-docs/SnippetEntity.md)
 - [StartVersionControlRequestEntity](nifi-docs/StartVersionControlRequestEntity.md)
 - [StateEntryDTO](nifi-docs/StateEntryDTO.md)
 - [StateMapDTO](nifi-docs/StateMapDTO.md)
 - [StatusDescriptorDTO](nifi-docs/StatusDescriptorDTO.md)
 - [StatusHistoryDTO](nifi-docs/StatusHistoryDTO.md)
 - [StatusHistoryEntity](nifi-docs/StatusHistoryEntity.md)
 - [StatusSnapshotDTO](nifi-docs/StatusSnapshotDTO.md)
 - [StorageUsageDTO](nifi-docs/StorageUsageDTO.md)
 - [StreamingOutput](nifi-docs/StreamingOutput.md)
 - [SubmitReplayRequestEntity](nifi-docs/SubmitReplayRequestEntity.md)
 - [SystemDiagnosticsDTO](nifi-docs/SystemDiagnosticsDTO.md)
 - [SystemDiagnosticsEntity](nifi-docs/SystemDiagnosticsEntity.md)
 - [SystemDiagnosticsSnapshotDTO](nifi-docs/SystemDiagnosticsSnapshotDTO.md)
 - [TemplateDTO](nifi-docs/TemplateDTO.md)
 - [TemplateEntity](nifi-docs/TemplateEntity.md)
 - [TemplatesEntity](nifi-docs/TemplatesEntity.md)
 - [TenantDTO](nifi-docs/TenantDTO.md)
 - [TenantEntity](nifi-docs/TenantEntity.md)
 - [TenantsEntity](nifi-docs/TenantsEntity.md)
 - [ThePositionOfAComponentOnTheGraph](nifi-docs/ThePositionOfAComponentOnTheGraph.md)
 - [TransactionResultEntity](nifi-docs/TransactionResultEntity.md)
 - [UpdateControllerServiceReferenceRequestEntity](nifi-docs/UpdateControllerServiceReferenceRequestEntity.md)
 - [UriBuilder](nifi-docs/UriBuilder.md)
 - [UserDTO](nifi-docs/UserDTO.md)
 - [UserEntity](nifi-docs/UserEntity.md)
 - [UserGroupDTO](nifi-docs/UserGroupDTO.md)
 - [UserGroupEntity](nifi-docs/UserGroupEntity.md)
 - [UserGroupsEntity](nifi-docs/UserGroupsEntity.md)
 - [UsersEntity](nifi-docs/UsersEntity.md)
 - [VariableDTO](nifi-docs/VariableDTO.md)
 - [VariableEntity](nifi-docs/VariableEntity.md)
 - [VariableRegistryDTO](nifi-docs/VariableRegistryDTO.md)
 - [VariableRegistryEntity](nifi-docs/VariableRegistryEntity.md)
 - [VariableRegistryUpdateRequestDTO](nifi-docs/VariableRegistryUpdateRequestDTO.md)
 - [VariableRegistryUpdateRequestEntity](nifi-docs/VariableRegistryUpdateRequestEntity.md)
 - [VariableRegistryUpdateStepDTO](nifi-docs/VariableRegistryUpdateStepDTO.md)
 - [VersionControlComponentMappingEntity](nifi-docs/VersionControlComponentMappingEntity.md)
 - [VersionControlInformationDTO](nifi-docs/VersionControlInformationDTO.md)
 - [VersionControlInformationEntity](nifi-docs/VersionControlInformationEntity.md)
 - [VersionInfoDTO](nifi-docs/VersionInfoDTO.md)
 - [VersionedConnection](nifi-docs/VersionedConnection.md)
 - [VersionedControllerService](nifi-docs/VersionedControllerService.md)
 - [VersionedFlow](nifi-docs/VersionedFlow.md)
 - [VersionedFlowCoordinates](nifi-docs/VersionedFlowCoordinates.md)
 - [VersionedFlowDTO](nifi-docs/VersionedFlowDTO.md)
 - [VersionedFlowSnapshot](nifi-docs/VersionedFlowSnapshot.md)
 - [VersionedFlowSnapshotEntity](nifi-docs/VersionedFlowSnapshotEntity.md)
 - [VersionedFlowUpdateRequestDTO](nifi-docs/VersionedFlowUpdateRequestDTO.md)
 - [VersionedFlowUpdateRequestEntity](nifi-docs/VersionedFlowUpdateRequestEntity.md)
 - [VersionedFunnel](nifi-docs/VersionedFunnel.md)
 - [VersionedLabel](nifi-docs/VersionedLabel.md)
 - [VersionedPort](nifi-docs/VersionedPort.md)
 - [VersionedProcessGroup](nifi-docs/VersionedProcessGroup.md)
 - [VersionedProcessor](nifi-docs/VersionedProcessor.md)
 - [VersionedPropertyDescriptor](nifi-docs/VersionedPropertyDescriptor.md)
 - [VersionedRemoteGroupPort](nifi-docs/VersionedRemoteGroupPort.md)
 - [VersionedRemoteProcessGroup](nifi-docs/VersionedRemoteProcessGroup.md)


## Documentation For Authorization

 All endpoints do not require authorization.


## Author

dev@nifi.apache.org

