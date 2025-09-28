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
import logging
import nipyapi

# Sandbox object names
SANDBOX_PREFIX = "sandbox"
SANDBOX_REGISTRY_CLIENT = f"{SANDBOX_PREFIX}_registry_client"
SANDBOX_BUCKET = f"{SANDBOX_PREFIX}_bucket"
SANDBOX_FLOW = f"{SANDBOX_PREFIX}_demo_flow"

log = logging.getLogger(__name__)


def get_profile_config(profile):
    """Get resolved configuration for the given profile."""
    profiles_path = nipyapi.utils.resolve_relative_paths('examples/profiles.yml')
    return nipyapi.profiles.resolve_profile_config(profile_name=profile, profiles_file_path=profiles_path)


def bootstrap_security_policies(profile, auth_metadata=None):
    """Bootstrap security policies for secure profiles.

    Args:
        profile (str): Name of the profile being used
        auth_metadata: Authentication metadata from profile switch:
                      - OIDC: token_data dict for UUID extraction
                      - Basic: username string
                      - mTLS: None

    Returns:
        str: 'success', 'manual_setup_required', or 'error'
    """
    # NiFi security policies
    if profile in ('secure-ldap', 'secure-mtls'):
        nipyapi.security.bootstrap_security_policies(service='nifi')
        log.info("NiFi security policies bootstrapped")
    elif profile == 'secure-oidc':
        result = _bootstrap_oidc_security_policies(auth_metadata)
        if result != 'success':
            return result  # Return early for manual setup or error

    # Registry security policies
    if profile in ('secure-ldap', 'secure-mtls'):
        # NiFi always needs to be a trusted proxy in secure deployments
        config = get_profile_config(profile)
        nifi_proxy_identity = config.get('nifi_proxy_identity')
        nipyapi.security.bootstrap_security_policies(service='registry', nifi_proxy_identity=nifi_proxy_identity)
        log.info("Registry security policies bootstrapped")
    else:
        log.info("Registry security policies skipped (single-user or oidc profile)")

    return 'success'


