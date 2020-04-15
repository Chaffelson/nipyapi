# -*- coding: utf-8 -*-

"""
Secure connectivity management for NiPyApi
"""

from __future__ import absolute_import
import logging
import ssl
from copy import copy
import six
import urllib3
import nipyapi

log = logging.getLogger(__name__)


__all__ = ['create_service_user', 'create_service_user_group',
           'set_service_auth_token', 'service_logout',
           'get_service_access_status', 'add_user_to_access_policy',
           'update_access_policy', 'get_access_policy_for_resource',
           'create_access_policy', 'list_service_users', 'get_service_user',
           'set_service_ssl_context', 'add_user_group_to_access_policy',
           'bootstrap_security_policies', 'service_login',
           'remove_service_user', 'list_service_user_groups',
           'get_service_user_group', 'remove_service_user_group'
           ]

# These are the known-valid policy actions
_valid_actions = ['read', 'write', 'delete']
# These are the services that these functions know how to configure
_valid_services = ['nifi', 'registry']


def list_service_users(service='nifi'):
    """Lists all users of a given service, takes a service name as a string"""
    assert service in _valid_services
    with nipyapi.utils.rest_exceptions():
        out = getattr(nipyapi, service).TenantsApi().get_users()
    if service == 'nifi':
        return out.users
    return out


def get_service_user(identifier, identifier_type='identity', service='nifi'):
    """
    Filters the all users list for a given identifier and type

    Args:
        identifier (str): the string to search for
        identifier_type (str): the field to search in
        service (str): the name of the service

    Returns:
        None if no match, list of multiple matches, else single object

    """
    assert service in _valid_services
    assert isinstance(identifier, six.string_types)
    assert isinstance(identifier_type, six.string_types)
    obj = list_service_users(service)
    out = nipyapi.utils.filter_obj(obj, identifier, identifier_type)
    return out


def remove_service_user(user, service='nifi', strict=True):
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
    if service == 'registry':
        assert isinstance(user, nipyapi.registry.User)
        submit = {
            'id': user.identifier
        }
    else:
        assert isinstance(user, nipyapi.nifi.UserEntity)
        submit = {
            'id': user.id,
            'version': user.revision.version
        }
    assert isinstance(strict, bool)
    try:
        return getattr(nipyapi, service).TenantsApi().remove_user(**submit)
    except getattr(nipyapi, service).rest.ApiException as e:
        if 'Unable to find user' in e.body or 'does not exist' in e.body:
            if not strict:
                return None
        raise ValueError(e.body)


def create_service_user(identity, service='nifi', strict=True):
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
    assert isinstance(identity, six.string_types)
    assert isinstance(strict, bool)
    if service == 'registry':
        user_obj = nipyapi.registry.User(
            identity=identity
        )
    else:
        # must be nifi
        user_obj = nipyapi.nifi.UserEntity(
            revision=nipyapi.nifi.RevisionDTO(
                version=0
            ),
            component=nipyapi.nifi.UserDTO(
                identity=identity
            )
        )
    try:
        return getattr(nipyapi, service).TenantsApi().create_user(user_obj)
    except (nipyapi.nifi.rest.ApiException,
            nipyapi.registry.rest.ApiException) as e:
        if 'already exists' in e.body and not strict:
            return get_service_user(identity, service=service)
        raise ValueError(e.body)


def create_service_user_group(identity, service='nifi',
                              users=None, strict=True):
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
    assert isinstance(identity, six.string_types)
    if service == 'nifi':
        assert all(isinstance(user, nipyapi.nifi.UserEntity) for user in users)
    else:
        assert all(isinstance(user, nipyapi.registry.User) for user in users)
    if service == 'registry':
        user_group_obj = nipyapi.registry.UserGroup(
            identity=identity,
            users=[{'identifier': user.identifier} for user in users]
        )
    else:
        # must be nifi
        user_group_obj = nipyapi.nifi.UserGroupEntity(
            revision=nipyapi.nifi.RevisionDTO(
                version=0
            ),
            component=nipyapi.nifi.UserGroupDTO(
                identity=identity,
                users=[{'id': user.id} for user in users]
            )
        )
    try:
        return getattr(nipyapi, service).TenantsApi().create_user_group(
            user_group_obj
        )
    except (nipyapi.nifi.rest.ApiException,
            nipyapi.registry.rest.ApiException) as e:
        if 'already exists' in e.body:
            if not strict:
                return get_service_user_group(identity, service=service)
        raise ValueError(e.body)


