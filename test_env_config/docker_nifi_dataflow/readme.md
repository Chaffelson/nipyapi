# Docker Image Quickstart

## Capabilities
This image currently supports running in unsecured standalone mode

## Building
You can build and run this image with the following command run from the directory of the Dockerfile:

    docker build -t nifi150-registry010 . && docker run -p 18080:18080 -p 8080:8080 --name nifi-150-registry-010 nifi150-registry010 

