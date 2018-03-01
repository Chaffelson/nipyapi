# -*- coding: utf-8 -*-

"""
Secure connectivity management for NiPyApi
"""

from __future__ import absolute_import
import logging
import six
import ssl
import urllib3
import nipyapi


log = logging.getLogger(__name__)

# --- NiFi Helper Methods


def create_nifi_ssl_context(
        ca_file=None,
        client_cert_file=None,
        client_key_file=None,
        client_key_password=None):
    """
    Create an SSLContext for connecting over https to a secured NiFi
    instance.

    This method can be used to  create an SSLContext for
    two-way TLS in which a client cert is used by the NiFi server
    to authenticate the client.

    This method can also be used for one-way TLS in which the client
    verifies the server's certificate, but authenticates using a
    different form of credentials, such as LDAP username/password.

    If you are using one-way TLS with a certificate signed by a
    root CA trusted by your system/platform, this step is not
    necessary as the default TLS-handshake should "just work."

    :param ca_file: A PEM file containing certs for the root CA(s)
        for the NiFi server
    :param client_cert_file: A PEM file containing the public
        certificates for the user/client identity
    :param client_key_file: An encrypted (password-protected) PEM file
        containing the client's secret key
    :param client_key_password: The password to decrypt the client_key_file
    :return:
    """
    _create_configuration_ssl_context(
        configuration=nipyapi.config.nifi_config,
        ca_file=ca_file,
        client_cert_file=client_cert_file,
        client_key_file=client_key_file,
        client_key_password=client_key_password)


def login_to_nifi(username=None, password=None, bool_response=False):
    """
    Login to the currently configured NiFi server.

    Login requires a secure connection over https.
    Prior to calling this method, the host must be specified
    and the SSLContext should be configured (if necessary).

    Successful login will result in a generated token (JWT) being
    cached in the nifi_config that will be passed in all future
    REST API calls. To clear that token, call logout_from_nifi().

    The token is temporary and will expire after a duration set by
    the NiFi server. After a token expires, you must call this
    method again to generate a new token.

    :param username: the user's directory username (e.g., LDAP)
    :param password: the user's directory password (e.g., LDAP)
    :param bool_response: If set to True, this function will return False if
    an exception is raised during the process. Useful for connection testing.
    """
    log_args = locals()
    log_args['password'] = 'REDACTED'
    log.info("Called login_to_nifi with args %s", log_args)
    # TODO: Tidy up logging and automate sensitive value redaction
    if not nipyapi.config.registry_config.host:
        raise Exception("NiFi host must be set prior to logging in.")
    if not nipyapi.config.registry_config.host.startswith("https"):
        raise Exception("Login is only available when connecting to a "
                        "secured NiFi over HTTPS.")

    # obtain temporary access token (jwt) using username/password credentials
    try:
        log.info("- Attempting to create access token")
        nifi_token = nipyapi.nifi.AccessApi().create_access_token(
            username=username, password=password)
    except urllib3.exceptions.MaxRetryError as e:
        log.info("- Connection TimeOut")
        if bool_response:
            return False
        raise e
    except nipyapi.nifi.rest.ApiException as e:
        raise ConnectionError(e.body)
    log.info("- Access token created, setting")
    set_nifi_auth_token(nifi_token)
    return True


def logout_from_nifi():
    """
    Clears a previously cached authentication token (JWT) that was
    generated from a call to login_to_nifi().
    """
    set_nifi_auth_token(None)


def set_nifi_auth_token(token=None):
    """
    Explicitly set a JWT trusted by the NiFi server that was generated
    outside of this config module.

    If your NiFi instance has another means of generating tokens
    (for example, Kerberos ticket exchange, Knox, or OIDC), you
    can generate a token outside of NiPyApi and pass it to the NiPyApi
    configuration to use with API calls using this method.

    :param token: The authentication token (JWT) to pass to the NiFi
        server in REST API calls.
    """
    _set_configuration_api_key(nipyapi.config.nifi_config, 'tokenAuth', token)


def get_nifi_access_status(bool_response=False):
    """
    Gets the access status for the current session
    :param bool_response: If True, the function will return False on hitting
    an Error instead of raising it. Useful for connection testing.
    :return:
    """
    if bool_response:
        # Assume we are using this as a connection test and therefore disable
        # the Warnings urllib3 will shower us with
        logging.getLogger('urllib3').setLevel(logging.ERROR)
    try:
        return nipyapi.nifi.AccessApi().get_access_status()
    except (ConnectionRefusedError, ssl.SSLEOFError, ssl.SSLError) as e:
        if bool_response:
            return False
        raise e


