"""Configuration fixtures for pytest for `nipyapi` package."""

import logging
import os
import tempfile
import textwrap
import zipfile
from collections import namedtuple

import pytest

import nipyapi
import nipyapi.profiles

log = logging.getLogger(__name__)


ACTIVE_PROFILE = os.getenv('NIPYAPI_PROFILE', 'single-user').strip()
ACTIVE_PROFILES_PATH = os.getenv('NIPYAPI_PROFILES_PATH', 'examples/profiles.yml').strip()

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
    profiles_path = nipyapi.utils.resolve_relative_paths(ACTIVE_PROFILES_PATH)
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
    """Remove all test process groups."""
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
    """Delete test parameter contexts, handling inheritance order.

    Contexts that inherit from others must be deleted first (parents before children
    in inheritance terms). This function iterates until all test contexts are deleted.
    """
    if SKIP_TEARDOWN:
        return None
    # check_version returns 1 if NiFi is OLDER than specified version, -1 if newer, 0 if equal
    # We skip cleanup if NiFi is older than 1.10.0 (doesn't have parameter contexts)
    if nipyapi.utils.check_version('1.10.0') > 0:
        log.info("NiFi version is older than 1.10, skipping Parameter Context cleanup")
        return None

    # Multiple passes to handle inheritance dependencies
    max_attempts = 5
    for attempt in range(max_attempts):
        contexts = [
            ctx for ctx in nipyapi.parameters.list_all_parameter_contexts()
            if test_basename in ctx.component.name
        ]
        if not contexts:
            return None

        deleted_any = False
        for ctx in contexts:
            try:
                nipyapi.parameters.delete_parameter_context(ctx)
                deleted_any = True
            except nipyapi.nifi.rest.ApiException as e:
                if e.status == 409:
                    # Referenced by another context - try again later
                    continue
                raise

        if not deleted_any and contexts:
            # No progress made, likely circular reference or unresolved deps
            log.warning("Could not delete %d parameter contexts after %d attempts",
                        len(contexts), attempt + 1)
            break
    return None


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
        nipyapi.profiles.switch(ACTIVE_PROFILE, profiles_file=ACTIVE_PROFILES_PATH)
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
    for rpg in nipyapi.canvas.list_all_remote_process_groups():
        try:
            nipyapi.canvas.delete_remote_process_group(rpg, force=True)
        except Exception:
            pass  # Best effort cleanup


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
    """Function-scoped fixture for creating test process groups.

    Only cleans up PGs created by this fixture instance, not all test PGs.
    This allows module-scoped shared fixtures to coexist.
    """
    created_pgs = []

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
            pg = nipyapi.canvas.create_process_group(
                target_pg,
                test_pg_name + suffix,
                location=(400.0, 400.0)
            )
            created_pgs.append(pg.id)
            return pg

    def cleanup():
        if SKIP_TEARDOWN:
            return
        for pg_id in created_pgs:
            try:
                pg = nipyapi.canvas.get_process_group(pg_id, 'id')
                if pg:
                    nipyapi.canvas.delete_process_group(pg, True, True)
            except Exception:
                pass  # PG may already be deleted

    request.addfinalizer(cleanup)
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


@pytest.fixture(name='fix_inherited_context_hierarchy', scope='function')
def fixture_inherited_context_hierarchy(request, fix_pg, fix_context):
    """
    Create a parameter context hierarchy with inheritance for testing.

    Creates:
    - child_ctx: Has one parameter "ChildParam"
    - parent_ctx: Inherits from child_ctx, has "ParentParam"
    - pg: Process group bound to parent_ctx

    This fixture allows testing of both simple (single context) and complex
    (inherited hierarchy) parameter operations.
    """
    FixtureInheritedContexts = namedtuple(
        'FixtureInheritedContexts',
        ('parent_ctx', 'child_ctx', 'pg', 'parent_param_name', 'child_param_name')
    )

    # Create child context with a parameter
    child_ctx = fix_context.generate(name=test_parameter_context_name + "_child")
    child_param = nipyapi.parameters.prepare_parameter(
        name="ChildParam",
        value="child_value",
        description="Parameter owned by child context"
    )
    nipyapi.parameters.upsert_parameter_to_context(child_ctx, child_param)

    # Refresh context after parameter update
    child_ctx = nipyapi.parameters.get_parameter_context(child_ctx.id, "id")

    # Create parent context that inherits from child
    parent_ctx = nipyapi.parameters.create_parameter_context(
        name=test_parameter_context_name + "_parent",
        inherited_contexts=[child_ctx]
    )
    parent_param = nipyapi.parameters.prepare_parameter(
        name="ParentParam",
        value="parent_value",
        description="Parameter owned by parent context"
    )
    nipyapi.parameters.upsert_parameter_to_context(parent_ctx, parent_param)

    # Refresh parent context
    parent_ctx = nipyapi.parameters.get_parameter_context(parent_ctx.id, "id")

    # Create PG and bind the parent context to it
    pg = fix_pg.generate(suffix="_params")
    nipyapi.parameters.assign_context_to_process_group(pg, parent_ctx.id)

    # Refresh PG
    pg = nipyapi.canvas.get_process_group(pg.id, "id")

    def cleanup():
        if SKIP_TEARDOWN:
            return
        # Delete parent context (must be done before child due to inheritance)
        try:
            nipyapi.parameters.delete_parameter_context(parent_ctx)
        except Exception as e:
            log.warning("Failed to delete parent context: %s", e)

    request.addfinalizer(cleanup)
    return FixtureInheritedContexts(
        parent_ctx=parent_ctx,
        child_ctx=child_ctx,
        pg=pg,
        parent_param_name="ParentParam",
        child_param_name="ChildParam"
    )


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


