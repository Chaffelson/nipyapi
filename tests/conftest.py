"""Configuration fixtures for pytest for `nipyapi` package."""

import logging
import pytest
import os
from collections import namedtuple

import nipyapi
import nipyapi.profiles

log = logging.getLogger(__name__)


ACTIVE_PROFILE = os.getenv('NIPYAPI_PROFILE', 'single-user').strip()

# Validate profile early and fail fast
# Note: github-cicd profile is NiFi-only (no Registry) for CI/CD testing
VALID_PROFILES = ('single-user', 'secure-ldap', 'secure-mtls', 'secure-oidc', 'github-cicd')
if ACTIVE_PROFILE not in VALID_PROFILES:
    raise ValueError(f"Invalid NIPYAPI_PROFILE: {ACTIVE_PROFILE}. Must be one of: {VALID_PROFILES}")

# Skip markers for profile-specific test requirements
requires_registry = pytest.mark.skipif(
    ACTIVE_PROFILE == 'github-cicd',
    reason='Test requires NiFi Registry service (not available in github-cicd profile)'
)


def _flag(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "on")

SKIP_TEARDOWN = _flag('SKIP_TEARDOWN', default=False)
ACTIVE_CONFIG = None


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
test_git_registry_client_name = test_basename + "_git_reg_client"

test_user_name = test_basename + '_user'
test_user_group_name = test_basename + '_user_group'


def remove_test_registry_client():
    _ = [nipyapi.versioning.delete_registry_client(li) for
         li in nipyapi.versioning.list_registry_clients().registries
         if test_registry_client_name in li.component.name
         ]


