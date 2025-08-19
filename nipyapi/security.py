# pylint: disable=C0302
"""
Secure connectivity management for NiPyApi
"""

import logging
import ssl
from copy import copy
import urllib3
import requests
import nipyapi

log = logging.getLogger(__name__)


__all__ = [
    "create_service_user",
    "create_service_user_group",
    "set_service_auth_token",
    "service_logout",
    "get_service_access_status",
    "add_user_to_access_policy",
    "update_access_policy",
    "get_access_policy_for_resource",
    "create_access_policy",
    "list_service_users",
    "get_service_user",
    "set_service_ssl_context",
    "add_user_group_to_access_policy",
    "bootstrap_security_policies",
    "service_login",
    "service_login_oidc",
    "remove_service_user",
    "list_service_user_groups",
    "get_service_user_group",
    "remove_service_user_group",
]

# These are the known-valid policy actions
_valid_actions = ["read", "write", "delete"]
# These are the services that these functions know how to configure
_valid_services = ["nifi", "registry"]


def list_service_users(service="nifi"):
    """Lists all users of a given service, takes a service name as a string"""
    assert service in _valid_services
    with nipyapi.utils.rest_exceptions():
        out = getattr(nipyapi, service).TenantsApi().get_users()
    if service == "nifi":
        return out.users
    return out


def get_service_user(identifier, identifier_type="identity", service="nifi"):
    """
    Gets the unique user matching to the given identifier and type.

    Args:
        identifier (str): the string to search for
        identifier_type (str): the field to search in
        service (str): the name of the service

    Returns:
        None if no match, else single object

    """
    assert service in _valid_services
    assert isinstance(identifier, str)
    assert isinstance(identifier_type, str)
    obj = list_service_users(service)
    out = nipyapi.utils.filter_obj(obj, identifier, identifier_type,
                                   greedy=False)
    return out


def remove_service_user(user, service="nifi", strict=True):
    """
    Removes a given User from the given Service

    Args:
        user: [(nifi.UserEntity), (registry.User)] Target User object
        service (str): 'nifi' or 'registry'
        strict (bool): Whether to throw an error if User not found

    Returns:
        Updated User Entity or None
    """
    assert service in _valid_services
    if service == "registry":
        assert isinstance(user, nipyapi.registry.User)
        submit = {"id": user.identifier, "version": user.revision.version}
    else:
        assert isinstance(user, nipyapi.nifi.UserEntity)
        submit = {"id": user.id, "version": user.revision.version}
    assert isinstance(strict, bool)
    try:
        return getattr(nipyapi, service).TenantsApi().remove_user(**submit)
    except getattr(nipyapi, service).rest.ApiException as e:
        if "Unable to find user" in e.body or "does not exist" in e.body:
            if not strict:
                return None
        raise ValueError(e.body) from e


def create_service_user(identity, service="nifi", strict=True):
    """
    Attempts to create a user with the provided identity in the given service

    Args:
        identity (str): Identity string for the user
        service (str): 'nifi' or 'registry'
        strict (bool): If Strict, will error if user already exists

    Returns:
        The new (User) or (UserEntity) object

    """
    assert service in _valid_services
    assert isinstance(identity, str)
    assert isinstance(strict, bool)
    if service == "registry":
        user_obj = nipyapi.registry.User(identity=identity)
    else:
        # must be nifi
        user_obj = nipyapi.nifi.UserEntity(
            revision=nipyapi.nifi.RevisionDTO(version=0),
            component=nipyapi.nifi.UserDTO(identity=identity),
        )
    try:
        return getattr(nipyapi, service).TenantsApi().create_user(user_obj)
    except (nipyapi.nifi.rest.ApiException,
            nipyapi.registry.rest.ApiException) as e:
        if "already exists" in e.body and not strict:
            return get_service_user(identity, service=service)
        raise ValueError(e.body) from e


