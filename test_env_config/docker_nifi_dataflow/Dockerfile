# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

FROM openjdk:8-jdk-slim
LABEL maintainer="Dan Chaffelson <chaffelson@gmail.com>"
LABEL site="https://github.com/Chaffelson/nipyapi"

ARG UID=1000
ARG GID=1000
ARG NIFI_REGISTRY_VERSION=0.1.0
ARG NIFI_VERSION=1.5.0
ARG MIRROR=https://archive.apache.org/dist

ENV BASE_DIR /opt/nifi
ENV NIFI_REGISTRY_BASE_DIR ${BASE_DIR}/nifi-registry
ENV NIFI_BASE_DIR ${BASE_DIR}/nifi
ENV NIFI_REGISTRY_HOME=${NIFI_REGISTRY_BASE_DIR}/nifi-registry-${NIFI_REGISTRY_VERSION}
ENV NIFI_REGISTRY_BINARY_URL=nifi/nifi-registry/nifi-registry-${NIFI_REGISTRY_VERSION}/nifi-registry-${NIFI_REGISTRY_VERSION}-bin.tar.gz
ENV NIFI_HOME=${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}
ENV NIFI_BINARY_URL=/nifi/${NIFI_VERSION}/nifi-${NIFI_VERSION}-bin.tar.gz

ADD sh/ ${BASE_DIR}/scripts/


# Setup NiFi user
RUN groupadd -g ${GID} nifi || groupmod -n nifi `getent group ${GID} | cut -d: -f1` \
    && useradd --shell /bin/bash -u ${UID} -g ${GID} -m nifi \
    && mkdir ${NIFI_REGISTRY_BASE_DIR} \
    && mkdir ${NIFI_BASE_DIR} \
    && chown -R nifi:nifi ${BASE_DIR} \
    && apt-get update -y \
    && apt-get install -y curl jq xmlstarlet

USER nifi

# Download, validate, and expand Apache NiFi-Registry binary.
RUN curl -fSL ${MIRROR}/${NIFI_REGISTRY_BINARY_URL} -o ${NIFI_REGISTRY_BASE_DIR}/nifi-registry-${NIFI_REGISTRY_VERSION}-bin.tar.gz \
    && echo "$(curl ${MIRROR}/${NIFI_REGISTRY_BINARY_URL}.sha256) *${NIFI_REGISTRY_BASE_DIR}/nifi-registry-${NIFI_REGISTRY_VERSION}-bin.tar.gz" | sha256sum -c - \
    && tar -xvzf ${NIFI_REGISTRY_BASE_DIR}/nifi-registry-${NIFI_REGISTRY_VERSION}-bin.tar.gz -C ${NIFI_REGISTRY_BASE_DIR} \
    && rm ${NIFI_REGISTRY_BASE_DIR}/nifi-registry-${NIFI_REGISTRY_VERSION}-bin.tar.gz \
    && chown -R nifi:nifi ${NIFI_REGISTRY_HOME}

# Download, validate, and expand Apache NiFi binary.
RUN curl -fSL ${MIRROR}/${NIFI_BINARY_URL} -o ${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}-bin.tar.gz \
    && echo "$(curl ${MIRROR}/${NIFI_BINARY_URL}.sha256) *${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}-bin.tar.gz" | sha256sum -c - \
    && tar -xvzf ${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}-bin.tar.gz -C ${NIFI_BASE_DIR} \
    && rm ${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}-bin.tar.gz \
    && chown -R nifi:nifi ${NIFI_HOME}

# Web HTTP(s) ports & Site2Site ports
EXPOSE 18080 8080 8443 10000

WORKDIR ${BASE_DIR}
# Apply configuration and start NiFi / Registry
CMD ${BASE_DIR}/scripts/start.sh
