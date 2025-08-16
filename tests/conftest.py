"""Configuration fixtures for pytest for `nipyapi` package."""

import logging
import pytest
import os
from collections import namedtuple
from time import sleep

import nipyapi
from urllib.parse import urlparse

log = logging.getLogger(__name__)

# Environment-driven test configuration
PROFIlE_DOC = """
Profile controls how tests connect to NiFi and Registry:
  - single-user: HTTPS NiFi with username/password; Registry over HTTP
  - secure-ldap: HTTPS NiFi and Registry with username/password; TLS CA required
  - secure-mtls: HTTPS NiFi and Registry with mutual TLS (client certs)

Defaults are applied for URLs, credentials, and TLS assets suitable for local
Docker-based testing. Environment variables override all defaults.
"""
PROFILE = os.getenv('NIPYAPI_AUTH_MODE', '').strip()

def _flag(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "on")

# Derive test flags from env, defaulting from NIPYAPI_AUTH_MODE when not explicitly set
TEST_SINGLE_USER = _flag('TEST_SINGLE_USER', default=(PROFILE == 'single-user'))
TEST_LDAP = _flag('TEST_LDAP', default=(PROFILE == 'secure-ldap'))
TEST_MTLS = _flag('TEST_MTLS', default=(PROFILE == 'secure-mtls'))
SKIP_TEARDOWN = _flag('SKIP_TEARDOWN', default=False)

# Backward-compatible names used elsewhere in tests
test_ldap = TEST_LDAP
test_mtls = TEST_MTLS

# API endpoints and credentials; env overrides take precedence, otherwise default by NIPYAPI_AUTH_MODE below
NIFI_API_ENDPOINT = os.getenv('NIFI_API_ENDPOINT')
REGISTRY_API_ENDPOINT = os.getenv('REGISTRY_API_ENDPOINT')
NIFI_USERNAME = os.getenv('NIFI_USERNAME')
NIFI_PASSWORD = os.getenv('NIFI_PASSWORD')
REGISTRY_USERNAME = os.getenv('REGISTRY_USERNAME')
REGISTRY_PASSWORD = os.getenv('REGISTRY_PASSWORD')
TLS_CA_CERT_PATH = os.getenv('TLS_CA_CERT_PATH')
NIFI_PROXY_IDENTITY = os.getenv('NIFI_PROXY_IDENTITY', 'C=US, O=NiPyAPI, CN=nifi')
MTLS_CLIENT_CERT = os.getenv('MTLS_CLIENT_CERT')
MTLS_CLIENT_KEY = os.getenv('MTLS_CLIENT_KEY')
MTLS_CLIENT_KEY_PASSWORD = os.getenv('MTLS_CLIENT_KEY_PASSWORD')

# Use only environment variable for CERT_PASSWORD (no file fallback)
CERT_PASSWORD = os.getenv('CERT_PASSWORD', 'changeit')

# ---- Profile helpers -------------------------------------------------------

def _active_profile() -> str:
    """Return one of 'single-user', 'secure-ldap', 'secure-mtls'."""
    if TEST_MTLS:
        return 'secure-mtls'
    if TEST_LDAP:
        return 'secure-ldap'
    return 'single-user'


_PROFILE_DEFAULT_URLS = {
    'single-user': {
        'nifi': 'https://localhost:9443/nifi-api',
        'registry': 'http://localhost:18080/nifi-registry-api',
    },
    'secure-ldap': {
        'nifi': 'https://localhost:9444/nifi-api',
        'registry': 'https://localhost:18444/nifi-registry-api',
    },
    'secure-mtls': {
        'nifi': 'https://localhost:9445/nifi-api',
        'registry': 'https://localhost:18445/nifi-registry-api',
    },
}

# Test Configuration parameters
test_host = nipyapi.config.default_host
test_basename = "nipyapi_test"
test_pg_name = test_basename + "_ProcessGroup"
test_another_pg_name = test_basename + "_AnotherProcessGroup"
test_registry_client_name = test_basename + "_reg_client"
test_processor_name = test_basename + "_proc"
test_bucket_name = test_basename + "_bucket"
test_versioned_flow_name = test_basename + "_ver_flow"
test_cloned_ver_flow_name = test_basename + '_cloned_ver_flow'
test_variable_registry_entry = [
    (test_basename + '_name', test_basename + '_name' + '_value')
]
test_write_file_path = test_basename + '_fs_write_dir'
test_read_file_path = test_basename + '_fs_read_dir'
test_write_file_name = test_basename + '_fs_write_file'
test_ver_export_tmpdir = test_basename + '_ver_flow_dir'
test_ver_export_filename = test_basename + "_ver_flow_export"
test_parameter_context_name = test_basename + "_parameter_context"
test_ssl_controller_name = test_basename + "_ssl_controller"

