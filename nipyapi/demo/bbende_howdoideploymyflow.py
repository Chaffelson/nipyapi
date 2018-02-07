# coding: utf-8

"""
An implementation helper for the demo explained by Bryan Bende at:
https://bryanbende.com/development/2018/01/19/apache-nifi-how-do-i-deploy-my-flow
"""

from __future__ import absolute_import
from time import sleep
import logging
import sys
import docker
from nipyapi.demo.utils import DockerContainer


log = logging.getLogger()
log.setLevel(logging.INFO)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.INFO)
log.addHandler(stream)


d_network_name = 'bbdemo'
# Note that port definitions are container:host
# the tuple fomat is (hostname, imagename, portmappings, environment variables)

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

log.info(
    "Creating Docker client using Environment Variables")
d_client = docker.from_env()

# Pull relevant Images
log.info("Pulling relevant Docker Images")
for image in set([(c.image_name + ':' + c.image_tag) for c in d_containers]):
    log.info("- Pulling ({0})".format(image))
    d_client.images.pull(image)

# Clear previous containers
log.info("Clearing previous containers for this demo")
d_clear_list = [li for li in d_client.containers.list(all=True)
                if li.name in [i.name for i in d_containers]]
for c in d_clear_list:
    log.info("- Removing old container ({0})".format(c.name))
    c.remove(force=True)

# Deploy/Get Network
log.info("Getting Docker bridge network")
d_n_list = [li for li in d_client.networks.list()
            if d_network_name in li.name]
if not d_n_list:
    d_network = d_client.networks.create(
        name=d_network_name,
        driver='bridge',
        check_duplicate=True
    )
elif len(d_n_list) > 1:
    raise EnvironmentError("Too many test networks found")
else:
    log.info("- Found network ({0})".format(d_n_list[0]))
    d_network = d_n_list[0]

# Deploy Containers
log.info("Starting relevant Docker Containers")
c_hooks = {}
for c in d_containers:
    log.info("- Starting Container ({0})".format(c.name))
    c_hooks[c.name] = d_client.containers.run(
        image=c.image_name + ':' + c.image_tag,
        detach=True,
        network=d_network_name,
        hostname=c.name,
        name=c.name,
        ports=c.ports,
        environment=c.env
    )

log.info("Waiting on Service Startup")
max_retry = 10
for retry in range(0, max_retry):
    current_status = [(c.name, c.get_test_url_status()) for c in d_containers]
    if str(list(set([i[1] for i in current_status]))) == '[200]':
        log.info("- All started; status: ({0})".format(current_status))
        break
    else:
        log.info("- Retry ({0}), Status: ({1})".format(retry, current_status))
        sleep(10)
