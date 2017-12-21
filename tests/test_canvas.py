#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from nipyapi import canvas
from swagger_client import ProcessGroupFlowEntity


def test_get_root_pg_id():
    r = canvas.get_root_pg_id()
    assert isinstance(r, str)


def test_process_group_status():
    r = canvas.get_process_group_status(pg_id='root', detail='names')
    assert isinstance(r, dict)


def test_get_flow():
    r = canvas.recurse_flow('root')
    assert isinstance(r, ProcessGroupFlowEntity)
    assert r.process_group_flow.breadcrumb.breadcrumb.name == 'NiFi Flow'


def test_recurse_flow():
    pass


def test_list_all_process_groups():
    r = canvas.list_all_process_groups()
    assert isinstance(r, list)


def test_get_process_group_by_name():
    pass


def test_delete_process_group():
    pass
