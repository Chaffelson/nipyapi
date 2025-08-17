#!/usr/bin/env python3
"""
Setup NiPyAPI playground environment with sample objects for experimentation.

This script replicates the exact setup sequence from tests/conftest.py to create
a ready-to-use environment with proper authentication, security bootstrapping,
and sample objects (registry client, bucket, sample flow).
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
}

# Playground object names
PLAYGROUND_PREFIX = "playground"
PLAYGROUND_REGISTRY_CLIENT = f"{PLAYGROUND_PREFIX}_registry_client"
PLAYGROUND_BUCKET = f"{PLAYGROUND_PREFIX}_bucket"
PLAYGROUND_FLOW = f"{PLAYGROUND_PREFIX}_demo_flow"

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
    if config['ca_path']:
        nipyapi.config.nifi_config.ssl_ca_cert = config['ca_path']
        nipyapi.config.registry_config.ssl_ca_cert = config['ca_path']
        log.info("✅ SSL CA certificate configured: %s", config['ca_path'])
    
    # mTLS client certificates for secure-mtls profile
    if config['profile'] == 'secure-mtls':
        if config['client_cert'] and config['client_key']:
            nipyapi.config.nifi_config.cert_file = config['client_cert']
            nipyapi.config.nifi_config.key_file = config['client_key']
            nipyapi.config.registry_config.cert_file = config['client_cert']
            nipyapi.config.registry_config.key_file = config['client_key']
            log.info("✅ mTLS client certificates configured")


def setup_authentication(config):
    """Setup NiFi and Registry authentication (from conftest.py patterns)."""
    # For secure-mtls, authentication is purely certificate-based (no username/password)
    if config['profile'] == 'secure-mtls':
        # NiFi authentication - certificates only
        nipyapi.utils.set_endpoint(config['nifi_url'], True, False)  # ssl=True, login=False
        log.info("✅ NiFi mTLS authentication configured: %s", config['nifi_url'])
        
        # Registry authentication - certificates only  
        nipyapi.utils.set_endpoint(config['registry_url'], True, False)  # ssl=True, login=False
        log.info("✅ Registry mTLS authentication configured: %s", config['registry_url'])
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
        ssl_enabled = config['registry_url'].startswith('https')
        nipyapi.utils.set_endpoint(
            config['registry_url'], 
            ssl_enabled, True, 
            config['registry_user'], 
            config['registry_pass']
        )
        log.info("✅ Registry authentication configured: %s@%s", config['registry_user'], config['registry_url'])


def bootstrap_security_policies(config):
    """Bootstrap security policies (from conftest.py patterns)."""
    # NiFi security policies: only for secure profiles
    if config['profile'] in ('secure-ldap', 'secure-mtls'):
        try:
            nipyapi.security.bootstrap_security_policies(service='nifi')
            log.info("✅ NiFi security policies bootstrapped")
        except Exception as e:
            log.warning("⚠️  NiFi security policy bootstrapping error (may be normal): %s", e)
    
    # Registry security policies: always needed (all profiles including single-user)
    try:
        nipyapi.security.bootstrap_security_policies(
            service='registry', 
            nifi_proxy_identity='C=US, O=NiPyAPI, CN=nifi'
        )
        log.info("✅ Registry security policies bootstrapped")
    except Exception as e:
        log.warning("⚠️  Registry security policy bootstrapping error (may be normal): %s", e)


def create_registry_client(config):
    """Create registry client (from conftest.py ensure_registry_client patterns)."""
    # Clean up existing client
    try:
        existing = nipyapi.versioning.get_registry_client(PLAYGROUND_REGISTRY_CLIENT)
        if existing:
            nipyapi.versioning.delete_registry_client(existing)
            log.info("🧹 Cleaned up existing registry client")
    except ValueError:
        pass
    
    # Create new registry client using internal Docker hostname
    registry_client = nipyapi.versioning.create_registry_client(
        name=PLAYGROUND_REGISTRY_CLIENT,
        uri=config['registry_internal'],  # Use internal Docker hostname
        description='NiPyAPI Playground Registry Client'
    )
    log.info("✅ Registry client created: %s → %s", PLAYGROUND_REGISTRY_CLIENT, config['registry_internal'])
    return registry_client


def create_sample_bucket():
    """Create sample bucket for experimentation."""
    # Clean up existing bucket
    try:
        existing = nipyapi.versioning.get_registry_bucket(PLAYGROUND_BUCKET)
        if existing:
            nipyapi.versioning.delete_registry_bucket(existing)
            log.info("🧹 Cleaned up existing bucket")
    except ValueError:
        pass
    
    # Create new bucket
    bucket = nipyapi.versioning.create_registry_bucket(PLAYGROUND_BUCKET)
    log.info("✅ Sample bucket created: %s", PLAYGROUND_BUCKET)
    return bucket


def create_sample_flow(registry_client, bucket):
    """Create a simple sample flow for experimentation."""
    # Clean up existing flow
    try:
        existing_pg = nipyapi.canvas.get_process_group(PLAYGROUND_FLOW)
        if existing_pg:
            nipyapi.canvas.delete_process_group(existing_pg, force=True)
            log.info("🧹 Cleaned up existing sample flow")
    except ValueError:
        pass
    
    # Create simple process group with GenerateFlowFile
    root_pg = nipyapi.canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id')
    
    # Create process group
    sample_pg = nipyapi.canvas.create_process_group(
        parent_pg=root_pg,
        new_pg_name=PLAYGROUND_FLOW,
        location=(200.0, 200.0)
    )
    
    # Add GenerateFlowFile processor
    generate_processor = nipyapi.canvas.create_processor(
        parent_pg=sample_pg,
        processor=nipyapi.canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 300.0),
        name=f"{PLAYGROUND_PREFIX}_generator",
        config=nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period='10s',
            auto_terminated_relationships=['success']
        )
    )
    
    log.info("✅ Sample flow created: %s (with GenerateFlowFile processor)", PLAYGROUND_FLOW)
    
    # Version the flow
    try:
        version_info = nipyapi.versioning.save_flow_ver(
            process_group=sample_pg,
            registry_client=registry_client,
            bucket=bucket,
            flow_name=PLAYGROUND_FLOW,
            comment='Initial playground flow version',
            desc='Simple flow for experimentation'
        )
        log.info("✅ Sample flow versioned: %s v1", PLAYGROUND_FLOW)
        return sample_pg, version_info
    except Exception as e:
        log.warning("⚠️  Flow versioning failed (flow still created): %s", e)
        return sample_pg, None


def main():
    """Main playground setup function."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <profile>")
        print(f"Profiles: {', '.join(PROFILE_ENDPOINTS.keys())}")
        sys.exit(1)
    
    profile = sys.argv[1]
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    try:
        log.info("🎮 Setting up NiPyAPI playground for profile: %s", profile)
        
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
        print("\n🎯 Playground setup complete!")
        print(f"  📋 Profile: {profile}")
        
        if config['profile'] == 'secure-mtls':
            # mTLS requires client certificate in browser
            cert_p12_path = config['client_cert'].replace('.crt', '.p12')
            print(f"  🌐 NiFi UI: {config['nifi_url'].replace('/nifi-api', '/nifi')}")
            print(f"  📊 Registry UI: {config['registry_url'].replace('/nifi-registry-api', '/nifi-registry')}")
            print(f"  🔐 Authentication: Client certificate required (ADVANCED)")
            print(f"")
            print(f"  💡 TIP: For easier setup, try:")
            print(f"      make playground NIPYAPI_AUTH_MODE=single-user  (recommended - simple setup)")
            print(f"      make playground NIPYAPI_AUTH_MODE=secure-ldap  (more complex security)")
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
        
        print(f"  🔗 Registry Client: {PLAYGROUND_REGISTRY_CLIENT}")
        print(f"  📦 Sample Bucket: {PLAYGROUND_BUCKET}")
        print(f"  🔄 Sample Flow: {PLAYGROUND_FLOW}")
        print("\n💡 Ready for experimentation! Run 'make down' when finished.")
        
    except Exception as e:
        log.error("❌ Playground setup failed: %s", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