def remove_test_git_registry_clients():
    if SKIP_TEARDOWN:
        return None
    _ = [nipyapi.versioning.delete_registry_client(li) for
         li in nipyapi.versioning.list_registry_clients().registries
         if li.component and test_git_registry_client_name in li.component.name
         ]


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
    global ACTIVE_CONFIG

    # Resolve configuration once for the entire session
    # Use NIPYAPI_PROFILES_FILE env var if set, otherwise default to examples/profiles.yml
    profiles_path = os.getenv('NIPYAPI_PROFILES_FILE', 'examples/profiles.yml')
    profiles_path = nipyapi.utils.resolve_relative_paths(profiles_path)
    log.info("Using profiles file: %s", profiles_path)
    ACTIVE_CONFIG = nipyapi.profiles.resolve_profile_config(
        profile_name=ACTIVE_PROFILE, profiles_file_path=profiles_path
    )

    # Configure authentication and SSL using standardized profiles system
    nipyapi.profiles.switch(ACTIVE_PROFILE, profiles_file=profiles_path)
    log.info("Profile configured: %s", ACTIVE_PROFILE)

    # NiFi readiness check
    _wait_until_service_up(nipyapi.config.nifi_config.host.replace('/nifi-api', '/nifi'))
    if not nipyapi.canvas.get_root_pg_id():
        raise ValueError("No Response from NiFi test call")

    # NiFi security bootstrapping for secure profiles
    if ACTIVE_PROFILE in ('secure-ldap', 'secure-mtls', 'secure-oidc'):
        try:
            nipyapi.security.bootstrap_security_policies(service='nifi')
            log.info("NiFi security policies bootstrapped for %s profile", ACTIVE_PROFILE)
        except Exception as e:
            log.warning("Security policy bootstrap failed (environment may need setup): %s", e)
            if ACTIVE_PROFILE == 'secure-oidc':
                log.info("For OIDC: Run 'make sandbox NIPYAPI_PROFILE=secure-oidc' first")
            raise
    cleanup_nifi()

    # Registry setup (authentication already configured by profiles.switch above)
    if nipyapi.config.registry_config.host:
        registry_ui_url = nipyapi.config.registry_config.host.replace('/nifi-registry-api', '/nifi-registry')
        _wait_until_service_up(registry_ui_url)

        # Registry security bootstrapping
        try:
            nipyapi.security.bootstrap_security_policies(
                service='registry', nifi_proxy_identity=ACTIVE_CONFIG.get('nifi_proxy_identity')
            )
        except Exception:
            pass
        cleanup_reg()

        # Ensure a registry client exists for all profiles
        registry_internal_url = ACTIVE_CONFIG.get('registry_internal_url') or nipyapi.config.registry_config.host
        _ = nipyapi.versioning.ensure_registry_client(
            name=test_registry_client_name,
            uri=registry_internal_url,
            description=f"Test Registry Client -> {registry_internal_url}"
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

    # Re-authenticate before cleanup to ensure we have a valid session
    # (Some tests may have modified authentication state)
    try:
        nipyapi.profiles.switch(ACTIVE_PROFILE)
        log.debug("Re-authenticated for final cleanup")
    except Exception as e:
        log.warning("Failed to re-authenticate for cleanup, skipping: %s", e)
        return None

    # Cleanup NiFi using authenticated session
    cleanup_nifi()
    if ACTIVE_PROFILE in ('secure-ldap', 'secure-mtls') and 'https' in ACTIVE_CONFIG['nifi_url']:
        remove_test_service_user_groups('nifi')
        remove_test_service_users('nifi')
        remove_test_controllers(include_reporting_tasks=True)
    # Cleanup Registry using authenticated session (only if Registry is configured)
    if nipyapi.config.registry_config.host:
        cleanup_reg()
    if ACTIVE_PROFILE in ('secure-ldap', 'secure-mtls') and ACTIVE_CONFIG.get('registry_url') and 'https' in ACTIVE_CONFIG['registry_url']:
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
    # Note: some connections may have None as name
    _ = [
        nipyapi.canvas.delete_connection(x, True)
        for x in nipyapi.canvas.list_all_connections()
        if x.destination_type == 'FUNNEL'
        or x.source_type == 'FUNNEL'
        or (x.component.name and test_basename in x.component.name)
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
        uri=ACTIVE_CONFIG['registry_internal_url'],
        description=f"Test Registry Client -> {ACTIVE_CONFIG['registry_internal_url']}"
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


@pytest.fixture(name='fix_profiles', scope='function')
def fixture_profiles():
    """Fixture providing test profile data for profile tests."""
    return {
        'complete': {
            'nifi_url': 'https://localhost:9444/nifi-api',
            'nifi_user': 'einstein',
            'nifi_pass': 'password',
            'oidc_token_endpoint': 'https://keycloak/token'
        },
        'sparse': {
            'nifi_url': 'https://localhost:9444/nifi-api'
            # Missing many keys
        }
    }


# =============================================================================
# Git-based Registry Fixtures (GitHub Flow Registry Client)
# =============================================================================
# These fixtures require a GitHub PAT via GH_REGISTRY_TOKEN environment variable
# environment variable. They use the nipyapi-actions repository test fixtures.

# Known test fixture versions in nipyapi-actions repo
# V1 is a stable older version (tagged) for version switching tests
GIT_REGISTRY_VERSION_V1 = '97549b88f2e1fb1dccddef57335e94628c74060b'  # v1.0.0 tag
# LATEST is looked up at runtime by fixtures - no hardcoded value needed


@pytest.fixture(name='fix_git_reg_client', scope='function')
def fixture_git_registry_client(request):
    """Create a GitHub registry client for testing with real credentials.

    Requires GH_REGISTRY_TOKEN environment variable.
    Uses the nipyapi-actions repository test flows in tests/ path.
    """
    token = os.environ.get('GH_REGISTRY_TOKEN')
    if not token:
        pytest.skip("GH_REGISTRY_TOKEN not set - skipping git registry tests")

    class Dummy:
        def __init__(self):
            self._client = None

        def generate(self, suffix=''):
            # Clean up any existing client with same name
            client_name = test_git_registry_client_name + suffix
            existing = nipyapi.versioning.list_registry_clients().registries
            for client in existing:
                if client.component and client_name in client.component.name:
                    nipyapi.versioning.delete_registry_client(client)

            # Create client pointing to nipyapi-actions test flows
            self._client = nipyapi.versioning.create_registry_client(
                name=client_name,
                reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
                description='Test client for git registry functions',
                properties={
                    'GitHub API URL': 'https://api.github.com/',
                    'Repository Owner': 'Chaffelson',
                    'Repository Name': 'nipyapi-actions',
                    'Repository Path': 'tests',
                    'Authentication Type': 'PERSONAL_ACCESS_TOKEN',
                    'Personal Access Token': token,
                    'Default Branch': 'main'
                }
            )
            return self._client

    request.addfinalizer(remove_test_git_registry_clients)
    return Dummy()


@pytest.fixture(name='fix_deployed_git_flow_shared', scope='module')
def fixture_deployed_git_flow_shared(request):
    """Module-scoped fixture that deploys a flow once for all tests.

    This is the actual deployment - expensive operation done once per module.
    Includes latest_version looked up at runtime to avoid hardcoded commit hashes.
    """
    token = os.environ.get('GH_REGISTRY_TOKEN')
    if not token:
        pytest.skip("GH_REGISTRY_TOKEN not set - skipping git registry tests")

    FixtureDeployedGitFlow = namedtuple(
        'FixtureDeployedGitFlow', ('client', 'pg', 'bucket_id', 'flow_id', 'latest_version')
    )

    # Create registry client
    client_name = test_git_registry_client_name + '_shared'
    existing = nipyapi.versioning.list_registry_clients().registries
    for client in existing:
        if client.component and client_name in client.component.name:
            nipyapi.versioning.delete_registry_client(client)

    client = nipyapi.versioning.create_registry_client(
        name=client_name,
        reg_type='org.apache.nifi.github.GitHubFlowRegistryClient',
        description='Shared test client for git registry functions',
        properties={
            'GitHub API URL': 'https://api.github.com/',
            'Repository Owner': 'Chaffelson',
            'Repository Name': 'nipyapi-actions',
            'Repository Path': 'tests',
            'Authentication Type': 'PERSONAL_ACCESS_TOKEN',
            'Personal Access Token': token,
            'Default Branch': 'main'
        }
    )

    root_id = nipyapi.canvas.get_root_pg_id()
    pg = nipyapi.versioning.deploy_git_registry_flow(
        registry_client_id=client.id,
        bucket_id='flows',
        flow_id='cicd-demo-flow',
        parent_id=root_id,
        location=(500, 500),
        version=None  # Latest
    )

    # Look up the actual latest version at runtime (deployed version is latest)
    vci = nipyapi.versioning.get_version_info(pg)
    latest_version = vci.version_control_information.version

    def cleanup():
        if SKIP_TEARDOWN:
            return
        try:
            nipyapi.canvas.schedule_process_group(pg.id, scheduled=False)
        except Exception:
            pass
        try:
            nipyapi.canvas.delete_process_group(pg, force=True)
        except Exception:
            pass
        try:
            nipyapi.versioning.delete_registry_client(client)
        except Exception:
            pass

    request.addfinalizer(cleanup)
    return FixtureDeployedGitFlow(
        client=client,
        pg=pg,
        bucket_id='flows',
        flow_id='cicd-demo-flow',
        latest_version=latest_version
    )


@pytest.fixture(name='fix_deployed_git_flow', scope='function')
def fixture_deployed_git_flow(request, fix_deployed_git_flow_shared):
    """Function-scoped fixture that provides access to the shared deployed flow.

    Restores the flow to a clean state (UP_TO_DATE at latest version) after
    each test, avoiding the need to redeploy for each test.
    """
    # Yield the shared fixture
    yield fix_deployed_git_flow_shared

    # Restore state after test
    if SKIP_TEARDOWN:
        return

    latest_version = fix_deployed_git_flow_shared.latest_version
    try:
        pg = nipyapi.canvas.get_process_group(fix_deployed_git_flow_shared.pg.id, 'id')
        if not pg:
            return  # PG was deleted, nothing to restore

        vci = nipyapi.versioning.get_version_info(pg)
        if not vci or not vci.version_control_information:
            return  # Not under version control

        state = vci.version_control_information.state
        version = vci.version_control_information.version

        # If locally modified, revert first (handles both LOCALLY_MODIFIED and LOCALLY_MODIFIED_AND_STALE)
        if 'LOCALLY_MODIFIED' in state:
            nipyapi.versioning.revert_flow_ver(pg, wait=True)
            pg = nipyapi.canvas.get_process_group(pg.id, 'id')
            # Re-check version after revert
            vci = nipyapi.versioning.get_version_info(pg)
            version = vci.version_control_information.version

        # If not at latest, change to latest
        if version != latest_version:
            nipyapi.versioning.update_git_flow_ver(pg, latest_version)

    except Exception as e:
        log.warning("Failed to restore git flow state after test: %s", e)