# def bootstrap_nifi_access_policy(force=True):
#     root_flow = nipyapi.nifi.FlowApi().get_flow('root')
#     current_user = nipyapi.security.get_nifi_access_status()
#     if force:
#         cp = nipyapi.nifi.PoliciesApi().get_access_policy_for_resource(
#             action='write',
#             resource='/process-groups/' + root_flow.process_group_flow.id
#         )
#         if cp:
#             nipyapi.nifi.PoliciesApi().remove_access_policy(cp.id)
#     return nipyapi.nifi.PoliciesApi().create_access_policy(
#         body=nipyapi.nifi.AccessPolicyEntity(
#             id=root_flow.process_group_flow.id,
#             revision=nipyapi.nifi.RevisionDTO(
#                 version=0
#             ),
#             component=nipyapi.nifi.AccessPolicyDTO(
#                 action='write',
#                 resource='/process-groups/' + root_flow.process_group_flow.id,
#                 users=[
#                     nipyapi.nifi.TenantEntity(
#                         component=nipyapi.nifi.TenantDTO(
#                             identity=current_user.access_status.identity
#                         ),
#                         permissions=nipyapi.nifi.PermissionsDTO(
#                             can_read=True,
#                             can_write=True
#                         )
#                     )
#                 ]
#             )
#         )
#     )


# --- NiFi Registry Helper Methods


def create_registry_ssl_context(
        ca_file=None,
        client_cert_file=None,
        client_key_file=None,
        client_key_password=None):
    """
    Create an SSLContext for connecting over https to a secured NiFi
    Registry instance.

    This method can be used to  create an SSLContext for
    two-way TLS in which a client cert is used by the NiFi Registry
    server to authenticate the client.

    This method can also be used for one-way TLS in which the client
    verifies the server's certificate, but authenticates using a
    different form of credentials, such as LDAP username/password.

    If you are using one-way TLS with a certificate signed by a
    root CA trusted by your system/platform, this step is not
    necessary as the default TLS-handshake should "just work."

    :param ca_file: A PEM file containing certs for the root CA(s)
        for the NiFi Registry server
    :param client_cert_file: A PEM file containing the public
        certificates for the user/client identity
    :param client_key_file: An encrypted (password-protected) PEM file
        containing the client's secret key
    :param client_key_password: The password to decrypt the client_key_file
    :return:
    """
    _create_configuration_ssl_context(
        configuration=nipyapi.config.registry_config,
        ca_file=ca_file,
        client_cert_file=client_cert_file,
        client_key_file=client_key_file,
        client_key_password=client_key_password)


def login_to_registry(username=None, password=None):
    """
    Login to the currently configured NiFi Registry server.

    Login requires a secure connection over https.
    Prior to calling this method, the host must be specified
    and the SSLContext should be configured (if necessary).

    Successful login will result in a generated token (JWT) being
    cached in the registry_config that will be passed in all future
    REST API calls. To clear that token, call logout_from_registry().

    The token is temporary and will expire after a duration set by
    the NiFi Registry server. After a token expires, you must call
    this method again to generate a new token.

    :param username: the user's directory username (e.g., LDAP)
    :param password: the user's directory password (e.g., LDAP)
    """

    if not nipyapi.config.registry_config.host:
        raise Exception("NiFi Registry host must be set prior to logging in.")
    if not nipyapi.config.registry_config.host.startswith("https"):
        raise Exception("Login is only available when connecting to a "
                        "secured NiFi Registry over HTTPS.")

    try:
        # set username/password in registry configuration for initial login
        nipyapi.config.registry_config.username = username
        nipyapi.config.registry_config.password = password
        # obtain temporary access token (jwt) using user/pass credentials
        registry_token = nipyapi.registry.AccessApi() \
            .create_access_token_using_basic_auth_credentials()
        set_registry_auth_token(registry_token)
    finally:
        # clear username/password credentials from registry configuration
        nipyapi.config.registry_config.username = None
        nipyapi.config.registry_config.password = None


def logout_from_registry():
    """
    Clears a previously cached authentication token (JWT) that was
    generated from a call to login_to_registry().
    """
    set_registry_auth_token(None)


def set_registry_auth_token(token=None):
    """
    Explicitly set a JWT trusted by the NiFi Registry server that was
    generated outside of this config module.

    If your NiFi Registry instance has another means of generating
    tokens (for example, Kerberos ticket exchange), you  can generate
    a token outside of NiPyApi and pass it to the NiPyApi
    configuration to use with API calls using this method.

    :param token: The authentication token (JWT) to pass to the NiFi
        Registry server in REST API calls.
    """
    _set_configuration_api_key(
        nipyapi.config.registry_config,
        'tokenAuth',
        token
    )


def get_registry_access_status(bool_response=False):
    """
    Returns the user access status for the connected NiFi Registry
    :param bool_response: if True, returns False if the connection
    fails, otherwise raises the error. Useful for connection testing
    :return:
    """
    log.info("Called get_registry_access_status with args %s", locals())
    if bool_response:
        # Assume we are using this as a connection test and therefore disable
        # the Warnings urllib3 will shower us with
        log.debug("- bool_response is True, disabling urllib3 warnings")
        logging.getLogger('urllib3').setLevel(logging.ERROR)
    try:
        log.debug("- Attempting to retrieve registry access status")
        return nipyapi.registry.AccessApi().get_access_status()
    except urllib3.exceptions.MaxRetryError as e:
        log.debug("- Caught exception %s", type(e))
        if bool_response:
            log.debug("- bool_response is True, returning False instead of"
                      " raising exception")
            return False
        log.debug("- bool_response is False, raising Exception")
        raise e

