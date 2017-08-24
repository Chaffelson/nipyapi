#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'nifi-python-swagger-client'
]

setup_requirements = [
    'pytest-runner',
    'nifi-python-swagger-client'
]

test_requirements = [
    'pytest',
    'nifi-python-swagger-client'
]

setup(
    name='nipyapi',
    version='0.1.1',
    description="Nifi-Python-Api: A convenient Python wrapper for the Apache NiFi Rest API",
    long_description=readme + '\n\n' + history,
    author="Daniel Chaffelson",
    author_email='chaffelson@gmail.com',
    url='https://github.com/Chaffelson/nipyapi',
    download_url = 'https://github.com/Chaffelson/nipyapi/archive/0.1.0.tar.gz',
    packages=find_packages(include=['nipyapi']),
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
    dependency_links=['git+git://github.com/Chaffelson/nifi-python-swagger-client.git#egg=nifi-python-swagger-client']
)
