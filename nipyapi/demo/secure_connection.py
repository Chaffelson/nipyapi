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

# connection test disabled as it is not configured with the correct SSLContext
nipyapi.utils.start_docker_containers(
    docker_containers=d_containers,
    network_name=d_network_name
)

log.info("Creating Registry security context")
nipyapi.config.registry_config.host = secured_registry_url
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
nipyapi.config.nifi_config.host = secured_nifi_url
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
pprint("All Done!")
