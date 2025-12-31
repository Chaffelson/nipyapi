"""
Simple profile management for NiPyAPI development configurations.
"""

import logging
import os

from nipyapi import config as nipy_config
from nipyapi import security, utils

log = logging.getLogger(__name__)

# Default profile configuration - all possible keys with null defaults (supports sparse profiles)
DEFAULT_PROFILE_CONFIG = {
    "nifi_url": None,
    "registry_url": None,
    "registry_internal_url": None,
    "nifi_user": None,
    "nifi_pass": None,
    "nifi_bearer_token": None,
    "registry_user": None,
    "registry_pass": None,
    "ca_path": None,
    "client_cert": None,
    "client_key": None,
    "client_key_password": None,
    "nifi_ca_path": None,
    "registry_ca_path": None,
    "nifi_client_cert": None,
    "registry_client_cert": None,
    "nifi_client_key": None,
    "registry_client_key": None,
    "nifi_client_key_password": None,
    "registry_client_key_password": None,
    "nifi_proxy_identity": None,
    "nifi_verify_ssl": None,
    "registry_verify_ssl": None,
    "suppress_ssl_warnings": None,
    # Explicit authentication method control (None = auto-detection)
    "nifi_auth_method": None,
    "registry_auth_method": None,
    "oidc_token_endpoint": None,
    "oidc_client_id": None,
    "oidc_client_secret": None,
    # NiFi CLI properties file integration
    "nifi_cli_properties_file": None,
}

# Environment variable mappings - maps config keys to their env var names
ENV_VAR_MAPPINGS = [
    # URLs and credentials
    ("nifi_url", "NIFI_API_ENDPOINT"),
    ("registry_url", "REGISTRY_API_ENDPOINT"),
    ("nifi_user", "NIFI_USERNAME"),
    ("nifi_pass", "NIFI_PASSWORD"),
    ("nifi_bearer_token", "NIFI_BEARER_TOKEN"),
    ("registry_user", "REGISTRY_USERNAME"),
    ("registry_pass", "REGISTRY_PASSWORD"),
    # Basic certificate paths and security config
    ("ca_path", "TLS_CA_CERT_PATH"),
    ("client_cert", "MTLS_CLIENT_CERT"),
    ("client_key", "MTLS_CLIENT_KEY"),
    ("client_key_password", "MTLS_CLIENT_KEY_PASSWORD"),
    ("nifi_proxy_identity", "NIFI_PROXY_IDENTITY"),
    # SSL verification control
    ("nifi_verify_ssl", "NIFI_VERIFY_SSL"),
    ("registry_verify_ssl", "REGISTRY_VERIFY_SSL"),
    # SSL warning suppression
    ("suppress_ssl_warnings", "NIPYAPI_SUPPRESS_SSL_WARNINGS"),
    # Explicit authentication method control
    ("nifi_auth_method", "NIPYAPI_NIFI_AUTH_METHOD"),
    ("registry_auth_method", "NIPYAPI_REGISTRY_AUTH_METHOD"),
    # OIDC configuration
    ("oidc_token_endpoint", "OIDC_TOKEN_ENDPOINT"),
    ("oidc_client_id", "OIDC_CLIENT_ID"),
    ("oidc_client_secret", "OIDC_CLIENT_SECRET"),
    # Per-service certificate overrides (complex PKI environments)
    ("nifi_ca_path", "NIFI_CA_CERT_PATH"),
    ("registry_ca_path", "REGISTRY_CA_CERT_PATH"),
    ("nifi_client_cert", "NIFI_CLIENT_CERT"),
    ("registry_client_cert", "REGISTRY_CLIENT_CERT"),
    ("nifi_client_key", "NIFI_CLIENT_KEY"),
    ("registry_client_key", "REGISTRY_CLIENT_KEY"),
    ("nifi_client_key_password", "NIFI_CLIENT_KEY_PASSWORD"),
    ("registry_client_key_password", "REGISTRY_CLIENT_KEY_PASSWORD"),
    # NiFi CLI properties file integration
    ("nifi_cli_properties_file", "NIPYAPI_NIFI_CLI_PROPERTIES_FILE"),
]

# Certificate management configuration
CERTIFICATE_SERVICES = ["nifi", "registry"]
CERTIFICATE_TYPES = ["ca_path", "client_cert", "client_key", "client_key_password"]

