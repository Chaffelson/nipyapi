#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from nipyapi import system, config, nifi
from nipyapi.nifi import models


def test_get_nifi_version_info(regress):
    r = system.get_nifi_version_info()
    assert isinstance(r, models.version_info_dto.VersionInfoDTO)
    assert "ni_fi_version" in r.to_dict().keys()
    # print("\nFound NiFi version ({0}) at URI ({1})".format(
    #     r.ni_fi_version,
    #     config.swagger_config.host
    # ))


def test_get_node():
    # Todo write test
    # r = system.get_node()
    # assert isinstance(r, models.NodeDTO)
    pass


def test_get_cluster():
    # todo write test
    pass