def create_service_user_group(identity, service="nifi", users=None,
                              strict=True):
    """
    Attempts to create a user with the provided identity and member users in
    the given service

    Args:
        identity (str): Identity string for the user group
        service (str): 'nifi' or 'registry'
        users (list): A list of nifi.UserEntity or registry.User
          belonging to the group
        strict (bool): Whether to throw an error on already exists

    Returns:
        The new (UserGroup) or (UserGroupEntity) object

    """
    assert service in _valid_services
    assert isinstance(identity, str)

    users_ids = None

    if service == "nifi":
        if users:
            assert all(isinstance(user, nipyapi.nifi.UserEntity)
                       for user in users)
            users_ids = [{"id": user.id} for user in users]
        user_group_obj = nipyapi.nifi.UserGroupEntity(
            revision=nipyapi.nifi.RevisionDTO(version=0),
            component=nipyapi.nifi.UserGroupDTO(identity=identity,
                                                users=users_ids),
        )
    else:
        if users:
            assert all(isinstance(user, nipyapi.registry.User)
                       for user in users)
            users_ids = [{"identifier": user.identifier} for user in users]
        user_group_obj = nipyapi.registry.UserGroup(identity=identity,
                                                    users=users_ids)
    try:
        return getattr(nipyapi, service).TenantsApi().create_user_group(
            user_group_obj)
    except (nipyapi.nifi.rest.ApiException,
            nipyapi.registry.rest.ApiException) as e:
        if "already exists" in e.body:
            if not strict:
                return get_service_user_group(identity, service=service)
        raise ValueError(e.body) from e


def list_service_user_groups(service="nifi"):
    """
    Returns list of service user groups for a given service
    Args:
        service (str): 'nifi' or 'registry'

    Returns:
        [(nifi.UserGroupEntity, registry.UserGroup)]

    """
    assert service in _valid_services
    with nipyapi.utils.rest_exceptions():
        out = getattr(nipyapi, service).TenantsApi().get_user_groups()
    if service == "nifi":
        return out.user_groups
    return out


def get_service_user_group(identifier, identifier_type="identity",
                           service="nifi"):
    """
    Gets the unique group matching to the given identifier and type.

    Args:
        identifier (str): the string to search for
        identifier_type (str): the field to search in, identity or id
        service (str): the name of the service

    Returns:
        None if no match, else single object

    """
    assert service in _valid_services
    assert isinstance(identifier, str)
    assert isinstance(identifier_type, str)
    obj = list_service_user_groups(service)
    out = nipyapi.utils.filter_obj(obj, identifier, identifier_type,
                                   greedy=False)
    return out


def remove_service_user_group(group, service="nifi", strict=True):
    """
    Removes a given User Group from the given Service

    Args:
        group: [(nifi.UserEntity), (registry.User)] Target User object
        service (str): 'nifi' or 'registry'
        strict (bool): Whether to throw an error if User not found

    Returns:
        Updated User Group or None
    """
    assert service in _valid_services
    if service == "registry":
        assert isinstance(group, nipyapi.registry.UserGroup)
        submit = {"id": group.identifier, "version": group.revision.version}
    else:
        assert isinstance(group, nipyapi.nifi.UserGroupEntity)
        submit = {"id": group.id, "version": group.revision.version}
    assert isinstance(strict, bool)
    try:
        return getattr(nipyapi, service).TenantsApi().remove_user_group(
            **submit)
    except getattr(nipyapi, service).rest.ApiException as e:
        if "Unable to find user" in e.body or "does not exist" in e.body:
            if not strict:
                return None
        raise ValueError(e.body) from e


def service_login(service="nifi", username=None, password=None,
                  bool_response=False):
    """
    Login to the currently configured NiFi or NiFi-Registry server.

    Login requires a secure connection over https.
    Prior to calling this method, the host must be specified
    and the SSLContext should be configured (if necessary).

    Successful login will result in a generated token (JWT) being
    cached in the api_client config that will be passed in all future
    REST API calls. To clear that token, call service_logout.

    The token is temporary and will expire after a duration set by
    the server. After a token expires, you must call
    this method again to generate a new token.

    Args:
        service (str): 'nifi' or 'registry'; the service to login to
        username (str): The username to submit
        password (str): The password to use
        bool_response (bool): If True, the function will return False instead
            of an error. Useful for connection testing.

    Returns:
        (bool): True if successful, False or an Error if not. See bool_response

    """
    log_args = locals()
    log_args["password"] = "REDACTED"
    log.info("Called service_login with args %s", log_args)
    assert service in _valid_services
    assert username is None or isinstance(username, str)
    assert password is None or isinstance(password, str)
    assert isinstance(bool_response, bool)

    configuration = getattr(nipyapi, service).configuration
    assert configuration.host, "Host must be set prior to logging in."
    assert configuration.host.startswith(
        "https"
    ), "Login is only available when connecting over HTTPS."
    default_pword = getattr(nipyapi.config, "default_" + service + "_password", None)
    default_uname = getattr(nipyapi.config, "default_" + service + "_username", None)
    # Prefer explicitly provided credentials, then configuration-set creds, then deprecated defaults
    cfg_uname = getattr(configuration, 'username', None)
    cfg_pword = getattr(configuration, 'password', None)
    uname = (username if username is not None
             else (copy(cfg_uname) if cfg_uname else copy(default_uname)))
    pword = (password if password is not None
             else (copy(cfg_pword) if cfg_pword else copy(default_pword)))
    assert pword, "Password must be set or in default config"
    assert uname, "Username must be set or in default config"
    # set username/password in configuration for initial login
    # Registry pulls from config, NiFi allows submission
    configuration.username = uname
    configuration.password = pword
    log.info(
        "Attempting bearerAuth login with user identity [%s]",
        configuration.username
    )
    try:
        if service == "nifi":
            token = nipyapi.nifi.AccessApi().create_access_token(
                username=uname, password=pword
            )
            set_service_auth_token(token=token, service=service)
            return True
        # else:
        token = (
            nipyapi.registry.AccessApi()
            .create_access_token_using_basic_auth_credentials()
        )
        set_service_auth_token(token=token, service=service)
        return True
    except getattr(nipyapi, service).rest.ApiException as e:
        if bool_response:
            return False
        raise ValueError(e.body) from e


