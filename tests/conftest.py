"""Configuration fixtures for pytest for `nipyapi` package."""

import logging
import pytest
import os
from collections import namedtuple

import nipyapi

log = logging.getLogger(__name__)

# Environment-driven test configuration
PROFIlE_DOC = """
Profile controls how tests connect to NiFi and Registry:
  - single-user: HTTPS NiFi with username/password; Registry over HTTP (default)
  - secure-ldap: HTTPS NiFi and Registry with username/password; TLS CA required
  - secure-mtls: HTTPS NiFi and Registry with mutual TLS (client certs)
  - secure-oidc: HTTPS NiFi with OIDC + basic Registry (requires manual setup)

Defaults are applied for URLs, credentials, and TLS assets suitable for local
Docker-based testing. Environment variables override all defaults.
"""
ACTIVE_PROFILE = os.getenv('NIPYAPI_AUTH_MODE', 'single-user').strip()

# Validate profile early and fail fast
if ACTIVE_PROFILE not in ('single-user', 'secure-ldap', 'secure-mtls', 'secure-oidc'):
    raise ValueError(f"Invalid NIPYAPI_AUTH_MODE: {ACTIVE_PROFILE}. Must be one of: single-user, secure-ldap, secure-mtls, secure-oidc")

def _flag(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "on")

SKIP_TEARDOWN = _flag('SKIP_TEARDOWN', default=False)


# ---- Profile Configuration ------------------------------------------------

# All profile defaults in one place - URLs, credentials, internal URLs
test_conf = {
    'single-user': {
        'nifi_url': 'https://localhost:9443/nifi-api',
        'registry_url': 'http://localhost:18080/nifi-registry-api',
        'registry_internal_url': 'http://registry-single:18080',
        'nifi_user': 'einstein',
        'nifi_pass': 'password1234',
        'registry_user': 'einstein',
        'registry_pass': 'password1234',
    },
    'secure-ldap': {
        'nifi_url': 'https://localhost:9444/nifi-api',
        'registry_url': 'https://localhost:18444/nifi-registry-api',
        'registry_internal_url': 'https://registry-ldap:18443',
        'nifi_user': 'einstein',
        'nifi_pass': 'password',
        'registry_user': 'einstein',
        'registry_pass': 'password',
    },
    'secure-mtls': {
        'nifi_url': 'https://localhost:9445/nifi-api',
        'registry_url': 'https://localhost:18445/nifi-registry-api',
        'registry_internal_url': 'https://registry-mtls:18443',
        'nifi_user': '',
        'nifi_pass': '',
        'registry_user': '',
        'registry_pass': '',
    },
    'secure-oidc': {
        'nifi_url': 'https://localhost:9446/nifi-api',
        'registry_url': 'http://localhost:18446/nifi-registry-api',
        'registry_internal_url': 'http://registry-oidc:18080',
        'nifi_user': 'einstein',
        'nifi_pass': 'password1234',
        'registry_user': 'einstein',
        'registry_pass': 'password1234',
    },
}

# Session-resolved configuration (set once during session_setup)
active_config = None


def _resolve_active_config():
    """Resolve the active configuration for the current session.

    Applies env var overrides to profile defaults and adds computed paths.
    Sets the global active_config for use throughout the session.
    """
    global active_config

    # Start with profile defaults
    profile_defaults = test_conf[ACTIVE_PROFILE]
    active_config = profile_defaults.copy()

    # Apply environment variable overrides
    active_config['nifi_url'] = os.getenv('NIFI_API_ENDPOINT') or active_config['nifi_url']
    active_config['registry_url'] = os.getenv('REGISTRY_API_ENDPOINT') or active_config['registry_url']
    active_config['nifi_user'] = os.getenv('NIFI_USERNAME') or active_config['nifi_user']
    active_config['nifi_pass'] = os.getenv('NIFI_PASSWORD') or active_config['nifi_pass']
    active_config['registry_user'] = os.getenv('REGISTRY_USERNAME') or active_config['registry_user']
    active_config['registry_pass'] = os.getenv('REGISTRY_PASSWORD') or active_config['registry_pass']

    # Add computed certificate paths
    repo_root = os.path.dirname(nipyapi.config.PROJECT_ROOT_DIR)
    local_ca = os.path.join(repo_root, 'resources', 'certs', 'client', 'ca.pem')
    client_crt = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.crt')
    client_key = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.key')

    # Certificate paths with env var overrides and fallbacks
    active_config['ca_path'] = os.getenv('TLS_CA_CERT_PATH')
    # All profiles use our generated CA for localhost HTTPS connections
    if not active_config['ca_path'] and os.path.exists(local_ca):
        active_config['ca_path'] = local_ca

    active_config['client_cert'] = os.getenv('MTLS_CLIENT_CERT') or (client_crt if os.path.exists(client_crt) else None)
    active_config['client_key'] = os.getenv('MTLS_CLIENT_KEY') or (client_key if os.path.exists(client_key) else None)
    active_config['client_key_password'] = os.getenv('MTLS_CLIENT_KEY_PASSWORD') or ''

    # Security configuration
    active_config['nifi_proxy_identity'] = os.getenv('NIFI_PROXY_IDENTITY', 'C=US, O=NiPyAPI, CN=nifi')

    # Add profile for reference
    active_config['profile'] = ACTIVE_PROFILE


