# coding: utf-8

"""
NiPyAPI: A convenient Python wrapper for the Apache NiFi Rest API
"""

from __future__ import absolute_import

import ssl

import nipyapi.nifi
import nipyapi.registry
from nipyapi.nifi import configuration as nifi_config
from nipyapi.registry import configuration as registry_config


# Method to check if we're compatible with the API endpoint
# If None, then no check has been done
# If True, then we have tested and there are no issues
# If False, then we believe we are incompatible
nifi_config.version_check = None
registry_config.version_check = None


# Note that changing the default hosts below will not
# affect an API connection that's already running.
# You'll need to change the .api_client.host for that.

# Set Default Host for NiFi
nifi_config.host = 'http://localhost:8080/nifi-api'

# Set Default Host for NiFi-Registry
registry_config.host = 'http://localhost:18080/nifi-registry-api'

# Task wait delays
# Set how fast to recheck for completion of a long running task in seconds
retry_delay = 0.5
# Set the max amount of time we will wait for a task to complete in seconds
retry_max_wait = 3


registered_filters = {
    'Bucket': {'id': ['identifier'], 'name': ['name']},
    'VersionedFlow': {'id': ['identifier'], 'name': ['name']},
    'RegistryClientEntity': {'id': ['id'], 'name': ['component', 'name']},
    'ProcessGroupEntity': {'id': ['id'], 'name': ['status', 'name']},
    'DocumentedTypeDTO': {'bundle': ['bundle', 'artifact'],
                          'name': ['type'],
                          'tag': ['tags']},  # This is Processor Types
    'ProcessorEntity': {'id': ['id'], 'name': ['status', 'name']},
}


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
        configuration=nifi_config,
        ca_file=ca_file,
        client_cert_file=client_cert_file,
        client_key_file=client_key_file,
        client_key_password=client_key_password)


def login_to_nifi(username=None, password=None):
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
    """

    if not registry_config.host:
        raise Exception("NiFi host must be set prior to logging in.")
    if not registry_config.host.startswith("https"):
        raise Exception("Login is only available when connecting to a "
                        "secured NiFi over HTTPS.")

    # obtain temporary access token (jwt) using username/password credentials
    nifi_token = nipyapi.nifi.AccessApi().create_access_token(
        username=username, password=password)
    set_nifi_auth_token(nifi_token)


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
    _set_configuration_api_key(nifi_config, 'tokenAuth', token)


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
        configuration=registry_config,
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

    if not registry_config.host:
        raise Exception("NiFi Registry host must be set prior to logging in.")
    if not registry_config.host.startswith("https"):
        raise Exception("Login is only available when connecting to a "
                        "secured NiFi Registry over HTTPS.")

    try:
        # set username/password in registry configuration for initial login
        registry_config.username = username
        registry_config.password = password
        # obtain temporary access token (jwt) using user/pass credentials
        registry_token = nipyapi.registry.AccessApi() \
            .create_access_token_using_basic_auth_credentials()
        set_registry_auth_token(registry_token)
    finally:
        # clear username/password credentials from registry configuration
        registry_config.username = None
        registry_config.password = None


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
    _set_configuration_api_key(registry_config, 'tokenAuth', token)


# --- Generic Helper Methods

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
        ssl_context.load_cert_chain(
            certfile=client_cert_file,
            keyfile=client_key_file,
            password=client_key_password)

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