# pylint: disable=too-many-arguments,too-many-positional-arguments
def service_login_oidc(service="nifi", username=None, password=None,
                       oidc_token_endpoint=None, client_id=None, client_secret=None,
                       bool_response=False, return_token_info=False):
    """
    Login to NiFi using OpenID Connect (OIDC) OAuth2 password flow.

    This method acquires an access token from an OIDC provider using the
    OAuth2 Resource Owner Password Credentials flow (RFC 6749) and configures
    the service to use bearer token authentication.
    NiFi does not currently provide native methods for OIDC authentication.

    Args:
        service (str): 'nifi' or 'registry'; the service to login to
            (currently only 'nifi' supports OIDC)
        username (str): The username to submit to the OIDC provider
        password (str): The password to use with the OIDC provider
        oidc_token_endpoint (str): The OIDC token endpoint URL
            (e.g., 'http://localhost:8080/realms/nipyapi/protocol/openid-connect/token')
        client_id (str): The OIDC client ID
        client_secret (str): The OIDC client secret
        bool_response (bool): If True, the function will return False instead
            of an error. Useful for connection testing.
        return_token_info (bool): If True, return the full OAuth2 token response
            instead of just a boolean. Useful for extracting user identity information.

    Returns:
        (bool or dict): True if successful (default), False if bool_response=True and failed,
            or full OAuth2 token response dict if return_token_info=True.
            See bool_response and return_token_info.

    """
    log_args = locals()
    log_args["password"] = "REDACTED"
    log_args["client_secret"] = "REDACTED"
    log.info("Called service_login_oidc with args %s", log_args)

    assert service in _valid_services
    assert username is None or isinstance(username, str)
    assert password is None or isinstance(password, str)
    assert oidc_token_endpoint is None or isinstance(oidc_token_endpoint, str)
    assert client_id is None or isinstance(client_id, str)
    assert client_secret is None or isinstance(client_secret, str)
    assert isinstance(bool_response, bool)

    if service == "registry":
        raise ValueError("OIDC authentication is not supported for Registry service")

    # Validate required parameters
    if not all([username, password, oidc_token_endpoint, client_id, client_secret]):
        raise ValueError(
            "OIDC login requires username, password, oidc_token_endpoint, "
            "client_id, and client_secret"
        )

    try:
        token_response = requests.post(
            oidc_token_endpoint,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30,
            data={
                'grant_type': 'password',
                'client_id': client_id,
                'client_secret': client_secret,
                'username': username,
                'password': password
            }
        )

        if token_response.status_code == 200:
            token_data = token_response.json()
            access_token = token_data['access_token']
            set_service_auth_token(token=access_token, service=service)

            if return_token_info:
                return token_data
            return True

        if bool_response:
            return False
        raise ValueError(
            f"OIDC token acquisition failed: {token_response.status_code} {token_response.text}"
        )

    except Exception as e:
        if bool_response:
            return False
        raise ValueError(f"OIDC authentication error: {e}") from e


def set_service_auth_token(token=None, token_name="bearerAuth", service="nifi"):
    """
    Helper method to set the auth token correctly for the specified service

    Args:
        token (Optional[str]): The token to set. Defaults to None.
        token_name (str): the api_key field name to set the token to. Defaults
            to 'bearerAuth'
        service (str): 'nifi' or 'registry', the service to set

    Returns:
        (bool): True on success, False if token not set
    """
    assert service in _valid_services
    assert isinstance(token_name, str)
    assert token is None or isinstance(token, str)
    if service == "registry":
        configuration = nipyapi.config.registry_config
    else:
        configuration = nipyapi.config.nifi_config
    if token:
        configuration.api_key[token_name] = token
        configuration.api_key_prefix[token_name] = "Bearer"
    else:
        # If not token, then assume we are doing logout and cleanup
        if token_name in configuration.api_key:
            configuration.api_key.pop(token_name)
    if token_name not in configuration.api_key:
        return False
    return True