# Cache for resolved V1 version SHA
_git_registry_version_v1_cache = None


def get_git_registry_version_v1():
    """Resolve v1.0.0 tag to commit SHA via GitHub API (cached)."""
    global _git_registry_version_v1_cache  # pylint: disable=global-statement
    if _git_registry_version_v1_cache is None:
        token = os.environ.get('GH_REGISTRY_TOKEN')
        if not token:
            pytest.skip("GH_REGISTRY_TOKEN not set - cannot resolve v1.0.0 tag")
        _git_registry_version_v1_cache = nipyapi.ci.resolve_git_ref(
            ref='v1.0.0',
            repo='Chaffelson/nipyapi-actions',
            token=token,
            provider='github'
        )
    return _git_registry_version_v1_cache



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
        flow_id='nipyapi_test_cicd_demo',
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
        flow_id='nipyapi_test_cicd_demo',
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


# =============================================================================
# NAR Builder Fixtures (for extension/multi-version tests)
# =============================================================================


def create_test_nar(version="0.0.1", processor_name="NipyapiTestProcessor", valid=True):
    """
    Create a Python processor NAR for testing.

    Generates a NAR file that can be uploaded to NiFi. By default creates
    a valid processor with the Java implements declaration that NiFi
    recognizes. Set valid=False to create an "invalid" NAR that uploads
    successfully but contains no recognizable processor types.

    Args:
        version: The ProcessorDetails.version value (e.g., "0.0.1" or "0.0.1-SNAPSHOT")
        processor_name: Name of the processor class
        valid: If True (default), include Java implements declaration so NiFi
            recognizes the processor. If False, omit it to test invalid NAR handling.

    Returns:
        str: Path to temporary NAR file (caller should clean up)

    Example:
        >>> # Valid NAR with recognizable processor
        >>> nar_path = create_test_nar(version="0.0.1")
        >>> nar = nipyapi.extensions.upload_nar(nar_path)
        >>> details = nipyapi.extensions.get_nar_details(nar.identifier)
        >>> assert len(details.processor_types) == 1

        >>> # Invalid NAR (uploads but no processors)
        >>> invalid_path = create_test_nar(version="0.0.1", valid=False)
        >>> nar = nipyapi.extensions.upload_nar(invalid_path)
        >>> details = nipyapi.extensions.get_nar_details(nar.identifier)
        >>> assert len(details.processor_types) == 0
    """
    # Ensure version has -SNAPSHOT suffix for ProcessorDetails
    proc_version = version if "-SNAPSHOT" in version else f"{version}-SNAPSHOT"
    # NAR coordinate version (without -SNAPSHOT)
    nar_version = version.replace("-SNAPSHOT", "")

    # Module name derived from processor name
    module_name = processor_name.lower()

    # Create temp file for NAR
    fd, nar_path = tempfile.mkstemp(suffix=".nar", prefix=f"test_nar_{nar_version}_")
    os.close(fd)

    # Build NAR contents
    manifest = textwrap.dedent(f"""\
        Manifest-Version: 1.0
        Created-By: nipyapi-test
        Build-Timestamp: 2025-01-01T00:00:00Z
        Nar-Id: {module_name}-nar
        Nar-Group: nipyapi.test
        Nar-Version: {nar_version}
    """)

    about_py = textwrap.dedent(f'''\
        __version__ = "{nar_version}"
    ''')

    init_py = ""

    # The Java class with implements declaration is what makes NiFi recognize
    # the processor. Without it, the NAR uploads but has no processor types.
    java_class_block = ""
    if valid:
        java_class_block = """
    class Java:
        implements = ['org.apache.nifi.python.processor.FlowFileTransform']
"""

    processor_py = f"""from nifiapi.flowfiletransform import FlowFileTransform, FlowFileTransformResult


class {processor_name}(FlowFileTransform):
    \"\"\"A minimal test processor for nipyapi extension tests.\"\"\"{java_class_block}
    class ProcessorDetails:
        version = "{proc_version}"
        description = "NiPyAPI test processor for extension testing"
        tags = ["test", "nipyapi"]
        dependencies = []

    def __init__(self, **kwargs):
        super().__init__()

    def transform(self, context, flow_file):
        \"\"\"Pass through - just returns success.\"\"\"
        return FlowFileTransformResult(relationship="success")
"""

    # Create the NAR (ZIP with specific structure)
    with zipfile.ZipFile(nar_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("META-INF/MANIFEST.MF", manifest)
        zf.writestr(f"{module_name}/__init__.py", init_py)
        zf.writestr(f"{module_name}/__about__.py", about_py)
        zf.writestr(f"{module_name}/{processor_name}.py", processor_py)

    log.debug("Created test NAR: %s (version=%s)", nar_path, nar_version)
    return nar_path


def _test_name_to_processor_name(test_name):
    """Convert a test name to a valid processor class name.

    Examples:
        test_valid_nar_has_processor_types -> ValidNarProc
        test_processor_init_lifecycle -> InitLifecycleProc
        test_missing_nar_detection -> MissingNarProc
    """
    # Remove 'test_' prefix
    name = test_name
    if name.startswith("test_"):
        name = name[5:]

    # Convert snake_case to PascalCase
    parts = name.split("_")

    # Skip common/redundant words to keep names unique but concise
    skip_words = {
        "has", "is", "the", "a", "an", "with", "for", "and", "or",
        "processor", "processors", "type", "types", "test", "nar", "nars"
    }
    meaningful_parts = [p for p in parts if p.lower() not in skip_words][:3]

    # Capitalize each part and join
    pascal_name = "".join(p.capitalize() for p in meaningful_parts)

    # Use 'Proc' suffix (shorter, avoids redundancy with 'Processor' in test names)
    return f"{pascal_name}Proc"


@pytest.fixture(name='fix_test_nar')
def fixture_test_nar(request):
    """Fixture providing a factory for creating test NAR files.

    Returns a factory function that creates Python processor NARs with
    test-specific names for clear log traceability.

    The processor name is derived from the test name by default:
    - test_valid_nar_has_processor_types -> ValidNarProcessor
    - test_processor_init_lifecycle -> InitLifecycleProcessor

    This makes it easy to identify which test produced which log entries.

    Example:
        def test_upload_nar(fix_test_nar):
            # Creates UploadNarProcessor with bundle uploadnarprocessor-nar
            nar_v1 = fix_test_nar(version="0.0.1")
            nar_v2 = fix_test_nar(version="0.0.2")

            # Override processor name if needed
            custom_nar = fix_test_nar(version="0.0.1", processor_name="CustomProcessor")

            # Invalid NAR (uploads but no processors)
            invalid_nar = fix_test_nar(version="0.0.1", valid=False)
    """
    # Get test name and derive default processor name
    test_name = request.node.name
    default_processor_name = _test_name_to_processor_name(test_name)

    created_files = []

    def factory(version="0.0.1", processor_name=None, valid=True):
        # Use test-derived name if not explicitly provided
        actual_name = processor_name if processor_name else default_processor_name
        nar_path = create_test_nar(version=version, processor_name=actual_name, valid=valid)
        created_files.append(nar_path)
        log.debug("Created NAR for test '%s': processor=%s, version=%s",
                  test_name, actual_name, version)
        return nar_path

    yield factory

    # Cleanup created NAR files
    for path in created_files:
        try:
            if os.path.exists(path):
                os.unlink(path)
        except Exception as e:
            log.warning("Failed to clean up test NAR %s: %s", path, e)


@pytest.fixture(name='fix_multi_version_nars', scope='module')
def fixture_multi_version_nars(request):
    """Module-scoped fixture providing v1 and v2 NARs uploaded once per module.

    Creates and uploads two versions of a test NAR, returning details needed
    for multi-version processor workflow tests. Expensive operation done once.
    """
    from collections import namedtuple

    FixtureMultiVersionNars = namedtuple(
        'FixtureMultiVersionNars',
        ('nar_v1', 'nar_v2', 'details_v1', 'details_v2',
         'proc_type_name', 'v1_bundle', 'v2_bundle')
    )

    # Create and upload NARs
    nar_path_v1 = create_test_nar(version="0.0.1", processor_name="MultiVersionProc")
    nar_path_v2 = create_test_nar(version="0.0.2", processor_name="MultiVersionProc")

    nar_v1 = nipyapi.extensions.upload_nar(nar_path_v1)
    nar_v2 = nipyapi.extensions.upload_nar(nar_path_v2)

    details_v1 = nipyapi.extensions.get_nar_details(nar_v1.identifier)
    details_v2 = nipyapi.extensions.get_nar_details(nar_v2.identifier)

    def cleanup():
        if SKIP_TEARDOWN:
            return
        # Cleanup NARs from NiFi
        for nar in [nar_v1, nar_v2]:
            try:
                if nipyapi.extensions.get_nar(nar.identifier):
                    nipyapi.extensions.delete_nar(nar.identifier, force=True)
            except Exception:
                pass
        # Cleanup local files
        for path in [nar_path_v1, nar_path_v2]:
            try:
                if os.path.exists(path):
                    os.unlink(path)
            except Exception:
                pass

    request.addfinalizer(cleanup)

    return FixtureMultiVersionNars(
        nar_v1=nar_v1,
        nar_v2=nar_v2,
        details_v1=details_v1,
        details_v2=details_v2,
        proc_type_name=details_v1.processor_types[0].type,
        v1_bundle=details_v1.processor_types[0].bundle.version,
        v2_bundle=details_v2.processor_types[0].bundle.version,
    )


@pytest.fixture(name='fix_state_flow', scope='function')
def fixture_state_flow(request, fix_pg):
    """
    Create a flow that generates state for both processor and controller:
    - MapCacheServer controller (stores cache entries)
    - DistributedMapCacheClientService controller (connects to server)
    - ListFile processor (lists files, stores listing state)
    - PutDistributedMapCache processor (writes to cache)
    - Connection: ListFile -> PutDistributedMapCache

    Running this flow populates state in both ListFile (processor) and
    MapCacheServer (controller).
    """
    import time

    f_pg = fix_pg.generate()

    # Create MapCacheServer controller
    server_type = nipyapi.canvas.get_controller_type('MapCacheServer')
    server = nipyapi.canvas.create_controller(f_pg, server_type, 'test_state_cache_server')
    server = nipyapi.canvas.schedule_controller(server, scheduled=True, refresh=True)

    # Create MapCacheClientService controller (connects to MapCacheServer)
    # Filter by exact type name since get_controller_type with greedy match returns multiple
    all_types = nipyapi.canvas.list_all_controller_types()
    client_type = next(
        t for t in all_types
        if t.type == 'org.apache.nifi.distributed.cache.client.MapCacheClientService'
    )
    client = nipyapi.canvas.create_controller(f_pg, client_type, 'test_state_cache_client')
    client = nipyapi.canvas.update_controller(client, nipyapi.nifi.ControllerServiceDTO(
        properties={
            'Server Hostname': 'localhost',
            'Server Port': '4557'
        }
    ))
    client = nipyapi.canvas.schedule_controller(client, scheduled=True, refresh=True)

    # Create ListFile processor pointing to NiFi logs dir
    list_type = nipyapi.canvas.get_processor_type('ListFile')
    list_proc = nipyapi.canvas.create_processor(f_pg, list_type, (100, 100), 'test_state_list_file')
    list_proc = nipyapi.canvas.update_processor(list_proc, nipyapi.nifi.ProcessorConfigDTO(
        properties={
            'Input Directory': '/opt/nifi/nifi-current/logs',
            'Recurse Subdirectories': 'false'
        }
    ))

    # Create PutDistributedMapCache processor
    put_type = nipyapi.canvas.get_processor_type('PutDistributedMapCache')
    put_proc = nipyapi.canvas.create_processor(f_pg, put_type, (100, 300), 'test_state_put_cache')
    put_proc = nipyapi.canvas.update_processor(put_proc, nipyapi.nifi.ProcessorConfigDTO(
        properties={
            'Distributed Cache Service': client.id,
            'Cache Entry Identifier': '${filename}'
        },
        auto_terminated_relationships=['success', 'failure']
    ))

    # Connect ListFile -> PutDistributedMapCache
    nipyapi.canvas.create_connection(list_proc, put_proc, ['success'], 'test_state_connection')

    # Run the flow to generate state
    nipyapi.canvas.schedule_processor(list_proc, scheduled=True, refresh=True)
    nipyapi.canvas.schedule_processor(put_proc, scheduled=True, refresh=True)
    time.sleep(3)  # Let processors run
    nipyapi.canvas.schedule_processor(list_proc, scheduled=False, refresh=True)
    nipyapi.canvas.schedule_processor(put_proc, scheduled=False, refresh=True)

    class StateFlowFixture:
        def __init__(self):
            self.pg = f_pg
            self.cache_server = server
            self.cache_client = client
            self.list_file_proc = list_proc
            self.put_cache_proc = put_proc

    # Cleanup is handled by fix_pg's finalizer (remove_test_pgs)
    return StateFlowFixture()