# Keys containing sensitive values that should be masked in output
SENSITIVE_KEYS = frozenset(
    [
        "nifi_pass",
        "registry_pass",
        "nifi_bearer_token",
        "client_key_password",
        "nifi_client_key_password",
        "registry_client_key_password",
        "oidc_client_secret",
        "github_registry_token",
    ]
)

# Path resolution keys for SSL libraries (require absolute paths)
PATH_RESOLUTION_KEYS = [
    "ca_path",
    "client_cert",
    "client_key",
    "nifi_ca_path",
    "registry_ca_path",
    "nifi_client_cert",
    "registry_client_cert",
    "nifi_client_key",
    "registry_client_key",
    "resolved_nifi_ca_path",
    "resolved_registry_ca_path",
    "resolved_nifi_client_cert",
    "resolved_registry_client_cert",
    "resolved_nifi_client_key",
    "resolved_registry_client_key",
]

# Authentication method definitions - data-driven approach for extensibility
NIFI_AUTH_METHODS = {
    "bearer": {
        "detection_keys": ["nifi_bearer_token"],
        "required_keys": ["nifi_bearer_token"],
        "optional_keys": [],
    },
    "oidc": {
        "detection_keys": ["oidc_token_endpoint"],
        "required_keys": [
            "oidc_token_endpoint",
            "oidc_client_id",
            "oidc_client_secret",
        ],
        # Optional keys are required for OIDC authentication as Resource Owner
        "optional_keys": ["nifi_user", "nifi_pass"],
    },
    "mtls": {
        "detection_keys": ["client_cert", "client_key"],
        "required_keys": ["client_cert", "client_key"],
        "optional_keys": ["client_key_password"],
    },
    "basic": {
        "detection_keys": ["nifi_user", "nifi_pass"],
        "required_keys": ["nifi_user", "nifi_pass"],
        "optional_keys": [],
    },
}

REGISTRY_AUTH_METHODS = {
    "mtls": {
        "detection_keys": ["client_cert", "client_key"],
        "required_keys": ["client_cert", "client_key"],
        "optional_keys": ["client_key_password"],
    },
    "basic": {
        "detection_keys": ["registry_user", "registry_pass"],
        "required_keys": ["registry_user", "registry_pass"],
        "optional_keys": [],
    },
    "unauthenticated": {
        "detection_keys": [],  # No keys required for detection
        "required_keys": [],  # No parameters required
        "optional_keys": [],  # No optional parameters
    },
}

# NiFi CLI properties to NiPyAPI profile key mappings
NIFI_CLI_PROPERTY_MAPPINGS = {
    "baseUrl": "nifi_url",
    "oidcTokenUrl": "oidc_token_endpoint",
    "oidcClientId": "oidc_client_id",
    "oidcClientSecret": "oidc_client_secret",
    # Note: truststore/keystore handled via certificate extraction utility
    # "truststore": handled separately via extract_jks_certs.sh
    # "keystore": handled separately via extract_jks_certs.sh
}


def _load_nifi_cli_properties(properties_file_path):
    """
    Load NiFi CLI properties file and convert to NiPyAPI profile configuration.

    Args:
        properties_file_path (str): Path to NiFi CLI properties file

    Returns:
        dict: Profile configuration with mapped keys

    Raises:
        FileNotFoundError: If properties file doesn't exist
        ValueError: If properties file is malformed
    """
    if not properties_file_path:
        return {}

    resolved_path = utils.resolve_relative_paths(properties_file_path)
    if not resolved_path:
        return {}

    try:
        properties = {}
        with open(resolved_path, "r", encoding="utf-8") as f:
            for _, line in enumerate(f, 1):
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#") or line.startswith("!"):
                    continue
                # Parse key=value pairs
                if "=" in line:
                    key, value = line.split("=", 1)
                    properties[key.strip()] = value.strip()

        # Map properties to NiPyAPI profile keys
        profile_config = {}
        for cli_key, profile_key in NIFI_CLI_PROPERTY_MAPPINGS.items():
            if cli_key in properties and properties[cli_key]:
                value = properties[cli_key]
                # Special handling for baseUrl: append /nifi-api if not present
                if cli_key == "baseUrl" and not value.endswith("/nifi-api"):
                    value = value.rstrip("/") + "/nifi-api"
                profile_config[profile_key] = value

        log.debug("Loaded %d properties from CLI file: %s", len(profile_config), resolved_path)
        return profile_config

    except FileNotFoundError:
        log.warning("NiFi CLI properties file not found: %s", resolved_path)
        return {}
    except (UnicodeDecodeError, PermissionError, OSError) as e:
        log.error("Error parsing NiFi CLI properties file %s: %s", resolved_path, e)
        return {}