def service_logout(service="nifi"):
    """
    Logs out from the service by resetting the token
    Args:
        service (str): 'nifi' or 'registry'; the target service

    Returns:
        (bool): True of access removed, False if still set

    """
    assert service in _valid_services
    set_service_auth_token(token=None, service=service)
    try:
        status = get_service_access_status(service, bool_response=True)
    except ValueError as e:
        if "Cannot set verify_mode to CERT_NONE" in str(e):
            status = None
            # Logout throws error with incorrect ssl setup
        else:
            raise e
    if not status:
        return True
    return False


def get_service_access_status(service="nifi", bool_response=False):
    """
    Gets the access status for the current session

    Args:
        service (str): A String of 'nifi' or 'registry' to indicate which
            service to check status for
        bool_response (bool): If True, the function will return False on
            hitting an Error instead of raising it. Useful for connection
            testing.

    Returns:
        (bool) if bool_response, else the Service Access Status of the User
    """
    log.info("Called get_service_access_status with args %s", locals())
    assert service in _valid_services
    assert isinstance(bool_response, bool)
    if bool_response:
        # Assume we are using this as a connection test and therefore disable
        # the Warnings urllib3 will shower us with
        log.debug("- bool_response is True, disabling urllib3 warnings")
        logging.getLogger("urllib3").setLevel(logging.ERROR)
    try:
        # NiFi 2.x: use FlowApi.get_current_user() as status check
        if service == "nifi":
            return nipyapi.nifi.FlowApi().get_current_user()
        # Registry 2.x: use AboutApi.get_version() as a benign reachability check
        # This does not assert auth, but serves as a health/status probe
        return nipyapi.registry.AboutApi().get_version()
    except AttributeError as e:
        # NiFi 2.x removed AccessApi.get_access_status; treat as unavailable
        log.debug("AccessApi.get_access_status not available: %s", e)
        if bool_response:
            return False
        raise
    except urllib3.exceptions.MaxRetryError as e:
        log.debug("- Caught exception %s", type(e))
        if bool_response:
            log.debug(
                "Connection failed with error %s and bool_response is "
                "True, returning False",
                e,
            )
            return False
        log.debug("- bool_response is False, raising Exception")
        raise e
    except getattr(nipyapi, service).rest.ApiException as e:
        expected_errors = [
            "Authentication object was not found",
            "only supported when running over HTTPS",
        ]
        if any(x in e.body for x in expected_errors):
            if bool_response:
                return False
            raise e


def add_user_to_access_policy(user, policy, service="nifi", refresh=True,
                              strict=True):
    """
    Attempts to add the given user object to the given access policy

    Args:
        user (User) or (UserEntity): User object to add
        policy (AccessPolicyEntity) or (AccessPolicy): Access Policy object
        service (str): 'nifi' or 'registry' to identify the target service
        refresh (bool): Whether to refresh the policy object before submit
        strict (bool): If True, will return error if user already present,
          if False will ignore the already exists

    Returns:
        Updated Policy object

    """
    assert service in _valid_services
    assert isinstance(
        policy,
        (
            nipyapi.registry.AccessPolicy
            if service == "registry"
            else nipyapi.nifi.AccessPolicyEntity
        ),
    )
    assert isinstance(
        user,
        nipyapi.registry.User if service == "registry"
        else nipyapi.nifi.UserEntity,
    )

    user_id = user.id if service == "nifi" else user.identifier

    if refresh:
        policy_tgt = (
            getattr(nipyapi, service)
            .PoliciesApi()
            .get_access_policy(policy.id if service == "nifi"
                               else policy.identifier)
        )
    else:
        policy_tgt = policy

    assert isinstance(
        policy_tgt,
        (
            nipyapi.registry.AccessPolicy
            if service == "registry"
            else nipyapi.nifi.AccessPolicyEntity
        ),
    )

    policy_users = (
        policy_tgt.users if service == "registry"
        else policy_tgt.component.users
    )
    policy_user_ids = [
        i.identifier if service == "registry" else i.id for i in policy_users
    ]
    # Add concise debug context to help trace registry bootstrap activity
    try:
        pol_resource = getattr(policy_tgt, "resource", None)
        pol_action = getattr(policy_tgt, "action", None)
        if pol_resource is None and hasattr(policy_tgt, "component"):
            pol_resource = getattr(policy_tgt.component, "resource", None)
            pol_action = getattr(policy_tgt.component, "action", None)
    except Exception:  # pylint: disable=broad-exception-caught  # best-effort logging only
        pol_resource = None
        pol_action = None
    if user_id not in policy_user_ids:
        log.info(
            "add_user_to_access_policy: service=%s action=%s resource=%s add user=%s",
            service, pol_action, pol_resource, getattr(user, "identity", user_id)
        )
        if service == "registry":
            policy_tgt.users.append(user)
        elif service == "nifi":
            policy_tgt.component.users.append({"id": user_id})

        return nipyapi.security.update_access_policy(policy_tgt, service)
    if strict and user_id in policy_user_ids:
        raise ValueError("Strict is True and User ID already in Policy")