test_user_name = test_basename + '_user'
test_user_group_name = test_basename + '_user_group'


log.info("Setting up Test Endpoints")

def _apply_global_ca_defaults():
    """Apply a CA bundle usable by both services for one-way TLS.

    If TLS_CA_CERT_PATH is set in the environment, use it. Otherwise, when a
    repo-local test CA exists, adopt it for convenience.
    This does not toggle verification policy; individual setup functions decide.
    """
    if TLS_CA_CERT_PATH:
        nipyapi.config.nifi_config.ssl_ca_cert = TLS_CA_CERT_PATH
        nipyapi.config.registry_config.ssl_ca_cert = TLS_CA_CERT_PATH
    else:
        # For local test convenience, if a repo-local CA exists, adopt it unless explicitly overridden
        local_ca = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'certs', 'client', 'ca.pem')
        if os.path.exists(local_ca):
            nipyapi.config.nifi_config.ssl_ca_cert = local_ca
            nipyapi.config.registry_config.ssl_ca_cert = local_ca


def _ensure_tls_for(service: str, base_url: str):
    """Ensure TLS verification and CA bundle are set for HTTPS URLs.

    - Prefers explicit CA (TLS_CA_CERT_PATH), else uses repo-local CA if present
    - Keeps verification enabled; does not toggle to insecure
    - Only applies to the target service and when base_url uses HTTPS
    """
    assert service in ('nifi', 'registry')
    cfg = nipyapi.config.nifi_config if service == 'nifi' else nipyapi.config.registry_config
    if base_url and base_url.startswith('https://'):
        # If an explicit env was provided earlier, cfg.ssl_ca_cert is already set
        if not getattr(cfg, 'ssl_ca_cert', None):
            local_ca = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'certs', 'client', 'ca.pem')
            if os.path.exists(local_ca):
                cfg.ssl_ca_cert = local_ca
        cfg.verify_ssl = True


def _apply_default_urls():
    """Apply profile-based default URLs when env overrides are not provided."""
    global NIFI_API_ENDPOINT, REGISTRY_API_ENDPOINT
    profile_key = _active_profile()
    defaults = _PROFILE_DEFAULT_URLS[profile_key]
    NIFI_API_ENDPOINT = NIFI_API_ENDPOINT or defaults['nifi']
    REGISTRY_API_ENDPOINT = REGISTRY_API_ENDPOINT or defaults['registry']


_apply_global_ca_defaults()
_apply_default_urls()

# Provide sensible default credentials for supported profiles when not set via env
if _active_profile() == 'secure-ldap':
    NIFI_USERNAME = NIFI_USERNAME or 'einstein'
    NIFI_PASSWORD = NIFI_PASSWORD or 'password'
    REGISTRY_USERNAME = REGISTRY_USERNAME or 'einstein'
    REGISTRY_PASSWORD = REGISTRY_PASSWORD or 'password'
elif _active_profile() == 'single-user':
    NIFI_USERNAME = NIFI_USERNAME or 'einstein'
    NIFI_PASSWORD = NIFI_PASSWORD or 'password1234'
    REGISTRY_USERNAME = REGISTRY_USERNAME or 'einstein'
    REGISTRY_PASSWORD = REGISTRY_PASSWORD or 'password'
 