def list_service_user_groups(service='nifi'):
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
    if service == 'nifi':
        return out.user_groups
    return out


def get_service_user_group(identifier, identifier_type='identity',
                           service='nifi'):
    """
    Filters the all groups list for a given identifier and type

    Args:
        identifier (str): the string to search for
        identifier_type (str): the field to search in, identity or id
        service (str): the name of the service

    Returns:
        None if no match, list of multiple matches, else single object

    """
    assert service in _valid_services
    assert isinstance(identifier, six.string_types)
    assert isinstance(identifier_type, six.string_types)
    obj = list_service_user_groups(service)
    out = nipyapi.utils.filter_obj(obj, identifier, identifier_type)
    return out


def remove_service_user_group(group, service='nifi', strict=True):
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
    if service == 'registry':
        assert isinstance(group, nipyapi.registry.UserGroup)
        submit = {
            'id': group.identifier
        }
    else:
        assert isinstance(group, nipyapi.nifi.UserGroupEntity)
        submit = {
            'id': group.id,
            'version': group.revision.version
        }
    assert isinstance(strict, bool)
    try:
        return getattr(
            nipyapi, service
        ).TenantsApi().remove_user_group(**submit)
    except getattr(nipyapi, service).rest.ApiException as e:
        if 'Unable to find user' in e.body or 'does not exist' in e.body:
            if not strict:
                return None
        raise ValueError(e.body)


