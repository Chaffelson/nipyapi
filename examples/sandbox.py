#!/usr/bin/env python3
"""
NiPyAPI Sandbox Setup Example

This comprehensive example demonstrates NiPyAPI best practices for:
• Multi-profile authentication (single-user, secure-ldap, secure-mtls, secure-oidc)
• SSL/TLS configuration and certificate handling
• Security policy bootstrapping for secure environments
• Registry client setup with Docker networking considerations
• Sample object creation (buckets, flows, versioning)
• Robust error handling and artifact reuse patterns

USAGE:
    python examples/sandbox.py <profile>

    Profiles: single-user, secure-ldap, secure-mtls, secure-oidc

    Example: python examples/sandbox.py secure-ldap

This script creates a ready-to-use NiFi environment with sample objects for
experimentation and learning. Copy and adapt this code for your own automation scripts.

WHAT IT CREATES:
• sandbox_registry_client: NiFi Registry client for version control
• sandbox_bucket: Sample bucket for storing flows
• sandbox_demo_flow: Simple GenerateFlowFile flow with versioning

The script handles authentication differences across profiles and provides
clear instructions for manual setup steps (especially OIDC).
"""

import sys
import os
import logging
import nipyapi

# Profile configurations (from conftest.py)
PROFILE_ENDPOINTS = {
    'single-user': {
        'nifi': 'https://localhost:9443/nifi-api',
        'registry': 'http://localhost:18080/nifi-registry-api',
        'registry_internal': 'http://registry-single:18080',
    },
    'secure-ldap': {
        'nifi': 'https://localhost:9444/nifi-api',
        'registry': 'https://localhost:18444/nifi-registry-api',
        'registry_internal': 'https://registry-ldap:18443',
    },
    'secure-mtls': {
        'nifi': 'https://localhost:9445/nifi-api',
        'registry': 'https://localhost:18445/nifi-registry-api',
        'registry_internal': 'https://registry-mtls:18443',
    },
    'secure-oidc': {
        'nifi': 'https://localhost:9446/nifi-api',
        'registry': 'http://localhost:18446/nifi-registry-api',
        'registry_internal': 'http://registry-oidc:18080',
    },
}

# Sandbox object names
SANDBOX_PREFIX = "sandbox"
SANDBOX_REGISTRY_CLIENT = f"{SANDBOX_PREFIX}_registry_client"
SANDBOX_BUCKET = f"{SANDBOX_PREFIX}_bucket"
SANDBOX_FLOW = f"{SANDBOX_PREFIX}_demo_flow"

log = logging.getLogger(__name__)


def resolve_profile_config(profile):
    """Resolve configuration for the given profile (from conftest.py patterns)."""
    endpoints = PROFILE_ENDPOINTS.get(profile)
    if not endpoints:
        raise ValueError(f"Unknown profile: {profile}. Must be one of: {list(PROFILE_ENDPOINTS.keys())}")

    # Default credentials (from conftest.py)
    if profile == 'secure-ldap':
        nifi_user, nifi_pass = 'einstein', 'password'
        reg_user, reg_pass = 'einstein', 'password'
    elif profile == 'single-user':
        nifi_user, nifi_pass = 'einstein', 'password1234'
        reg_user, reg_pass = 'einstein', 'password1234'
    elif profile == 'secure-mtls':
        nifi_user, nifi_pass = 'einstein', 'password'
        reg_user, reg_pass = 'einstein', 'password'
    elif profile == 'secure-oidc':
        nifi_user, nifi_pass = 'einstein', 'password1234'
        reg_user, reg_pass = 'einstein', 'password1234'

    # Certificate paths (calculate repo root from package root for development)
    repo_root = os.path.dirname(nipyapi.config.PROJECT_ROOT_DIR)
    ca_path = os.path.join(repo_root, 'resources', 'certs', 'client', 'ca.pem')
    client_cert = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.crt')
    client_key = os.path.join(repo_root, 'resources', 'certs', 'client', 'client.key')

    return {
        'profile': profile,
        'nifi_url': endpoints['nifi'],
        'registry_url': endpoints['registry'],
        'registry_internal': endpoints['registry_internal'],
        'nifi_user': nifi_user,
        'nifi_pass': nifi_pass,
        'registry_user': reg_user,
        'registry_pass': reg_pass,
        'ca_path': ca_path if os.path.exists(ca_path) else None,
        'client_cert': client_cert if os.path.exists(client_cert) else None,
        'client_key': client_key if os.path.exists(client_key) else None,
    }