# Test Configuration parameters
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


def remove_test_registry_client():
    _ = [nipyapi.versioning.delete_registry_client(li) for
         li in nipyapi.versioning.list_registry_clients().registries
         if test_registry_client_name in li.component.name
         ]


def _setup_nifi_single_user():
    # SSL configuration (including verification) already applied in session_setup
    nipyapi.utils.set_endpoint(active_config['nifi_url'], True, True, active_config['nifi_user'], active_config['nifi_pass'])


def _setup_nifi_secure_ldap():
    # LDAP behaves the same as single-user for client auth (username/password)
    _setup_nifi_single_user()


def _setup_nifi_secure_mtls():
    # Apply certificates (CA cert and SSL verification already applied in session_setup)
    if active_config['client_cert'] and active_config['client_key']:
        nipyapi.config.nifi_config.cert_file = active_config['client_cert']
        nipyapi.config.nifi_config.key_file = active_config['client_key']

    nipyapi.utils.set_endpoint(active_config['nifi_url'], True, False)


def _setup_nifi_secure_oidc():
    # SSL configuration (including verification) already applied in session_setup

    # Configure host endpoint without login (OIDC uses bearer tokens)
    nipyapi.config.nifi_config.host = active_config['nifi_url'].rstrip('/')
    nipyapi.config.nifi_config.api_client = None  # Force new client creation

    # Use the standard OIDC login function
    nipyapi.security.service_login_oidc(
        service='nifi',
        username=active_config['nifi_user'],
        password=active_config['nifi_pass'],
        oidc_token_endpoint='http://localhost:8080/realms/nipyapi/protocol/openid-connect/token',
        client_id='nipyapi-client',
        client_secret='nipyapi-secret'
    )


def _setup_registry_single_user():
    # SSL configuration (including verification) already applied in session_setup
    nipyapi.utils.set_endpoint(active_config['registry_url'], True, True, active_config['registry_user'], active_config['registry_pass'])


def _setup_registry_secure_ldap():
    _setup_registry_single_user()


def _setup_registry_secure_mtls():
    # Apply certificates (CA cert and SSL verification already applied in session_setup)
    if active_config['client_cert'] and active_config['client_key']:
        nipyapi.config.registry_config.cert_file = active_config['client_cert']
        nipyapi.config.registry_config.key_file = active_config['client_key']

    nipyapi.utils.set_endpoint(active_config['registry_url'], True, False)


def _setup_registry_secure_oidc():
    # OIDC Registry uses single-user mode (basic auth)
    _setup_registry_single_user()


_NIFI_SETUP_MAP = {
    'single-user': _setup_nifi_single_user,
    'secure-ldap': _setup_nifi_secure_ldap,
    'secure-mtls': _setup_nifi_secure_mtls,
    'secure-oidc': _setup_nifi_secure_oidc,
}

