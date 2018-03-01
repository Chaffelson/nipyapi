# coding: utf-8

"""
An implementation helper for connecting to secure NiFi instances.
"""

from __future__ import absolute_import
import logging
from pprint import pprint
from os import path
import nipyapi
from nipyapi.utils import DockerContainer

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

_basename = "nipyapi_secure"
_rc0 = _basename + '_reg_client_0'

d_network_name = 'securedemo'

secured_registry_url = 'https://localhost:18443/nifi-registry-api'
secured_nifi_url = 'https://localhost:8443/nifi-api'

host_certs_path = path.abspath(
    nipyapi.config.PROJECT_ROOT_DIR + "/../tests/resources/keys"
)

tls_env_vars = {
    'AUTH': 'tls',
    'KEYSTORE_PATH': '/opt/certs/localhost-ks.jks',
    'KEYSTORE_TYPE': 'JKS',
    'KEYSTORE_PASSWORD': 'localhostKeystorePassword',
    'TRUSTSTORE_PATH': '/opt/certs/localhost-ts.jks',
    'TRUSTSTORE_PASSWORD': 'localhostTruststorePassword',
    'TRUSTSTORE_TYPE': 'JKS',
    'INITIAL_ADMIN_IDENTITY': 'CN=user1, OU=nifi',
}

ldap_env_vars = {
    'AUTH': 'ldap',
    'KEYSTORE_PATH': '/opt/certs/localhost-ks.jks',
    'KEYSTORE_TYPE': 'JKS',
    'KEYSTORE_PASSWORD': 'localhostKeystorePassword',
    'TRUSTSTORE_PATH': '/opt/certs/localhost-ts.jks',
    'TRUSTSTORE_PASSWORD': 'localhostTruststorePassword',
    'TRUSTSTORE_TYPE': 'JKS',
    'INITIAL_ADMIN_IDENTITY': 'nobel',
    'LDAP_AUTHENTICATION_STRATEGY': 'SIMPLE',
    'LDAP_MANAGER_DN': 'cn=read-only-admin,dc=example,dc=com',
    'LDAP_MANAGER_PASSWORD': 'password',
    'LDAP_USER_SEARCH_BASE': 'dc=example,dc=com',
    'LDAP_USER_SEARCH_FILTER': '(uid={0})',
    'LDAP_IDENTITY_STRATEGY': 'USE_USERNAME',
    'LDAP_URL': 'ldap://ldap.forumsys.com:389',
}

d_containers = [
    DockerContainer(
        name='nipyapi_secure_nifi',
        image_name='chaffelson/nifi',
        image_tag='1.5.0',
        ports={'8443/tcp': 8443},
        env=ldap_env_vars,
        volumes={
            host_certs_path: {'bind': '/opt/certs', 'mode': 'ro'}
        },
    ),
    DockerContainer(
        name='nipyapi_secure_reg',
        image_name='chaffelson/nifi-registry',
        image_tag='0.1.0',
        ports={'18443/tcp': 18443},
        env=tls_env_vars,
        volumes={
            host_certs_path: {'bind': '/opt/certs', 'mode': 'ro'}
        },
    ),
    # TODO update chaffelson/nifi-registry:0.1 image to fix LDAP configuration
    # TODO add ldap docker container.
    # For now this uses a publicly available LDAP test server
]





def get_or_create_registry_access_policy(action, resource):
    """
    Get a Registry access policy for the specified action, resource pair.

    If the access policy does not exist, it will be created.

    :param action: The policy action, e.g., "read", "write", or "delete"
    :param resource: The policy resource, e.g., "/buckets"
    :return: a nypiapi.registry.AccessPolicy object
    """
    resolved_policy = None

    # Strip leading '/' from resource as this lookup endpoint prepends a '/'
    stripped_resource = resource[1:] if resource.startswith('/') else resource

    try:
        policy = nipyapi.registry.PoliciesApi().get_access_policy_for_resource(action, stripped_resource)
        log.debug("Found existing Registry policy for '%s:%s'", action, resource)
        resolved_policy = policy
    except nipyapi.registry.rest.ApiException:
        log.debug("Registry policy for '%s:%s' does not exist, creating...", action, resource)
        policy_to_create = nipyapi.registry.AccessPolicy(
            action=action,
            resource=resource)
        try:
            created_policy = nipyapi.registry.PoliciesApi().create_access_policy(policy_to_create)
            log.debug("Successfully created Registry policy for '%s:%s'", action, resource)
            resolved_policy = created_policy
        except nipyapi.registry.rest.ApiException as e:
            log.warning("Encountered REST API error: %s", e)

    if resolved_policy is not None:
        return resolved_policy
    else:
        log.error("Failed to find or create Registry policy for %s:%s'", action, resource)
        return None


def add_registry_user_to_access_policies(user_identity, access_policies=[]):
    """
    Add a specified user to a list of access policies in the Registry server.

    Access policies in the form [ ('action1', 'resource1'), ('action2', 'resource2'), ... ]

    :param user_identity: the identity of the user to whom you want to give access
    :param access_policies: a list of ('action', 'resource') pairs for the access polices
                            to grant the specified user
    """
    user = nipyapi.security.get_service_user(user_identity, service='registry')

    for policy in access_policies:
        ap = get_or_create_registry_access_policy(policy[0], policy[1])
        if ap is not None:
            # TODO, should probably check that user is not already a member of this access policy
            ap.users.append(user)
            try:
                nipyapi.registry.PoliciesApi().update_access_policy(ap.identifier, ap)
            except nipyapi.registry.rest.ApiException as e:
                log.debug("Encountered REST API error: %s", e)


