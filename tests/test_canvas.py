#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from pprint import pprint

from nipyapi import canvas


class TestCanvas(object):
    def test_get_root_pg_id(self):
        r = canvas.get_root_pg_id()
        assert isinstance(r, str)

    def test_process_group_status(self):
        r = canvas.process_group_status(pg_id='root', detail='names')
        assert isinstance(r, dict)

    def test_recurse_flows(self):
        r = canvas._recurse_flows()
        assert isinstance(r, dict)

    def test_flow(self):
        r = canvas.flow('root')
        assert isinstance(r, dict)
        assert 'NiFi Flow' in r['name']

    def test_list_all_process_groups(self):
        r = canvas.list_all_process_groups()
        assert isinstance(r, list)

    def test_get_process_group_by_name(self):
        pass

    def test_delete_process_group(self):
        pass
