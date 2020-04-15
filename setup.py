#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('docs/history.rst') as history_file:
    history = history_file.read()

proj_version = '0.14.3'

with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()

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
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: User Interfaces'
    ],
    test_suite='tests'
)