def _resolve_profile_defaults():
    """Resolve connection defaults for the active NIPYAPI_AUTH_MODE.

    Precedence:
      1) Env vars: URLs, credentials, TLS_CA_CERT_PATH, MTLS_CLIENT_CERT/KEY
      2) Profile defaults (URLs, credentials)
      3) Repo-local TLS assets for secure profiles

    Returns a dict used to configure nipyapi.config and setup handlers.
    """
    profile_key = _active_profile()
    defaults = _PROFILE_DEFAULT_URLS[profile_key]
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    local_ca = os.path.join(repo_root, 'resources', 'certs', 'client', 'ca.pem')
    client_crt = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.crt')
    client_key = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.key')

    nifi_url = NIFI_API_ENDPOINT or defaults['nifi']
    reg_url = REGISTRY_API_ENDPOINT or defaults['registry']

    if profile_key == 'secure-ldap':
        nifi_user = NIFI_USERNAME or 'einstein'
        nifi_pass = NIFI_PASSWORD or 'password'
        reg_user = REGISTRY_USERNAME or 'einstein'
        reg_pass = REGISTRY_PASSWORD or 'password'
    elif profile_key == 'single-user':
        nifi_user = NIFI_USERNAME or 'einstein'
        nifi_pass = NIFI_PASSWORD or 'password1234'
        reg_user = REGISTRY_USERNAME or 'einstein'
        reg_pass = REGISTRY_PASSWORD or 'password'
    else:
        nifi_user = NIFI_USERNAME or ''
        nifi_pass = NIFI_PASSWORD or ''
        reg_user = REGISTRY_USERNAME or (REGISTRY_USERNAME or '')
        reg_pass = REGISTRY_PASSWORD or (REGISTRY_PASSWORD or '')

    ca_path = TLS_CA_CERT_PATH
    if not ca_path and profile_key in ('secure-ldap', 'secure-mtls') and os.path.exists(local_ca):
        ca_path = local_ca

    client_cert = MTLS_CLIENT_CERT or (client_crt if os.path.exists(client_crt) else None)
    key_path = MTLS_CLIENT_KEY or (client_key if os.path.exists(client_key) else None)
    client_key_password = MTLS_CLIENT_KEY_PASSWORD or ''

    return {
        'profile': profile_key,
        'nifi_url': nifi_url,
        'registry_url': reg_url,
        'nifi_user': nifi_user,
        'nifi_pass': nifi_pass,
        'registry_user': reg_user,
        'registry_pass': reg_pass,
        'ca_path': ca_path,
        'client_cert': client_cert,
        'client_key': key_path,
        'client_key_password': client_key_password,
    }
def pytest_generate_tests(metafunc):
    # Single target per profile; no parametrization
    return None


# Note that it's important that the regress function is the first called if
# you are stacking fixtures
@pytest.fixture(scope="function")
def regress_nifi(request):
    # Deprecated; kept as no-op shim during cleanup
    return None


def remove_test_registry_client():
    _ = [nipyapi.versioning.delete_registry_client(li) for
         li in nipyapi.versioning.list_registry_clients().registries
         if test_registry_client_name in li.component.name
         ]


def ensure_registry_client(uri):
    # Compute an internal URI NiFi can reach inside the compose network
    internal_uri = uri
    try:
        parsed = urlparse(uri)
        host = (parsed.hostname or '').lower()
        if host in ('localhost', '127.0.0.1'):
            if TEST_SINGLE_USER:
                internal_uri = 'http://registry-single:18080'
            elif TEST_LDAP:
                internal_uri = 'https://registry-ldap:18443'
            elif TEST_MTLS:
                internal_uri = 'https://registry-mtls:18443'
    except Exception:
        internal_uri = uri

    # Ensure SSL Context Service exists and is enabled when connecting to HTTPS registry
    log.info('ensure_registry_client: target internal URI %s', internal_uri)
    ssl_context = None
    if 'https' in internal_uri:
        ssl_context = nipyapi.canvas.get_controller(test_ssl_controller_name, 'name')
        if ssl_context is None:
            parent_pg = nipyapi.canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id')
            # Use NiFi node keystore (CN=nifi) so Registry authenticates the trusted proxy identity via mTLS
            ks_file = '/certs/nifi/keystore.p12'
            ssl_context = nipyapi.security.create_ssl_context_controller_service(
                parent_pg=parent_pg,
                name=test_ssl_controller_name,
                keystore_file=ks_file,
                keystore_password=CERT_PASSWORD,
                truststore_file='/certs/truststore/truststore.p12',
                truststore_password=CERT_PASSWORD,
                keystore_type='PKCS12', truststore_type='PKCS12',
                ssl_service_type='org.apache.nifi.ssl.StandardSSLContextService'
            )
        try:
            nipyapi.canvas.schedule_controller(ssl_context, scheduled=True, refresh=True)
        except Exception as e:
            # Log validation errors for easier debugging
            try:
                svc = nipyapi.nifi.ControllerServicesApi().get_controller_service(ssl_context.id)
                verrs = getattr(svc.component, 'validation_errors', None)
                log.warning('SSLContextService validation errors: %s', verrs)
            except Exception:
                pass
            raise
    safe_name = test_registry_client_name
    client = None
    try:
        client = nipyapi.versioning.create_registry_client(
            name=safe_name,
            uri=internal_uri,
            description=internal_uri,
            ssl_context_service=ssl_context
        )
    except ValueError as e:
        if 'already exists with the name' in str(e):
            client = nipyapi.versioning.get_registry_client(identifier=safe_name)
        else:
            try:
                clients = nipyapi.versioning.list_registry_clients().registries
                client = next((c for c in clients if getattr(c.component, 'uri', '') == internal_uri), None)
            except Exception:
                client = None

    if not isinstance(client, nipyapi.nifi.FlowRegistryClientEntity):
        raise ValueError("Could not create Registry Client")

    # Ensure properties (url and ssl-context-service) are correct
    try:
        reg_client = nipyapi.nifi.ControllerApi().get_flow_registry_client(client.id)
        comp = reg_client.component.to_dict()
        desc = (reg_client.component.descriptors or {})
        log.info('ensure_registry_client: descriptor keys=%s', list(desc.keys()))
        props = comp.get('properties') or {}
        props['url'] = internal_uri
        if ssl_context is not None:
            props['ssl-context-service'] = ssl_context.id
        comp['properties'] = props
        updated = nipyapi.nifi.ControllerApi().update_flow_registry_client(
            id=reg_client.id,
            body={'component': comp, 'revision': {'version': reg_client.revision.version}}
        )
        client = updated
        # verify properties persisted
        reg_client2 = nipyapi.nifi.ControllerApi().get_flow_registry_client(client.id)
        cur_props = (reg_client2.component.properties or {})
        log.info('ensure_registry_client: persisted props keys=%s', list(cur_props.keys()))
        if 'https' in internal_uri and not cur_props.get('ssl-context-service'):
            log.warning('ensure_registry_client: ssl-context-service not set; retrying property update')
            comp = reg_client2.component.to_dict()
            props = comp.get('properties') or {}
            if ssl_context is not None:
                props['ssl-context-service'] = ssl_context.id
            comp['properties'] = props
            client = nipyapi.nifi.ControllerApi().update_flow_registry_client(
                id=reg_client2.id,
                body={'component': comp, 'revision': {'version': reg_client2.revision.version}}
            )
    except Exception:
        pass

    return client