def _detect_and_validate_auth(config, auth_methods, service_name):
    """
    Generic authentication detection and validation.

    First checks for explicit authentication method specification, then falls back
    to auto-detection based on available configuration parameters.

    Args:
        config (dict): Configuration dictionary
        auth_methods (dict): Dict of method definitions (e.g., NIFI_AUTH_METHODS)
        service_name (str): Service name for error messages ('nifi' or 'registry')

    Returns:
        tuple: (auth_method, validated_params)

    Raises:
        ValueError: If no valid authentication method is detected or required parameters
                   are missing
    """
    # Check for explicit authentication method specification first
    explicit_auth_key = f"{service_name.lower()}_auth_method"
    explicit_method = config.get(explicit_auth_key)

    if explicit_method:
        # Validate explicit method is supported
        if explicit_method not in auth_methods:
            available_method_names = list(auth_methods.keys())
            raise ValueError(
                f"Invalid {service_name} authentication method '{explicit_method}'. "
                f"Available methods: {available_method_names}"
            )

        # Validate required parameters for explicit method
        method_def = auth_methods[explicit_method]
        missing = [k for k in method_def["required_keys"] if not config.get(k)]
        if missing:
            raise ValueError(f"{service_name} {explicit_method} authentication requires: {missing}")

        # Collect validated parameters (required + any present optional)
        params = {k: config[k] for k in method_def["required_keys"]}
        for k in method_def["optional_keys"]:
            if config.get(k):
                params[k] = config[k]

        return explicit_method, params

    # Fall back to auto-detection: try each method in priority order
    for method_name, method_def in auth_methods.items():
        # Check if all detection keys are present and non-empty
        if all(config.get(key) for key in method_def["detection_keys"]):
            # Validate all required keys are present
            missing = [k for k in method_def["required_keys"] if not config.get(k)]
            if missing:
                raise ValueError(f"{service_name} {method_name} authentication requires: {missing}")

            # Collect validated parameters (required + any present optional)
            params = {k: config[k] for k in method_def["required_keys"]}
            for k in method_def["optional_keys"]:
                if config.get(k):
                    params[k] = config[k]

            return method_name, params

    # No method detected
    available_keys = [
        k for method in auth_methods.values() for k in method["detection_keys"] if config.get(k)
    ]
    raise ValueError(
        f"No valid {service_name} authentication method detected. "
        f"Available params: {available_keys}"
    )


def load_profiles_from_file(file_path=None):
    """
    Load profile configurations from a YAML or JSON file.

    Supports both YAML and JSON formats since JSON is a subset of YAML syntax.

    Args:
        file_path (str, optional): Path to YAML or JSON file containing profile definitions.
                                  If None, resolves using:
                                  1. NIPYAPI_PROFILES_FILE environment variable
                                  2. ~/.nipyapi/profiles.yml (user-level config)
                                  3. nipyapi.config.default_profiles_file (development fallback)

    Returns:
        dict: Profile configurations
    """
    if file_path is None:
        # Check environment variable first
        file_path = utils.getenv("NIPYAPI_PROFILES_FILE")

        # Then check user-level config location
        if not file_path:
            user_path = os.path.expanduser(nipy_config.user_profiles_file)
            if os.path.exists(user_path):
                file_path = user_path
                log.debug("Using user profiles file: %s", user_path)

        # Finally fall back to development default
        if not file_path:
            file_path = nipy_config.default_profiles_file

    file_content = utils.fs_read(file_path)
    return utils.load(file_content)