def setup_ssl_config(config):
    """Configure SSL certificates using helper functions."""
    # Set SSL verification enabled (we have properly signed certificates)
    nipyapi.config.nifi_config.verify_ssl = True
    nipyapi.config.registry_config.verify_ssl = True
    nipyapi.config.disable_insecure_request_warnings = True

    # Set shared CA certificate using helper function
    if config['ca_path']:
        nipyapi.security.set_shared_ca_cert(config['ca_path'])
        log.info("SSL CA certificate configured: %s", config['ca_path'])

    # mTLS client certificates for secure-mtls profile
    if config['profile'] == 'secure-mtls':
        if config['client_cert'] and config['client_key']:
            nipyapi.config.nifi_config.cert_file = config['client_cert']
            nipyapi.config.nifi_config.key_file = config['client_key']
            nipyapi.config.registry_config.cert_file = config['client_cert']
            nipyapi.config.registry_config.key_file = config['client_key']
            log.info("mTLS client certificates configured")

    # Apply all configuration changes using helper function
    nipyapi.security.apply_ssl_configuration()

    log.info("SSL configuration applied (verification enabled with CA, warnings suppressed)")


def setup_registry_basic_auth(config):
    """Setup Registry authentication using username/password (for non-mTLS profiles)."""
    ssl_enabled = config['registry_url'].startswith('https')
    nipyapi.utils.set_endpoint(
        config['registry_url'],
        ssl_enabled, True,
        config['registry_user'],
        config['registry_pass']
    )
    log.info(
        "Registry authentication configured: %s@%s",
        config['registry_user'],
        config['registry_url'],
    )


def setup_authentication(config):
    """Setup NiFi and Registry authentication (from conftest.py patterns).

    Returns:
        str: 'success' or 'manual_setup_required' for OIDC first-run
    """
    if config['profile'] == 'secure-mtls':
        # For secure-mtls, authentication is purely certificate-based (no username/password)
        nipyapi.utils.set_endpoint(config['nifi_url'], True, False)  # ssl=True, login=False
        log.info("NiFi mTLS authentication configured: %s", config['nifi_url'])

        # Registry authentication - certificates only
        nipyapi.utils.set_endpoint(config['registry_url'], True, False)  # ssl=True, login=False
        log.info("Registry mTLS authentication configured: %s", config['registry_url'])
        return 'success'
    elif config['profile'] == 'secure-oidc':
        # OIDC requires a multi-step manual setup process
        log.info("OIDC Profile requires manual policy configuration...")

        # Step 1: Attempt OAuth2 to discover the OIDC app UUID
        nipyapi.config.nifi_config.host = config['nifi_url'].rstrip('/')
        nipyapi.config.nifi_config.api_client = None  # Force new client creation

        try:
            # Get OIDC token information including user identity
            token_data = nipyapi.security.service_login_oidc(
                service='nifi',
                username=config['nifi_user'],
                password=config['nifi_pass'],
                oidc_token_endpoint='http://localhost:8080/realms/nipyapi/protocol/openid-connect/token',
                client_id='nipyapi-client',
                client_secret='nipyapi-secret',
                return_token_info=True  # Get full token data instead of just boolean
            )

            # Extract user UUID from JWT token (much more robust than parsing logs)
            try:
                oidc_uuid = nipyapi.utils.extract_oidc_user_identity(token_data)
                log.info("OIDC user identity extracted from token: %s", oidc_uuid)
            except Exception as e:
                log.error("Failed to extract OIDC user identity: %s", e)
                return 'error'

            # Test access - will fail (403) on first run but succeed on retry
            try:
                nipyapi.nifi.FlowApi().get_about_info()
                log.info("NiFi OIDC authentication successful - proceeding with setup")
                # Success - continue to registry setup below

            except Exception:
                # Expected 403 on first run - show manual setup instructions
                log.info("WARNING: OIDC authentication requires one-time manual policy setup")
                log.info("MANUAL SETUP REQUIRED (one-time only):")
                log.info("   1. Open browser: %s", config['nifi_url'].replace('/nifi-api', '/nifi'))
                log.info("   2. Login via OIDC as: %s / %s", config['nifi_user'], config['nifi_pass'])
                log.info("   3. Go to: Settings → Users → Add User")
                log.info("   4. Create user: %s", oidc_uuid)
                log.info("   5. Go to: Settings → Policies")
                log.info("   6. Grant these policies to UUID: %s", oidc_uuid)
                log.info("      • 'view the user interface'")
                log.info("      • 'view users' (view)")
                log.info("      • 'view policies' (view)")
                log.info("      • 'modify policies' (modify)")
                log.info("   7. Re-run: make sandbox NIPYAPI_AUTH_MODE=secure-oidc")
                log.info("TIP: After manual setup, the same command will work automatically")

                # Don't proceed with sample objects - manual setup required
                return 'manual_setup_required'

        except Exception as e:
            log.error("OIDC authentication setup failed: %s", e)
            raise

        # Registry uses basic auth (single-user mode)
        setup_registry_basic_auth(config)
        return 'success'
    else:
        # For single-user and secure-ldap, use username/password authentication
        nipyapi.utils.set_endpoint(
            config['nifi_url'],
            True, True,
            config['nifi_user'],
            config['nifi_pass']
        )
        log.info("NiFi authentication configured: %s@%s", config['nifi_user'], config['nifi_url'])

        # Registry authentication
        setup_registry_basic_auth(config)
        return 'success'


