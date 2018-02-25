# coding: utf-8

"""
Common utils for demos
"""

from __future__ import absolute_import

import logging
from time import sleep

import docker
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__all__ = ['DockerContainer', 'start_docker_containers']


class DockerContainer(object):
    """
    Helper class for Docker container automation without using Ansible
    """
    def __init__(self, name=None, image_name=None, image_tag=None, ports=None,
                 env=None, volumes=None, test_url=None, endpoint=None):
        self.name = name
        self.image_name = image_name
        self.image_tag = image_tag
        self.ports = ports
        self.env = env
        self.volumes = volumes
        self.test_url = test_url
        self.endpoint = endpoint

    def get_test_url_status(self):
        """
        Checks if a URL is available
        :return: status code if available, String 'ConnectionError' if not
        """
        try:
            return requests.get(self.test_url).status_code
        except requests.ConnectionError:
            return 'ConnectionError'


def start_docker_containers(
        docker_containers, network_name='demo', test_connection=True):
    """
    Start a docker container on a given network.

    :param docker_containers: a list of docker containers to start
    :param network_name: the name of the Docker bridge network to create
        for the containers
    :param test_connection: a boolean flag (True or False) to control if this
        helper method should try the test url endpoint to verify each
        container starts.
    """
    logger.info("Creating Docker client using Environment Variables")
    d_client = docker.from_env()

    # Pull relevant Images
    logger.info("Pulling relevant Docker Images")
    for image in set([(c.image_name + ':' + c.image_tag)
                      for c in docker_containers]):
        logger.info("- Pulling %s", image)
        d_client.images.pull(image)

    # Clear previous containers
    logger.info("Clearing previous containers for this demo")
    d_clear_list = [li for li in d_client.containers.list(all=True)
                    if li.name in [i.name for i in docker_containers]]
    for c in d_clear_list:
        logger.info("- Removing old container %s", c.name)
        c.remove(force=True)

    # Deploy/Get Network
    logger.info("Getting Docker bridge network")
    d_n_list = [li for li in d_client.networks.list()
                if network_name in li.name]
    if not d_n_list:
        d_network = d_client.networks.create(
            name=network_name,
            driver='bridge',
            check_duplicate=True
        )
    elif len(d_n_list) > 1:
        raise EnvironmentError("Too many test networks found")
    else:
        d_network = d_n_list[0]
    logger.info("Using Docker network: {}".format(d_network.short_id))

    # Deploy Containers
    logger.info("Starting relevant Docker Containers")
    c_hooks = {}
    for c in docker_containers:
        logger.info("- Starting Container %s", c.name)
        c_hooks[c.name] = d_client.containers.run(
            image=c.image_name + ':' + c.image_tag,
            detach=True,
            network=network_name,
            hostname=c.name,
            name=c.name,
            ports=c.ports,
            environment=c.env,
            volumes=c.volumes
        )

    if test_connection:
        logger.info("Waiting on Service Startup")
        max_retry = 10
        for retry in range(0, max_retry):
            current_status = [(c.name, c.get_test_url_status())
                              for c in docker_containers]
            if str(list(set([i[1] for i in current_status]))) == '[200]':
                logger.info("- All started; status: %s", current_status)
                break
            else:
                logger.info("- Retry %s Status: %s", retry, current_status)
                sleep(10)