def get_default_profile_name():
    """
    Get the first profile name from the profiles file.

    Resolution order:
        1. NIPYAPI_PROFILES_FILE environment variable
        2. ~/.nipyapi/profiles.yml (user-level config)

    Returns:
        str: Profile name, or None if no profiles file exists
    """
    # Check environment variable first (supports testing and CI overrides)
    env_profiles_file = utils.getenv("NIPYAPI_PROFILES_FILE")
    if env_profiles_file:
        resolved_path = utils.resolve_relative_paths(env_profiles_file)
        if resolved_path and os.path.exists(resolved_path):
            try:
                profiles = load_profiles_from_file(resolved_path)
                if profiles:
                    first_profile = next(iter(profiles.keys()))
                    log.debug(
                        "Auto-detected profile '%s' from env: %s", first_profile, resolved_path
                    )
                    return first_profile
            except Exception as e:  # pylint: disable=broad-exception-caught
                log.debug("Could not read profiles from env path: %s", e)

    # Fall back to user profiles file
    user_path = os.path.expanduser(nipy_config.user_profiles_file)
    if not os.path.exists(user_path):
        return None

    try:
        profiles = load_profiles_from_file(user_path)
        if profiles:
            first_profile = next(iter(profiles.keys()))
            log.debug("Auto-detected profile: %s", first_profile)
            return first_profile
    except Exception as e:  # pylint: disable=broad-exception-caught
        log.debug("Could not read user profiles: %s", e)

    return None


def resolve_profile_config(profile_name, profiles_file_path=None):
    # pylint: disable=too-many-branches
    """
    Complete profile configuration resolution with environment overrides and absolute paths.

    Supports both simple shared certificates and complex per-service PKI configurations.
    Accepts both YAML and JSON profile files.

    Special "env" profile: When profile_name is "env", configuration is loaded entirely
    from environment variables without requiring a profiles file. This is useful for
    CI/CD pipelines and containerized deployments where all configuration comes from
    the environment.

    Args:
        profile_name (str): Name of profile to resolve. Use "env" for pure environment
                           variable configuration without a profiles file.
        profiles_file_path (str, optional): Path to profiles YAML or JSON file.
                                          Default resolution handled by
                                          load_profiles_from_file(). Ignored when
                                          profile_name is "env".

    Returns:
        dict: Fully resolved configuration with all paths and overrides applied
    """
    # Special "env" profile - explicit environment variable mode for CI/CD
    # This is strict: requires NIFI_API_ENDPOINT to be set. For auto-resolution
    # (env vars -> profile file fallback), use switch(None) instead.
    if profile_name == "env":
        if not utils.getenv("NIFI_API_ENDPOINT"):
            raise ValueError(
                "Profile 'env' requires NIFI_API_ENDPOINT environment variable. "
                "For auto-resolution (env vars or profile file), call "
                "nipyapi.profiles.switch() with no arguments."
            )
        config = DEFAULT_PROFILE_CONFIG.copy()
        log.debug("Using 'env' profile - configuration from environment variables")
    else:
        # Load profiles from file (handles default resolution)
        all_profiles = load_profiles_from_file(profiles_file_path)

        if profile_name not in all_profiles:
            raise ValueError(
                f"Profile '{profile_name}' not found. Available: {list(all_profiles.keys())}"
            )

        # Start with defaults, then apply profile values
        config = DEFAULT_PROFILE_CONFIG.copy()
        config.update(all_profiles[profile_name])

    # Load and merge NiFi CLI properties file if specified
    # (Environment variable can override which file to use)
    properties_file = utils.getenv("NIPYAPI_NIFI_CLI_PROPERTIES_FILE") or config.get(
        "nifi_cli_properties_file"
    )
    if properties_file:
        properties_config = _load_nifi_cli_properties(properties_file)
        config.update(properties_config)
        log.debug("Merged NiFi CLI properties from: %s", properties_file)

    # Apply environment variable overrides
    for config_key, env_var in ENV_VAR_MAPPINGS:
        # Use boolean parsing for SSL and warning flags
        if config_key in (
            "nifi_verify_ssl",
            "registry_verify_ssl",
            "suppress_ssl_warnings",
        ):
            env_value = utils.getenv_bool(env_var)
            if env_value is not None:
                config[config_key] = env_value
        else:
            config[config_key] = utils.getenv(env_var) or config[config_key]

    # Apply smart defaults for SSL settings based on URL protocol
    if config.get("nifi_url") and config.get("nifi_verify_ssl") is None:
        config["nifi_verify_ssl"] = config["nifi_url"].startswith("https://")

    if config.get("registry_url") and config.get("registry_verify_ssl") is None:
        config["registry_verify_ssl"] = config["registry_url"].startswith("https://")

    # Normalize URLs by removing trailing slashes (standard REST API practice)
    for url_field in ["nifi_url", "registry_url", "registry_internal_url", "oidc_token_endpoint"]:
        if config.get(url_field):
            config[url_field] = config[url_field].rstrip("/")

    # Resolve final certificate paths: per-service takes precedence over shared
    # Generate resolved_{service}_{cert_type} = {service}_{cert_type} or {cert_type}
    for service in CERTIFICATE_SERVICES:
        for cert_type in CERTIFICATE_TYPES:
            config[f"resolved_{service}_{cert_type}"] = (
                config[f"{service}_{cert_type}"] or config[cert_type]
            )

    # Convert relative paths to absolute using utility function
    # SSL libraries generally require absolute paths for certificate files
    # Check for environment variable override of root path
    cert_root = utils.getenv("NIPYAPI_CERTS_ROOT_PATH")
    for path_key in PATH_RESOLUTION_KEYS:
        config[path_key] = utils.resolve_relative_paths(config[path_key], cert_root)

    # Add profile name for reference
    config["profile"] = profile_name

    return config