@pytest.fixture(scope="function")
def regress_flow_reg(request):
    # Deprecated; kept as no-op shim during cleanup
    return None


def _setup_nifi_single_user():
    _ensure_tls_for('nifi', NIFI_API_ENDPOINT or '')
    nipyapi.utils.set_endpoint(NIFI_API_ENDPOINT, True, True, NIFI_USERNAME, NIFI_PASSWORD)


def _setup_nifi_secure_ldap():
    # LDAP behaves the same as single-user for client auth (username/password)
    _setup_nifi_single_user()


def _setup_nifi_secure_mtls():
    # Ensure CA and client certs are configured for mTLS
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    local_ca = os.path.join(repo_root, 'resources', 'certs', 'client', 'ca.pem')
    client_crt = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.crt')
    client_key = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.key')
    if TLS_CA_CERT_PATH or os.path.exists(local_ca):
        nipyapi.config.nifi_config.verify_ssl = True
        nipyapi.config.nifi_config.ssl_ca_cert = TLS_CA_CERT_PATH or local_ca
    # Prefer env-provided client certs; otherwise use repo-local test certs
    cert_path = MTLS_CLIENT_CERT if MTLS_CLIENT_CERT else (client_crt if os.path.exists(client_crt) else None)
    key_path = MTLS_CLIENT_KEY if MTLS_CLIENT_KEY else (client_key if os.path.exists(client_key) else None)
    if cert_path and key_path:
        nipyapi.config.nifi_config.cert_file = cert_path
        nipyapi.config.nifi_config.key_file = key_path
    nipyapi.utils.set_endpoint(NIFI_API_ENDPOINT, True, False)


def _setup_registry_single_user():
    _ensure_tls_for('registry', REGISTRY_API_ENDPOINT or '')
    nipyapi.utils.set_endpoint(REGISTRY_API_ENDPOINT, True, True, REGISTRY_USERNAME, REGISTRY_PASSWORD)


def _setup_registry_secure_ldap():
    _setup_registry_single_user()


def _setup_registry_secure_mtls():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    local_ca = os.path.join(repo_root, 'resources', 'certs', 'client', 'ca.pem')
    client_crt = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.crt')
    client_key = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.key')
    if TLS_CA_CERT_PATH or os.path.exists(local_ca):
        nipyapi.config.registry_config.verify_ssl = True
        nipyapi.config.registry_config.ssl_ca_cert = TLS_CA_CERT_PATH or local_ca
    cert_path = MTLS_CLIENT_CERT if MTLS_CLIENT_CERT else (client_crt if os.path.exists(client_crt) else None)
    key_path = MTLS_CLIENT_KEY if MTLS_CLIENT_KEY else (client_key if os.path.exists(client_key) else None)
    if cert_path and key_path:
        nipyapi.config.registry_config.cert_file = cert_path
        nipyapi.config.registry_config.key_file = key_path
    nipyapi.utils.set_endpoint(REGISTRY_API_ENDPOINT, True, False)