# def add_nifi_user_to_access_policies(user_identity, access_policies=[],
#                                      read=True, write=True):
#     """
#     Add a specified user to a list of access policies in the NiFi server.
#
#     Access policies in the form [ ('action1', 'resource1'), ('action2', 'resource2'), ... ]
#
#     :param user_identity: the identity of the user to whom you want to give access
#     :param access_policies: a list of ('action', 'resource') pairs for the access polices
#                             to grant the specified user
#     """
#     user = nipyapi.security.get_service_user(user_identity)
#     user_tenant = nipyapi.nifi.TenantEntity(
#         component=nipyapi.nifi.TenantDTO(
#             id=user.component.id,
#             identity=user.component.identity
#         ),
#         permissions=nipyapi.nifi.PermissionsDTO(
#             can_write=write,
#             can_read=read
#         )
#     )
#
#     for policy in access_policies:
#         ap = get_or_create_nifi_access_policy(policy[0], policy[1], policy[2])
#         if ap is not None:
#             # TODO, should probably check that user is not already a member of this access policy
#             ap.component.users.append(user_tenant)
#             try:
#                 nipyapi.nifi.PoliciesApi().update_access_policy(ap.component.id, ap)
#             except nipyapi.nifi.rest.ApiException as e:
#                 log.debug("Encountered REST API error: %s", e)


def connect_nifi_to_registry():
    """
    Add the NiFi server as a trusted client/proxy for the NiFi Registry
    """

    # Add NiFi server identity as user to NiFi Registry
    nifi_proxy = nipyapi.registry.User(identity="CN=localhost, OU=nifi")
    nifi_proxy = nipyapi.registry.TenantsApi().create_user(nifi_proxy)

    # Make NiFi server a trusted proxy in NiFi Registry
    proxy_access_policies = [
        ("write", "/proxy"),
        ("read", "/buckets"),
    ]
    add_registry_user_to_access_policies(nifi_proxy.identity, proxy_access_policies)

    # Add current NiFi user (our NiFi admin) as user to NiFi Registry
    nifi_access_status = nipyapi.nifi.AccessApi().get_access_status()
    nifi_current_user_identity = nifi_access_status.access_status.identity
    nobel_user = nipyapi.registry.User(identity=nifi_current_user_identity)
    nobel_user = nipyapi.registry.TenantsApi().create_user(nobel_user)

    # Make NiFi "nobel" user have access to all buckets in Registry
    all_buckets_access_policies = [
        ("read", "/buckets"),
        ("write", "/buckets"),
        ("delete", "/buckets")
    ]
    add_registry_user_to_access_policies(nifi_current_user_identity, all_buckets_access_policies)


def bootstrap_nifi_access_policies():
    """
    Grant the current nifi user access to the root process group

    Note: Not sure not work with the current LDAP-configured Docker image.
          It may need to be tweaked to configure the ldap-user-group-provider.
    """
    rpg_id = nipyapi.canvas.get_root_pg_id()
    nifi_user_identity = nipyapi.security.get_service_user('nobel')

    access_policies = [
        ('write', 'process-groups', rpg_id),
        ('read', 'process-groups', rpg_id)
    ]
    for pol in access_policies:
        ap = nipyapi.security.create_access_policy(
            resource=pol[1],
            action=pol[0],
            r_id=pol[2],
            service='nifi'
        )
        nipyapi.security.add_user_to_access_policy(
            nifi_user_identity,
            policy=ap,
            service='nifi'
        )


# Uncomment the block below to enable logging
# import nipyapi.config
# nipyapi.config.nifi_config.debug=True
# nipyapi.config.registry_config.debug=True
# root_logger = logging.getLogger()
# root_logger.setLevel(logging.DEBUG)

# connection test disabled as it is not configured with the correct SSLContext
nipyapi.utils.start_docker_containers(
    docker_containers=d_containers,
    network_name=d_network_name
)

log.info("Creating Registry security context")
nipyapi.utils.set_endpoint(secured_registry_url)
nipyapi.security.create_registry_ssl_context(
    ca_file=host_certs_path + '/ca-cert.pem',
    client_cert_file=host_certs_path + '/client-cert.pem',
    client_key_file=host_certs_path + '/client-key.pem',
    client_key_password='clientKeystorePassword'
)
log.debug("Waiting for Registry to be ready for login")
registry_user = nipyapi.utils.wait_to_complete(
    test_function=nipyapi.security.get_registry_access_status,
    bool_response=True,
    nipyapi_delay=5,
    nipyapi_max_wait=60
)
pprint('nipyapi_secured_registry CurrentUser: ' + registry_user.identity)

log.info("Creating NiFi security context")
nipyapi.utils.set_endpoint(secured_nifi_url)
nipyapi.security.create_nifi_ssl_context(
    ca_file=host_certs_path + '/ca-cert.pem'
)
log.debug("Waiting for NiFi to be ready for login")
nipyapi.utils.wait_to_complete(
    test_function=nipyapi.security.login_to_nifi,
    username='nobel',
    password='password',
    bool_response=True,
    nipyapi_delay=5,
    nipyapi_max_wait=60
)
nifi_user = nipyapi.nifi.AccessApi().get_access_status()
pprint('nipyapi_secured_nifi CurrentUser: ' + nifi_user.access_status.identity)

log.info("Granting NiFi user access to root process group")
bootstrap_nifi_access_policies()

log.info("Connecting secured NiFi to secured Registry and granting NiFi user access to Registry")
connect_nifi_to_registry()

log.info("Creating reg_client_0 as NiFi Registry Client named %s", _rc0)
try:
    reg_client_0 = nipyapi.versioning.create_registry_client(
        name=_rc0,
        uri='https://localhost:18443',
        description='NiPyApi Secure Test'
    )
except ValueError:
    reg_client_0 = nipyapi.versioning.get_registry_client(_rc0)

pprint("All Done!")