def add_user_group_to_access_policy(user_group, policy, service="nifi",
                                    refresh=True):
    """
    Attempts to add the given user group object to the given access policy

    Args:
        user_group (UserGroup) or (UserGroupEntity): User group object to add
        policy (AccessPolicyEntity) or (AccessPolicy): Access Policy object
        service (str): 'nifi' or 'registry' to identify the target service
        refresh (bool): Whether to refresh the policy object before submission

    Returns:
        Updated Policy object

    """
    assert service in _valid_services
    assert isinstance(
        policy,
        (
            nipyapi.registry.AccessPolicy
            if service == "registry"
            else nipyapi.nifi.AccessPolicyEntity
        ),
    )
    assert isinstance(
        user_group,
        (
            nipyapi.registry.UserGroup
            if service == "registry"
            else nipyapi.nifi.UserGroupEntity
        ),
    )
    user_group_id = (
        user_group.id if service == "nifi" else user_group.identifier
    )

    if refresh:
        policy_tgt = (
            getattr(nipyapi, service)
            .PoliciesApi()
            .get_access_policy(policy.id if service == "nifi"
                               else policy.identifier)
        )
    else:
        policy_tgt = policy

    assert isinstance(
        policy_tgt,
        (
            nipyapi.registry.AccessPolicy
            if service == "registry"
            else nipyapi.nifi.AccessPolicyEntity
        ),
    )

    policy_user_groups = (
        policy_tgt.users if service == "registry"
        else policy_tgt.component.user_groups
    )
    policy_user_group_ids = [
        i.identifier if service == "registry" else i.id
        for i in policy_user_groups
    ]

    assert user_group_id not in policy_user_group_ids

    if service == "registry":
        policy_tgt.user_groups.append(user_group)
    elif service == "nifi":
        policy_tgt.component.user_groups.append({"id": user_group_id})

    return nipyapi.security.update_access_policy(policy_tgt, service)


def update_access_policy(policy, service="nifi"):
    """
    Applies an updated access policy to the service indicated

    Args:
        policy (PolicyEntity): The policy object to submit
        service (str): 'nifi' or 'registry' to indicate the target service

    Returns:
        (PolicyEntity): The updated policy if successful

    """
    assert service in _valid_services
    assert isinstance(
        policy,
        (
            nipyapi.registry.AccessPolicy
            if service == "registry"
            else nipyapi.nifi.AccessPolicyEntity
        ),
    ), "Policy type {0} not valid.".format(type(policy))
    with nipyapi.utils.rest_exceptions():
        return (
            getattr(nipyapi, service)
            .PoliciesApi()
            .update_access_policy(
                id=policy.id if service == "nifi" else policy.identifier,
                body=policy
            )
        )


def get_access_policy_for_resource(
    resource, action, r_id=None, service="nifi", auto_create=False
):
    """
    Attempts to retrieve the access policy for a given resource and action,
    and optionally resource_id if targeting NiFi. Optionally creates the policy
    if it doesn't already exist

    Args:
        resource (str): A valid resource in the target service
        action (str): A valid action, typically 'read', 'write' or 'delete'
        r_id (Optional[str]): The UUID of the resource, valid only if targeting
            NiFi resources
        service (str): Which service to target, typically 'nifi' or 'registry'
        auto_create (bool): Whether to create the targeted policy if it doesn't
            already exist

    Returns:
        The relevant AccessPolicy object

    """
    assert service in _valid_services
    assert action in _valid_actions
    assert r_id is None or isinstance(r_id, str)
    assert isinstance(resource, str)
    assert isinstance(auto_create, bool)
    log.info("Called get_access_policy_for_resource with Args %s", locals())

    # Strip leading '/' from resource as lookup endpoint prepends a '/'
    resource = resource[1:] if resource.startswith("/") else resource
    log.info("Getting %s Policy for %s:%s:%s", service, action, resource,
             str(r_id))
    if service == "nifi":
        pol_api = nipyapi.nifi.PoliciesApi()
    else:
        pol_api = nipyapi.registry.PoliciesApi()
    try:
        nipyapi.utils.bypass_slash_encoding(service, True)
        response = pol_api.get_access_policy_for_resource(
            action=action,
            resource="/".join([resource, r_id]) if r_id else resource
        )
        nipyapi.utils.bypass_slash_encoding(service, False)
        return response
    except (nipyapi.nifi.rest.ApiException, nipyapi.registry.rest.ApiException) as e:
        if any(
            pol_string in e.body
            for pol_string in [
                "Unable to find access policy",
                "No policy found",
                "No access policy found",
            ]
        ):
            log.info("Access policy not found")
            if not auto_create:
                return None
            return nipyapi.security.create_access_policy(
                resource, action, r_id, service
            )
        log.info("Unexpected Error, raising...")
        raise ValueError(e.body) from e
    finally:
        nipyapi.utils.bypass_slash_encoding(service, False)


