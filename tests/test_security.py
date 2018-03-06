#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for nipyapi security module."""

import pytest
from tests import conftest
import nipyapi


def test_bootstrap_secured_nifi():
    pass
    # u = nipyapi.security.get_service_user('nobel')
    # p = nipyapi.security.create_access_policy(
    #     resource='process-groups',
    #     action='write',
    #     r_id=nipyapi.canvas.get_root_pg_id(),
    #     service='nifi'
    # )
    # nipyapi.security.add_user_to_access_policy(
    #     user=u,
    #     policy=p,
    #     service='nifi'
    # )