_NIFI_SETUP_MAP = {
    'single-user': _setup_nifi_single_user,
    'secure-ldap': _setup_nifi_secure_ldap,
    'secure-mtls': _setup_nifi_secure_mtls,
}

_REGISTRY_SETUP_MAP = {
    'single-user': _setup_registry_single_user,
    'secure-ldap': _setup_registry_secure_ldap,
    'secure-mtls': _setup_registry_secure_mtls,
}


def _wait_until_service_up(gui_url: str):
    if not nipyapi.utils.wait_to_complete(
        nipyapi.utils.is_endpoint_up,
        gui_url,
        nipyapi_delay=nipyapi.config.long_retry_delay,
        nipyapi_max_wait=nipyapi.config.long_max_wait):
        pytest.exit(f"Expected Service endpoint ({gui_url}) is not responding")


# Tests that the Docker test environment is available before running test suite
@pytest.fixture(scope="session", autouse=True)
def session_setup(request):
    log.info("Commencing test session setup")
    # Resolve effective connection defaults from env + profile
    resolved = _resolve_profile_defaults()
    profile_key = resolved['profile']
    # Apply CA bundle to both configs if present
    if resolved['ca_path']:
        nipyapi.config.nifi_config.ssl_ca_cert = resolved['ca_path']
        nipyapi.config.registry_config.ssl_ca_cert = resolved['ca_path']
    # Apply mTLS client certs for secure-mtls
    if profile_key == 'secure-mtls':
        if resolved['client_cert'] and resolved['client_key']:
            nipyapi.config.nifi_config.cert_file = resolved['client_cert']
            nipyapi.config.nifi_config.key_file = resolved['client_key']
        if resolved['client_cert'] and resolved['client_key']:
            nipyapi.config.registry_config.cert_file = resolved['client_cert']
            nipyapi.config.registry_config.key_file = resolved['client_key']
    # Stabilize module-level globals for downstream calls
    global NIFI_API_ENDPOINT, REGISTRY_API_ENDPOINT, NIFI_USERNAME, NIFI_PASSWORD, REGISTRY_USERNAME, REGISTRY_PASSWORD
    NIFI_API_ENDPOINT = resolved['nifi_url']
    REGISTRY_API_ENDPOINT = resolved['registry_url']
    NIFI_USERNAME = resolved['nifi_user']
    NIFI_PASSWORD = resolved['nifi_pass']
    REGISTRY_USERNAME = resolved['registry_user']
    REGISTRY_PASSWORD = resolved['registry_pass']

    # NiFi setup and readiness
    _NIFI_SETUP_MAP[profile_key]()
    _wait_until_service_up(NIFI_API_ENDPOINT.replace('-api', ''))
    if not nipyapi.canvas.get_root_pg_id():
        raise ValueError("No Response from NiFi test call")
    if profile_key in ('secure-ldap', 'secure-mtls'):
        try:
            nipyapi.security.bootstrap_security_policies(service='nifi')
        except Exception:
            pass
    cleanup_nifi()

    # Registry setup and readiness
    _REGISTRY_SETUP_MAP[profile_key]()
    _wait_until_service_up(REGISTRY_API_ENDPOINT.replace('-api', ''))
    _ = nipyapi.system.get_registry_version_info()
    try:
        # Baseline registry bootstrap handles proxy and global bucket policies
        nipyapi.security.bootstrap_security_policies(
            service='registry', nifi_proxy_identity=NIFI_PROXY_IDENTITY
        )
    except Exception:
        pass
    cleanup_reg()

    # Ensure a registry client exists for secure profiles
    if profile_key == 'secure-ldap':
        _ = ensure_registry_client('https://registry-ldap:18443')
    elif profile_key == 'secure-mtls':
        _ = ensure_registry_client('https://registry-mtls:18443')

    request.addfinalizer(final_cleanup)
    log.info("Completing Test Session Setup")


def remove_test_templates():
    # Templates are not supported in NiFi 2.x and the feature is removed from NiPyAPI
    return None


def remove_test_pgs():
    if SKIP_TEARDOWN:
        return None
    _ = [
        nipyapi.canvas.delete_process_group(x, True, True)
        for x in nipyapi.nifi.ProcessGroupsApi().get_process_groups('root').process_groups
        if test_basename in x.status.name
    ]


def remove_test_processors():
    if SKIP_TEARDOWN:
        return None
    _ = [
        nipyapi.canvas.delete_processor(x, force=True)
        for x in nipyapi.canvas.list_all_processors()
        if test_basename in x.status.name
    ]


