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
logging.getLogger('nipyapi.utils').setLevel(logging.INFO)
logging.getLogger('nipyapi.security').setLevel(logging.INFO)
logging.getLogger('nipyapi.versioning').setLevel(logging.INFO)

# Uncomment the block below to enable debug logging
# nipyapi.config.nifi_config.debug=True
# nipyapi.config.registry_config.debug=True
# root_logger = logging.getLogger()
# root_logger.setLevel(logging.DEBUG)


_basename = "nipyapi_secure"
_rc0 = _basename + '_reg_client_0'

d_network_name = 'securedemo'

secured_registry_url = 'https://localhost:18443/nifi-registry-api'
secured_nifi_url = 'https://localhost:8443/nifi-api'

host_certs_path = path.join(
    nipyapi.config.PROJECT_ROOT_DIR,
    "demo/resources/keys"
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
        name='secure-nifi',
        image_name='chaffelson/nifi',
        image_tag='1.5.0',
        ports={'8443/tcp': 8443},
        env=ldap_env_vars,
        volumes={
            host_certs_path: {'bind': '/opt/certs', 'mode': 'ro'}
        },
    ),
    DockerContainer(
        name='secure-registry',
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


def connect_nifi_to_registry():
    """
    Add the NiFi server as a trusted client/proxy for the NiFi Registry
    """

    # Add NiFi server identity as user to NiFi Registry
    # nifi_proxy = nipyapi.registry.User(identity="CN=localhost, OU=nifi")
    # nifi_proxy = nipyapi.registry.TenantsApi().create_user(nifi_proxy)
    nifi_proxy = nipyapi.security.create_service_user(
        identity="CN=localhost, OU=nifi",
        service='registry'
    )

    # Make NiFi server a trusted proxy in NiFi Registry
    proxy_access_policies = [
        ("write", "/proxy"),
        ("read", "/buckets"),
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
            service='registry'
        )
    # add_registry_user_to_access_policies(nifi_proxy.identity,
    #                                      proxy_access_policies)

    # Add current NiFi user (our NiFi admin) as user to NiFi Registry
    nifi_user_obj = nipyapi.security.get_service_user('nobel')
    nifi_reg_user = nipyapi.security.create_service_user(
        identity=nifi_user_obj.component.identity,
        service='registry'
    )
    # nifi_reg_user = nipyapi.registry.TenantsApi().create_user(
    #     nipyapi.registry.User(
    #         identity=nifi_user_obj.component.identity
    #     )
    # )

    # Make NiFi "nobel" user have access to all buckets in Registry
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
        nipyapi.security.add_user_to_access_policy(
            user=nifi_reg_user,
            policy=pol,
            service='registry'
        )


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
            action=pol[0],
            resource=pol[1],
            r_id=pol[2],
            service='nifi'
        )
        nipyapi.security.add_user_to_access_policy(
            nifi_user_identity,
            policy=ap,
            service='nifi'
        )


# connection test disabled as it not configured with the correct SSLContext
log.info("Starting Secured NiFi and NiFi-Registry Docker Containers")
nipyapi.utils.start_docker_containers(
    docker_containers=d_containers,
    network_name=d_network_name
)

log.info("Creating Registry security context")
nipyapi.utils.set_endpoint(secured_registry_url)
log.info("Using demo certs from %s", host_certs_path)
nipyapi.security.set_service_ssl_context(
    service='registry',
    ca_file=path.join(host_certs_path, 'localhost-ts.pem'),
    client_cert_file=path.join(host_certs_path, 'client-cert.pem'),
    client_key_file=path.join(host_certs_path, 'client-key.pem'),
    client_key_password='clientPassword'
)
log.info("Waiting for Registry to be ready for login")
registry_user = nipyapi.utils.wait_to_complete(
    test_function=nipyapi.security.get_service_access_status,
    service='registry',
    bool_response=True,
    nipyapi_delay=nipyapi.config.long_retry_delay,
    nipyapi_max_wait=nipyapi.config.long_max_wait
)
pprint('nipyapi_secured_registry CurrentUser: ' + registry_user.identity)

log.info("Creating NiFi security context")
nipyapi.utils.set_endpoint(secured_nifi_url)
nipyapi.security.set_service_ssl_context(
    service='nifi',
    ca_file=host_certs_path + '/localhost-ts.pem'
)
log.info("Waiting for NiFi to be ready for login")
nipyapi.utils.wait_to_complete(
    test_function=nipyapi.security.service_login,
    service='nifi',
    username='nobel',
    password='password',
    bool_response=True,
    nipyapi_delay=nipyapi.config.long_retry_delay,
    nipyapi_max_wait=nipyapi.config.long_max_wait
)
nifi_user = nipyapi.security.get_service_access_status(service='nifi')
pprint(
    'nipyapi_secured_nifi CurrentUser: ' + nifi_user.access_status.identity
)

log.info("Granting NiFi user access to root process group")
bootstrap_nifi_access_policies()

log.info("Connecting secured NiFi to secured Registry and granting NiFi "
         "user "
         "access to Registry")
connect_nifi_to_registry()

log.info("Creating reg_client_0 as NiFi Registry Client named %s", _rc0)
try:
    reg_client_0 = nipyapi.versioning.create_registry_client(
        name=_rc0,
        uri='https://secure-registry:18443',
        description='NiPyApi Secure Test'
    )
except ValueError:
    reg_client_0 = nipyapi.versioning.get_registry_client(_rc0)

pprint("All Done!")
