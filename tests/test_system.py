#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nipyapi` package."""

import pytest
from nipyapi import system
from swagger_client import models


def test_get_nifi_version_info():
    r = system.get_nifi_version_info()
    assert isinstance(r, models.version_info_dto.VersionInfoDTO)
    assert "ni_fi_version" in r.to_dict().keys()


# def test_get_node():
#     r = system.get_node()
#     assert isinstance(r, models.NodeDTO)