def remove_test_funnels():
    if SKIP_TEARDOWN:
        return None
    # Note that Funnels cannot be given labels so scoping is by PG only
    remove_test_connections()
    _ = [
        nipyapi.canvas.delete_funnel(x)
        for x in nipyapi.canvas.list_all_funnels()
    ]


def remove_test_parameter_contexts():
    if SKIP_TEARDOWN:
        return None
    if nipyapi.utils.check_version('1.10.0') < 1:
        _ = [
            nipyapi.parameters.delete_parameter_context(li) for li
            in nipyapi.parameters.list_all_parameter_contexts() if
            test_basename in li.component.name
        ]
    else:
        log.info("NiFi version is older than 1.10, skipping Parameter Context cleanup")


def remove_test_buckets():
    if SKIP_TEARDOWN:
        return None
    _ = [nipyapi.versioning.delete_registry_bucket(li) for li
         in nipyapi.versioning.list_registry_buckets() if
         test_bucket_name in li.name]


def final_cleanup():
    if SKIP_TEARDOWN:
        log.info("SKIP_TEARDOWN is true; skipping final cleanup")
        return None
    # Cleanup NiFi using the existing authenticated session
    cleanup_nifi()
    if (test_ldap or test_mtls) and 'https' in NIFI_API_ENDPOINT:
        remove_test_service_user_groups('nifi')
        remove_test_service_users('nifi')
        remove_test_controllers(include_reporting_tasks=True)
    # Cleanup Registry using the existing authenticated session
    cleanup_reg()
    if (test_ldap or test_mtls) and 'https' in REGISTRY_API_ENDPOINT:
        remove_test_service_user_groups('registry')
        remove_test_service_users('registry')


def remove_test_service_users(service='both'):
    if SKIP_TEARDOWN:
        return None
    if service == 'nifi' or service == 'both':
        _ = [
            nipyapi.security.remove_service_user(x, 'nifi')
            for x in
            nipyapi.security.list_service_users('nifi')
            if x.component.identity.startswith(test_basename)
        ]
    if service == 'registry' or service == 'both':
        _ = [
            nipyapi.security.remove_service_user(x, 'registry')
            for x in
            nipyapi.security.list_service_users('registry')
            if x.identity.startswith(test_basename)
        ]


def remove_test_service_user_groups(service='both'):
    if SKIP_TEARDOWN:
        return None
    if service == 'nifi' or service == 'both':
        _ = [
            nipyapi.security.remove_service_user_group(x, 'nifi') for x in
            nipyapi.security.list_service_user_groups('nifi')
            if x.component.identity.startswith(test_basename)
        ]
    if service == 'registry' or service == 'both':
        _ = [
            nipyapi.security.remove_service_user_group(x, 'registry') for x in
            nipyapi.security.list_service_user_groups('registry')
            if x.identity.startswith(test_basename)
        ]


def cleanup_nifi():
    if SKIP_TEARDOWN:
        log.info("SKIP_TEARDOWN is true; skipping cleanup_nifi")
        return None
    # Only bulk-cleanup universally compatible components
    # Ideally we would clean each test environment, but it's too slow to do it
    # per test, so we rely on individual fixture cleanup
    log.info("Bulk cleanup called on host %s",
             nipyapi.config.nifi_config.host)
    # Check if NiFi version is 2 or newer
    if nipyapi.utils.check_version('2', service='nifi') == 1:  # We're on an older version
        remove_test_templates()
    remove_test_pgs()
    remove_test_connections()
    remove_test_controllers()
    remove_test_processors()
    remove_test_ports()
    remove_test_funnels()
    remove_test_rpgs()
    remove_test_parameter_contexts()

def remove_test_rpgs():
    if SKIP_TEARDOWN:
        return None
    _ = [
        nipyapi.canvas.delete_remote_process_group(x)
        for x in nipyapi.canvas.list_all_remote_process_groups()
    ]


def remove_test_connections():
    if SKIP_TEARDOWN:
        return None
    # Funnels don't have a name, have to go by type
    _ = [
        nipyapi.canvas.delete_connection(x, True)
        for x in nipyapi.canvas.list_all_connections()
        if x.destination_type == 'FUNNEL'
        or x.source_type == 'FUNNEL'
        or test_basename in x.component.name
    ]


def remove_test_ports():
    if SKIP_TEARDOWN:
        return None
    _ = [
        nipyapi.canvas.delete_port(x)
        for x in nipyapi.canvas.list_all_by_kind('input_ports')
        if test_basename in x.component.name
    ]
    _ = [
        nipyapi.canvas.delete_port(x)
        for x in nipyapi.canvas.list_all_by_kind('output_ports')
        if test_basename in x.component.name
    ]


