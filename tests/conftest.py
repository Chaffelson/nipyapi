#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configuration fixtures for pytest for `nipyapi` package."""

from __future__ import absolute_import
import logging
import pytest
from os import environ, path
from collections import namedtuple
import nipyapi

log = logging.getLogger(__name__)

# Test Suite Controls
test_default = True  # Default to True for release
test_security = False  # Default to False for release
test_regression = False  # Default to False for release

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

test_user_name = test_basename + '_user'
test_user_group_name = test_basename + '_user_group'

test_resource_dir = 'resources'
# Test template filenames should match the template PG name
test_templates = {
    'basic': test_basename + 'Template_00',
    'complex': test_basename + 'Template_01'
}

# Determining test environment
# Can't use skiptest with parametrize for Travis
# Mostly because loading up all the environments takes too long

default_nifi_endpoints = ['http://localhost:8080/nifi-api']
regress_nifi_endpoints = [
            'http://' + test_host + ':10112/nifi-api',
            'http://' + test_host + ':10120/nifi-api',
            'http://' + test_host + ':10180/nifi-api',
        ]
secure_nifi_endpoints = ['https://' + test_host + ':8443/nifi-api']
default_registry_endpoints = [
        ('http://localhost:18080/nifi-registry-api',
         'http://registry:18080',
         'http://localhost:8080/nifi-api'
         )
    ]
regress_registry_endpoints = [
            ('http://' + test_host + ':18010/nifi-registry-api',
                'http://registry-010:18010',
             'http://' + test_host + ':8080/nifi-api'
             )
        ]
secure_registry_endpoints = [
        ('https://' + test_host + ':18443/nifi-registry-api',
         'https://secure-registry:18443',
         'https://' + test_host + ':8443/nifi-api'
         )]

if "TRAVIS" in environ and environ["TRAVIS"] == "true":
    log.info("Running tests on TRAVIS, skipping regression suite")
    nifi_test_endpoints = default_nifi_endpoints
    registry_test_endpoints = default_registry_endpoints
else:
    log.info("Running tests on NOT TRAVIS, enabling regression suite")
    # Note that these endpoints are assumed to be available
    # look in Nipyapi/test_env_config/docker_compose_full_test for
    # convenient Docker configs and port mappings.

    # NOTE: it is important that the latest version is the last in the list
    # So that after a parametrized test we leave the single tests against
    # The latest release without bulking the test suite ensuring they change
    # back each time.
    nifi_test_endpoints = []
    registry_test_endpoints = []
    if test_default:
        nifi_test_endpoints += default_nifi_endpoints
        registry_test_endpoints += default_registry_endpoints
    if test_regression:
        nifi_test_endpoints += regress_nifi_endpoints
        registry_test_endpoints += regress_registry_endpoints
    if test_security:
        nifi_test_endpoints += secure_nifi_endpoints
        registry_test_endpoints += secure_registry_endpoints


# 'regress' generates tests against previous versions of NiFi or sub-projects.
# If you are using regression, note that you have to create NiFi objects within
# the Test itself. This is because the fixture is generated before the
# PyTest parametrize call, making the order
# new test_func > fixtures > parametrize > run_test_func > teardown > next
def pytest_generate_tests(metafunc):
    log.info("Metafunc Fixturenames are %s", metafunc.fixturenames)
    if 'regress_nifi' in metafunc.fixturenames:
        log.info("NiFi Regression testing requested for ({0})."
                 .format(metafunc.function.__name__))
        metafunc.parametrize(
            argnames='regress_nifi',
            argvalues=nifi_test_endpoints,
            indirect=True
        )
    elif 'regress_flow_reg' in metafunc.fixturenames:
        log.info("NiFi Flow Registry Regression testing requested for ({0})."
                 .format(metafunc.function.__name__))
        metafunc.parametrize(
            argnames='regress_flow_reg',
            argvalues=registry_test_endpoints,
            indirect=True
        )


# Note that it's important that the regress function is the first called if
# you are stacking fixtures
@pytest.fixture(scope="function")
def regress_nifi(request):
    log.info("NiFi Regression test setup called against endpoint %s",
             request.param)
    nipyapi.utils.set_endpoint(request.param, True, True)


def remove_test_registry_client():
    _ = [nipyapi.versioning.delete_registry_client(li) for
         li in nipyapi.versioning.list_registry_clients().registries
         if test_registry_client_name in li.component.name
         ]


