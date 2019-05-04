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

FROM python:3.6-alpine

LABEL maintainer="Dan Chaffelson <chaffelson@gmail.com>"
LABEL site="https://github.com/Chaffelson/nipyapi"

ENV PYTHONUNBUFFERED=0
ENV TZ=${TZ:-"Europe/London"}
ENV BRANCH=${BRANCH:-"master"}

RUN apk update && apk upgrade \
    && apk add --no-cache --virtual .build-deps git gcc libffi-dev musl-dev \
    libressl-dev ca-certificates python3-dev linux-headers tzdata  \
    && apk add --no-cache libxslt-dev libxml2-dev libgcrypt-dev \
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

COPY . /nipyapi
WORKDIR /nipyapi

RUN pip install --no-cache --no-use-pep517 -r requirements.txt

ENV PYTHONPATH=/nipyapi

ENTRYPOINT ["python3"]