def switch(profile_name=None, profiles_file=None, login=True):
    # pylint: disable=too-many-branches,too-many-statements
    """
    Switch to a different profile at runtime using configuration-driven authentication.

    Automatically detects authentication methods based on available configuration
    parameters rather than profile names, making it flexible for custom profiles.

    Supports OIDC (requires oidc_token_endpoint, oidc_client_id, oidc_client_secret),
    mTLS (requires client_cert, client_key), and Basic auth (requires nifi_user/nifi_pass).

    Args:
        profile_name (str, optional): Profile to switch to. None auto-resolves from
            env vars or profiles file. "env" uses explicit environment variables.
            Any other string uses that named profile from the profiles file.
        profiles_file (str, optional): Path to profiles file. Defaults to
            NIPYAPI_PROFILES_FILE env var or nipyapi.config.default_profiles_file.
        login (bool, optional): Whether to attempt authentication. Defaults to True.
            If False, configures SSL/endpoints but skips login attempts.

    Returns:
        tuple of (profile_name, metadata). Metadata varies by auth method: OIDC
        returns token_data dict, Basic returns username string, mTLS and
        login=False return None.

    Raises:
        ValueError: If profile not found or required authentication parameters are missing

    Example::

        >>> import nipyapi.profiles
        >>> nipyapi.profiles.switch()  # Auto-resolve: env vars or user profile
        >>> nipyapi.profiles.switch('single-user')  # Uses basic auth
        >>> nipyapi.profiles.switch('secure-mtls')  # Uses mTLS auth
        >>> nipyapi.profiles.switch('secure-oidc')  # Uses OIDC auth
        >>> nipyapi.profiles.switch('my-custom')    # Uses whatever auth method is configured
        >>>
        >>> # Explicit environment variable mode for CI/CD (strict - fails if not set)
        >>> nipyapi.profiles.switch('env')
        >>>
        >>> # Custom profiles file
        >>> nipyapi.profiles.switch('production',
        ...                          profiles_file='/home/user/.nipyapi/profiles.yml')

    """

    # 1. Auto-resolve profile when None (similar to AWS CLI behavior)
    if profile_name is None:
        if utils.getenv("NIFI_API_ENDPOINT"):
            log.debug("Auto-resolve: using environment variables (NIFI_API_ENDPOINT is set)")
            profile_name = "env"
        elif utils.getenv("NIPYAPI_PROFILE"):
            # Explicit profile selection via environment variable
            profile_name = utils.getenv("NIPYAPI_PROFILE")
            log.debug("Auto-resolve: using profile '%s' from NIPYAPI_PROFILE env var", profile_name)
        else:
            default_profile = get_default_profile_name()
            if default_profile:
                log.debug("Auto-resolve: using profile '%s' from user config", default_profile)
                profile_name = default_profile
            else:
                raise ValueError(
                    "No configuration found. Either:\n"
                    "  1. Set NIFI_API_ENDPOINT environment variable, or\n"
                    "  2. Create ~/.nipyapi/profiles.yml with your connection settings"
                )

    # 2. Resolve target profile configuration
    # Default file resolution is handled by load_profiles_from_file()
    config = resolve_profile_config(profile_name, profiles_file)

    log.info("Switching to profile: %s", profile_name)

    # Initialize metadata tracking for different auth methods
    auth_metadata = None

    # 2. Determine what services to connect to
    connect_to_nifi = bool(config.get("nifi_url"))
    connect_to_registry = bool(config.get("registry_url"))

    log.debug("Service connections: NiFi=%s Registry=%s", connect_to_nifi, connect_to_registry)

    if not connect_to_nifi and not connect_to_registry:
        raise ValueError(
            f"Profile '{profile_name}' has no nifi_url or registry_url - nothing to connect to"
        )

    # 3. Clean teardown of existing connections (best effort)
    # Always reset both services to ensure deterministic state on profile switch.
    # This prevents stale configuration from previous profiles affecting the new one.
    security.reset_service_connections()

    # Clear hosts for services not in this profile to prevent code from
    # assuming they're available based on leftover default values
    if not connect_to_registry:
        nipy_config.registry_config.host = None
    if not connect_to_nifi:
        nipy_config.nifi_config.host = None

    # 4. Apply SSL configuration
    # Apply CA certificate first if provided
    if config.get("ca_path"):
        security.set_shared_ca_cert(config["ca_path"])

    # Set SSL verification from resolved config
    if connect_to_nifi:
        nipy_config.nifi_config.verify_ssl = config["nifi_verify_ssl"]

    if connect_to_registry:
        nipy_config.registry_config.verify_ssl = config["registry_verify_ssl"]

    # Apply SSL warning suppression from profile config
    if config.get("suppress_ssl_warnings") is not None:
        security.set_ssl_warning_suppression(config["suppress_ssl_warnings"])

    # 5. Configuration-driven NiFi setup
    if connect_to_nifi:
        log.debug("Detecting NiFi authentication method...")
        log.debug(
            "Available auths: nifi_user=%s, nifi_pass=%s, client_cert=%s, oidc_token=%s",
            bool(config.get("nifi_user")),
            bool(config.get("nifi_pass")),
            bool(config.get("client_cert")),
            bool(config.get("oidc_token_endpoint")),
        )

        nifi_auth_method, nifi_auth_params = _detect_and_validate_auth(
            config, NIFI_AUTH_METHODS, "NiFi"
        )

        log.info("Using NiFi authentication method: %s", nifi_auth_method)
        log.debug("Auth params: %s", list(nifi_auth_params.keys()))

        # Set NiFi endpoint URL once (regardless of authentication method)
        nipy_config.nifi_config.host = config["nifi_url"].rstrip("/")

        if nifi_auth_method == "oidc":
            log.debug("Configuring OIDC authentication for NiFi...")
            # OIDC requires special setup

            if login:
                # Always capture token data for OIDC (needed for UUID extraction)
                auth_metadata = security.service_login_oidc(
                    service="nifi",
                    username=nifi_auth_params.get("nifi_user"),  # Optional for client credentials
                    password=nifi_auth_params.get("nifi_pass"),  # Optional for client credentials
                    oidc_token_endpoint=nifi_auth_params["oidc_token_endpoint"],
                    client_id=nifi_auth_params["oidc_client_id"],
                    client_secret=nifi_auth_params["oidc_client_secret"],
                    return_token_info=True,
                    verify_ssl=config.get("nifi_verify_ssl"),  # Use profile's SSL setting
                )
                log.debug("OIDC authentication completed")
            else:
                log.debug("OIDC configuration completed (no login attempted)")
        elif nifi_auth_method == "bearer":
            log.debug("Configuring bearer token authentication for NiFi...")
            if login:
                security.set_service_auth_token(
                    token=nifi_auth_params["nifi_bearer_token"],
                    service="nifi",
                )
                log.debug("Bearer token authentication completed")
            else:
                log.debug("Bearer token configuration completed (no login attempted)")
        elif nifi_auth_method == "mtls":
            log.debug("Configuring mTLS authentication for NiFi...")
            # Apply client certificates for mTLS
            nipy_config.nifi_config.cert_file = nifi_auth_params["client_cert"]
            nipy_config.nifi_config.key_file = nifi_auth_params["client_key"]
            log.debug("mTLS authentication completed")
        elif nifi_auth_method == "basic":
            log.debug(
                "Configuring basic authentication for NiFi with user: %s",
                nifi_auth_params["nifi_user"],
            )

            if login:
                # Perform basic authentication directly
                security.service_login(
                    service="nifi",
                    username=nifi_auth_params["nifi_user"],
                    password=nifi_auth_params["nifi_pass"],
                )
                # For basic auth, return the logged-in username as metadata
                auth_metadata = nifi_auth_params["nifi_user"]
                log.debug("Basic authentication completed")
            else:
                log.debug("Basic auth configuration completed (no login attempted)")
        else:
            log.debug("No authentication method detected for NiFi")

    # 6. Configuration-driven Registry setup
    if connect_to_registry:
        log.debug("Detecting Registry authentication method...")

        registry_auth_method, registry_auth_params = _detect_and_validate_auth(
            config, REGISTRY_AUTH_METHODS, "Registry"
        )

        log.info("Using Registry authentication method: %s", registry_auth_method)
        log.debug("Auth params: %s", list(registry_auth_params.keys()))

        # Set Registry endpoint URL once (regardless of authentication method)
        nipy_config.registry_config.host = config["registry_url"].rstrip("/")

        if registry_auth_method == "mtls":
            log.debug("Configuring mTLS authentication for Registry...")
            # Apply client certificates for mTLS
            nipy_config.registry_config.cert_file = registry_auth_params["client_cert"]
            nipy_config.registry_config.key_file = registry_auth_params["client_key"]
            log.debug("Registry mTLS authentication completed")
        elif registry_auth_method == "basic":
            log.debug(
                "Configuring basic authentication for Registry with user: %s",
                registry_auth_params["registry_user"],
            )

            if login:
                # Registry HTTP doesn't require authentication, only HTTPS does
                if config["registry_url"].startswith("https://"):
                    # Perform basic authentication for HTTPS Registry
                    security.service_login(
                        service="registry",
                        username=registry_auth_params["registry_user"],
                        password=registry_auth_params["registry_pass"],
                    )
                    log.debug("Registry HTTPS basic authentication completed")
                else:
                    log.debug("Registry HTTP - no authentication required")
            else:
                log.debug("Registry basic auth configuration completed (no login attempted)")
        elif registry_auth_method == "unauthenticated":
            log.debug("Registry configured for unauthenticated HTTP access")
            # No authentication configuration or login needed
        else:
            log.debug("No authentication method detected for Registry")

    # Note: Bootstrap security policies are NOT handled here as they change server state.
    # Bootstrap should remain in conftest.py, sandbox.py, and other setup scripts.
    # This function only handles CLIENT-side connection configuration.

    # 7. Apply GitHub Flow Registry Client configuration if present
    # These are used for CI/CD workflows with GitHub as a flow registry
    if config.get("github_registry_token"):
        nipy_config.github_registry_token = config["github_registry_token"]
    if config.get("github_registry_repo"):
        nipy_config.github_registry_repo = config["github_registry_repo"]
    if config.get("github_registry_branch"):
        nipy_config.github_registry_branch = config["github_registry_branch"]

    log.debug("Profile switch completed successfully: %s", profile_name)

    # Always return tuple (profile_name, metadata)
    return profile_name, auth_metadata


