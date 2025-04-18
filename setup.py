#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('docs/history.rst') as history_file:
    history = history_file.read()

proj_version = '0.22.0'

with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()

tests_require=[
    'pytest>=7.2.0'
]

extras_require={
    'demo': ['docker>=2.5.1']
}

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
    tests_require=tests_require,
    extras_require=extras_require,
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: User Interfaces'
    ],
    test_suite='tests'
)
