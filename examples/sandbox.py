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
        # OIDC uses browser authentication for NiFi, basic auth for Registry
        nifi_user, nifi_pass = 'einstein', 'password1234'
        reg_user, reg_pass = 'einstein', 'password1234'
    
    # Certificate paths (from conftest.py)
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
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
    """Configure SSL certificates (from conftest.py patterns)."""
    # Disable SSL verification for sandbox environments (all use self-signed certificates)
    nipyapi.config.nifi_config.verify_ssl = False
    nipyapi.config.registry_config.verify_ssl = False
    
    # Use project's established pathway for disabling SSL warnings
    nipyapi.config.disable_insecure_request_warnings = True
    nipyapi.config.apply_ssl_warning_settings()  # Apply the warning setting
    
    log.info("✅ SSL verification disabled (sandbox uses self-signed certificates)")
    
    if config['ca_path']:
        nipyapi.config.set_shared_ca_cert(config['ca_path'])
        log.info("✅ SSL CA certificate configured: %s", config['ca_path'])
    
    # mTLS client certificates for secure-mtls profile
    if config['profile'] == 'secure-mtls':
        if config['client_cert'] and config['client_key']:
            nipyapi.config.nifi_config.cert_file = config['client_cert']
            nipyapi.config.nifi_config.key_file = config['client_key']
            nipyapi.config.registry_config.cert_file = config['client_cert']
            nipyapi.config.registry_config.key_file = config['client_key']
            log.info("✅ mTLS client certificates configured")


def setup_registry_basic_auth(config):
    """Setup Registry authentication using username/password (for non-mTLS profiles)."""
    ssl_enabled = config['registry_url'].startswith('https')
    nipyapi.utils.set_endpoint(
        config['registry_url'], 
        ssl_enabled, True, 
        config['registry_user'], 
        config['registry_pass']
    )
    log.info("✅ Registry authentication configured: %s@%s", config['registry_user'], config['registry_url'])


def setup_authentication(config):
    """Setup NiFi and Registry authentication (from conftest.py patterns)."""
    if config['profile'] == 'secure-mtls':
        # For secure-mtls, authentication is purely certificate-based (no username/password)
        nipyapi.utils.set_endpoint(config['nifi_url'], True, False)  # ssl=True, login=False
        log.info("✅ NiFi mTLS authentication configured: %s", config['nifi_url'])
        
        # Registry authentication - certificates only  
        nipyapi.utils.set_endpoint(config['registry_url'], True, False)  # ssl=True, login=False
        log.info("✅ Registry mTLS authentication configured: %s", config['registry_url'])
    elif config['profile'] == 'secure-oidc':
        # OIDC requires a multi-step manual setup process
        log.info("🔧 OIDC Profile requires manual policy configuration...")
        
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
                log.info("🎯 OIDC user identity extracted from token: %s", oidc_uuid)
            except Exception as e:
                log.error("❌ Failed to extract OIDC user identity: %s", e)
                return config
            
            # Test access - will fail (403) on first run but succeed on retry
            try:
                nipyapi.nifi.FlowApi().get_about_info()
                log.info("✅ NiFi OIDC authentication successful - proceeding with setup")
                    
            except Exception:
                # Expected 403 on first run - show manual setup instructions
                log.info("⚠️  OIDC authentication requires one-time manual policy setup")
                log.info("📋 MANUAL SETUP REQUIRED (one-time only):")
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
                log.info("💡 After manual setup, the same command will work automatically")
                
                # Don't proceed with sample objects - manual setup required
                raise OIDCManualSetupRequired("OIDC manual setup needed")
                
        except Exception as e:
            log.error("❌ OIDC authentication setup failed: %s", e)
            raise
        
        # Registry uses basic auth (single-user mode)
        setup_registry_basic_auth(config)
    else:
        # For single-user and secure-ldap, use username/password authentication
        nipyapi.utils.set_endpoint(
            config['nifi_url'], 
            True, True, 
            config['nifi_user'], 
            config['nifi_pass']
        )
        log.info("✅ NiFi authentication configured: %s@%s", config['nifi_user'], config['nifi_url'])
        
        # Registry authentication
        setup_registry_basic_auth(config)


