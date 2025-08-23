"""
Simple profile management for NiPyAPI development configurations.
"""

import logging
from nipyapi import utils, security, config as nipy_config

log = logging.getLogger(__name__)

# Default profile configuration - all possible keys with null defaults (supports sparse profiles)
DEFAULT_PROFILE_CONFIG = {
    'nifi_url': None,
    'registry_url': None,
    'registry_internal_url': None,
    'nifi_user': None,
    'nifi_pass': None,
    'registry_user': None,
    'registry_pass': None,
    'ca_path': None,
    'client_cert': None,
    'client_key': None,
    'client_key_password': None,
    'nifi_ca_path': None,
    'registry_ca_path': None,
    'nifi_client_cert': None,
    'registry_client_cert': None,
    'nifi_client_key': None,
    'registry_client_key': None,
    'nifi_client_key_password': None,
    'registry_client_key_password': None,
    'nifi_proxy_identity': None,
    'nifi_verify_ssl': None,
    'registry_verify_ssl': None,
    'oidc_token_endpoint': None,
    'oidc_client_id': None,
    'oidc_client_secret': None,
}

# Environment variable mappings - maps config keys to their env var names
ENV_VAR_MAPPINGS = [
    # URLs and credentials
    ('nifi_url', 'NIFI_API_ENDPOINT'),
    ('registry_url', 'REGISTRY_API_ENDPOINT'),
    ('nifi_user', 'NIFI_USERNAME'),
    ('nifi_pass', 'NIFI_PASSWORD'),
    ('registry_user', 'REGISTRY_USERNAME'),
    ('registry_pass', 'REGISTRY_PASSWORD'),

    # Basic certificate paths and security config
    ('ca_path', 'TLS_CA_CERT_PATH'),
    ('client_cert', 'MTLS_CLIENT_CERT'),
    ('client_key', 'MTLS_CLIENT_KEY'),
    ('client_key_password', 'MTLS_CLIENT_KEY_PASSWORD'),
    ('nifi_proxy_identity', 'NIFI_PROXY_IDENTITY'),

    # SSL verification control
    ('nifi_verify_ssl', 'NIFI_VERIFY_SSL'),
    ('registry_verify_ssl', 'REGISTRY_VERIFY_SSL'),

    # OIDC configuration
    ('oidc_token_endpoint', 'OIDC_TOKEN_ENDPOINT'),
    ('oidc_client_id', 'OIDC_CLIENT_ID'),
    ('oidc_client_secret', 'OIDC_CLIENT_SECRET'),

    # Per-service certificate overrides (complex PKI environments)
    ('nifi_ca_path', 'NIFI_CA_CERT_PATH'),
    ('registry_ca_path', 'REGISTRY_CA_CERT_PATH'),
    ('nifi_client_cert', 'NIFI_CLIENT_CERT'),
    ('registry_client_cert', 'REGISTRY_CLIENT_CERT'),
    ('nifi_client_key', 'NIFI_CLIENT_KEY'),
    ('registry_client_key', 'REGISTRY_CLIENT_KEY'),
    ('nifi_client_key_password', 'NIFI_CLIENT_KEY_PASSWORD'),
    ('registry_client_key_password', 'REGISTRY_CLIENT_KEY_PASSWORD'),
]

# Certificate management configuration
CERTIFICATE_SERVICES = ['nifi', 'registry']
CERTIFICATE_TYPES = ['ca_path', 'client_cert', 'client_key', 'client_key_password']

# Path resolution keys for SSL libraries (require absolute paths)
PATH_RESOLUTION_KEYS = [
    'ca_path', 'client_cert', 'client_key',
    'nifi_ca_path', 'registry_ca_path',
    'nifi_client_cert', 'registry_client_cert',
    'nifi_client_key', 'registry_client_key',
    'resolved_nifi_ca_path', 'resolved_registry_ca_path',
    'resolved_nifi_client_cert', 'resolved_registry_client_cert',
    'resolved_nifi_client_key', 'resolved_registry_client_key'
]

# Authentication method definitions - data-driven approach for extensibility
NIFI_AUTH_METHODS = {
    'oidc': {
        'detection_keys': ['oidc_token_endpoint'],
        'required_keys': [
            'oidc_token_endpoint', 'oidc_client_id', 'oidc_client_secret',
            'nifi_user', 'nifi_pass'
            ],
        'optional_keys': []
    },
    'mtls': {
        'detection_keys': ['client_cert', 'client_key'],
        'required_keys': ['client_cert', 'client_key'],
        'optional_keys': ['client_key_password']
    },
    'basic': {
        'detection_keys': ['nifi_user', 'nifi_pass'],
        'required_keys': ['nifi_user', 'nifi_pass'],
        'optional_keys': []
    }
}

