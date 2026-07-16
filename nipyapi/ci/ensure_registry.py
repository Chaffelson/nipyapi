# pylint: disable=duplicate-code
"""
ensure_registry - convenience function for Git Flow Registry Client setup.

Wraps nipyapi.versioning.ensure_registry_client with:
- Environment variable support for CI/CD
- Provider abstraction (GitHub/GitLab/Azure DevOps)
- Sensible defaults
"""

import logging
import os
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)

# Provider configurations
PROVIDERS = {
    "github": {
        "reg_type": "org.apache.nifi.github.GitHubFlowRegistryClient",
        "api_url_key": "GitHub API URL",
        "api_url_default": "https://api.github.com/",
        "owner_key": "Repository Owner",
        "auth_type_key": "Authentication Type",
        "auth_type_value": "PERSONAL_ACCESS_TOKEN",
        "token_key": "Personal Access Token",
    },
    "gitlab": {
        "reg_type": "org.apache.nifi.gitlab.GitLabFlowRegistryClient",
        "api_url_key": "GitLab API URL",
        "api_url_default": "https://gitlab.com/",
        "owner_key": "Repository Namespace",
        "auth_type_key": "Authentication Type",
        "auth_type_value": "ACCESS_TOKEN",
        "token_key": "Access Token",
    },
}


# pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
def ensure_registry(
    token: Optional[str] = None,
    repo: Optional[str] = None,
    client_name: Optional[str] = None,
    provider: Optional[str] = None,
    api_url: Optional[str] = None,
    default_branch: Optional[str] = None,
    repository_path: Optional[str] = None,
    tenant_id: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
    repository: Optional[str] = None,
) -> dict:
    """
    Ensure a Git Flow Registry Client exists with the desired configuration.

    Args:
        token: Personal Access Token. Env: GH_REGISTRY_TOKEN or GL_REGISTRY_TOKEN
        repo: Repository in owner/repo format. Env: NIFI_REGISTRY_REPO
        client_name: Registry client name. Env: NIFI_REGISTRY_CLIENT_NAME
        provider: "github", "gitlab", or "azuredevops". Env: NIFI_REGISTRY_PROVIDER
        api_url: API URL override. Env: NIFI_REGISTRY_API_URL
        default_branch: Default branch. Env: NIFI_REGISTRY_BRANCH
        repository_path: Path in repo. Env: NIFI_REPOSITORY_PATH
        tenant_id: (azuredevops) Entra tenant id. Env: NIFI_ADO_TENANT_ID
        client_id: (azuredevops) service principal client id. Env: NIFI_ADO_CLIENT_ID
        client_secret: (azuredevops) service principal secret. Env: NIFI_ADO_CLIENT_SECRET
        organization: (azuredevops) Azure DevOps organization. Env: NIFI_ADO_ORG
        project: (azuredevops) Azure DevOps project. Env: NIFI_ADO_PROJECT
        repository: (azuredevops) Azure DevOps repository name. Env: NIFI_ADO_REPO

    Returns:
        dict with registry_client_id and registry_client_name

    Raises:
        ValueError: Missing required parameters
        Exception: NiFi API errors
    """
    # Resolve from env vars with defaults
    # Determine provider first so we can select the correct token env var
    provider = (provider or os.environ.get("NIFI_REGISTRY_PROVIDER") or "github").lower()

    # Azure DevOps authenticates with a service principal (OAuth2 client
    # credentials) and requires two controller services, which do not fit the
    # token-property provider model below. Dispatch to the dedicated helper.
    if provider in ("azuredevops", "azure-devops", "ado"):
        return _ensure_registry_azuredevops(
            client_name=client_name,
            default_branch=default_branch,
            repository_path=repository_path,
            api_url=api_url,
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            organization=organization,
            project=project,
            repository=repository,
        )

    # Select token based on provider - check provider-specific env var first
    if not token:
        if provider == "gitlab":
            token = os.environ.get("GL_REGISTRY_TOKEN") or os.environ.get("GH_REGISTRY_TOKEN")
        else:
            token = os.environ.get("GH_REGISTRY_TOKEN") or os.environ.get("GL_REGISTRY_TOKEN")

    repo = repo or os.environ.get("NIFI_REGISTRY_REPO")
    client_name = client_name or os.environ.get("NIFI_REGISTRY_CLIENT_NAME")
    api_url = api_url or os.environ.get("NIFI_REGISTRY_API_URL")
    default_branch = default_branch or os.environ.get("NIFI_REGISTRY_BRANCH") or "main"
    repository_path = repository_path or os.environ.get("NIFI_REPOSITORY_PATH") or ""

    # Validate
    if provider not in PROVIDERS:
        raise ValueError(
            f"Invalid provider '{provider}'. Must be 'github', 'gitlab', or 'azuredevops'"
        )
    if not token:
        raise ValueError("token is required (or set GH_REGISTRY_TOKEN / GL_REGISTRY_TOKEN)")
    if not repo or "/" not in repo:
        raise ValueError("repo must be in owner/repo format (or set NIFI_REGISTRY_REPO)")

    # Default client name based on provider
    if not client_name:
        client_name = f"{provider.title()}-FlowRegistry"

    config = PROVIDERS[provider]
    repo_owner, repo_name = repo.split("/", 1)

    log.info(
        "Ensuring %s registry client '%s' for %s/%s", provider, client_name, repo_owner, repo_name
    )

    # Build properties
    resolved_api_url = api_url or config["api_url_default"]
    properties = {
        config["api_url_key"]: resolved_api_url,
        config["owner_key"]: repo_owner,
        "Repository Name": repo_name,
        config["auth_type_key"]: config["auth_type_value"],
        config["token_key"]: token,
        "Default Branch": default_branch,
        "Parameter Context Values": "IGNORE_CHANGES",
    }
    if repository_path:
        properties["Repository Path"] = repository_path

    log.debug("API URL: %s", resolved_api_url)
    log.debug("Default branch: %s", default_branch)
    if repository_path:
        log.debug("Repository path: %s", repository_path)

    # Create/update registry client
    log.debug("Calling ensure_registry_client with reg_type=%s", config["reg_type"])
    client = nipyapi.versioning.ensure_registry_client(
        name=client_name,
        reg_type=config["reg_type"],
        description=f"{provider.title()} Registry Client for {repo_owner}/{repo_name}",
        properties=properties,
    )

    log.info("Registry client ready: %s (ID: %s)", client.component.name, client.id)
    log.debug("Validation status: %s", client.component.validation_status)

    return {
        "registry_client_id": client.id,
        "registry_client_name": client.component.name,
    }


