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


def test_upload_template(regress_nifi, fix_templates):
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


def test_all_templates(regress_nifi, fix_templates):
    pg = fix_templates.pg.generate()
    _ = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.b_file
    )
    r = nipyapi.templates.list_all_templates()
    assert (isinstance(r, nipyapi.nifi.TemplatesEntity))
    assert len(r.templates) > 0


def test_get_templates_by_name(regress_nifi, fix_templates):
    pg = fix_templates.pg.generate()
    _ = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.b_file
    )
    r = nipyapi.templates.get_template_by_name(fix_templates.b_name)
    assert r is not None
    assert isinstance(r, nipyapi.nifi.TemplateEntity)


def test_get_template(regress_nifi, fix_templates):
    pg = fix_templates.pg.generate()
    _ = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.b_file
    )
    r0 = nipyapi.templates.get_template(fix_templates.b_name)
    assert r0 is not None
    assert isinstance(r0, nipyapi.nifi.TemplateEntity)
    r1 = nipyapi.templates.get_template(fix_templates.b_name, greedy=True)
    assert r1 is not None
    assert isinstance(r1, nipyapi.nifi.TemplateEntity)
    _ = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.g_file
    )
    r3 = nipyapi.templates.get_template(fix_templates.b_name)
    assert r3 is not None
    assert isinstance(r3, nipyapi.nifi.TemplateEntity)
    r4 = nipyapi.templates.get_template(fix_templates.b_name, greedy=True)
    assert r4 is not None
    assert isinstance(r4, list)
    assert isinstance(r4[0], nipyapi.nifi.TemplateEntity)
    assert len(r4) == 2


def test_deploy_template(regress_nifi, fix_templates):
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


def test_get_snippet(regress_nifi, fix_pg):
    t_pg = fix_pg.generate()
    r = nipyapi.templates.create_pg_snippet(t_pg.id)
    assert isinstance(r, nipyapi.nifi.SnippetEntity)


def test_create_template(regress_nifi, fix_pg):
    t_pg = fix_pg.generate()
    r = nipyapi.templates.create_template(
        pg_id=t_pg.id,
        name=conftest.test_basename + 'Template_99',
        desc='Nothing Here'
    )
    assert isinstance(r, nipyapi.nifi.TemplateEntity)


def test_export_template(regress_nifi, fix_templates):
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


def test_delete_template(regress_nifi, fix_templates):
    pg = fix_templates.pg.generate()
    t1 = nipyapi.templates.upload_template(
        pg.id,
        fix_templates.b_file
    )
    r = nipyapi.templates.delete_template(t1.id)
    assert isinstance(r, nipyapi.nifi.TemplateEntity)
    with pytest.raises(ValueError):
        _ = nipyapi.templates.delete_template('invalid')


def test_load_template_from_file_path(fix_templates):
    template_entity = nipyapi.templates.load_template_from_xml_file_path(fix_templates.c_file)
    assert isinstance(template_entity, nipyapi.nifi.TemplateEntity)
    # we should be able to DeepDiff these
    # but the template _from_ NIFI does not have the inner
    # snipit
    # pg = fix_templates.pg.generate()
    # _ = nipyapi.templates.upload_template(
    #    pg.id,
    #    fix_templates.c_file
    # )
    # nifi_template = nipyapi.templates.get_template(fix_templates.c_name)
    # assert nifi_template is not None
    # assert isinstance(nifi_template, nipyapi.nifi.TemplateEntity)
    # from deepdiff import DeepDiff
    # diff_output = DeepDiff(template_entity, nifi_template, ignore_order=True)
    # assert len(diff_output['type_changes']) == 6


def test_load_template_from_file_path_bad_path():
    with pytest.raises(AssertionError):
        nipyapi.templates.load_template_from_xml_file_path('nothing-to-see-here.nope')
    with pytest.raises(AssertionError):
        # TODO: fix so that we can test None as well
        nipyapi.templates.load_template_from_xml_file_path("")


def test_load_template_from_xml_file(fix_templates):
    with open(fix_templates.c_file, "r") as template_file:
        template_entity = nipyapi.templates.load_template_from_xml_file_stream(template_file)
        assert isinstance(template_entity, nipyapi.nifi.TemplateEntity)


def test_load_template_from_xml_string(fix_templates):
    with open(fix_templates.c_file, "r") as template_file:
        data = template_file.read()
        template_entity = nipyapi.templates.load_template_from_xml_string(data)
        assert isinstance(template_entity, nipyapi.nifi.TemplateEntity)


def test_load_template_from_xml_really_json_string():
    from pyexpat import ExpatError
    with pytest.raises(ExpatError):
        nipyapi.templates.load_template_from_xml_string("{'foo':'bar'}")
