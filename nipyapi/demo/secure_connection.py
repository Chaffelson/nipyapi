# coding: utf-8

"""
An implementation helper for connecting to secure NiFi instances.
"""

from __future__ import absolute_import
import logging
from pprint import pprint
from time import sleep
from os import path

from nipyapi import config, registry, nifi
from nipyapi.demo.utils import DockerContainer, start_docker_containers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

d_network_name = 'securedemo'

host_certs_path = path.abspath("../../tests/resources/keys")

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
start_docker_containers(d_containers, d_network_name, test_connection=False)

docker_startup_wait = 60
logging.info("Waiting for docker containers to start "
             "(sleeping {} seconds)...".format(docker_startup_wait))
sleep(docker_startup_wait)  # seconds

logging.info('Attempting connections. '
             'If this fails, try increasing the sleep duration.')

logging.info('Attempting connection to Registry using two-way TLS:')
config.registry_config.host = 'https://localhost:18443/nifi-registry-api'
config.create_registry_ssl_context(
    ca_file=host_certs_path + '/ca-cert.pem',
    client_cert_file=host_certs_path + '/client-cert.pem',
    client_key_file=host_certs_path + '/client-key.pem',
    client_key_password='clientKeystorePassword')
currentUser = registry.AccessApi().get_access_status()
pprint(currentUser)

logging.info('Attempting connection to NiFi using LDAP credentials:')
config.nifi_config.host = 'https://localhost:8443/nifi-api'
config.create_nifi_ssl_context(
    ca_file=host_certs_path + '/ca-cert.pem')
config.login_to_nifi(username='nobel', password='password')
currentUser = nifi.AccessApi().get_access_status()
pprint(currentUser)