def create_access_policy(resource, action, r_id=None, service="nifi"):
    """
    Creates an access policy for the given resource, action and optionally
    resource_id for NiFi.

    Args:
        resource (str): a valid resource type for this service, e.g. 'bucket'
        action (str): a valid action type for this service, typically 'read',
            'write' or 'delete'
        r_id (optional[str]): if NiFi, the resource ID of the resource
        service (str): the service to target

    Returns:
        An access policy object for that service

    """
    assert isinstance(resource, str)
    assert action in _valid_actions
    assert r_id is None or isinstance(r_id, str)
    assert service in _valid_services
    if resource[0] != "/":
        r = "/" + resource
    else:
        r = resource
    with nipyapi.utils.rest_exceptions():
        if service == "nifi":
            return nipyapi.nifi.PoliciesApi().create_access_policy(
                body=nipyapi.nifi.AccessPolicyEntity(
                    revision=nipyapi.nifi.RevisionDTO(version=0),
                    component=nipyapi.nifi.AccessPolicyDTO(
                        action=action,
                        resource="/".join([r, r_id]) if r_id else r
                    ),
                )
            )
        # elif service == 'registry':
        return nipyapi.registry.PoliciesApi().create_access_policy(
            body=nipyapi.registry.AccessPolicy(action=action, resource=r)
        )


# pylint: disable=R0913, R0917
def set_service_ssl_context(
    service="nifi",
    ca_file=None,
    client_cert_file=None,
    client_key_file=None,
    client_key_password=None,
    check_hostname=None,
    purpose=None,
):
    """
    Create an SSLContext for connecting over https to a secured NiFi or
    NiFi-Registry instance.

    This method can be used to create an SSLContext for
    two-way TLS in which a client cert is used by the service to authenticate
    the client.

    This method can also be used for one-way TLS in which the client
    verifies the server's certificate, but authenticates using a
    different form of credentials, such as LDAP username/password.

    If you are using one-way TLS with a certificate signed by a
    root CA trusted by your system/platform, this step is not
    necessary as the default TLS-handshake should "just work."

    Args:
        service (str): 'nifi' or 'registry' to indicate which service
            config to set the ssl context to
        ca_file (str): A PEM file containing certs for the root CA(s)
            for the NiFi Registry server
        client_cert_file (str): A PEM file containing the public
            certificates for the user/client identity
        client_key_file (str): An encrypted (password-protected) PEM file
            containing the client's secret key
        client_key_password (str): The password to decrypt the client_key_file
        check_hostname (bool): Enable or Disable hostname checking
        purpose (ssl.Purpose): The purpose of the SSLContext

    Returns:
        (None)
    """
    assert service in ["nifi", "registry"]
    ssl_context = ssl.create_default_context(
        purpose=purpose or ssl.Purpose.SERVER_AUTH
        )
    if client_cert_file is not None and client_key_file is not None:
        try:
            ssl_context.load_cert_chain(
                certfile=client_cert_file,
                keyfile=client_key_file,
                password=client_key_password,
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "Unable to read keyfile {0} or certfile {1}".format(
                    client_key_file, client_cert_file
                )
            ) from e
        except ssl.SSLError as e:
            if e.errno == 9:
                raise ssl.SSLError(
                    "This error possibly pertains to a mis-typed or "
                    "incorrect key password"
                ) from e

    if ca_file is not None:
        ssl_context.load_verify_locations(cafile=ca_file)

    if check_hostname is not None:
        ssl_context.check_hostname = check_hostname
    else:
        ssl_context.check_hostname = nipyapi.config.global_ssl_host_check

    if service == "registry":
        nipyapi.config.registry_config.ssl_context = ssl_context
    elif service == "nifi":
        nipyapi.config.nifi_config.ssl_context = ssl_context