# --- Generic Helper Methods


def add_user_to_access_policy(user, policy, service='nifi', refresh=True):
    assert service in ['nifi', 'registry']
    if service == 'nifi':
        assert isinstance(user, nipyapi.nifi.UserEntity)
        assert isinstance(policy, nipyapi.nifi.AccessPolicyEntity)
    if refresh:
        user_tgt = nipyapi.security.get_service_user(user.id, 'id', 'nifi')
        policy_tgt = nipyapi.nifi.PoliciesApi().get_access_policy(policy.id)
    else:
        user_tgt = user
        policy_tgt = policy
    user_obj = nipyapi.nifi.TenantEntity(
        id=user_tgt.id,
        permissions=nipyapi.nifi.PermissionsDTO(
            can_write=True,
            can_read=True
        ),
        revision=nipyapi.nifi.RevisionDTO(
            version=0
        ),
        component=nipyapi.nifi.TenantDTO(
            id=user_tgt.id,
            configurable=True,
            identity=user_tgt.component.identity
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
    try:
        return nipyapi.nifi.PoliciesApi().update_access_policy(
            id=policy.id,
            body=policy
        )
    except nipyapi.nifi.rest.ApiException as e:
        raise ValueError(e.body)


def get_access_policy_for_resource(resource,
                                   action,
                                   r_id=None,
                                   service='nifi'):
    assert service in ['nifi', 'registry']
    assert action in ['read', 'write']
    assert r_id is None or isinstance(r_id, six.string_types)
    assert isinstance(resource, six.string_types)
    log.info("Called get_access_policy_for_resource with Args %s", locals())
    if service == 'nifi':
        try:
            log.info("Getting %s policy for %s/%s",
                     action, resource, r_id)
            return nipyapi.nifi.PoliciesApi().get_access_policy_for_resource(
                action=action,
                resource=resource,
                id=r_id
            )
        except nipyapi.nifi.rest.ApiException as e:
            if 'Unable to find access policy' in e.body:
                log.info("Access policy not found, returning None")
                return None
            log.info("Unexpected Error, raising...")
            raise ValueError(e.body)


def create_access_policy(resource, action, r_id, service='nifi'):
    assert isinstance(resource, six.string_types)
    assert action in ['read', 'write']
    assert isinstance(r_id, six.string_types)
    assert service in ['nifi', 'registry']
    if resource[0] != '/':
        resource = '/' + resource
    try:
        return nipyapi.nifi.PoliciesApi().create_access_policy(
            body=nipyapi.nifi.AccessPolicyEntity(
                revision=nipyapi.nifi.RevisionDTO(version=0),
                component=nipyapi.nifi.AccessPolicyDTO(
                    action=action,
                    resource=resource + '/' + r_id
                )
            )
        )
    except nipyapi.nifi.rest.ApiException as f:
        log.info("Policy creation unsuccessful, raising error")
        raise ValueError(f.body)


def list_service_users(service='nifi'):
    assert service in ['nifi', 'registry']
    try:
        out = getattr(nipyapi, service).TenantsApi().get_users()
    except getattr(nipyapi, service).rest.ApiException as e:
        raise ValueError(e.body)
    if service == 'nifi':
        return out.users
    return out


def get_service_user(identifier, identifier_type='identity', service='nifi'):
    assert service in ['nifi', 'registry']
    assert isinstance(identifier, six.string_types)
    assert isinstance(identifier_type, six.string_types)
    obj = list_service_users(service)
    out = nipyapi.utils.filter_obj(obj, identifier, identifier_type)
    return out


def _create_configuration_ssl_context(
        configuration,
        ca_file=None,
        client_cert_file=None,
        client_key_file=None,
        client_key_password=None):
    """
    A helper method for creating an SSLContext in a Swagger client
    configuration.
    """

    if client_key_file is None:
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    else:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        try:
            ssl_context.load_cert_chain(
                certfile=client_cert_file,
                keyfile=client_key_file,
                password=client_key_password)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "Unable to read keyfile {0} or certfile {1}, error was "
                "{2}".format(client_cert_file, client_key_file, e))

    if ca_file is not None:
        ssl_context.load_verify_locations(cafile=ca_file)

    configuration.ssl_context = ssl_context


def _set_configuration_api_key(configuration, api_key_name, api_key_value):
    """
    A helper method for setting the value of an authentication token
    in a Swagger client configuration.
    """
    configuration.api_key[api_key_name] = api_key_value
    configuration.api_key_prefix[api_key_name] = 'Bearer'
