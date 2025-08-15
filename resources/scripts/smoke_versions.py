#!/usr/bin/env python
import os
import sys
import nipyapi


def main() -> int:
    nifi = os.getenv('NIFI_API_ENDPOINT')
    reg = os.getenv('REGISTRY_API_ENDPOINT')
    if not nifi or not reg:
        print('ERROR: NIFI_API_ENDPOINT and REGISTRY_API_ENDPOINT must be set')
        return 2

    # Respect CA bundle if provided
    ca = os.getenv('TLS_CA_CERT_PATH') or os.getenv('REQUESTS_CA_BUNDLE')
    if ca:
        nipyapi.config.nifi_config.ssl_ca_cert = ca
        nipyapi.config.registry_config.ssl_ca_cert = ca
        nipyapi.config.nifi_config.verify_ssl = True
        nipyapi.config.registry_config.verify_ssl = True

    # If basic auth creds provided, set them; otherwise let calls run unauthenticated
    n_user = os.getenv('NIFI_USERNAME')
    n_pass = os.getenv('NIFI_PASSWORD')
    r_user = os.getenv('REGISTRY_USERNAME')
    r_pass = os.getenv('REGISTRY_PASSWORD')
    if n_user:
        nipyapi.config.nifi_config.username = n_user
    if n_pass:
        nipyapi.config.nifi_config.password = n_pass
    if r_user:
        nipyapi.config.registry_config.username = r_user
    if r_pass:
        nipyapi.config.registry_config.password = r_pass

    # Configure mTLS if certs provided (login=False pattern)
    crt = os.getenv('MTLS_CLIENT_CERT')
    key = os.getenv('MTLS_CLIENT_KEY')
    key_pw = os.getenv('MTLS_CLIENT_KEY_PASSWORD')
    if crt and key:
        nipyapi.config.nifi_config.cert_file = crt
        nipyapi.config.nifi_config.key_file = key
        nipyapi.config.nifi_config.key_password = key_pw or None
        nipyapi.config.registry_config.cert_file = crt
        nipyapi.config.registry_config.key_file = key
        nipyapi.config.registry_config.key_password = key_pw or None

    # Establish endpoints (authenticate if creds provided)
    try:
        nipyapi.utils.set_endpoint(nifi, ssl=nifi.startswith('https://'), login=bool(n_user or n_pass))
        nipyapi.utils.set_endpoint(reg, ssl=reg.startswith('https://'), login=bool(r_user or r_pass))
    except Exception as e:
        print('set_endpoint_error=', str(e).split('\n')[0])
        return 3

    # Version probes (should not require policy bootstrap)
    try:
        nv = nipyapi.system.get_nifi_version_info()
        print('nifi_version=', getattr(nv, 'ni_fi_version', nv))
    except Exception as e:
        print('nifi_version_error=', str(e).split('\n')[0])
        return 4
    try:
        rv = nipyapi.system.get_registry_version_info()
        print('registry_version=', rv)
    except Exception as e:
        print('registry_version_error=', str(e).split('\n')[0])
        return 5
    return 0


if __name__ == '__main__':
    sys.exit(main())


