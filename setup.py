#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('docs/history.rst') as history_file:
    history = history_file.read()

proj_version = '0.6.1'

requirements = [
    'certifi',
    'six',
    'python_dateutil',
    'urllib3',
    'lxml',
    'nifi-python-swagger-client>=1.2.1, <1.3'
]

setup_requirements = [
    'certifi',
    'pytest-runner'
]

test_requirements = [
    'certifi',
    'pytest'
]

setup(
    name='nipyapi',
    version=proj_version,
    description="Nifi-Python-Api: A convenient Python wrapper for the Apache NiFi Rest API",
    long_description=readme + '\n\n' + history,
    author="Daniel Chaffelson",
    author_email='chaffelson@gmail.com',
    url='https://github.com/Chaffelson/nipyapi',
    download_url='https://github.com/Chaffelson/nipyapi/archive/' + proj_version + '.tar.gz',
    packages=find_packages(
        include=['nipyapi'],
        exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']
    ),
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords=['nipyapi', 'nifi', 'api', 'wrapper'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