def list_profiles(profiles_file=None):
    """
    List available profile names from the profiles file.

    Args:
        profiles_file (str, optional): Path to profiles file. Uses default resolution if None.

    Returns:
        list: Profile names available in the profiles file.
    """
    profiles = load_profiles_from_file(profiles_file)
    return list(profiles.keys())


def show(profile_name, profiles_file=None, mask_secrets=True):
    """
    Show a profile's resolved configuration.

    Args:
        profile_name (str): Name of the profile to show.
        profiles_file (str, optional): Path to profiles file. Uses default resolution if None.
        mask_secrets (bool): If True, mask sensitive values. Defaults to True.

    Returns:
        dict: Profile configuration with secrets optionally masked.
    """
    config = resolve_profile_config(profile_name, profiles_file)

    if mask_secrets:
        config = {k: "********" if k in SENSITIVE_KEYS and v else v for k, v in config.items()}

    # Filter out None values for cleaner output
    return {k: v for k, v in config.items() if v is not None}


def current():
    """
    Show the currently configured endpoints.

    Returns:
        dict: Current endpoint configuration.
    """
    return {
        "nifi_url": nipy_config.nifi_config.host if nipy_config.nifi_config else None,
        "registry_url": nipy_config.registry_config.host if nipy_config.registry_config else None,
    }
