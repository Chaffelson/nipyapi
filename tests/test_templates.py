#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from pprint import pprint
from random import randint

from nipyapi import Templates, Canvas

t = Templates()
c = Canvas()
root_pg_id = c.get_root_pg_id()


class Testtemplates:
    def test_get_templates_by_name(self):
        try:
            r1 = t.get_template_by_name('testTemplate_00')
            # Template found, remove it to test again
            r2 = t.delete_template(r1['id'])
        except ValueError:
            # We don't want the Template to already be present
            # TODO: Turn this into test init calls
            pass

    def test_upload_template(self):
        r = t.upload_template(
            pg_id=root_pg_id,
            template_file='test_env_config/testTemplate_00.xml'
        )

    def test_deploy_template(self):
        r = t.deploy_template(
            root_pg_id,
            t.get_template_by_name('testTemplate_00')['id']
        )

    def test_get_snippet(self):
        from nipyapi.swagger_client import SnippetEntity
        # This assumes the above Template deployment tests have been run
        # TODO: Make tests independent rather than sequence dependent
        test_pg_id = c.get_process_group_by_name('Layer0')['id']
        r = t._make_pg_snippet(test_pg_id)
        assert isinstance(r, SnippetEntity)

    def test_create_template(self):
        from nipyapi.swagger_client import TemplateEntity
        test_pg_id = c.get_process_group_by_name('Layer0')['id']
        r = t.create_template(
            pg_id=test_pg_id,
            name='ATotallyUniqueTemplate' + str(randint(0, 50)),
            desc='Nothing Here'
        )
        assert isinstance(r, TemplateEntity)