def bootstrap_security_policies(config):
    """Bootstrap security policies (from conftest.py patterns).

    Returns:
        str: 'success', 'manual_setup_required', or 'error'
    """
    # NiFi security policies
    if config['profile'] in ('secure-ldap', 'secure-mtls'):
        nipyapi.security.bootstrap_security_policies(service='nifi')
        log.info("NiFi security policies bootstrapped")
    elif config['profile'] == 'secure-oidc':
        result = _bootstrap_oidc_security_policies()
        if result != 'success':
            return result  # Return early for manual setup or error

    # Registry security policies
    if config['profile'] in ('secure-ldap', 'secure-mtls'):
        # NiFi always needs to be a trusted proxy in secure deployments
        nifi_proxy_identity = 'C=US, O=NiPyAPI, CN=nifi'
        nipyapi.security.bootstrap_security_policies(service='registry', nifi_proxy_identity=nifi_proxy_identity)
        log.info("Registry security policies bootstrapped")
    else:
        log.info("Registry security policies skipped (single-user or oidc profile)")

    return 'success'


def _bootstrap_oidc_security_policies():
    """
    OIDC bootstrap is a two-phase process:

    Phase 1 (first run): OIDC app has no rights → 403 → manual setup instructions
    Phase 2 (second run): Bootstrap both OIDC app + Einstein with full admin rights

    Returns:
        str: 'success', 'manual_setup_required', or 'error'
    """
    try:
        # Bootstrap the OIDC application user (programmatic bearer token access)
        # Needed so we can use the sandbox for testing OIDC authentication
        nipyapi.security.bootstrap_security_policies(service='nifi')

        # Bootstrap Einstein user for full UI access (including flow modification)
        # Einstein starts with minimal rights, needs full admin rights after manual setup
        einstein_user = nipyapi.security.get_service_user('einstein@example.com', service="nifi")
        if einstein_user:
            nipyapi.security.bootstrap_security_policies(service='nifi', user_identity=einstein_user)
            log.info("OIDC bootstrap complete: both app and Einstein have full admin rights")
        else:
            log.info("OIDC app bootstrap complete (Einstein user not found)")

        return 'success'

    except Exception as e:
        if '403' in str(e):
            # Phase 1: Expected on first run - manual setup required
            log.info("OIDC authentication requires one-time manual policy setup")
            _print_oidc_manual_setup_instructions()
            return 'manual_setup_required'
        else:
            log.warning("OIDC security policy bootstrapping error: %s", e)
            return 'error'