def service_login(service='nifi', username=None, password=None,
                  bool_response=False, auth_type='token'):
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
        auth_type (str): token (default) or basic

    Returns:
        (bool): True if successful, False or an Error if not. See bool_response

    """
    log_args = locals()
    log_args['password'] = 'REDACTED'
    log.info("Called service_login with args %s", log_args)
    assert service in _valid_services
    assert username is None or isinstance(username, six.string_types)
    assert password is None or isinstance(password, six.string_types)
    assert isinstance(bool_response, bool)

    configuration = getattr(nipyapi, service).configuration
    assert configuration.host, "Host must be set prior to logging in."
    assert configuration.host.startswith("https"), \
        "Login is only available when connecting over HTTPS."
    default_pword = getattr(nipyapi.config, 'default_' + service + '_password')
    default_uname = getattr(nipyapi.config, 'default_' + service + '_username')
    # We use copy so we don't clobber the default by mistake
    pword = password if password else copy(default_pword)
    uname = username if username else copy(default_uname)
    assert pword, "Password must be set or in default config"
    assert uname, "Username must be set or in default config"
    # set username/password in configuration for initial login
    # Registry pulls from config, NiFi allows submission
    configuration.username = uname
    configuration.password = pword
    if auth_type == 'token':
        log.info("Attempting tokenAuth login with user identity [%s]",
                 configuration.username)
        try:
            if service == 'nifi':
                token = nipyapi.nifi.AccessApi().create_access_token(
                    username=uname, password=pword)
            else:
                token = nipyapi.registry.AccessApi() \
                    .create_access_token_using_basic_auth_credentials()
        except getattr(nipyapi, service).rest.ApiException as e:
            if bool_response:
                return False
            raise ValueError(e.body)
        set_service_auth_token(token=token, service=service)
    elif auth_type == 'basic':
        log.info("basicAuth set, skipping token retrieval")
    return True


def set_service_auth_token(token=None, token_name='tokenAuth', service='nifi'):
    """
    Helper method to set the auth token correctly for the specified service

    Args:
        token (Optional[str]): The token to set. Defaults to None.
        token_name (str): the api_key field name to set the token to. Defaults
            to 'tokenAuth'
        service (str): 'nifi' or 'registry', the service to set

    Returns:
        (bool): True on success, False if token not set
    """
    assert service in _valid_services
    assert isinstance(token_name, six.string_types)
    assert token is None or isinstance(token, six.string_types)
    if service == 'registry':
        configuration = nipyapi.config.registry_config
    else:
        configuration = nipyapi.config.nifi_config
    if token:
        configuration.api_key[token_name] = token
        configuration.api_key_prefix[token_name] = 'Bearer'
    else:
        # If not token, then assume we are doing logout and cleanup
        if token_name in configuration.api_key:
            configuration.api_key.pop(token_name)
    if token_name not in configuration.api_key:
        return False
    return True


def service_logout(service='nifi'):
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
        if 'Cannot set verify_mode to CERT_NONE' in str(e):
            status = None
            # Logout throws error with incorrect ssl setup
        else:
            raise e
    # Set to empty string and not None as basic auth setup will still
    # run even if not used
    getattr(nipyapi, service).configuration.password = ''
    getattr(nipyapi, service).configuration.username = ''
    if not status:
        return True
    return False


def get_service_access_status(service='nifi', bool_response=False):
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
        logging.getLogger('urllib3').setLevel(logging.ERROR)
    try:
        out = getattr(nipyapi, service).AccessApi().get_access_status()
        log.info("Got server response, returning")
        return out
    except urllib3.exceptions.MaxRetryError as e:
        log.debug("- Caught exception %s", type(e))
        if bool_response:
            log.debug("Connection failed with error %s and bool_response is "
                      "True, returning False", e)
            return False
        log.debug("- bool_response is False, raising Exception")
        raise e
    except getattr(nipyapi, service).rest.ApiException as e:
        expected_errors = [
            'Authentication object was not found',
            'only supported when running over HTTPS'
        ]
        if any(x in e.body for x in expected_errors):
            if bool_response:
                return False
            raise e


def add_user_to_access_policy(user, policy, service='nifi', refresh=True,
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
        nipyapi.registry.AccessPolicy if service == 'registry'
        else nipyapi.nifi.AccessPolicyEntity
    )
    assert isinstance(
        user,
        nipyapi.registry.User if service == 'registry'
        else nipyapi.nifi.UserEntity
    )

    user_id = user.id if service == 'nifi' else user.identifier

    if refresh:
        policy_tgt = getattr(nipyapi, service).PoliciesApi().get_access_policy(
            policy.id if service == 'nifi' else policy.identifier
        )
    else:
        policy_tgt = policy

    assert isinstance(
        policy_tgt,
        nipyapi.registry.AccessPolicy if service == 'registry' else
        nipyapi.nifi.AccessPolicyEntity
    )

    policy_users = policy_tgt.users if service == 'registry' else\
        policy_tgt.component.users
    policy_user_ids = [
        i.identifier if service == 'registry' else i.id for i in policy_users
    ]
    if user_id not in policy_user_ids:
        if service == 'registry':
            policy_tgt.users.append(user)
        elif service == 'nifi':
            policy_tgt.component.users.append({'id': user_id})

        return nipyapi.security.update_access_policy(policy_tgt, service)
    if strict and user_id in policy_user_ids:
        raise ValueError("Strict is True and User ID already in Policy")


def add_user_group_to_access_policy(user_group, policy, service='nifi',
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
        nipyapi.registry.AccessPolicy if service == 'registry'
        else nipyapi.nifi.AccessPolicyEntity
    )
    assert isinstance(
        user_group,
        nipyapi.registry.UserGroup if service == 'registry'
        else nipyapi.nifi.UserGroupEntity
    )
    user_group_id = user_group.id if service == 'nifi' else \
        user_group.identifier

    if refresh:
        policy_tgt = getattr(nipyapi, service).PoliciesApi().get_access_policy(
            policy.id if service == 'nifi' else policy.identifier
        )
    else:
        policy_tgt = policy

    assert isinstance(
        policy_tgt,
        nipyapi.registry.AccessPolicy if service == 'registry' else
        nipyapi.nifi.AccessPolicyEntity
    )

    policy_user_groups = policy_tgt.users if service == 'registry' else\
        policy_tgt.component.user_groups
    policy_user_group_ids = [
        i.identifier if service == 'registry' else i.id
        for i in policy_user_groups
    ]

    assert user_group_id not in policy_user_group_ids

    if service == 'registry':
        policy_tgt.user_groups.append(user_group)
    elif service == 'nifi':
        policy_tgt.component.user_groups.append({'id': user_group_id})

    return nipyapi.security.update_access_policy(policy_tgt, service)


def update_access_policy(policy, service='nifi'):
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
        nipyapi.registry.AccessPolicy if service == 'registry'
        else nipyapi.nifi.AccessPolicyEntity
    ), "Policy type {0} not vaid.".format(type(policy))
    with nipyapi.utils.rest_exceptions():
        return getattr(nipyapi, service).PoliciesApi().update_access_policy(
            id=policy.id if service == 'nifi' else policy.identifier,
            body=policy
        )


def get_access_policy_for_resource(resource,
                                   action,
                                   r_id=None,
                                   service='nifi',
                                   auto_create=False):
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
    assert r_id is None or isinstance(r_id, six.string_types)
    assert isinstance(resource, six.string_types)
    assert isinstance(auto_create, bool)
    log.info("Called get_access_policy_for_resource with Args %s", locals())

    # Strip leading '/' from resource as lookup endpoint prepends a '/'
    resource = resource[1:] if resource.startswith('/') else resource
    log.info("Getting %s Policy for %s:%s:%s", service, action,
             resource, str(r_id))
    if service == 'nifi':
        pol_api = nipyapi.nifi.PoliciesApi()
    else:
        pol_api = nipyapi.registry.PoliciesApi()
    try:
        nipyapi.utils.bypass_slash_encoding(service, True)
        response = pol_api.get_access_policy_for_resource(
            action=action,
            resource='/'.join([resource, r_id]) if r_id else resource
        )
        nipyapi.utils.bypass_slash_encoding(service, False)
        return response
    except nipyapi.nifi.rest.ApiException as e:
        if 'Unable to find access policy' in e.body:
            log.info("Access policy not found")
            if not auto_create:
                return None
            return nipyapi.security.create_access_policy(
                resource, action, r_id, service
            )
        log.info("Unexpected Error, raising...")
        raise ValueError(e.body)
    finally:
        nipyapi.utils.bypass_slash_encoding(service, False)


def create_access_policy(resource, action, r_id=None, service='nifi'):
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
    assert isinstance(resource, six.string_types)
    assert action in _valid_actions
    assert r_id is None or isinstance(r_id, six.string_types)
    assert service in _valid_services
    if resource[0] != '/':
        r = '/' + resource
    else:
        r = resource
    with nipyapi.utils.rest_exceptions():
        if service == 'nifi':
            return nipyapi.nifi.PoliciesApi().create_access_policy(
                body=nipyapi.nifi.AccessPolicyEntity(
                    revision=nipyapi.nifi.RevisionDTO(version=0),
                    component=nipyapi.nifi.AccessPolicyDTO(
                        action=action,
                        resource='/'.join([r, r_id]) if r_id else r
                    )
                )
            )
        # elif service == 'registry':
        return nipyapi.registry.PoliciesApi().create_access_policy(
            body=nipyapi.registry.AccessPolicy(
                action=action,
                resource=r
            )
        )


def set_service_ssl_context(
        service='nifi',
        ca_file=None,
        client_cert_file=None,
        client_key_file=None,
        client_key_password=None):
    """
    Create an SSLContext for connecting over https to a secured NiFi or
    NiFi-Registry instance.

    This method can be used to  create an SSLContext for
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

    Returns:
        (None)
    """
    assert service in ['nifi', 'registry']
    if client_key_file is None:
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    else:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        try:
            ssl_context.load_cert_chain(
                certfile=client_cert_file,
                keyfile=client_key_file,
                password=client_key_password
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "Unable to read keyfile {0} or certfile {1}, error was "
                "{2}".format(client_key_file, client_cert_file, e))

    if ca_file is not None:
        ssl_context.load_verify_locations(cafile=ca_file)

    if service == 'registry':
        nipyapi.config.registry_config.ssl_context = ssl_context
    nipyapi.config.nifi_config.ssl_context = ssl_context


def bootstrap_security_policies(service, user_identity=None,
                                group_identity=None):
    """
    Creates a default security context within NiFi or Nifi-Registry

    Args:
        service (str): 'nifi' or 'registry' to indicate which service
        user_identity: a service user to establish in the security context
        group_identity: a service group to establish in the security context

    Returns:
        None

    """
    assert service in _valid_services, "service not in %s" % _valid_services
    valid_ident_obj = [nipyapi.nifi.UserEntity, nipyapi.registry.User]
    if user_identity is not None:
        assert user_identity in valid_ident_obj
    if 'nifi' in service:
        rpg_id = nipyapi.canvas.get_root_pg_id()
        if user_identity is None and group_identity is None:
            nifi_user_identity = nipyapi.security.get_service_user(
                nipyapi.config.default_nifi_username,
                service='nifi'
            )
        else:
            nifi_user_identity = user_identity
        access_policies = [
            ('write', 'process-groups', rpg_id),
            ('read', 'process-groups', rpg_id),
            ('write', 'data/process-groups', rpg_id),
            ('read', 'data/process-groups', rpg_id),
            ('read', 'system', None),
        ]
        for pol in access_policies:
            ap = nipyapi.security.get_access_policy_for_resource(
                action=pol[0],
                resource=pol[1],
                r_id=pol[2],
                service='nifi',
                auto_create=True
            )
            if nifi_user_identity is None:
                # I should not rely upon a try/catch there
                # but it's the simplest way (I just hope it won't
                # break the server :-) )
                try:
                    nipyapi.security.add_user_group_to_access_policy(
                        user_group=group_identity,
                        policy=ap,
                        service='nifi'
                    )
                except:  # noqa
                    pass
            else:
                nipyapi.security.add_user_to_access_policy(
                    user=nifi_user_identity,
                    policy=ap,
                    service='nifi',
                    strict=False
                )
    else:
        if user_identity is None and group_identity is None:
            reg_user_identity = nipyapi.security.get_service_user(
                nipyapi.config.default_registry_username,
                service='registry'
            )
        else:
            reg_user_identity = user_identity
        all_buckets_access_policies = [
            ("read", "/buckets"),
            ("write", "/buckets"),
            ("delete", "/buckets")
        ]
        for action, resource in all_buckets_access_policies:
            pol = nipyapi.security.get_access_policy_for_resource(
                resource=resource,
                action=action,
                service='registry',
                auto_create=True
            )
            if reg_user_identity is None:
                nipyapi.security.add_user_group_to_access_policy(
                    user_group=group_identity,
                    policy=pol,
                    service='registry'
                )
            else:
                nipyapi.security.add_user_to_access_policy(
                    user=reg_user_identity,
                    policy=pol,
                    service='registry',
                    strict=False
                )
        # Setup Proxy Access
        nifi_proxy = nipyapi.security.create_service_user(
            identity=nipyapi.config.default_proxy_user,
            service='registry',
            strict=False
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
                service='registry',
                auto_create=True
            )
            nipyapi.security.add_user_to_access_policy(
                user=nifi_proxy,
                policy=pol,
                service='registry',
                strict=False
            )
