# Docker Compose for NiPyApi test environment

## Pre-Requisites

- install docker-compose [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Usage

Start a cluster:

- ```docker-compose up -d ```

Stop a cluster:

- ```docker-compose stop```

## Environment Details

- Apache NiFi 1.2.0 available on port 10120
- Apache NiFi 1.4.0 available on port 10140
- Apache NiFi 1.5.0 available on port 8080
- Apache NiFi-Registry 0.1.0 available on port 18080

### Notes
Where possible the latest version will be available on the defaul port, with older versions on identifiable ports for back testing