def _print_oidc_manual_setup_instructions():
    """Print OIDC manual setup instructions."""
    log.info("MANUAL SETUP REQUIRED (one-time only):")
    log.info("   1. Open browser: %s", nipyapi.config.nifi_config.host.replace('/nifi-api', '/nifi'))
    log.info("   2. Login via OIDC as: einstein / password1234")
    log.info("   3. Go to: Settings → Users → Add User")
    log.info("   4. Create user with extracted UUID from token")
    log.info("   5. Go to: Settings → Policies")
    log.info("   6. Grant these policies to the UUID:")
    log.info("      • 'view the user interface'")
    log.info("      • 'view users' (view)")
    log.info("      • 'view policies' (view)")
    log.info("      • 'modify policies' (modify)")
    log.info("   7. Re-run: make sandbox NIPYAPI_AUTH_MODE=secure-oidc")
    log.info("TIP: After manual setup, the same command will work automatically")


def _print_setup_complete_summary(config, profile):
    """Print detailed setup completion summary with profile-specific instructions."""
    print("\nSandbox setup complete!")
    print(f"  Profile: {profile}")

    if config['profile'] == 'secure-mtls':
        _print_mtls_certificate_instructions(config)
    else:
        # Username/password authentication for single-user and secure-ldap
        nifi_ui = config['nifi_url'].replace('/nifi-api', '/nifi')
        registry_ui = config['registry_url'].replace('/nifi-registry-api', '/nifi-registry')
        print(f"  NiFi UI: {nifi_ui} ({config['nifi_user']}/{config['nifi_pass']})")
        print(f"  Registry UI: {registry_ui} ({config['registry_user']}/{config['registry_pass']})")

    print(f"  Registry Client: {SANDBOX_REGISTRY_CLIENT}")
    print(f"  Sample Bucket: {SANDBOX_BUCKET}")
    print(f"  Sample Flow: {SANDBOX_FLOW}")
    print("\nReady for experimentation! Run 'make down' when finished.")


def _print_mtls_certificate_instructions(config):
    """Print detailed mTLS certificate setup instructions."""
    cert_p12_path = config['client_cert'].replace('.crt', '.p12')
    nifi_ui = config['nifi_url'].replace('/nifi-api', '/nifi')
    registry_ui = config['registry_url'].replace('/nifi-registry-api', '/nifi-registry')

    print(f"  NiFi UI: {nifi_ui}")
    print(f"  Registry UI: {registry_ui}")
    print(f"  Authentication: Client certificate required (ADVANCED)")
    print()
    print("  TIP: For easier setup, try:")
    print("      make sandbox NIPYAPI_AUTH_MODE=single-user  (recommended - simple setup)")
    print("      make sandbox NIPYAPI_AUTH_MODE=secure-ldap  (more complex security)")
    print()
    print("  IMPORT CLIENT CERTIFICATE FIRST:")
    print(f"      Certificate file: {cert_p12_path}")
    print("      Import password: changeit")
    print("      Certificate name: client (configured for admin access)")
    print()
    print("  BROWSER IMPORT INSTRUCTIONS:")
    print()
    print("  Chrome/Edge:")
    print("    1. Settings → Privacy & Security → Security → Manage certificates")
    print(f"    2. Personal tab → Import → Browse to: {cert_p12_path}")
    print("    3. Enter password: changeit")
    print("    4. ✓ Mark keys as exportable → Next → Finish")
    print()
    print("  Firefox:")
    print("    1. Settings → Privacy & Security → Certificates → View Certificates")
    print(f"    2. Your Certificates tab → Import → Select: {cert_p12_path}")
    print("    3. Enter password: changeit")
    print()
    print("  Safari:")
    print(f"    1. Double-click: {cert_p12_path}")
    print("    2. Keychain Access → Enter password: changeit")
    print("    3. Trust Settings → Always Trust")
    print()
    print("  WARNING: THEN visit URLs above - browser will prompt to select 'client' certificate")


def create_registry_client(config):
    """Create registry client using ensure pattern for robust automation."""
    registry_client = nipyapi.versioning.ensure_registry_client(
        name=SANDBOX_REGISTRY_CLIENT,
        uri=config['registry_internal'],  # Use internal Docker hostname
        description='NiPyAPI Sandbox Registry Client'
    )
    log.info("Registry client ready: %s → %s", SANDBOX_REGISTRY_CLIENT, config['registry_internal'])
    return registry_client


def create_sample_bucket():
    """Create sample bucket using ensure pattern for robust automation."""
    bucket = nipyapi.versioning.ensure_registry_bucket(SANDBOX_BUCKET)
    log.info("Sample bucket ready: %s", SANDBOX_BUCKET)
    return bucket


