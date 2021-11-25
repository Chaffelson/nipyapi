#!/usr/bin/env bash

set -x
set -e
set -u

sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum update -y
sudo yum install -y centos-release-scl yum-utils device-mapper-persistent-data lvm2
sudo yum install -y rh-python38 docker
sudo systemctl start docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
source /opt/rh/rh-python38/enable
pip install --upgrade pip
pip install -r ../../requirements.txt
pip install -r ../../requirements_dev.txts