def bootstrap_security_policies(config):
    """Bootstrap security policies (from conftest.py patterns)."""
    # NiFi security policies: only for secure profiles
    if config['profile'] in ('secure-ldap', 'secure-mtls', 'secure-oidc'):
        try:
            nipyapi.security.bootstrap_security_policies(service='nifi')
            
            # For OIDC: also grant admin policies to the UI user (einstein@example.com)
            # since the above bootstrap only grants to the OAuth2 app identity
            if config['profile'] == 'secure-oidc':
                ui_user_identity = 'einstein@example.com'
                try:
                    # Get or create the UI user entity
                    ui_user = nipyapi.security.get_service_user(ui_user_identity, service="nifi")
                    if not ui_user:
                        ui_user = nipyapi.security.create_service_user(
                            identity=ui_user_identity, service="nifi", strict=False
                        )
                    
                    # Bootstrap policies for the UI user as well
                    nipyapi.security.bootstrap_security_policies(
                        service='nifi', user_identity=ui_user
                    )
                    log.info("✅ OIDC UI user (%s) also granted admin policies", ui_user_identity)
                except Exception as ui_bootstrap_e:
                    # For OIDC, 403 errors are expected on first run - don't log details
                    if config['profile'] == 'secure-oidc' and '403' in str(ui_bootstrap_e):
                        pass  # Expected - already shown manual setup instructions
                    else:
                        log.warning("⚠️  Could not grant admin policies to UI user %s: %s", 
                                  ui_user_identity, ui_bootstrap_e)
            
            log.info("✅ NiFi security policies bootstrapped")
        except Exception as e:
            # For OIDC, 403 errors are expected on first run - handle gracefully
            if config['profile'] == 'secure-oidc' and '403' in str(e):
                # Don't log anything here - manual setup instructions already shown
                # Re-raise for OIDC so the manual setup flow can handle it properly
                raise OIDCManualSetupRequired("OIDC manual setup needed") from e
            else:
                log.warning("⚠️  NiFi security policy bootstrapping error (may be normal): %s", e)
    
    # Registry security policies: only for secure profiles with managed authorizers
    # Skip for single-user and secure-oidc (both use single-user Registry)
    if config['profile'] in ('secure-ldap', 'secure-mtls'):
        try:
            nipyapi.security.bootstrap_security_policies(
                service='registry', 
                nifi_proxy_identity='C=US, O=NiPyAPI, CN=nifi'
            )
            log.info("✅ Registry security policies bootstrapped")
        except Exception as e:
            log.warning("⚠️  Registry security policy bootstrapping error (may be normal): %s", e)
    else:
        log.info("ℹ️  Registry security policies skipped (single-user mode)")


class OIDCManualSetupRequired(Exception):
    """Custom exception for OIDC manual setup flow."""
    pass


def create_registry_client(config):
    """Create registry client (from conftest.py ensure_registry_client patterns)."""
    # Check if client already exists and reuse it
    try:
        existing = nipyapi.versioning.get_registry_client(SANDBOX_REGISTRY_CLIENT)
        if existing:
            log.info("✅ Reusing existing registry client: %s", SANDBOX_REGISTRY_CLIENT)
            return existing
    except Exception:
        # Client doesn't exist, we'll create it below
        pass
    
    # Create new registry client using internal Docker hostname
    try:
        registry_client = nipyapi.versioning.create_registry_client(
            name=SANDBOX_REGISTRY_CLIENT,
            uri=config['registry_internal'],  # Use internal Docker hostname
            description='NiPyAPI Sandbox Registry Client'
        )
        log.info("✅ Registry client created: %s → %s", SANDBOX_REGISTRY_CLIENT, config['registry_internal'])
        return registry_client
    except Exception as e:
        # If creation fails, try to get existing client (race condition handling)
        if "already exists" in str(e):
            try:
                existing = nipyapi.versioning.get_registry_client(SANDBOX_REGISTRY_CLIENT)
                log.info("✅ Found existing registry client after failed creation: %s", SANDBOX_REGISTRY_CLIENT)
                return existing
            except Exception:
                pass
        raise e


def create_sample_bucket():
    """Create sample bucket for experimentation."""
    # Check if bucket already exists and reuse it
    try:
        existing = nipyapi.versioning.get_registry_bucket(SANDBOX_BUCKET)
        if existing:
            log.info("✅ Reusing existing bucket: %s", SANDBOX_BUCKET)
            return existing
    except Exception:
        # Bucket doesn't exist, we'll create it below
        pass
    
    # Create new bucket
    try:
        bucket = nipyapi.versioning.create_registry_bucket(SANDBOX_BUCKET)
        log.info("✅ Sample bucket created: %s", SANDBOX_BUCKET)
        return bucket
    except Exception as e:
        # If creation fails, try to get existing bucket (race condition handling)
        if "already exists" in str(e):
            try:
                existing = nipyapi.versioning.get_registry_bucket(SANDBOX_BUCKET)
                log.info("✅ Found existing bucket after failed creation: %s", SANDBOX_BUCKET)
                return existing
            except Exception:
                pass
        raise e