def _bootstrap_oidc_security_policies(auth_metadata=None):
    """
    OIDC bootstrap is a two-phase process:

    Phase 1 (first run): OIDC app has no rights → 403 → manual setup instructions
    Phase 2 (second run): Bootstrap both OIDC app + Einstein with full admin rights

    Args:
        auth_metadata: OIDC token data from profile switch for UUID extraction

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

            # Extract UUID from auth_metadata if available
            oidc_uuid = None
            if auth_metadata:
                try:
                    oidc_uuid = nipyapi.utils.extract_oidc_user_identity(auth_metadata)
                except Exception as extract_error:
                    log.warning("Could not extract OIDC UUID from metadata: %s", extract_error)

            _print_oidc_manual_setup_instructions(oidc_uuid)
            return 'manual_setup_required'
        else:
            log.warning("OIDC security policy bootstrapping error: %s", e)
            return 'error'



def _print_oidc_manual_setup_instructions(oidc_uuid=None):
    """Print OIDC manual setup instructions with the extracted UUID."""
    log.info("MANUAL SETUP REQUIRED (one-time only):")
    log.info("   1. Open browser: %s", nipyapi.config.nifi_config.host.replace('/nifi-api', '/nifi'))
    log.info("   2. Login via OIDC as: einstein / password1234")
    log.info("   3. Go to: Settings → Users → Add User")

    if oidc_uuid:
        log.info("   4. Create user with this exact UUID: %s", oidc_uuid)
    else:
        log.info("   4. Create user with extracted UUID from token (see error above)")

    log.info("   5. Go to: Settings → Policies")
    if oidc_uuid:
        log.info("   6. Grant these policies to UUID %s:", oidc_uuid)
    else:
        log.info("   6. Grant these policies to the UUID:")
    log.info("      • 'view the user interface'")
    log.info("      • 'view users' (view)")
    log.info("      • 'view policies' (view)")
    log.info("      • 'modify policies' (modify)")
    log.info("   7. Re-run: make sandbox NIPYAPI_PROFILE=secure-oidc")
    log.info("TIP: After manual setup, the same command will work automatically")


def _print_setup_complete_summary(profile):
    """Print detailed setup completion summary with profile-specific instructions."""
    print("\nSandbox setup complete!")
    print(f"  Profile: {profile}")

    if profile == 'secure-mtls':
        _print_mtls_certificate_instructions()
    else:
        # Get config for UI URLs and credentials
        config = get_profile_config(profile)
        nifi_ui = config['nifi_url'].replace('/nifi-api', '/nifi')
        registry_ui = config['registry_url'].replace('/nifi-registry-api', '/nifi-registry')
        print(f"  NiFi UI: {nifi_ui} ({config['nifi_user']}/{config['nifi_pass']})")
        print(f"  Registry UI: {registry_ui} ({config['registry_user']}/{config['registry_pass']})")

    print(f"  Registry Client: {SANDBOX_REGISTRY_CLIENT}")
    print(f"  Sample Bucket: {SANDBOX_BUCKET}")
    print(f"  Sample Flow: {SANDBOX_FLOW}")
    print("\nReady for experimentation! Run 'make down' when finished.")


def _print_mtls_certificate_instructions():
    """Print detailed mTLS certificate setup instructions."""
    config = get_profile_config('secure-mtls')
    cert_p12_path = config['client_cert'].replace('.crt', '.p12')
    nifi_ui = config['nifi_url'].replace('/nifi-api', '/nifi')
    registry_ui = config['registry_url'].replace('/nifi-registry-api', '/nifi-registry')

    print(f"  NiFi UI: {nifi_ui}")
    print(f"  Registry UI: {registry_ui}")
    print(f"  Authentication: Client certificate required (ADVANCED)")
    print()
    print("  TIP: For easier setup, try:")
    print("      make sandbox NIPYAPI_PROFILE=single-user  (recommended - simple setup)")
    print("      make sandbox NIPYAPI_PROFILE=secure-ldap  (more complex security)")
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


def create_registry_client(registry_internal_url):
    """Create registry client using ensure pattern for robust automation."""
    registry_client = nipyapi.versioning.ensure_registry_client(
        name=SANDBOX_REGISTRY_CLIENT,
        uri=registry_internal_url,
        description='NiPyAPI Sandbox Registry Client'
    )
    log.info("Registry client ready: %s → %s", SANDBOX_REGISTRY_CLIENT, registry_internal_url)
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
        # Load available profiles from the profiles system
        try:
            profiles_path = nipyapi.utils.resolve_relative_paths('examples/profiles.yml')
            profiles = nipyapi.profiles.load_profiles_from_file(profiles_path)
            available_profiles = ', '.join(sorted(profiles.keys()))
        except Exception as e:
            available_profiles = "Error loading profiles"
            print(f"Warning: Could not load profiles: {e}")

        print(f"Usage: {sys.argv[0]} <profile>")
        print(f"Available profiles: {available_profiles}")
        print(f"Profile 'single-user' recommended for new users")
        sys.exit(1)

    profile = sys.argv[1]

    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    try:
        log.info("Setting up NiPyAPI sandbox for profile: %s", profile)

        # 1. Use centralized profile switching (replaces config resolution, SSL setup, authentication)
        profiles_path = nipyapi.utils.resolve_relative_paths('examples/profiles.yml')
        profile_name, auth_metadata = nipyapi.profiles.switch(profile, profiles_path)
        log.info("Profile switching complete: %s", profile_name)

        # 2. Get config for sample object creation
        config = get_profile_config(profile)

        # 3. Bootstrap security policies (server-side setup)
        bootstrap_result = bootstrap_security_policies(profile, auth_metadata)
        if bootstrap_result == 'manual_setup_required':
            print("\nOIDC manual setup required - follow instructions above")
            print("   After completing setup, re-run: make sandbox NIPYAPI_PROFILE=secure-oidc")
            sys.exit(0)  # Clean exit, not an error
        elif bootstrap_result == 'error':
            log.error("Security policy bootstrap failed")
            sys.exit(1)

        # 4. Create registry client
        registry_client = create_registry_client(config['registry_internal_url'])

        # 5. Create sample bucket
        bucket = create_sample_bucket()

        # 6. Create sample flow
        _, _ = create_sample_flow(registry_client, bucket)

        # Success summary
        _print_setup_complete_summary(profile)

        # Final success message (only shown when setup actually completes)
        print("\n=== 4/4: Sandbox ready! ===")
        print("Your NiPyAPI sandbox is ready for experimentation!")
        print("   Run 'make down' when finished to clean up")

    except Exception as e:
        log.error("Sandbox setup failed: %s", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
