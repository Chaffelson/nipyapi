# nipyapi CLI Quickstart

## Prerequisites

```bash
brew install uv
```

## Install

```bash
uv pip install "nipyapi[cli] @ git+https://github.com/Chaffelson/nipyapi.git@feature/cli"
```

## Configure

```bash
export NIFI_API_ENDPOINT="https://your-nifi-host/nifi-api"
export NIFI_BEARER_TOKEN="your-jwt-token"
```

## Explore

```bash
# Check connection
nipyapi system get_nifi_version_info

# List registry clients
nipyapi versioning list_registry_clients

# Get a specific registry client by name
nipyapi versioning get_registry_client "ConnectorFlowRegistryClient"
```

## Deploy a Flow

```bash
# Get the registry client ID
REGISTRY_ID=$(nipyapi versioning get_registry_client "ConnectorFlowRegistryClient" | jq -r '.id')

# Deploy a flow from the registry
nipyapi ci deploy_flow \
  --registry_client_id "$REGISTRY_ID" \
  --bucket "connectors" \
  --flow "postgresql"
```