_REGISTRY_SETUP_MAP = {
    'single-user': _setup_registry_single_user,
    'secure-ldap': _setup_registry_secure_ldap,
    'secure-mtls': _setup_registry_secure_mtls,
    'secure-oidc': _setup_registry_secure_oidc,
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
    # Resolve configuration once for the entire session
    _resolve_active_config()
    # Apply CA bundle to both configs if present
    if active_config['ca_path']:
        nipyapi.security.set_shared_ca_cert(active_config['ca_path'])

    # Enable SSL verification for HTTPS endpoints (we provide CA certs for verification)
    if active_config['nifi_url'] and active_config['nifi_url'].startswith('https://'):
        nipyapi.config.nifi_config.verify_ssl = True
    if active_config['registry_url'] and active_config['registry_url'].startswith('https://'):
        nipyapi.config.registry_config.verify_ssl = True

    # Apply all SSL configuration changes once
    nipyapi.security.apply_ssl_configuration()

    # NiFi setup and readiness
    if ACTIVE_PROFILE == 'secure-mtls':
        _NIFI_SETUP_MAP[ACTIVE_PROFILE]()
    else:
        _NIFI_SETUP_MAP[ACTIVE_PROFILE]()
    _wait_until_service_up(active_config['nifi_url'].replace('-api', ''))
    if not nipyapi.canvas.get_root_pg_id():
        raise ValueError("No Response from NiFi test call")
    if ACTIVE_PROFILE in ('secure-ldap', 'secure-mtls', 'secure-oidc'):
        try:
            nipyapi.security.bootstrap_security_policies(service='nifi')
            log.info("NiFi security policies bootstrapped for %s profile", ACTIVE_PROFILE)
        except Exception as e:
            log.warning("Security policy bootstrap failed (environment may need setup): %s", e)
            if ACTIVE_PROFILE == 'secure-oidc':
                log.info("For OIDC: Run 'make sandbox NIPYAPI_AUTH_MODE=secure-oidc' first")
            raise
    cleanup_nifi()

    # Registry setup and readiness
    if ACTIVE_PROFILE == 'secure-mtls':
        _REGISTRY_SETUP_MAP[ACTIVE_PROFILE]()
    else:
        _REGISTRY_SETUP_MAP[ACTIVE_PROFILE]()
    _wait_until_service_up(active_config['registry_url'].replace('-api', ''))
    try:
        # Baseline registry bootstrap handles proxy and global bucket policies
        nipyapi.security.bootstrap_security_policies(
            service='registry', nifi_proxy_identity=active_config['nifi_proxy_identity']
        )
    except Exception:
        pass
    cleanup_reg()

    # Ensure a registry client exists for all profiles (uses global SSL config)
    _ = nipyapi.versioning.ensure_registry_client(
        name=test_registry_client_name,
        uri=active_config['registry_internal_url'],
        description=f"Test Registry Client -> {active_config['registry_internal_url']}"
    )

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
    if ACTIVE_PROFILE in ('secure-ldap', 'secure-mtls') and 'https' in active_config['nifi_url']:
        remove_test_service_user_groups('nifi')
        remove_test_service_users('nifi')
        remove_test_controllers(include_reporting_tasks=True)
    # Cleanup Registry using the existing authenticated session
    cleanup_reg()
    if ACTIVE_PROFILE in ('secure-ldap', 'secure-mtls') and 'https' in active_config['registry_url']:
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
    if ACTIVE_PROFILE in ('secure-ldap', 'secure-mtls') and 'https' in nipyapi.registry.configuration.host:
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
            return nipyapi.versioning.ensure_registry_bucket(target_name)
    request.addfinalizer(remove_test_buckets)
    return Dummy()


@pytest.fixture(name='fix_ver_flow', scope='function')
def fixture_ver_flow(request, fix_bucket, fix_pg, fix_proc):
    log.info("Starting setup of Fixture fix_ver_flow")
    FixtureVerFlow = namedtuple(
        'FixtureVerFlow', ('client', 'bucket', 'pg', 'proc', 'info',
                           'flow', 'snapshot', 'dto')
    )
    f_reg_client = nipyapi.versioning.ensure_registry_client(
        name=test_registry_client_name,
        uri=active_config['registry_internal_url'],
        description=f"Test Registry Client -> {active_config['registry_internal_url']}"
    )
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

    # Wait for flow to be available in registry instead of arbitrary sleep
    def _check_flow_available():
        try:
            flow = nipyapi.versioning.get_flow_in_bucket(
                bucket_id=f_bucket.identifier,
                identifier=f_info.version_control_information.flow_id,
                identifier_type='id'
            )
            return flow if flow else False
        except Exception:
            return False

    flow_result = nipyapi.utils.wait_to_complete(
        _check_flow_available,
        nipyapi_delay=0.1,  # Check every 100ms instead of sleeping for 500ms
        nipyapi_max_wait=10  # Wait up to 10 seconds max
    )

    if not flow_result:
        raise RuntimeError("Flow not available in registry after save_flow_ver")

    f_flow = flow_result
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
