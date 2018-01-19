# Docker Image Quickstart

This will create a single docker image containing both NiFi and the NiFi-Registry.  
This may not be desirable over using Docker Compose to create an environment more traditionally.

## Capabilities
This image currently supports running in unsecured standalone mode

## Building
You can build and run this image with the following command run from the directory of the Dockerfile:

    docker build -t nifi-dataflow:latest . && docker run -p 18080:18080 -p 8080:8080 --name nifi-dataflow nifi-dataflow:latest