# pylint: disable=W0702,R0912,r0914,R0915
def bootstrap_security_policies(
        service, user_identity=None, group_identity=None, nifi_proxy_identity=None):
    """Creates a default security context within NiFi or Nifi-Registry.

    Args:
        service (str): The service to configure security for ('nifi' or 'registry')
        user_identity (nipyapi.nifi.UserEntity or nipyapi.registry.User, optional):
            User identity to apply policies to
        group_identity (nipyapi.nifi.UserGroupEntity or nipyapi.registry.UserGroup, optional):
            Group identity to apply policies to

    Returns:
        None
    """
    assert service in _valid_services, "service not in %s" % _valid_services
    valid_ident_obj = [nipyapi.nifi.UserEntity, nipyapi.registry.User]
    if user_identity is not None:
        assert type(user_identity) in valid_ident_obj

    if "nifi" in service:
        rpg_id = nipyapi.canvas.get_root_pg_id()
        if user_identity is None and group_identity is None:
            # Prefer currently authenticated user for policy bootstrapping
            current_user = nipyapi.nifi.FlowApi().get_current_user()
            current_identity = None
            if current_user and not getattr(current_user, 'anonymous', True):
                current_identity = current_user.identity
            # Resolve or create a NiFi user entity for the current identity
            nifi_user_identity = None
            if current_identity:
                nifi_user_identity = nipyapi.security.get_service_user(
                    current_identity, service="nifi"
                )
                if not nifi_user_identity:
                    # Ensure a user entity exists to attach policies
                    nifi_user_identity = nipyapi.security.create_service_user(
                        identity=current_identity, service="nifi", strict=False
                    )
            # If no current identity could be resolved, skip attaching a default
            # identity here. Callers should pass explicit identities.
            if not nifi_user_identity:
                log.warning(
                    "bootstrap_nifi: no current user identity resolved; "
                    "skipping user policy attachment"
                )
        else:
            nifi_user_identity = user_identity

        access_policies = [
            ("write", "process-groups", rpg_id),
            ("read", "process-groups", rpg_id),
            ("write", "data/process-groups", rpg_id),
            ("read", "data/process-groups", rpg_id),
            ("read", "system", None),
            ("read", "system-diagnostics", None),
            ("read", "policies", None),
            ("read", "controller", None),
            ("write", "controller", None),
        ]
        for pol in access_policies:
            ap = nipyapi.security.get_access_policy_for_resource(
                action=pol[0],
                resource=pol[1],
                r_id=pol[2],
                service="nifi",
                auto_create=True,
            )
            if nifi_user_identity is None:
                # I should not rely upon a try/catch there
                # but it's the simplest way (I just hope it won't
                # break the server :-) )
                try:
                    nipyapi.security.add_user_group_to_access_policy(
                        user_group=group_identity,
                        policy=ap,
                        service="nifi"
                    )
                except:  # noqa
                    pass
            else:
                nipyapi.security.add_user_to_access_policy(
                    user=nifi_user_identity,
                    policy=ap,
                    service="nifi",
                    strict=False
                )
    else:
        log.info("bootstrap_security_policies: starting registry bootstrap")
        # Respect explicit caller-provided identity only; do not guess defaults here
        if user_identity is None and group_identity is None:
            reg_user_identity = None
        else:
            reg_user_identity = user_identity
        if reg_user_identity:
            log.info(
                "bootstrap_registry: resolved reg_user_identity=%s",
                getattr(reg_user_identity, "identity", None),
            )

        try:
            all_buckets_access_policies = [
                ("read", "/buckets"),
                ("write", "/buckets"),
                ("delete", "/buckets"),
            ]
            for action, resource in all_buckets_access_policies:
                pol = nipyapi.security.get_access_policy_for_resource(
                    resource=resource,
                    action=action,
                    service="registry",
                    auto_create=True
                )
                log.info(
                    "bootstrap_registry: ensure policy action=%s resource=%s id=%s",
                    action, resource, getattr(pol, "identifier", None),
                )
                if reg_user_identity is None:
                    if group_identity:  # Only try to add group if it exists
                        nipyapi.security.add_user_group_to_access_policy(
                            user_group=group_identity,
                            policy=pol,
                            service="registry"
                        )
                else:
                    nipyapi.security.add_user_to_access_policy(
                        user=reg_user_identity,
                        policy=pol,
                        service="registry",
                        strict=False
                    )
        except Exception as e:  # pylint: disable=broad-exception-caught
            log.warning("Registry bucket policy bootstrap skipped due to error: %s", e)
        # Setup Proxy Access for NiFi's TLS client identity if provided
        if nifi_proxy_identity:
            log.info(
                "bootstrap_registry: ensuring proxy DN=%s user and policies",
                nifi_proxy_identity,
            )
            nifi_proxy_user = nipyapi.security.create_service_user(
                identity=nifi_proxy_identity,
                service="registry",
                strict=False
            )
            # Grant global buckets read/write so proxy can operate across all buckets
            for action in ("read", "write"):
                pol = nipyapi.security.get_access_policy_for_resource(
                    resource="/buckets",
                    action=action,
                    service="registry",
                    auto_create=True,
                )
                log.info(
                    "bootstrap_registry: attach proxy to /buckets action=%s policy id=%s",
                    action, getattr(pol, "identifier", None),
                )
                nipyapi.security.add_user_to_access_policy(
                    user=nifi_proxy_user,
                    policy=pol,
                    service="registry",
                    strict=False,
                )
            proxy_access_policies = [
                ("read", "/proxy"),
                ("write", "/proxy"),
                ("delete", "/proxy"),
            ]
            for action, resource in proxy_access_policies:
                pol = nipyapi.security.get_access_policy_for_resource(
                    resource=resource,
                    action=action,
                    service="registry",
                    auto_create=True
                )
                log.info(
                    "bootstrap_registry: attach proxy to %s action=%s policy id=%s",
                    resource, action, getattr(pol, "identifier", None),
                )
                nipyapi.security.add_user_to_access_policy(
                    user=nifi_proxy_user,
                    policy=pol,
                    service="registry",
                    strict=False
                )