def create_sample_flow(registry_client, bucket):
    """Create a simple sample flow for experimentation."""
    # Check if flow already exists and reuse it
    try:
        existing_pg = nipyapi.canvas.get_process_group(SANDBOX_FLOW)
        if existing_pg:
            log.info("✅ Reusing existing sample flow: %s", SANDBOX_FLOW)
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
                log.info("✅ Found existing process group after failed creation: %s", SANDBOX_FLOW)
                return sample_pg, None  # Return None for version_info since we're reusing
            except Exception:
                pass
        raise e
    
    # Add GenerateFlowFile processor
    generate_processor = nipyapi.canvas.create_processor(
        parent_pg=sample_pg,
        processor=nipyapi.canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 300.0),
        name=f"{SANDBOX_PREFIX}_generator",
        config=nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period='10s',
            auto_terminated_relationships=['success']
        )
    )
    
    log.info("✅ Sample flow created: %s (with GenerateFlowFile processor)", SANDBOX_FLOW)
    
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
        log.info("✅ Sample flow versioned: %s v1", SANDBOX_FLOW)
        return sample_pg, version_info
    except Exception as e:
        log.warning("⚠️  Flow versioning failed (flow still created): %s", e)
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
        log.info("🏗️ Setting up NiPyAPI sandbox for profile: %s", profile)
        
        # 1. Resolve configuration
        config = resolve_profile_config(profile)
        
        # 2. Setup SSL certificates
        setup_ssl_config(config)
        
        # 3. Setup authentication
        setup_authentication(config)
        
        # 4. Bootstrap security policies (for secure profiles)
        bootstrap_security_policies(config)
        
        # 5. Create registry client
        registry_client = create_registry_client(config)
        
        # 6. Create sample bucket
        bucket = create_sample_bucket()
        
        # 7. Create sample flow
        sample_pg, version_info = create_sample_flow(registry_client, bucket)
        
        # Success summary
        print("\n🎯 Sandbox setup complete!")
        print(f"  📋 Profile: {profile}")
        
        if config['profile'] == 'secure-mtls':
            # mTLS requires client certificate in browser
            cert_p12_path = config['client_cert'].replace('.crt', '.p12')
            print(f"  🌐 NiFi UI: {config['nifi_url'].replace('/nifi-api', '/nifi')}")
            print(f"  📊 Registry UI: {config['registry_url'].replace('/nifi-registry-api', '/nifi-registry')}")
            print(f"  🔐 Authentication: Client certificate required (ADVANCED)")
            print(f"")
            print(f"  💡 TIP: For easier setup, try:")
            print(f"      make sandbox NIPYAPI_AUTH_MODE=single-user  (recommended - simple setup)")
            print(f"      make sandbox NIPYAPI_AUTH_MODE=secure-ldap  (more complex security)")
            print(f"")
            print(f"  📥 IMPORT CLIENT CERTIFICATE FIRST:")
            print(f"      Certificate file: {cert_p12_path}")
            print(f"      Import password: changeit")
            print(f"      Certificate name: client (configured for admin access)")
            print(f"")
            print(f"  🔧 BROWSER IMPORT INSTRUCTIONS:")
            print(f"")
            print(f"  Chrome/Edge:")
            print(f"    1. Settings → Privacy & Security → Security → Manage certificates")
            print(f"    2. Personal tab → Import → Browse to: {cert_p12_path}")
            print(f"    3. Enter password: changeit")
            print(f"    4. ✓ Mark keys as exportable → Next → Finish")
            print(f"")
            print(f"  Firefox:")
            print(f"    1. Settings → Privacy & Security → Certificates → View Certificates")
            print(f"    2. Your Certificates tab → Import → Select: {cert_p12_path}")
            print(f"    3. Enter password: changeit")
            print(f"")
            print(f"  Safari:")
            print(f"    1. Double-click: {cert_p12_path}")
            print(f"    2. Keychain Access → Enter password: changeit")
            print(f"    3. Trust Settings → Always Trust")
            print(f"")
            print(f"  ⚠️  THEN visit URLs above - browser will prompt to select 'client' certificate")
        else:
            # Username/password authentication for single-user and secure-ldap
            print(f"  🌐 NiFi UI: {config['nifi_url'].replace('/nifi-api', '/nifi')} ({config['nifi_user']}/{config['nifi_pass']})")
            print(f"  📊 Registry UI: {config['registry_url'].replace('/nifi-registry-api', '/nifi-registry')} ({config['registry_user']}/{config['registry_pass']})")
        
        print(f"  🔗 Registry Client: {SANDBOX_REGISTRY_CLIENT}")
        print(f"  📦 Sample Bucket: {SANDBOX_BUCKET}")
        print(f"  🔄 Sample Flow: {SANDBOX_FLOW}")
        print("\n💡 Ready for experimentation! Run 'make down' when finished.")
        
        # Final success message (only shown when setup actually completes)
        print("\n=== 4/4: Sandbox ready! ===")
        print("🎯 Your NiPyAPI sandbox is ready for experimentation!")
        print("   Run 'make down' when finished to clean up")
        
    except OIDCManualSetupRequired:
        # Expected OIDC flow - manual setup instructions already shown
        print("\n🔧 OIDC manual setup required - follow instructions above")
        print("   After completing setup, re-run: make sandbox NIPYAPI_AUTH_MODE=secure-oidc")
        sys.exit(0)  # Clean exit, not an error
    except Exception as e:
        log.error("❌ Sandbox setup failed: %s", e)
        sys.exit(1)



if __name__ == '__main__':
    main()
