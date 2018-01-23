# AccessPolicy

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | **str** | The id of the policy. Set by server at creation time. | [optional] 
**resource** | **str** | The resource for this access policy. | [optional] 
**action** | **str** | The action associated with this access policy. | [optional] 
**configurable** | **bool** | Indicates if this access policy is configurable, based on which Authorizer has been configured to manage it. | [optional] 
**users** | [**list[Tenant]**](Tenant.md) | The set of user IDs associated with this access policy. | [optional] 
**user_groups** | [**list[Tenant]**](Tenant.md) | The set of user group IDs associated with this access policy. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