def remove_test_controllers(include_reporting_tasks=False):
    if SKIP_TEARDOWN:
        return None
    _ = [nipyapi.canvas.delete_controller(li, True) for li
         in nipyapi.canvas.list_all_controllers(include_reporting_tasks=include_reporting_tasks) if
         test_basename in li.component.name]


def cleanup_reg():
    if SKIP_TEARDOWN:
        log.info("SKIP_TEARDOWN is true; skipping cleanup_reg")
        return None
    # Bulk cleanup for tests involving NiFi Registry
    remove_test_pgs()
    remove_test_buckets()
    if (test_ldap or test_mtls) and 'https' in nipyapi.registry.configuration.host:
        remove_test_service_user_groups('registry')
        remove_test_service_users('registry')


@pytest.fixture(name='fix_templates', scope='function')
def fixture_templates(request, fix_pg):
    # Legacy fixture removed; keep a stub so parametrized tests won’t break during transition
    request.addfinalizer(remove_test_templates)
    return None


@pytest.fixture(name='fix_pg')
def fixture_pg(request):
    class Dummy:
        def __init__(self):
            pass

        def generate(self, parent_pg=None, suffix=''):
            if parent_pg is None:
                target_pg = nipyapi.canvas.get_process_group(
                    nipyapi.canvas.get_root_pg_id(), 'id'
                )
            else:
                target_pg = parent_pg
            return nipyapi.canvas.create_process_group(
                    target_pg,
                    test_pg_name + suffix,
                    location=(400.0, 400.0)
                )

    request.addfinalizer(remove_test_pgs)
    return Dummy()


@pytest.fixture(name='fix_proc')
def fixture_proc(request):
    class Dummy:
        def __init__(self):
            pass

        def generate(self, parent_pg=None, suffix='', kind=None, config=None):
            if parent_pg is None:
                target_pg = nipyapi.canvas.get_process_group(
                    nipyapi.canvas.get_root_pg_id(), 'id'
                )
            else:
                target_pg = parent_pg
            kind = kind if kind else 'GenerateFlowFile'
            return nipyapi.canvas.create_processor(
                parent_pg=target_pg,
                processor=nipyapi.canvas.get_processor_type(
                    kind),
                location=(400.0, 400.0),
                name=test_processor_name + suffix,
                config=nipyapi.nifi.ProcessorConfigDTO(
                    scheduling_period='1s',
                    auto_terminated_relationships=['success']
                )
            )

    request.addfinalizer(remove_test_processors)
    return Dummy()


@pytest.fixture(name='fix_context')
def fixture_context(request):
    class Dummy:
        def __init__(self):
            pass

        def generate(self, name=test_parameter_context_name):
            return nipyapi.parameters.create_parameter_context(name)

    request.addfinalizer(remove_test_parameter_contexts)
    return Dummy()


@pytest.fixture(name='fix_funnel')
def fixture_funnel(request):
    class Dummy:
        def __init__(self):
            pass

        def generate(self, parent_pg=None, position=(400, 400)):
            if parent_pg is None:
                target_pg = nipyapi.canvas.get_process_group(
                    nipyapi.canvas.get_root_pg_id(), 'id'
                )
            else:
                target_pg = parent_pg
            return nipyapi.canvas.create_funnel(target_pg.id, position)

    request.addfinalizer(remove_test_funnels)
    return Dummy()


@pytest.fixture(name='fix_bucket', scope='function')
def fixture_bucket(request):
    class Dummy:
        def __init__(self):
            pass

        def __call__(self, name=test_bucket_name, suffix=''):
            target_name = name + suffix
            try:
                return nipyapi.versioning.create_registry_bucket(target_name)
            except ValueError as e:
                if 'already exists' in str(e):
                    # Reuse existing bucket by name
                    buckets = nipyapi.versioning.list_registry_buckets()
                    for b in buckets:
                        if b.name == target_name:
                            return b
                raise
    request.addfinalizer(remove_test_buckets)
    return Dummy()


