#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` _utils package."""

from __future__ import absolute_import
import pytest
from tests import conftest
import json
from ruamel.yaml import safe_load
from deepdiff import DeepDiff
from nipyapi import _utils
# Fix for Py3 introducing better IO errors, but not available in Py2
try:
    from nipyapi._utils import PermissionError, FileNotFoundError
except ImportError:
    pass


def test_dump(fix_flow_serde):
    # Testing that we don't modify or lose information in the round trip
    # Processing in memory for json
    ss_json = _utils.dump(
        obj=fix_flow_serde.snapshot.flow_contents,
        mode='json'
    )
    assert isinstance(ss_json, str)
    round_trip_json = safe_load(ss_json)
    # assert that a basic match of the dicts is true
    assert round_trip_json == fix_flow_serde.snapshot.flow_contents.to_dict()
    # Deepdiff returns an empty dict on no variations at a much deeper detail
    assert DeepDiff(
        fix_flow_serde.snapshot.flow_contents.to_dict(),
        round_trip_json,
        verbose_level=2
    ) == {}
    # Todo: test sorting


def test_load(fix_flow_serde):
    # Validating load testing again in case we break the 'dump' test
    r1 = _utils.load(
        obj=fix_flow_serde.json
    )
    # Validate dicts match
    assert r1 == fix_flow_serde.snapshot.flow_contents.to_dict()
    assert DeepDiff(
        fix_flow_serde.snapshot.flow_contents.to_dict(),
        r1,
        verbose_level=2
    ) == {}
    # TODO: Test sorting


def test_fs_write(tmpdir):
    f_fdir = tmpdir.mkdir(conftest.test_write_file_path)
    f_fpath = f_fdir.join(conftest.test_write_file_name)
    test_obj = conftest.test_write_file_name
    r1 = _utils.fs_write(
        obj=test_obj,
        file_path=f_fpath
    )
    assert r1 == test_obj
    # Test writing to an invalid location
    with pytest.raises(PermissionError):
        _ = _utils.fs_write(
            obj=test_obj,
            file_path='/dev/AlmostCertainlyNotAValidDevice'
        )
    # Test writing an invalid object
    with pytest.raises(TypeError):
        _ = _utils.fs_write(
            obj={},
            file_path=f_fpath
        )


def test_fs_read(fix_flow_serde, tmpdir):
    r1 = _utils.fs_read(
        file_path=fix_flow_serde.filepath
    )
    assert r1 == fix_flow_serde.json
    # Test reading from unreachable file
    with pytest.raises(FileNotFoundError):
        _ = _utils.fs_read(
            file_path='/dev/AlmostCertainlyNotAValidDevice'
        )