def create_sample_flow(registry_client, bucket):
    """Create a simple sample flow for experimentation."""
    # Check if flow already exists and reuse it
    try:
        existing_pg = nipyapi.canvas.get_process_group(SANDBOX_FLOW)
        if existing_pg:
            log.info("Reusing existing sample flow: %s", SANDBOX_FLOW)
            return existing_pg, None  # Return None for version_info since we're reusing
    except Exception:
        # Flow doesn't exist, we'll create it below
        pass

    # Create simple process group with GenerateFlowFile
    root_pg = nipyapi.canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id')

    # Create process group
    try:
        sample_pg = nipyapi.canvas.create_process_group(
            parent_pg=root_pg,
            new_pg_name=SANDBOX_FLOW,
            location=(200.0, 200.0)
        )
    except Exception as e:
        # If creation fails, try to get existing process group (race condition handling)
        if "already exists" in str(e) or "duplicate" in str(e).lower():
            try:
                sample_pg = nipyapi.canvas.get_process_group(SANDBOX_FLOW)
                log.info("Found existing process group after failed creation: %s", SANDBOX_FLOW)
                return sample_pg, None  # Return None for version_info since we're reusing
            except Exception:
                pass
        raise e

    # Add GenerateFlowFile processor
    _ = nipyapi.canvas.create_processor(
        parent_pg=sample_pg,
        processor=nipyapi.canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 300.0),
        name=f"{SANDBOX_PREFIX}_generator",
        config=nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period='10s',
            auto_terminated_relationships=['success']
        )
    )

    log.info("Sample flow created: %s (with GenerateFlowFile processor)", SANDBOX_FLOW)

    # Version the flow
    try:
        version_info = nipyapi.versioning.save_flow_ver(
            process_group=sample_pg,
            registry_client=registry_client,
            bucket=bucket,
            flow_name=SANDBOX_FLOW,
            comment='Initial sandbox flow version',
            desc='Simple flow for experimentation'
        )
        log.info("Sample flow versioned: %s v1", SANDBOX_FLOW)
        return sample_pg, version_info
    except Exception as e:
        log.warning("Flow versioning failed (flow still created): %s", e)
        return sample_pg, None


def main():
    """Main sandbox setup function."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <profile>")
        print(f"Profiles: {', '.join(PROFILE_ENDPOINTS.keys())}")
        sys.exit(1)

    profile = sys.argv[1]

    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    try:
        log.info("Setting up NiPyAPI sandbox for profile: %s", profile)

        # 1. Resolve configuration
        config = resolve_profile_config(profile)

        # 2. Setup SSL certificates
        setup_ssl_config(config)

        # 3. Setup authentication
        auth_result = setup_authentication(config)
        if auth_result == 'manual_setup_required':
            print("\nOIDC manual setup required - follow instructions above")
            print("   After completing setup, re-run: make sandbox NIPYAPI_AUTH_MODE=secure-oidc")
            sys.exit(0)  # Clean exit, not an error
        elif auth_result == 'error':
            log.error("Authentication setup failed")
            sys.exit(1)

        # 4. Bootstrap security policies (for secure profiles)
        bootstrap_result = bootstrap_security_policies(config)
        if bootstrap_result == 'manual_setup_required':
            print("\nOIDC manual setup required - follow instructions above")
            print("   After completing setup, re-run: make sandbox NIPYAPI_AUTH_MODE=secure-oidc")
            sys.exit(0)  # Clean exit, not an error
        elif bootstrap_result == 'error':
            log.error("Security policy bootstrap failed")
            sys.exit(1)

        # 5. Create registry client
        registry_client = create_registry_client(config)

        # 6. Create sample bucket
        bucket = create_sample_bucket()

        # 7. Create sample flow
        _, _ = create_sample_flow(registry_client, bucket)

        # Success summary
        _print_setup_complete_summary(config, profile)

        # Final success message (only shown when setup actually completes)
        print("\n=== 4/4: Sandbox ready! ===")
        print("Your NiPyAPI sandbox is ready for experimentation!")
        print("   Run 'make down' when finished to clean up")

    except Exception as e:
        log.error("Sandbox setup failed: %s", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
