#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from tests import conftest
import six
from lxml import etree
import nipyapi

if six.PY3:
    from io import StringIO
elif six.PY2:
    from StringIO import StringIO


def test_upload_template(fix_templates, regress):
    pg = fix_templates.pg.generate()
    r0 = nipyapi.templates.upload_template(
        pg_id=pg.id,
        template_file=fix_templates.c_file
    )
    assert isinstance(r0, nipyapi.nifi.TemplateEntity)
    # Check it's not an empty object
    assert isinstance(r0.template.uri, six.string_types)
    # Export it again and check it's good
    r1 = nipyapi.templates.export_template(
        r0.id,
        output='file',
        file_path='/tmp/nipyapi_test_template_001.xml'
    )
    # This test needs to be hand run, as it's difficult to test for the changed
    # UUIDs and timestamps and unimportant information.
    # t1 = etree.parse('/tmp/nipyapi_test_template_001.xml')
    # t2 = etree.parse(fix_templates.c_file)
    # DeepDiff(t1.getroot().itertext(), t2.getroot().itertext(), ignore_order=True)
    # Try to upload a nonexistant file
    with pytest.raises(AssertionError):
        _ = nipyapi.templates.upload_template(
            pg_id=pg.id,
            template_file='/tmp/haha/definitelynotafile.jpg'
        )
    # Try to upload an unopenable file
    with pytest.raises(AssertionError):
        _ = nipyapi.templates.upload_template(
            pg_id=pg.id,
            template_file='/dev/null'
        )
    # Try to upload an already existing template
    with pytest.raises(ValueError):
        _ = nipyapi.templates.upload_template(
            pg_id=pg.id,
            template_file=fix_templates.c_file
        )


def test_all_templates(fix_templates, regress):
    pg = fix_templates.pg.generate()
    _ = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.b_file
    )
    r = nipyapi.templates.list_all_templates()
    assert (isinstance(r, nipyapi.nifi.TemplatesEntity))
    assert len(r.templates) > 0


def test_get_templates_by_name(fix_templates, regress):
    pg = fix_templates.pg.generate()
    _ = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.b_file
    )
    r = nipyapi.templates.get_template_by_name(fix_templates.b_name)
    assert r is not None
    assert isinstance(r, nipyapi.nifi.TemplateEntity)


def test_deploy_template(fix_templates, regress):
    pg = fix_templates.pg.generate()
    t1 = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.b_file
    )
    r = nipyapi.templates.deploy_template(
        pg.id,
        t1.id
    )
    assert isinstance(r, nipyapi.nifi.FlowEntity)


def test_get_snippet(fix_pg, regress):
    t_pg = fix_pg.generate()
    r = nipyapi.templates.create_pg_snippet(t_pg.id)
    assert isinstance(r, nipyapi.nifi.SnippetEntity)


def test_create_template(fix_pg, regress):
    t_pg = fix_pg.generate()
    r = nipyapi.templates.create_template(
        pg_id=t_pg.id,
        name=conftest.test_basename + 'Template_99',
        desc='Nothing Here'
    )
    assert isinstance(r, nipyapi.nifi.TemplateEntity)


def test_export_template(fix_templates, regress):
    pg = fix_templates.pg.generate()
    t1 = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.b_file
    )
    assert isinstance(t1, nipyapi.nifi.TemplateEntity)
    r0 = nipyapi.templates.export_template(t1.id)
    assert r0[0] == '<'
    r1 = nipyapi.templates.export_template(
        t1.id,
        output='file',
        file_path='/tmp/nifi_template_test.xml'
    )
    assert r1[0] == '<'
    _ = etree.parse('/tmp/nifi_template_test.xml')
    with pytest.raises(AssertionError):
        _ = nipyapi.templates.export_template(
            t1.id,
            output='file',
            file_path='/definitelynotapath/to/anythingthatshould/exist_'
        )
    with pytest.raises(AssertionError):
        _ = nipyapi.templates.export_template(
            t_id=t1.id,
            output='invalid'
        )


def test_delete_template(fix_templates, regress):
    pg = fix_templates.pg.generate()
    t1 = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.b_file
    )
    r = nipyapi.templates.delete_template(t1.id)
    assert isinstance(r, nipyapi.nifi.TemplateEntity)
    with pytest.raises(ValueError):
        _ = nipyapi.templates.delete_template('invalid')
