#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from pprint import pprint
from random import randint

from nipyapi import Templates

test_templates = Templates()


class Testtemplates:
    def test_get_snippet(self):
        from nipyapi.swagger_client import SnippetEntity
        r = test_templates._make_pg_snippet('a61fdf81-015e-1000-0742-f7ab59855f67')
        assert isinstance(r, SnippetEntity)
        pprint(r)

    def test_create_template(self):
        from nipyapi.swagger_client import TemplateEntity
        r = test_templates.create_template(
            pg_id='a61fdf81-015e-1000-0742-f7ab59855f67',
            name='ATotallyUniqueTemplate' + str(randint(0, 50)),
            desc='Nothing Here'
        )
        assert isinstance(r, TemplateEntity)
        pprint(r)
