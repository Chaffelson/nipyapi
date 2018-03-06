# -*- coding: utf-8 -*-

"""
Secure connectivity management for NiPyApi
"""

from __future__ import absolute_import
import logging
import ssl
import six
import urllib3
import nipyapi


log = logging.getLogger(__name__)

__all__ = ['create_service_user', 'service_login', 'set_service_auth_token',
           'service_logout', 'get_service_access_status',
           'add_user_to_access_policy', 'update_access_policy',
           'get_access_policy_for_resource', 'create_access_policy',
           'list_service_users', 'get_service_user', 'set_service_ssl_context']

# These are the known-valid policy actions
_valid_actions = ['read', 'write', 'delete']
# These are the services that these functions know how to configure
_valid_services = ['nifi', 'registry']


def create_service_user(identity, service='nifi'):
    """
    Attempts to create a user with the provided identity in the given service

    Args:
        identity (str): Identity string for the user
        service (str): 'nifi' or 'registry'

    Returns:
        The new (User) or (UserEntity) object

    """
    assert service in _valid_services
    assert isinstance(identity, six.string_types)
    if service == 'registry':
        user_obj = nipyapi.registry.User(
            identity=identity
        )
    else:
        # must be nifi
        user_obj = nipyapi.nifi.UserEntity(
            component=nipyapi.nifi.UserDTO(
                identity=identity
            )
        )
    try:
        return getattr(nipyapi, service).TenantsApi().create_user(user_obj)
    except (
            nipyapi.nifi.rest.ApiException,
            nipyapi.registry.rest.ApiException) as e:
        raise ValueError(e.body)


def service_login(service='nifi', username=None, password=None,
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
    log_args['password'] = 'REDACTED'
    log.info("Called login_to_nifi with args %s", log_args)
    # TODO: Tidy up logging and automate sensitive value redaction
    assert service in _valid_services
    assert isinstance(username, six.string_types)
    assert isinstance(password, six.string_types)
    assert isinstance(bool_response, bool)

    if service == 'registry':
        configuration = nipyapi.config.registry_config
    else:
        configuration = nipyapi.config.nifi_config

    assert configuration.host, "Host must be set prior to logging in."
    assert configuration.host.startswith("https"), \
        "Login is only available when connecting over HTTPS."

    if service == 'registry':
        try:
            # set username/password in configuration for initial login
            configuration.username = username
            configuration.password = password
            # obtain temporary access token (jwt) using user/pass credentials
            registry_token = nipyapi.registry.AccessApi() \
                .create_access_token_using_basic_auth_credentials()
            set_service_auth_token(token=registry_token, service=service)
            return True
        except nipyapi.nifi.rest.ApiException as e:
            if bool_response:
                return False
            raise ValueError(e.body)
        finally:
            # clear username/password credentials from configuration
            configuration.username = None
            configuration.password = None
    else:
        # service == 'nifi'
        try:
            nifi_token = nipyapi.nifi.AccessApi().create_access_token(
                username=username, password=password)
        except urllib3.exceptions.MaxRetryError as e:
            if bool_response:
                return False
            raise e
        except nipyapi.nifi.rest.ApiException as e:
            raise ConnectionError(e.body)
        set_service_auth_token(token=nifi_token, service='nifi')
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
    configuration.api_key[token_name] = token
    configuration.api_key_prefix[token_name] = 'Bearer'
    if not configuration.api_key[token_name]:
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
    if not get_service_access_status(service, bool_response=True):
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


def add_user_to_access_policy(user, policy, service='nifi', refresh=True):
    """
    Attempts to add the given user object to the given access policy

    Args:
        user (User) or (UserEntity): User object to add
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
        user,
        nipyapi.registry.User if service == 'registry'
        else nipyapi.nifi.UserEntity
    )
    user_id = user.id if service == 'nifi' else user.identifier
    user_identity = user.component.identity if service == 'nifi'\
        else user.identity

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
    assert user_id not in policy_user_ids
    if service == 'registry':
        policy_tgt.users.append(user)
        return nipyapi.security.update_access_policy(policy_tgt, 'registry')
    # else if service == 'nifi':
    # This nifi endpoint caused me a lot of trouble, so have gone really
    # overboard in exactly duplicating the typical API submission objects
    user_obj = nipyapi.nifi.TenantEntity(
        id=user_id,
        permissions=nipyapi.nifi.PermissionsDTO(
            can_write=True,
            can_read=True
        ),
        revision=nipyapi.nifi.RevisionDTO(
            version=0
        ),
        component=nipyapi.nifi.TenantDTO(
            id=user_id,
            configurable=True,
            identity=user_identity
        )
    )
    policy_obj = nipyapi.nifi.AccessPolicyEntity(
        revision=nipyapi.nifi.RevisionDTO(
            version=policy_tgt.revision.version
        ),
        id=policy_tgt.id,
        component=nipyapi.nifi.AccessPolicyDTO(
            id=policy_tgt.id,
            user_groups=policy_tgt.component.user_groups,
            users=policy_tgt.component.users
        )
    )
    policy_obj.component.users.append(user_obj)
    return nipyapi.security.update_access_policy(policy_obj, service)


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
    try:
        return getattr(nipyapi, service).PoliciesApi().update_access_policy(
            id=policy.id if service == 'nifi' else policy.identifier,
            body=policy
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


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
        resource (str): A valid resource in the taret service
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

    try:
        if service == 'nifi':
            log.info("Getting NiFi policy for %s:%s/%s",
                     action, resource, r_id)
            return nipyapi.nifi.PoliciesApi().get_access_policy_for_resource(
                action=action,
                resource=resource,
                id=r_id
            )
        # if service == 'registry:
        log.info("Getting Registry policy for '%s:%s",
                 action, resource)
        # Strip leading '/' from resource as lookup endpoint prepends a '/'
        stripped_resource = resource[1:] if resource.startswith(
            '/') else resource
        return nipyapi.registry.PoliciesApi().get_access_policy_for_resource(
            action, stripped_resource
        )
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
        resource = '/' + resource
    try:
        if service == 'nifi':
            return nipyapi.nifi.PoliciesApi().create_access_policy(
                body=nipyapi.nifi.AccessPolicyEntity(
                    revision=nipyapi.nifi.RevisionDTO(version=0),
                    component=nipyapi.nifi.AccessPolicyDTO(
                        action=action,
                        resource=resource + '/' + r_id
                    )
                )
            )
        # elif service == 'registry':
        return nipyapi.registry.PoliciesApi().create_access_policy(
            body=nipyapi.registry.AccessPolicy(
                action=action,
                resource=resource
            )
        )
    except nipyapi.nifi.rest.ApiException as f:
        log.info("Policy creation unsuccessful, raising error")
        raise ValueError(f.body)


def list_service_users(service='nifi'):
    """Lists all users of a given service, takes a service name as a string"""
    assert service in _valid_services
    try:
        out = getattr(nipyapi, service).TenantsApi().get_users()
    except getattr(nipyapi, service).rest.ApiException as e:
        raise ValueError(e.body)
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
                "{2}".format(client_cert_file, client_key_file, e))

    if ca_file is not None:
        ssl_context.load_verify_locations(cafile=ca_file)

    if service == 'registry':
        nipyapi.config.registry_config.ssl_context = ssl_context
    nipyapi.config.nifi_config.ssl_context = ssl_context