def ensure_registry_client(uri):
    try:
        client = nipyapi.versioning.create_registry_client(
            name=test_registry_client_name + uri,
            uri=uri,
            description=uri
        )
    except ValueError as e:
        if 'already exists with the name' in str(e):
            client = nipyapi.versioning.get_registry_client(
                identifier=test_registry_client_name + uri
            )
        else:
            raise e
    if isinstance(client, nipyapi.nifi.RegistryClientEntity):
        return client
    else:
        raise ValueError("Could not create Registry Client")


@pytest.fixture(scope="function")
def regress_flow_reg(request):
    log.info("NiFi-Registry regression test called against endpoints %s",
             request.param)
    # Set Registry connection
    nipyapi.utils.set_endpoint(request.param[0], True, True)
    # Set paired NiFi connection
    nipyapi.utils.set_endpoint(request.param[2], True, True)
    # because pytest won't let you eaily cascade parameters through fixtures
    # we set the docker URI in the config for retrieval later on
    nipyapi.config.registry_local_name = request.param[1]


# Tests that the Docker test environment is available before running test suite
@pytest.fixture(scope="session", autouse=True)
def session_setup(request):
    log.info("Commencing test session setup")
    for url in nifi_test_endpoints + [x[0] for x in registry_test_endpoints]:
        nipyapi.utils.set_endpoint(url, ssl=True, login=True)
        # ssl and login will only work if https is in the url, else will silently skip
        gui_url = url.replace('-api', '')
        if not nipyapi.utils.wait_to_complete(
            nipyapi.utils.is_endpoint_up,
            gui_url,
            nipyapi_delay=nipyapi.config.long_retry_delay,
            nipyapi_max_wait=nipyapi.config.long_max_wait):
            pytest.exit(
                "Expected Service endpoint ({0}) is not responding"
                .format(gui_url)
            )
        # Test API client connection
        if 'nifi-api' in url:
            if not nipyapi.canvas.get_root_pg_id():
                raise ValueError("No Response from NiFi test call")
            # that should've created a new API client connection
            api_host = nipyapi.config.nifi_config.api_client.host
            if api_host != url:
                raise ValueError("Client expected [{0}], but got [{1}] "
                                 "instead".format(url, api_host))
            log.info("Tested NiFi client connection, got response from %s",
                     url)
            if 'https://' in url:
                nipyapi.security.bootstrap_security_policies(service='nifi')
            cleanup_nifi()
        elif 'nifi-registry-api' in url:
            if nipyapi.registry.FlowsApi().get_available_flow_fields():
                log.info("Tested NiFi-Registry client connection, got "
                         "response from %s", url)
                if 'https://' in url:
                    nipyapi.security.bootstrap_security_policies(service='registry')
                cleanup_reg()
            else:
                raise ValueError("No Response from NiFi-Registry test call"
                                 )
        else:
            raise ValueError("Bad API Endpoint")
    request.addfinalizer(final_cleanup)
    log.info("Completing Test Session Setup")


def remove_test_templates():
    all_templates = nipyapi.templates.list_all_templates(native=False)
    if all_templates is not None:
        for this_template in all_templates:
            if test_basename in this_template.template.name:
                nipyapi.templates.delete_template(this_template.id)


def remove_test_pgs():
    test_pgs = nipyapi.canvas.get_process_group(test_basename)
    if test_pgs:
        if not isinstance(test_pgs, list):
            test_pgs = [test_pgs]
        for this_test_pg in test_pgs:
            nipyapi.canvas.delete_process_group(
                this_test_pg,
                force=True,
                refresh=True
            )


def remove_test_processors():
    target_list = [li for
                   li in nipyapi.canvas.list_all_processors()
                   if test_basename in li.status.name
                   ]
    for target in target_list:
        nipyapi.canvas.delete_processor(target, force=True)


def remove_test_buckets():
    _ = [nipyapi.versioning.delete_registry_bucket(li) for li
         in nipyapi.versioning.list_registry_buckets() if
         test_bucket_name in li.name]


def final_cleanup():
    for url in nifi_test_endpoints + [x[0] for x in registry_test_endpoints]:
        nipyapi.utils.set_endpoint(url, True, True)
        if 'nifi-api' in url:
            cleanup_nifi()
        elif 'nifi-registry-api' in url:
            cleanup_reg()


