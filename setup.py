#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Legacy shim delegating to declarative config.

Setuptools will pick metadata from pyproject.toml. Keep a minimal setup() call
for compatibility with tooling that still invokes setup.py.
"""

from setuptools import setup

setup()