def create_ssl_context_controller_service(
        parent_pg, name,
        keystore_file=None, keystore_password=None,
        truststore_file=None, truststore_password=None,
        key_password=None, keystore_type=None, truststore_type=None, ssl_protocol=None,
        ssl_service_type=None):
    """
    Creates and configures an SSL Context Service for secure client connections.
    Note that once created it can be listed and deleted using the standard canvas functions.

    Args:
        parent_pg (ProcessGroupEntity): The Process Group to create the service in
        name (str): Name for the SSL Context Service
        keystore_file (str): Path to the client certificate/keystore file
        keystore_password (str): Password for the keystore
        truststore_file (str): Path to the truststore file
        truststore_password (str): Password for the truststore
        key_password (Optional[str]): Password for the key, defaults to keystore_password if not set
        keystore_type (Optional[str]): Type of keystore (JKS, PKCS12), defaults to JKS
        truststore_type (Optional[str]): Type of truststore (JKS, PKCS12), defaults to JKS
        ssl_protocol (Optional[str]): SSL protocol version, defaults to TLS
        ssl_service_type (Optional[str]): SSL service type, defaults to
            StandardRestrictedSSLContextService

    Returns:
        (ControllerServiceEntity): The configured SSL Context Service
    """
    assert isinstance(parent_pg, nipyapi.nifi.ProcessGroupEntity)
    assert isinstance(name, str)
    assert keystore_file is None or isinstance(keystore_file, str)
    assert keystore_password is None or isinstance(keystore_password, str)
    assert isinstance(truststore_file, str)
    assert isinstance(truststore_password, str)
    assert key_password is None or isinstance(key_password, str)
    assert keystore_type is None or isinstance(keystore_type, str)
    assert truststore_type is None or isinstance(truststore_type, str)
    assert ssl_protocol is None or isinstance(ssl_protocol, str)

    default_ssl_service_type = 'org.apache.nifi.ssl.StandardRestrictedSSLContextService'
    with nipyapi.utils.rest_exceptions():
        props = {
            'Truststore Filename': truststore_file,
            'Truststore Password': truststore_password,
            'Truststore Type': truststore_type or 'JKS',
            'SSL Protocol': ssl_protocol or 'TLS'
        }
        if keystore_file:
            props.update({
                'Keystore Filename': keystore_file,
                'Keystore Password': keystore_password or '',
                'key-password': key_password or keystore_password or '',
                'Keystore Type': keystore_type or 'JKS',
            })
        return nipyapi.nifi.ControllerApi().create_controller_service(
            body=nipyapi.nifi.ControllerServiceEntity(
                revision=nipyapi.nifi.RevisionDTO(
                    version=0
                ),
                component=nipyapi.nifi.ControllerServiceDTO(
                    type=ssl_service_type or default_ssl_service_type,
                    name=name,
                    properties=props)))
