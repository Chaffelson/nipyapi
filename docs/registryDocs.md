## Documentation for NiFi-Registry API Endpoints

All URIs are relative to *http://localhost/nifi-registry-api*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AccessApi* | [**create_access_token_by_trying_all_providers**](registry-docs/AccessApi.md#create_access_token_by_trying_all_providers) | **POST** /access/token | Creates a token for accessing the REST API via auto-detected method of verifying client identity claim credentials
*AccessApi* | [**create_access_token_using_form_login**](registry-docs/AccessApi.md#create_access_token_using_form_login) | **POST** /access/token/login | Creates a token for accessing the REST API via username/password
*AccessApi* | [**create_access_token_using_identity_provider_credentials**](registry-docs/AccessApi.md#create_access_token_using_identity_provider_credentials) | **POST** /access/token/identity-provider | Creates a token for accessing the REST API via a custom identity provider.
*AccessApi* | [**create_access_token_using_kerberos_ticket**](registry-docs/AccessApi.md#create_access_token_using_kerberos_ticket) | **POST** /access/token/kerberos | Creates a token for accessing the REST API via Kerberos Service Tickets or SPNEGO Tokens (which includes Kerberos Service Tickets)
*AccessApi* | [**get_access_status**](registry-docs/AccessApi.md#get_access_status) | **GET** /access | Returns the current client&#39;s authenticated identity and permissions to top-level resources
*AccessApi* | [**get_identity_provider_usage_instructions**](registry-docs/AccessApi.md#get_identity_provider_usage_instructions) | **GET** /access/token/identity-provider/usage | Provides a description of how the currently configured identity provider expects credentials to be passed to POST /access/token/identity-provider
*AccessApi* | [**test_identity_provider_recognizes_credentials_format**](registry-docs/AccessApi.md#test_identity_provider_recognizes_credentials_format) | **POST** /access/token/identity-provider/test | Tests the format of the credentials against this identity provider without preforming authentication on the credentials to validate them.
*BucketFlowsApi* | [**create_flow**](registry-docs/BucketFlowsApi.md#create_flow) | **POST** /buckets/{bucketId}/flows | Creates a flow
*BucketFlowsApi* | [**create_flow_version**](registry-docs/BucketFlowsApi.md#create_flow_version) | **POST** /buckets/{bucketId}/flows/{flowId}/versions | Creates the next version of a flow
*BucketFlowsApi* | [**delete_flow**](registry-docs/BucketFlowsApi.md#delete_flow) | **DELETE** /buckets/{bucketId}/flows/{flowId} | Deletes a flow.
*BucketFlowsApi* | [**get_flow**](registry-docs/BucketFlowsApi.md#get_flow) | **GET** /buckets/{bucketId}/flows/{flowId} | Gets a flow
*BucketFlowsApi* | [**get_flow_diff**](registry-docs/BucketFlowsApi.md#get_flow_diff) | **GET** /buckets/{bucketId}/flows/{flowId}/diff/{versionA}/{versionB} | Returns a list of differences between 2 versions of a flow
*BucketFlowsApi* | [**get_flow_version**](registry-docs/BucketFlowsApi.md#get_flow_version) | **GET** /buckets/{bucketId}/flows/{flowId}/versions/{versionNumber} | Gets the given version of a flow
*BucketFlowsApi* | [**get_flow_versions**](registry-docs/BucketFlowsApi.md#get_flow_versions) | **GET** /buckets/{bucketId}/flows/{flowId}/versions | Gets summary information for all versions of a flow. Versions are ordered newest-&gt;oldest.
*BucketFlowsApi* | [**get_flows**](registry-docs/BucketFlowsApi.md#get_flows) | **GET** /buckets/{bucketId}/flows | Gets all flows in the given bucket
*BucketFlowsApi* | [**get_latest_flow_version**](registry-docs/BucketFlowsApi.md#get_latest_flow_version) | **GET** /buckets/{bucketId}/flows/{flowId}/versions/latest | Get the latest version of a flow
*BucketFlowsApi* | [**get_latest_flow_version_metadata**](registry-docs/BucketFlowsApi.md#get_latest_flow_version_metadata) | **GET** /buckets/{bucketId}/flows/{flowId}/versions/latest/metadata | Get the metadata for the latest version of a flow
*BucketFlowsApi* | [**update_flow**](registry-docs/BucketFlowsApi.md#update_flow) | **PUT** /buckets/{bucketId}/flows/{flowId} | Updates a flow
*BucketsApi* | [**create_bucket**](registry-docs/BucketsApi.md#create_bucket) | **POST** /buckets | Creates a bucket
*BucketsApi* | [**delete_bucket**](registry-docs/BucketsApi.md#delete_bucket) | **DELETE** /buckets/{bucketId} | Deletes a bucket along with all objects stored in the bucket
*BucketsApi* | [**get_available_bucket_fields**](registry-docs/BucketsApi.md#get_available_bucket_fields) | **GET** /buckets/fields | Retrieves field names for searching or sorting on buckets.
*BucketsApi* | [**get_bucket**](registry-docs/BucketsApi.md#get_bucket) | **GET** /buckets/{bucketId} | Gets a bucket
*BucketsApi* | [**get_buckets**](registry-docs/BucketsApi.md#get_buckets) | **GET** /buckets | Gets all buckets
*BucketsApi* | [**update_bucket**](registry-docs/BucketsApi.md#update_bucket) | **PUT** /buckets/{bucketId} | Updates a bucket
*FlowsApi* | [**get_available_flow_fields**](registry-docs/FlowsApi.md#get_available_flow_fields) | **GET** /flows/fields | Retrieves the available field names that can be used for searching or sorting on flows.
*ItemsApi* | [**get_available_bucket_item_fields**](registry-docs/ItemsApi.md#get_available_bucket_item_fields) | **GET** /items/fields | Retrieves the available field names for searching or sorting on bucket items.
*ItemsApi* | [**get_items**](registry-docs/ItemsApi.md#get_items) | **GET** /items | Get items across all buckets
*ItemsApi* | [**get_items_in_bucket**](registry-docs/ItemsApi.md#get_items_in_bucket) | **GET** /items/{bucketId} | Gets items of the given bucket
*PoliciesApi* | [**create_access_policy**](registry-docs/PoliciesApi.md#create_access_policy) | **POST** /policies | Creates an access policy
*PoliciesApi* | [**get_access_policies**](registry-docs/PoliciesApi.md#get_access_policies) | **GET** /policies | Gets all access policies
*PoliciesApi* | [**get_access_policy**](registry-docs/PoliciesApi.md#get_access_policy) | **GET** /policies/{id} | Gets an access policy
*PoliciesApi* | [**get_access_policy_for_resource**](registry-docs/PoliciesApi.md#get_access_policy_for_resource) | **GET** /policies/{action}/{resource} | Gets an access policy for the specified action and resource
*PoliciesApi* | [**get_resources**](registry-docs/PoliciesApi.md#get_resources) | **GET** /policies/resources | Gets the available resources that support access/authorization policies
*PoliciesApi* | [**remove_access_policy**](registry-docs/PoliciesApi.md#remove_access_policy) | **DELETE** /policies/{id} | Deletes an access policy
*PoliciesApi* | [**update_access_policy**](registry-docs/PoliciesApi.md#update_access_policy) | **PUT** /policies/{id} | Updates a access policy
*TenantsApi* | [**create_user**](registry-docs/TenantsApi.md#create_user) | **POST** /tenants/users | Creates a user
*TenantsApi* | [**create_user_group**](registry-docs/TenantsApi.md#create_user_group) | **POST** /tenants/user-groups | Creates a user group
*TenantsApi* | [**get_user**](registry-docs/TenantsApi.md#get_user) | **GET** /tenants/users/{id} | Gets a user
*TenantsApi* | [**get_user_group**](registry-docs/TenantsApi.md#get_user_group) | **GET** /tenants/user-groups/{id} | Gets a user group
*TenantsApi* | [**get_user_groups**](registry-docs/TenantsApi.md#get_user_groups) | **GET** /tenants/user-groups | Gets all user groups
*TenantsApi* | [**get_users**](registry-docs/TenantsApi.md#get_users) | **GET** /tenants/users | Gets all users
*TenantsApi* | [**remove_user**](registry-docs/TenantsApi.md#remove_user) | **DELETE** /tenants/users/{id} | Deletes a user
*TenantsApi* | [**remove_user_group**](registry-docs/TenantsApi.md#remove_user_group) | **DELETE** /tenants/user-groups/{id} | Deletes a user group
*TenantsApi* | [**update_user**](registry-docs/TenantsApi.md#update_user) | **PUT** /tenants/users/{id} | Updates a user
*TenantsApi* | [**update_user_group**](registry-docs/TenantsApi.md#update_user_group) | **PUT** /tenants/user-groups/{id} | Updates a user group


## Documentation For NiFi-Registry Models

 - [AccessPolicy](registry-docs/AccessPolicy.md)
 - [AccessPolicySummary](registry-docs/AccessPolicySummary.md)
 - [BatchSize](registry-docs/BatchSize.md)
 - [Bucket](registry-docs/Bucket.md)
 - [BucketItem](registry-docs/BucketItem.md)
 - [Bundle](registry-docs/Bundle.md)
 - [ConnectableComponent](registry-docs/ConnectableComponent.md)
 - [ControllerServiceAPI](registry-docs/ControllerServiceAPI.md)
 - [CurrentUser](registry-docs/CurrentUser.md)
 - [Fields](registry-docs/Fields.md)
 - [Link](registry-docs/Link.md)
 - [Permissions](registry-docs/Permissions.md)
 - [Resource](registry-docs/Resource.md)
 - [ResourcePermissions](registry-docs/ResourcePermissions.md)
 - [Tenant](registry-docs/Tenant.md)
 - [ThePositionOfAComponentOnTheGraph](registry-docs/ThePositionOfAComponentOnTheGraph.md)
 - [UriBuilder](registry-docs/UriBuilder.md)
 - [User](registry-docs/User.md)
 - [UserGroup](registry-docs/UserGroup.md)
 - [VersionedConnection](registry-docs/VersionedConnection.md)
 - [VersionedControllerService](registry-docs/VersionedControllerService.md)
 - [VersionedFlow](registry-docs/VersionedFlow.md)
 - [VersionedFlowCoordinates](registry-docs/VersionedFlowCoordinates.md)
 - [VersionedFlowSnapshot](registry-docs/VersionedFlowSnapshot.md)
 - [VersionedFlowSnapshotMetadata](registry-docs/VersionedFlowSnapshotMetadata.md)
 - [VersionedFunnel](registry-docs/VersionedFunnel.md)
 - [VersionedLabel](registry-docs/VersionedLabel.md)
 - [VersionedPort](registry-docs/VersionedPort.md)
 - [VersionedProcessGroup](registry-docs/VersionedProcessGroup.md)
 - [VersionedProcessor](registry-docs/VersionedProcessor.md)
 - [VersionedPropertyDescriptor](registry-docs/VersionedPropertyDescriptor.md)
 - [VersionedRemoteGroupPort](registry-docs/VersionedRemoteGroupPort.md)
 - [VersionedRemoteProcessGroup](registry-docs/VersionedRemoteProcessGroup.md)


## Documentation For Authorization

 All endpoints do not require authorization.


## Author

dev@nifi.apache.org

