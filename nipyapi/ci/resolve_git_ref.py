"""
Resolve git refs (tags/branches) to commit SHAs.
"""

import re
import urllib.parse
from typing import Optional

import requests


def resolve_git_ref(
    ref: Optional[str],
    repo: Optional[str] = None,
    token: Optional[str] = None,
    provider: str = "github",
) -> Optional[str]:
    """
    Resolve a git ref (tag/branch/SHA) to a commit SHA.

    If the ref already looks like a SHA (7-40 hex characters), returns it as-is.
    Otherwise, calls the GitHub or GitLab API to resolve the ref to a SHA.

    Args:
        ref: Tag name, branch name, or commit SHA. If None or empty, returns None.
        repo: Repository in owner/repo format (GitHub) or namespace/repo (GitLab).
        token: Personal access token for API access.
        provider: Git provider - "github" or "gitlab" (default: github).

    Returns:
        Resolved commit SHA, or None if ref was empty.

    Raises:
        ValueError: If the ref cannot be resolved.

    Example::

        >>> resolve_git_ref("v1.0.0", "owner/repo", "ghp_xxx", "github")
        "abc123def456..."
        >>> resolve_git_ref("abc123def456", None, None)  # Already a SHA
        "abc123def456"
    """
    if not ref:
        return None  # Caller wants latest version

    # Already a SHA (7-40 hex characters) - return as-is
    if re.match(r"^[0-9a-fA-F]{7,40}$", ref):
        return ref

    # Need repo and token to resolve via API
    if not repo:
        raise ValueError(
            f"Cannot resolve git ref '{ref}': repository not specified. "
            "Pass the full SHA or provide repo/token."
        )
    if not token:
        raise ValueError(
            f"Cannot resolve git ref '{ref}': {provider} token not available. "
            "Pass the full SHA or provide a token."
        )

    if provider == "gitlab":
        # GitLab API: /projects/:id/repository/commits/:sha
        encoded_repo = urllib.parse.quote(repo, safe="")
        url = f"https://gitlab.com/api/v4/projects/{encoded_repo}/repository/commits/{ref}"
        headers = {"PRIVATE-TOKEN": token}
    else:
        # GitHub API
        url = f"https://api.github.com/repos/{repo}/commits/{ref}"
        headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code == 404:
        raise ValueError(f"Could not resolve git ref '{ref}' - not found in {repo}")
    resp.raise_for_status()

    sha = resp.json()["id" if provider == "gitlab" else "sha"]
    return sha
