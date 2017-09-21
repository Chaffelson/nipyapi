#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from pprint import pprint

from nipyapi import Canvas

test_canvas = Canvas()


class TestCanvas:
    def test_process_group(self):
        r = test_canvas.process_group(pg_id='root', detail='names')
        assert isinstance(r, dict)

    def test_get_tree(self):
        r = test_canvas._get_tree()
        pprint(r)
