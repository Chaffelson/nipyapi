# coding: utf-8

"""
An implementation helper for the demo explained by Bryan Bende at:
https://bryanbende.com/development/2018/01/19/apache-nifi-how-do-i-deploy-my-flow
"""

from __future__ import absolute_import
import logging
import sys
import nipyapi
from nipyapi.utils import DockerContainer


log = logging.getLogger()
log.setLevel(logging.INFO)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.INFO)
log.addHandler(stream)


d_network_name = 'bbdemo'

d_containers = [
    DockerContainer(
        name='nipyapi_nifi_1',
        image_name='chaffelson/nifi',
        image_tag='1.5.0',
        ports={'8080/tcp': 8080},
        test_url='http://localhost:8080/nifi'
    ),
    DockerContainer(
        name='nipyapi_nifi_2',
        image_name='chaffelson/nifi',
        image_tag='1.5.0',
        ports={'9090/tcp': 9090},
        env=['NIFI_WEB_HTTP_PORT=9090'],
        test_url='http://localhost:9090/nifi'
    ),
    DockerContainer(
        name='nipyapi_reg',
        image_name='chaffelson/nifi-registry',
        image_tag='0.1.0',
        ports={'18080/tcp': 18080},
        test_url='http://localhost:18080/nifi-registry'
    ),
    DockerContainer(
        name='nipyapi_solr',
        image_name='solr',
        image_tag='7.2.1',
        ports={'8983/tcp': 8983},
        test_url='http://localhost:8983'
    ),
]

nipyapi.utils.start_docker_containers(
    d_containers,
    d_network_name
)