# pylint: disable=too-many-arguments,too-many-positional-arguments
def _ensure_registry_azuredevops(
    client_name=None,
    default_branch=None,
    repository_path=None,
    api_url=None,
    tenant_id=None,
    client_id=None,
    client_secret=None,
    organization=None,
    project=None,
    repository=None,
) -> dict:
    """
    Ensure an Azure DevOps Flow Registry Client (service-principal auth).

    Resolves Azure DevOps parameters from arguments or NIFI_ADO_* environment
    variables, then provisions the required controller services and the registry
    client via nipyapi.versioning.ensure_azuredevops_registry.
    """
    tenant_id = tenant_id or os.environ.get("NIFI_ADO_TENANT_ID")
    client_id = client_id or os.environ.get("NIFI_ADO_CLIENT_ID")
    client_secret = client_secret or os.environ.get("NIFI_ADO_CLIENT_SECRET")
    organization = organization or os.environ.get("NIFI_ADO_ORG")
    project = project or os.environ.get("NIFI_ADO_PROJECT")
    repository = repository or os.environ.get("NIFI_ADO_REPO")
    default_branch = default_branch or os.environ.get("NIFI_REGISTRY_BRANCH") or "main"
    repository_path = repository_path or os.environ.get("NIFI_REPOSITORY_PATH") or None
    client_name = (
        client_name or os.environ.get("NIFI_REGISTRY_CLIENT_NAME") or "AzureDevOps-FlowRegistry"
    )

    required = {
        "tenant_id": tenant_id,
        "client_id": client_id,
        "client_secret": client_secret,
        "organization": organization,
        "project": project,
        "repository": repository,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise ValueError(
            "Azure DevOps provider requires "
            + ", ".join(missing)
            + " (or the corresponding NIFI_ADO_* environment variables)"
        )

    extra = {}
    if api_url:
        extra["api_url"] = api_url
    if repository_path:
        extra["repository_path"] = repository_path

    log.info(
        "Ensuring azuredevops registry client '%s' for %s/%s/%s",
        client_name,
        organization,
        project,
        repository,
    )
    client = nipyapi.versioning.ensure_azuredevops_registry(
        name=client_name,
        organization=organization,
        project=project,
        repository=repository,
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
        default_branch=default_branch,
        **extra,
    )
    log.info("Registry client ready: %s (ID: %s)", client.component.name, client.id)
    return {
        "registry_client_id": client.id,
        "registry_client_name": client.component.name,
    }