@pytest.fixture(name='fix_ver_flow', scope='function')
def fixture_ver_flow(request, fix_bucket, fix_pg, fix_proc):
    log.info("Starting setup of Fixture fix_ver_flow")
    FixtureVerFlow = namedtuple(
        'FixtureVerFlow', ('client', 'bucket', 'pg', 'proc', 'info',
                           'flow', 'snapshot', 'dto')
    )
    f_reg_client = ensure_registry_client(REGISTRY_API_ENDPOINT)
    assert f_reg_client is not None
    f_pg = fix_pg.generate()
    f_bucket = fix_bucket()
    f_proc = fix_proc.generate(parent_pg=f_pg)
    f_info = nipyapi.versioning.save_flow_ver(
            process_group=f_pg,
            registry_client=f_reg_client,
            bucket=f_bucket,
            flow_name=test_versioned_flow_name,
            comment='NiPyApi Test',
            desc='NiPyApi Test'
        )
    sleep(0.5)
    f_flow = nipyapi.versioning.get_flow_in_bucket(
            bucket_id=f_bucket.identifier,
            identifier=f_info.version_control_information.flow_id,
            identifier_type='id'
        )
    f_snapshot = nipyapi.versioning.get_latest_flow_ver(
        f_bucket.identifier,
        f_flow.identifier
    )
    f_dto = ('registry', 'VersionedFlowSnapshot')
    request.addfinalizer(cleanup_reg)
    log.info("Finished setting up Fixture fix_ver_flow")
    return FixtureVerFlow(
        client=f_reg_client,
        bucket=f_bucket,
        pg=f_pg,
        proc=f_proc,
        info=f_info,
        flow=f_flow,
        snapshot=f_snapshot,
        dto=f_dto
    )


@pytest.fixture(name='fix_flow_serde', scope='function')
def fixture_flow_serde(request, tmpdir, fix_ver_flow):
    FixtureFlowSerde = namedtuple(
        'FixtureFlowSerde',
        getattr(fix_ver_flow, '_fields') + ('filepath', 'json', 'yaml', 'raw')
    )
    f_filepath = str(tmpdir.mkdir(test_ver_export_tmpdir)
                     .join(test_ver_export_filename))
    f_raw = nipyapi.versioning.get_flow_version(
        bucket_id=fix_ver_flow.bucket.identifier,
        flow_id=fix_ver_flow.flow.identifier,
        export=True
    )
    f_json = nipyapi.versioning.export_flow_version(
        bucket_id=fix_ver_flow.bucket.identifier,
        flow_id=fix_ver_flow.flow.identifier,
        file_path=f_filepath + '.json',
        mode='json'
    )
    f_yaml = nipyapi.versioning.export_flow_version(
        bucket_id=fix_ver_flow.bucket.identifier,
        flow_id=fix_ver_flow.flow.identifier,
        file_path=f_filepath + '.yaml',
        mode='yaml'
    )
    request.addfinalizer(cleanup_reg)
    return FixtureFlowSerde(
        *fix_ver_flow,
        filepath=f_filepath,
        json=f_json,
        yaml=f_yaml,
        raw=f_raw
    )


@pytest.fixture(name='fix_cont', scope='function')
def fixture_controller(request):
    class Dummy:
        def __init__(self):
            pass

        def __call__(self, parent_pg=None, kind=None):
            if parent_pg is None:
                target_pg = nipyapi.canvas.get_process_group(
                    nipyapi.canvas.get_root_pg_id(), 'id'
                )
            else:
                target_pg = parent_pg
            kind = kind if kind else 'CSVReader'
            cont_type = [
                x for x in nipyapi.canvas.list_all_controller_types()
                if kind in x.type
            ][0]
            c_1 = nipyapi.canvas.create_controller(
                parent_pg=target_pg,
                controller=cont_type
            )
            c_2 = nipyapi.canvas.update_controller(
                c_1,
                nipyapi.nifi.ControllerServiceDTO(
                    name=test_basename + c_1.component.name
                )
            )
            return c_2

    request.addfinalizer(remove_test_controllers)
    return Dummy()


@pytest.fixture(name='fix_users', scope='function')
def fixture_users(request):
    class Dummy:
        def __init__(self):
            pass

        def __call__(self, name=test_user_name, suffix=''):
            return (
                nipyapi.security.create_service_user(name + suffix),
                nipyapi.security.create_service_user(name + suffix, 'registry')
            )
    request.addfinalizer(remove_test_service_users)
    return Dummy()


@pytest.fixture(name='fix_user_groups', scope='function')
def fixture_user_groups(request, fix_users):
    class Dummy:
        def __init__(self):
            pass

        def __call__(self, name=test_user_group_name, suffix=''):
            n_user, r_user = fix_users()
            return (
                nipyapi.security.create_service_user_group(
                    name + suffix, service='nifi', users=[n_user]),
                nipyapi.security.create_service_user_group(
                    name + suffix, service='registry', users=[r_user])
            )
    request.addfinalizer(remove_test_service_user_groups)
    return Dummy()
