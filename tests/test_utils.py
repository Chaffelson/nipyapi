#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` _utils package."""

from __future__ import absolute_import
import sys
import pytest
import six
from tests import conftest
import json
from deepdiff import DeepDiff
from nipyapi import utils, nifi, system
from nipyapi.config import default_string_encoding as DEF_ENCODING


def test_dump(regress_flow_reg, fix_flow_serde):
    # Testing that we don't modify or lose information in the round trip
    # Processing in memory for json
    export_obj = json.loads(fix_flow_serde.raw.decode(DEF_ENCODING))
    ss_json = utils.dump(
        obj=export_obj,
        mode='json'
    )
    assert isinstance(ss_json, six.string_types)
    round_trip_json = utils.load(ss_json)
    with pytest.raises(AssertionError):
        _ = utils.dump('', 'FakeNews')
    with pytest.raises(TypeError):
        _ = utils.dump({None}, 'json')
    # Test Yaml
    ss_yaml = utils.dump(
        obj=export_obj,
        mode='yaml'
    )
    assert isinstance(ss_yaml, six.string_types)
    round_trip_yaml = utils.load(ss_yaml)
    assert DeepDiff(
        round_trip_json,
        round_trip_yaml,
        verbose_level=2,
        ignore_order=False
    ) == {}


def test_load(regress_flow_reg, fix_flow_serde):
    # Validating load testing again in case we break the 'dump' test
    r1 = utils.load(
        obj=fix_flow_serde.json,
        dto=fix_flow_serde.dto
    )
    # Validate match
    assert DeepDiff(
        fix_flow_serde.snapshot.flow_contents,
        r1.flow_contents,
        verbose_level=2,
        ignore_order=True
    ) == {}
    with pytest.raises(AssertionError):
        _ = utils.load({})


def test_fs_write(tmpdir):
    f_fdir = tmpdir.mkdir(conftest.test_write_file_path)
    f_fpath = f_fdir.join(conftest.test_write_file_name)
    test_obj = conftest.test_write_file_name
    r1 = utils.fs_write(
        obj=test_obj,
        file_path=f_fpath
    )
    assert r1 == test_obj
    # Test writing to an invalid location
    if sys.version_info >= (3,3):
        with pytest.raises((OSError, IOError, PermissionError)):
            _ = utils.fs_write(
                obj=test_obj,
                file_path='/dev/AlmostCertainlyNotAValidDevice'
            )
    else:
        with pytest.raises((OSError, IOError)):
            _ = utils.fs_write(
                obj=test_obj,
                file_path='/dev/AlmostCertainlyNotAValidDevice'
            )
    # Test writing an invalid object
    with pytest.raises((TypeError,AttributeError)):
        _ = utils.fs_write(
            obj={},
            file_path=f_fpath
        )


def test_fs_read(fix_flow_serde):
    r1 = utils.fs_read(
        file_path=fix_flow_serde.filepath + '.json'
    )
    assert r1 == fix_flow_serde.json
    # Test reading from unreachable file
    if sys.version_info >= (3,3):
        with pytest.raises((OSError, IOError, FileNotFoundError, PermissionError)):
            _ = utils.fs_read(
                file_path='/dev/AlmostCertainlyNotAValidDevice'
            )
    else:
        with pytest.raises((OSError, IOError)):
            _ = utils.fs_read(
                file_path='/dev/AlmostCertainlyNotAValidDevice'
            )


def test_filter_obj(fix_pg):
    f_pg = fix_pg.generate()
    t_1 = ['pie']
    with pytest.raises(ValueError):
        _ = utils.filter_obj(t_1, '', '')
    with pytest.raises(ValueError):
        _ = utils.filter_obj([f_pg], '', 'pie')
    r1 = utils.filter_obj([f_pg], conftest.test_pg_name, 'name')
    assert isinstance(r1, nifi.ProcessGroupEntity)
    r2 = utils.filter_obj([f_pg], 'FakeNews', 'name')
    assert r2 is None
    f_pg2 = fix_pg.generate(suffix='2')
    # Test greedy
    r3 = utils.filter_obj([f_pg, f_pg2], conftest.test_pg_name, 'name')
    assert isinstance(r3, list)
    # Test not greedy
    r4 = utils.filter_obj([f_pg, f_pg2], conftest.test_pg_name, 'name',
                          greedy=False)
    assert isinstance(r4, nifi.ProcessGroupEntity)
    r5 = utils.filter_obj([], '', '')
    assert r5 is None


def test_wait_to_complete():
    # TODO: Implement test
    pass


def test_check_version(regress_nifi):
    # We expect the passed version to be older than the system version, and
    # the response to therefore be -1 (older/negative, newer/positive)

    # minimum version test
    assert utils.check_version('1.1.2') <= 0
    # Check equivalence
    assert utils.check_version('1.2.3', '1.2.3') == 0
    # base is older than comp
    assert utils.check_version('1.1.3', '1.2.3') == -1
    # base is newer than comp
    assert utils.check_version('1.2.3', '0.2.3') == 1
    # Check RC
    assert utils.check_version('1.0.0-rc1', '1.0.0') == -1
    # Check that snapshots are disregarded
    assert utils.check_version('1.11.0', '1.13.0-SNAPSHOT') == -1
    assert utils.check_version('1.11.0', "1.11.0-SNAPSHOT") == 0
    assert utils.check_version('1.11.0', "1.10.0-SNAPSHOT") == 1
    # Check current version
    assert utils.check_version(
        system.get_nifi_version_info().ni_fi_version
    ) == 0
