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

# Test Configuration parameters
test_host = 'localhost'
test_basename = "nipyapi_test"
test_pg_name = test_basename + "_ProcessGroup"
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

test_resource_dir = 'resources'
# Test template filenames should match the template PG name
test_templates = {
    'basic': test_basename + 'Template_00',
    'complex': test_basename + 'Template_01'
}

# Determining test environment
# Can't use skiptest with parametrize for Travis
# Mostly because loading up all the environments takes too long
if "TRAVIS" in environ and environ["TRAVIS"] == "true":
    log.info("Running tests on TRAVIS, skipping regression suite")
    nifi_test_endpoints = ['http://localhost:8080/nifi-api']
    registry_test_endpoints = [
        ('http://localhost:18080/nifi-registry-api',
         'http://registry:18080',
         'http://localhost:8080/nifi-api'
         )
    ]
else:
    log.info("Running tests on NOT TRAVIS, enabling regression suite")
    # Note that these endpoints are assumed to be available
    # look in Nipyapi/test_env_config/docker_compose_full_test for
    # convenient Docker configs and port mappings.

    # NOTE: it is important that the latest version is the last in the list
    # So that after a parametrized test we leave the single tests against
    # The latest release without bulking the test suite ensuring they change
    # back each time.
    nifi_test_endpoints = [
        'http://' + test_host + ':10112/nifi-api',
        'http://' + test_host + ':10120/nifi-api',
        'http://' + test_host + ':10160/nifi-api',
        'http://' + test_host + ':8080/nifi-api'  # Default to latest
    ]
    # These are paired into api & docker labels with a paired nifi instance
    registry_test_endpoints = [
        ('http://' + test_host + ':18010/nifi-registry-api',
            'http://registry-010:18010',
         'http://' + test_host + ':8080/nifi-api'
         ),
        ('http://' + test_host + ':18020/nifi-registry-api',
            'http://registry-020:18020',
         'http://' + test_host + ':8080/nifi-api'
         )  # Default to latest version
    ]


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
    nipyapi.utils.set_endpoint(request.param)


def remove_test_registry_client():
    _ = [nipyapi.versioning.delete_registry_client(li) for
         li in nipyapi.versioning.list_registry_clients().registries
         if test_registry_client_name in li.component.name
         ]


def ensure_registry_client(uri):
    client = nipyapi.versioning.create_registry_client(
        name=test_registry_client_name + uri,
        uri=uri,
        description=uri
    )
    if isinstance(client, nipyapi.nifi.RegistryClientEntity):
        return client
    else:
        raise ValueError("Could not create Registry Client")


@pytest.fixture(scope="function")
def regress_flow_reg(request):
    log.info("NiFi-Registry regression test called against endpoints %s",
             request.param)
    # Set Registry connection
    nipyapi.utils.set_endpoint(request.param[0])
    # Set paired NiFi connection
    nipyapi.utils.set_endpoint(request.param[2])
    # because pytest won't let you eaily cascade parameters through fixtures
    # we set the docker URI in the config for retrieval later on
    nipyapi.config.registry_local_name = request.param[1]


# Tests that the Docker test environment is available before running test suite
@pytest.fixture(scope="session", autouse=True)
def session_setup(request):
    log.info("Commencing test session setup")
    for url in nifi_test_endpoints + [x[0] for x in registry_test_endpoints]:
        nipyapi.utils.set_endpoint(url)
        target_url = url.replace('-api', '')
        if not nipyapi.utils.wait_to_complete(
            nipyapi.utils.is_endpoint_up,
            target_url,
            nipyapi_delay=nipyapi.config.long_retry_delay,
            nipyapi_max_wait=nipyapi.config.long_max_wait):
            pytest.exit(
                "Expected Service endpoint ({0}) is not responding"
                .format(target_url)
            )
        else:
            # Test API client connection
            if 'nifi-api' in url:
                if nipyapi.canvas.get_root_pg_id():
                    log.info("Tested Nifi client connection for test suite to"
                             "service endpoint at %s", url)
                    cleanup()
                    request.addfinalizer(cleanup)
                else:
                    raise ValueError("No Response from NiFi test call")
            elif 'nifi-registry-api' in url:
                if nipyapi.registry.FlowsApi().get_available_flow_fields():
                    log.info("Tested NiFi-Registry client connection, got "
                             "response from %s", url)
                    cleanup_reg()
                    request.addfinalizer(cleanup_reg)
                else:
                    raise ValueError("No Response from NiFi-Registry test call"
                                     )
            else:
                raise ValueError("Bad API Endpoint")
    log.info("Completing Test Session Setup")


