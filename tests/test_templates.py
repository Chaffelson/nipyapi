#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from os import path
from nipyapi import templates, nifi, canvas
from tests import conftest
from nipyapi.nifi import models as nifi_models
from lxml.etree import fromstring, parse


@pytest.mark.usefixtures('template_class_wrapper')
class TestTemplates(object):
    # Note that tests in this class are incremental
    # so consider order when adding new tests or modifying them
    t_type = 'basic'
    t_name = conftest.test_templates[t_type]
    t_filename = t_name + '.xml'
    t_path = path.join(
        path.dirname(__file__),
        conftest.test_resource_dir,
        t_filename
    )

    def test_upload_template(self):
        r = templates.upload_template(
            pg_id=canvas.get_root_pg_id(),
            template_file=self.t_path
        )
        assert isinstance(r, nifi_models.template_entity.TemplateEntity)
        with pytest.raises(AssertionError):
            r = templates.upload_template(
                pg_id=canvas.get_root_pg_id(),
                template_file='/tmp/haha/definitelynotafile.jpg'
            )
        # Try to upload an already existing template
        with pytest.raises(ValueError):
            r = templates.upload_template(
                pg_id=canvas.get_root_pg_id(),
                template_file=self.t_path
            )

    def test_all_templates(self):
        r = templates.list_all_templates()
        assert (isinstance(r, nifi_models.templates_entity.TemplatesEntity))

    def test_get_templates_by_name(self):
        r = templates.get_template_by_name(self.t_name)
        assert r is not None
        assert isinstance(r, nifi_models.template_entity.TemplateEntity)

    def test_deploy_template(self):
        r = templates.deploy_template(
            canvas.get_root_pg_id(),
            templates.get_template_by_name(self.t_name).id
        )
        assert isinstance(r, nifi_models.flow_entity.FlowEntity)

    def test_get_snippet(self):
        from nipyapi.nifi import SnippetEntity
        t_id = canvas.get_process_group('nipyapi_test_0').id
        r = templates.create_pg_snippet(t_id)
        assert isinstance(r, SnippetEntity)

    def test_create_template(self):
        from nipyapi.nifi import TemplateEntity
        t_id = canvas.get_process_group('nipyapi_test_0').id
        r = templates.create_template(
            pg_id=t_id,
            name='nipyapi_testTemplate_01',
            desc='Nothing Here'
        )
        assert isinstance(r, TemplateEntity)

    def test_export_template(self):
        template = templates.get_template_by_name(self.t_name)
        r = templates.export_template(template.id)
        _ = fromstring(r)
        r = templates.export_template(
            template.id,
            output='file',
            file_path='/tmp/nifi_template_test.xml'
        )
        assert r == '/tmp/nifi_template_test.xml'
        _ = parse('/tmp/nifi_template_test.xml')
        with pytest.raises(AssertionError):
            r = templates.export_template(
                template.id,
                output='file',
                file_path='/definitelynotapath/to/anythingthatshould/exist_'
            )
        with pytest.raises(ValueError):
            _ = templates.export_template(
                t_id=template.id,
                output='invalid'
            )

    def test_delete_template(self):
        template = templates.get_template_by_name('nipyapi_testTemplate_00')
        r = templates.delete_template(template.id)
        assert r is None
        with pytest.raises(ValueError):
            _ = templates.delete_template('invalid')

    def test_list_all_templates(self):
        # TODO: Implement test
        pass