def remove_test_service_users(service='both'):
    nifi_test_users = [
        x for x in
        nipyapi.security.list_service_users('nifi')
        if x.component.identity.startswith(test_basename)
    ]
    reg_test_users = [
        x for x in
        nipyapi.security.list_service_users('registry')
        if x.identity.startswith(test_basename)
    ]
    if service != 'registry':
        _ = [
            nipyapi.security.remove_service_user(x, 'nifi')
            for x in nifi_test_users
        ]
    if service != 'nifi':
        _ = [
            nipyapi.security.remove_service_user(x, 'registry')
            for x in reg_test_users
        ]


def remove_test_service_user_groups(service='both'):
    nifi_test_user_groups = [
        x for x in
        nipyapi.security.list_service_user_groups('nifi')
        if x.component.identity.startswith(test_basename)
    ]
    reg_test_user_groups = [
        x for x in
        nipyapi.security.list_service_user_groups('registry')
        if x.identity.startswith(test_basename)
    ]
    if service != 'registry':
        _ = [
            nipyapi.security.remove_service_user_group(x, 'nifi')
            for x in nifi_test_user_groups
        ]
    if service != 'nifi':
        _ = [
            nipyapi.security.remove_service_user_group(x, 'registry')
            for x in reg_test_user_groups
        ]


def cleanup_nifi():
    # Only bulk-cleanup universally compatible components
    # Ideally we would clean each test environment, but it's too slow to do it
    # per test, so we rely on individual fixture cleanup
    log.info("Bulk cleanup called on host %s",
             nipyapi.config.nifi_config.host)
    remove_test_templates()
    remove_test_connections()
    remove_test_controllers()
    remove_test_processors()
    remove_test_ports()
    remove_test_pgs()
    if test_security and 'https' in nipyapi.nifi.configuration.host:
        remove_test_service_user_groups('nifi')
        remove_test_service_users('nifi')


def remove_test_connections():
    _ = [
        nipyapi.canvas.delete_connection(x, True)
        for x in nipyapi.canvas.list_all_connections()
        if test_basename in x.component.name
    ]


def remove_test_ports():
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


def remove_test_controllers():
    _ = [nipyapi.canvas.delete_controller(li, True) for li
         in nipyapi.canvas.list_all_controllers() if
         test_basename in li.component.name]


def cleanup_reg():
    # Bulk cleanup for tests involving NiFi Registry
    remove_test_pgs()
    remove_test_buckets()
    remove_test_registry_client()
    if test_security and 'https' in nipyapi.registry.configuration.host:
        remove_test_service_user_groups('registry')
        remove_test_service_users('registry')


@pytest.fixture(name='fix_templates', scope='function')
def fixture_templates(request, fix_pg):
    log.info("Creating PyTest Fixture fix_templates on endpoint %s",
             nipyapi.config.nifi_config.host)
    FixtureTemplates = namedtuple(
        'FixtureTemplates', ('pg', 'b_file', 'b_name', 'c_file',
                             'c_name')
    )
    f_pg = fix_pg
    f_b_file = path.join(
            path.dirname(__file__),
            test_resource_dir,
            test_templates['basic'] + '.xml'
        )
    f_b_name = 'nipyapi_testTemplate_00'
    f_c_file = path.join(
            path.dirname(__file__),
            test_resource_dir,
            test_templates['complex'] + '.xml'
        )
    f_c_name = 'nipyapi_testTemplate_01'
    out = FixtureTemplates(
        pg=f_pg,
        b_name=f_b_name,
        c_name=f_c_name,
        b_file=f_b_file,
        c_file=f_c_file
    )
    request.addfinalizer(remove_test_templates)
    log.info("- Returning PyTest Fixture fix_templates")
    return out


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


@pytest.fixture(name='fix_bucket', scope='function')
def fixture_bucket(request):
    class Dummy:
        def __init__(self):
            pass

        def __call__(self, name=test_bucket_name, suffix=''):
            return nipyapi.versioning.create_registry_bucket(
                name + suffix
            )
    request.addfinalizer(remove_test_buckets)
    return Dummy()


@pytest.fixture(name='fix_ver_flow', scope='function')
def fixture_ver_flow(request, fix_bucket, fix_pg, fix_proc):
    log.info("Starting setup of Fixture fix_ver_flow")
    FixtureVerFlow = namedtuple(
        'FixtureVerFlow', ('client', 'bucket', 'pg', 'proc', 'info',
                           'flow', 'snapshot', 'dto')
    )
    f_reg_client = ensure_registry_client(nipyapi.config.registry_local_name)
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
    f_filepath = str(tmpdir.mkdir(test_ver_export_tmpdir)\
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
            kind = kind if kind else 'DistributedMapCacheClientService'
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