def remove_test_templates():
    all_templates = nipyapi.templates.list_all_templates().templates
    if all_templates is not None:
        for this_template in all_templates:
            if test_basename in this_template.template.name:
                nipyapi.templates.delete_template(this_template.id)


def remove_test_pgs():
    test_pgs = nipyapi.canvas.get_process_group(test_basename)
    if isinstance(test_pgs, list):
        for this_test_pg in test_pgs:
            nipyapi.canvas.delete_process_group(
                this_test_pg,
                force=True,
                refresh=True
            )
    elif isinstance(test_pgs, nipyapi.nifi.ProcessGroupEntity):
        nipyapi.canvas.delete_process_group(
            test_pgs,
            force=True,
            refresh=True
        )
    else:
        pass


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


def cleanup():
    # Only bulk-cleanup universally compatible components
    # Ideally we would clean each test environment, but it's too slow to do it
    # per test, so we rely on individual fixture cleanup
    log.info("Running bulk cleanup on %s",
             nipyapi.config.nifi_config.api_client.host)
    remove_test_templates()
    remove_test_processors()
    remove_test_pgs()


def cleanup_reg():
    # Bulk cleanup for tests involving NiFi Registry
    remove_test_pgs()
    remove_test_buckets()
    remove_test_registry_client()


@pytest.fixture(name='fix_templates', scope='function')
def fixture_templates(request, fix_pg):
    log.info("Creating PyTest Fixture fix_templates on endpoint %s",
             nipyapi.config.nifi_config.api_client.host)
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
    request.addfinalizer(cleanup)
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

    request.addfinalizer(cleanup)
    return Dummy()


@pytest.fixture(name='fix_proc')
def fixture_proc(request):
    class Dummy:
        def __init__(self):
            pass

        def generate(self, parent_pg=None, suffix='', valid=True):
            if parent_pg is None:
                target_pg = nipyapi.canvas.get_process_group(
                    nipyapi.canvas.get_root_pg_id(), 'id'
                )
            else:
                target_pg = parent_pg
            if valid:
                proc_type = 'GenerateFlowFile'
            else:
                proc_type = 'ListenSyslog'
            return nipyapi.canvas.create_processor(
                parent_pg=target_pg,
                processor=nipyapi.canvas.get_processor_type(
                    proc_type),
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
                test_bucket_name + suffix
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


@pytest.fixture(name='fix_ctv', scope='function')
def fixture_complex_template_versioning(request, fix_ver_flow):
    FixtureCTV = namedtuple(
        'FixtureCTV', getattr(fix_ver_flow, '_fields') + (
            'template', 'info_w_template', 'snapshot_w_template'
        )
    )
    f_t_type = 'complex'
    f_t_name = test_templates[f_t_type]
    f_t_filename = f_t_name + '.xml'
    f_t_path = path.join(
        path.dirname(__file__),
        test_resource_dir,
        f_t_filename
    )
    f_template = nipyapi.templates.get_template_by_name(f_t_name)
    if not f_template:
        nipyapi.templates.upload_template(
            pg_id=fix_ver_flow.pg.id,
            template_file=f_t_path
        )
        f_template = nipyapi.templates.get_template_by_name(f_t_name)
    _ = nipyapi.templates.deploy_template(
        fix_ver_flow.pg.id,
        f_template.id
    )
    f_info_2 = nipyapi.versioning.save_flow_ver(
        process_group=fix_ver_flow.pg,
        registry_client=fix_ver_flow.client,
        bucket=fix_ver_flow.bucket,
        flow_id=fix_ver_flow.flow.identifier
    )
    f_snapshot_2 = nipyapi.versioning.get_latest_flow_ver(
        fix_ver_flow.bucket.identifier,
        fix_ver_flow.flow.identifier
    )
    request.addfinalizer(cleanup)
    request.addfinalizer(cleanup_reg)
    return FixtureCTV(
        *fix_ver_flow,
        template=f_template,
        info_w_template=f_info_2,
        snapshot_w_template=f_snapshot_2
    )