REGISTRY_AUTH_METHODS = {
    'mtls': {
        'detection_keys': ['client_cert', 'client_key'],
        'required_keys': ['client_cert', 'client_key'],
        'optional_keys': ['client_key_password']
    },
    'basic': {
        'detection_keys': ['registry_user', 'registry_pass'],
        'required_keys': ['registry_user', 'registry_pass'],
        'optional_keys': []
    }
}


def _detect_and_validate_auth(config, auth_methods, service_name):
    """
    Generic authentication detection and validation.

    Detects the appropriate authentication method based on available configuration
    and validates that all required parameters are present.

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
    # Try each method in priority order (OIDC first, then mTLS, then password)
    for method_name, method_def in auth_methods.items():
        # Check if all detection keys are present and non-empty
        if all(config.get(key) for key in method_def['detection_keys']):
            # Validate all required keys are present
            missing = [k for k in method_def['required_keys'] if not config.get(k)]
            if missing:
                raise ValueError(
                    f"{service_name} {method_name} authentication requires: {missing}"
                )

            # Collect validated parameters (required + any present optional)
            params = {k: config[k] for k in method_def['required_keys']}
            for k in method_def['optional_keys']:
                if config.get(k):
                    params[k] = config[k]

            return method_name, params

    # No method detected
    available_keys = [k for method in auth_methods.values()
                      for k in method['detection_keys'] if config.get(k)]
    raise ValueError(f"No valid {service_name} authentication method detected. "
                     f"Available params: {available_keys}")


def load_profiles_from_file(file_path=None):
    """
    Load profile configurations from a YAML or JSON file.

    Supports both YAML and JSON formats since JSON is a subset of YAML syntax.

    Args:
        file_path (str, optional): Path to YAML or JSON file containing profile definitions.
                                  If None, resolves using:
                                  1. NIPYAPI_PROFILES_FILE environment variable
                                  2. nipyapi.config.default_profiles_file

    Returns:
        dict: Profile configurations
    """
    if file_path is None:
        file_path = (
            utils.getenv('NIPYAPI_PROFILES_FILE') or
            nipy_config.default_profiles_file
        )

    file_content = utils.fs_read(file_path)
    return utils.load(file_content)


def resolve_profile_config(profile_name, profiles_file_path=None):
    """
    Complete profile configuration resolution with environment overrides and absolute paths.

    Supports both simple shared certificates and complex per-service PKI configurations.
    Accepts both YAML and JSON profile files.

    Args:
        profile_name (str): Name of profile to resolve
        profiles_file_path (str, optional): Path to profiles YAML or JSON file.
                                          Default resolution handled by
                                          load_profiles_from_file()

    Returns:
        dict: Fully resolved configuration with all paths and overrides applied
    """
    # Load profiles from file (handles default resolution)
    all_profiles = load_profiles_from_file(profiles_file_path)

    if profile_name not in all_profiles:
        raise ValueError(
            f"Profile '{profile_name}' not found. Available: {list(all_profiles.keys())}"
        )

    # Start with defaults, then apply profile values
    config = DEFAULT_PROFILE_CONFIG.copy()
    config.update(all_profiles[profile_name])

    # Apply all environment variable overrides
    for config_key, env_var in ENV_VAR_MAPPINGS:
        # Use boolean parsing for SSL verification flags
        if config_key in ('nifi_verify_ssl', 'registry_verify_ssl'):
            env_value = utils.getenv_bool(env_var)
            if env_value is not None:
                config[config_key] = env_value
        else:
            config[config_key] = utils.getenv(env_var) or config[config_key]

    # Normalize URLs by removing trailing slashes (standard REST API practice)
    for url_field in ['nifi_url', 'registry_url', 'registry_internal_url', 'oidc_token_endpoint']:
        if config.get(url_field):
            config[url_field] = config[url_field].rstrip('/')

    # Resolve final certificate paths: per-service takes precedence over shared
    # Generate resolved_{service}_{cert_type} = {service}_{cert_type} or {cert_type}
    for service in CERTIFICATE_SERVICES:
        for cert_type in CERTIFICATE_TYPES:
            config[f'resolved_{service}_{cert_type}'] = (
                config[f'{service}_{cert_type}'] or config[cert_type]
            )

    # Convert relative paths to absolute using utility function
    # SSL libraries generally require absolute paths for certificate files
    # Check for environment variable override of root path
    cert_root = utils.getenv('NIPYAPI_CERTS_ROOT_PATH')
    for path_key in PATH_RESOLUTION_KEYS:
        config[path_key] = utils.resolve_relative_paths(config[path_key], cert_root)

    # Add profile name for reference
    config['profile'] = profile_name

    return config


def switch(profile_name, profiles_file=None, login=True):
    # pylint: disable=too-many-branches,too-many-statements
    """
    Switch to a different profile at runtime using configuration-driven authentication.

    Automatically detects authentication methods based on available configuration
    parameters rather than profile names, making it flexible for custom profiles.

        Supported authentication methods:

    - OIDC: Requires oidc_token_endpoint, oidc_client_id, oidc_client_secret,
            nifi_user, nifi_pass
    - mTLS: Requires client_cert, client_key (+ optional client_key_password)
    - Basic: Requires nifi_user/nifi_pass for NiFi, registry_user/registry_pass for Registry

    Args:
        profile_name (str): Name of the profile to switch to
        profiles_file (str, optional): Path to profiles file. Resolution order:
                                      1. Explicit profiles_file parameter
                                      2. NIPYAPI_PROFILES_FILE environment variable
                                      3. nipyapi.config.default_profiles_file
        login (bool, optional): Whether to attempt authentication. Defaults to True.
                               If False, configures SSL/endpoints but skips login attempts.
                               Useful for readiness checks where you don't want to
                               send credentials.

    Returns:
        tuple: (profile_name, metadata) where metadata varies by authentication method:
              - OIDC: token_data dict containing JWT token info for UUID extraction (login=True)
              - Basic: username string of the logged-in user (login=True)
              - mTLS: None (no metadata extracted)
              - Any method with login=False: None

    Raises:
        ValueError: If profile not found or required authentication parameters are missing

    Example:
        >>> import nipyapi.profiles
        >>> nipyapi.profiles.switch('single-user')  # Uses basic auth (nifi_user/nifi_pass)
        >>> nipyapi.profiles.switch('secure-mtls')  # Uses mTLS auth (client_cert/client_key)
        >>> nipyapi.profiles.switch('secure-oidc')  # Uses OIDC auth (oidc_* params)
        >>> nipyapi.profiles.switch('my-custom')    # Uses whatever auth method is configured
        >>>
        >>> # Custom profiles file
        >>> nipyapi.profiles.switch('production',
        ...                          profiles_file='/home/user/.nipyapi/profiles.yml')

    """

    # 1. Resolve target profile configuration
    # Default file resolution is handled by load_profiles_from_file()
    config = resolve_profile_config(profile_name, profiles_file)

    log.info("Switching to profile: %s", profile_name)

    # Initialize metadata tracking for different auth methods
    auth_metadata = None

    # 2. Determine what services to connect to
    connect_to_nifi = bool(config.get('nifi_url'))
    connect_to_registry = bool(config.get('registry_url'))

    log.debug("Service connections: NiFi=%s Registry=%s", connect_to_nifi, connect_to_registry)

    if not connect_to_nifi and not connect_to_registry:
        raise ValueError(
            f"Profile '{profile_name}' has no nifi_url or registry_url - nothing to connect to")

    # 3. Clean teardown of existing connections (best effort)
    if connect_to_nifi:
        log.debug("Attempting NiFi logout...")
        try:
            security.service_logout('nifi')
            log.debug("NiFi logout successful")
        except Exception as e:  # pylint: disable=broad-exception-caught
            log.debug("NiFi logout failed (expected if not logged in): %s", e)

    if connect_to_registry:
        log.debug("Attempting Registry logout...")
        try:
            security.service_logout('registry')
            log.debug("Registry logout successful")
        except Exception as e:  # pylint: disable=broad-exception-caught
            log.debug("Registry logout failed (expected if not logged in): %s", e)

    # Force fresh API clients after logout to ensure clean state
    if connect_to_nifi:
        nipy_config.nifi_config.api_client = None
        log.debug("Reset NiFi API client")
    if connect_to_registry:
        nipy_config.registry_config.api_client = None
        log.debug("Reset Registry API client")

    # 4. Apply SSL configuration (exactly matching conftest.py pattern)
    # Apply CA certificate first if provided
    if config.get('ca_path'):
        security.set_shared_ca_cert(config['ca_path'])

    # Set SSL verification - user override or smart default based on protocol
    if connect_to_nifi:
        if config.get('nifi_verify_ssl') is not None:
            # User explicitly set verification preference
            nipy_config.nifi_config.verify_ssl = config['nifi_verify_ssl']
        else:
            # Smart default: True for HTTPS, False for HTTP
            nipy_config.nifi_config.verify_ssl = config['nifi_url'].startswith('https://')

    if connect_to_registry:
        if config.get('registry_verify_ssl') is not None:
            # User explicitly set verification preference
            nipy_config.registry_config.verify_ssl = config['registry_verify_ssl']
        else:
            # Smart default: True for HTTPS, False for HTTP
            nipy_config.registry_config.verify_ssl = (
                config['registry_url'].startswith('https://'))

    # Apply all SSL configuration changes once
    security.apply_ssl_configuration()

    # 5. Configuration-driven NiFi setup
    if connect_to_nifi:
        log.debug("Detecting NiFi authentication method...")
        log.debug("Available auths: nifi_user=%s, nifi_pass=%s, client_cert=%s, oidc_token=%s",
                  bool(config.get('nifi_user')), bool(config.get('nifi_pass')),
                  bool(config.get('client_cert')), bool(config.get('oidc_token_endpoint')))

        nifi_auth_method, nifi_auth_params = _detect_and_validate_auth(
            config, NIFI_AUTH_METHODS, 'NiFi')

        log.info("Using NiFi authentication method: %s", nifi_auth_method)
        log.debug("Auth params: %s", list(nifi_auth_params.keys()))

        if nifi_auth_method == 'oidc':
            log.debug("Configuring OIDC authentication for NiFi...")
            # OIDC requires special setup
            nipy_config.nifi_config.host = config['nifi_url']

            if login:
                # Always capture token data for OIDC (needed for UUID extraction)
                auth_metadata = security.service_login_oidc(
                    service='nifi',
                    username=nifi_auth_params['nifi_user'],
                    password=nifi_auth_params['nifi_pass'],
                    oidc_token_endpoint=nifi_auth_params['oidc_token_endpoint'],
                    client_id=nifi_auth_params['oidc_client_id'],
                    client_secret=nifi_auth_params['oidc_client_secret'],
                    return_token_info=True
                )
                log.debug("OIDC authentication completed")
            else:
                log.debug("OIDC configuration completed (no login attempted)")
        elif nifi_auth_method == 'mtls':
            log.debug("Configuring mTLS authentication for NiFi...")
            # Apply client certificates for mTLS
            nipy_config.nifi_config.cert_file = nifi_auth_params['client_cert']
            nipy_config.nifi_config.key_file = nifi_auth_params['client_key']
            # mTLS uses certificate auth, not username/password
            utils.set_endpoint(config['nifi_url'], True, False)  # SSL enabled, auth disabled
            log.debug("mTLS authentication completed")
        elif nifi_auth_method == 'basic':
            log.debug("Configuring basic authentication for NiFi with user: %s",
                      nifi_auth_params['nifi_user'])
            if login:
                # Standard HTTP Basic authentication using set_endpoint's login capability
                utils.set_endpoint(
                    config['nifi_url'],
                    True, True,  # SSL enabled, auth enabled
                    nifi_auth_params['nifi_user'],
                    nifi_auth_params['nifi_pass']
                )
                # For basic auth, return the logged-in username as metadata
                auth_metadata = nifi_auth_params['nifi_user']
                log.debug("Basic authentication completed")
            else:
                # For readiness checks, just configure the host and let SSL be
                # handled by ssl_ca_cert
                nipy_config.nifi_config.host = config['nifi_url']
                log.debug("Basic auth configuration completed (no login attempted)")
        else:
            log.debug("No authentication method detected for NiFi")

    # 6. Configuration-driven Registry setup
    if connect_to_registry:
        log.debug("Detecting Registry authentication method...")
        registry_auth_method, registry_auth_params = _detect_and_validate_auth(
            config, REGISTRY_AUTH_METHODS, 'Registry')

        log.info("Using Registry authentication method: %s", registry_auth_method)
        log.debug("Auth params: %s", list(registry_auth_params.keys()))

        if registry_auth_method == 'mtls':
            log.debug("Configuring mTLS authentication for Registry...")
            # Apply client certificates for mTLS
            nipy_config.registry_config.cert_file = registry_auth_params['client_cert']
            nipy_config.registry_config.key_file = registry_auth_params['client_key']
            # mTLS uses certificate auth, not username/password
            # SSL enabled, auth disabled
            utils.set_endpoint(config['registry_url'], True, False)
            log.debug("Registry mTLS authentication completed")
        elif registry_auth_method == 'basic':
            log.debug("Configuring basic authentication for Registry with user: %s",
                      registry_auth_params['registry_user'])
            if login:
                # Basic username/password authentication for Registry using
                # set_endpoint's login capability
                utils.set_endpoint(
                    config['registry_url'],
                    True, True,  # SSL enabled, auth enabled
                    registry_auth_params['registry_user'],
                    registry_auth_params['registry_pass']
                )
                log.debug("Registry basic authentication completed")
            else:
                # For readiness checks, just configure the host and let SSL be
                # handled by ssl_ca_cert
                nipy_config.registry_config.host = config['registry_url']
                log.debug("Registry basic auth configuration completed (no login attempted)")
        else:
            log.debug("No authentication method detected for Registry")

    # Note: Bootstrap security policies are NOT handled here as they change server state.
    # Bootstrap should remain in conftest.py, sandbox.py, and other setup scripts.
    # This function only handles CLIENT-side connection configuration.

    log.debug("Profile switch completed successfully: %s", profile_name)

    # Always return tuple (profile_name, metadata)
    return profile_name, auth_metadata
