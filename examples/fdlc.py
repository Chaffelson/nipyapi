"""
Flow Development Lifecycle (FDLC) Example using NiFi Registry

This example demonstrates the complete iterative workflow for enterprise NiFi development
done using NiFi Registry for version control.

NOTE: This example uses NiFi Registry as the persistence provider. Modern NiFi
deployments increasingly use Git-based persistence providers for version control.
This Registry-based approach remains valuable for understanding core concepts.

Prerequisites:
- Docker and Docker Compose installed
- nipyapi project with make commands available
- This script should be run from the nipyapi project root

The FDLC workflow demonstrates:
1. DEV: Create flow and establish version control
2. → PROD: Export and import flow to production 
3. ← DEV: Make changes and commit new version
4. → PROD: Promote changes and update production

This iterative cycle is the heart of enterprise NiFi development.
"""

import logging
import subprocess
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# Import nipyapi - required for all operations
import nipyapi

# Two-environment setup for realistic FDLC
DEV_PROFILE = 'single-user'   # Development: rapid iteration
PROD_PROFILE = 'secure-ldap'  # Production: enterprise security

# Environment endpoints 
DEV_NIFI_API = 'https://localhost:9443/nifi-api'
DEV_REGISTRY_API = 'http://localhost:18080/nifi-registry-api'
PROD_NIFI_API = 'https://localhost:9444/nifi-api'  
PROD_REGISTRY_API = 'https://localhost:18444/nifi-registry-api'  # HTTPS for secure-ldap

# Component names for the demo
FLOW_NAMES = {
    'process_group': 'fdlc_demo_flow',
    'processor': 'fdlc_generator',
    'dev_registry_client': 'dev_registry_client',
    'prod_registry_client': 'prod_registry_client',
    'dev_bucket': 'development', 
    'prod_bucket': 'production',
    'versioned_flow': 'demo_data_pipeline'
}

def check_prerequisites():
    """Quick prerequisite check"""
    if not Path('Makefile').exists():
        raise RuntimeError("Run from nipyapi project root: cd /path/to/nipyapi && python examples/fdlc.py")
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise RuntimeError("Docker not available")

def run_make_command(command):
    """Helper to run make commands"""
    log.info(f"Running: make {command}")
    result = subprocess.run(['make'] + command.split(), capture_output=True, text=True)
    if result.returncode != 0:
        log.error(f"Command failed: {result.stderr}")
        raise RuntimeError(f"Make command failed: make {command}")
    return result

def connect_to_dev():
    """Switch to development environment"""
    log.info("→ Connecting to DEVELOPMENT environment") 
    # Configure SSL for self-signed certificates  
    nipyapi.config.nifi_config.ssl_ca_cert = 'resources/certs/ca/ca.crt'
    nipyapi.config.registry_config.ssl_ca_cert = 'resources/certs/ca/ca.crt'
    nipyapi.utils.set_endpoint(DEV_NIFI_API, True, True, 'einstein', 'password1234')
    nipyapi.utils.set_endpoint(DEV_REGISTRY_API, True, True, 'einstein', 'password1234')  # Single-user profile uses basic auth

def connect_to_prod():
    """Switch to production environment"""
    log.info("→ Connecting to PRODUCTION environment") 
    # Configure SSL for self-signed certificates
    nipyapi.config.nifi_config.ssl_ca_cert = 'resources/certs/ca/ca.crt'
    nipyapi.config.registry_config.ssl_ca_cert = 'resources/certs/ca/ca.crt'
    nipyapi.utils.set_endpoint(PROD_NIFI_API, True, True, 'einstein', 'password')
    nipyapi.utils.set_endpoint(PROD_REGISTRY_API, True, True, 'einstein', 'password')  # secure-ldap Registry also uses basic auth

def step_1_setup_environments():
    """
    Step 1: Quick setup of both development and production environments
    
    Gets both environments running so we can focus on the FDLC workflow.
    """
    print("""
=== STEP 1: Environment Setup ===

Setting up TWO environments for FDLC demonstration:
• DEVELOPMENT (single-user): https://localhost:9443 + http://localhost:18080  
• PRODUCTION (secure-ldap): https://localhost:9444 + https://localhost:18444

This gives us realistic environment separation for demonstrating promotion workflows.
    """)
    
    check_prerequisites()
    
    # Clean slate
    log.info("Cleaning up any existing containers...")
    run_make_command('down')
    
    # Generate certificates
    log.info("Generating certificates...")
    run_make_command('certs')
    
    # Start both environments
    log.info("Starting development environment...")
    run_make_command(f'up NIPYAPI_AUTH_MODE={DEV_PROFILE}')
    run_make_command(f'wait-ready NIPYAPI_AUTH_MODE={DEV_PROFILE}')
    
    log.info("Starting production environment...")
    run_make_command(f'up NIPYAPI_AUTH_MODE={PROD_PROFILE}')
    run_make_command(f'wait-ready NIPYAPI_AUTH_MODE={PROD_PROFILE}')
    
    # nipyapi already imported at module level
    
    print("""
✅ Both environments ready!

DEVELOPMENT: https://localhost:9443/nifi (einstein/password1234)
PRODUCTION:  https://localhost:9444/nifi (einstein/password)

Next: step_2_create_dev_flow() - Create flow in development
    """)

def step_2_create_dev_flow():
    """
    Step 2: Create and prepare flow in development environment
    
    Creates a simple flow and establishes version control - the foundation
    for the promotion workflow.
    """
    print("""
=== STEP 2: Create Development Flow ===

Creating a simple data processing flow in DEVELOPMENT environment
and establishing version control foundation.
    """)
    
    connect_to_dev()
    
    # Clean up any existing components
    log.info("Cleaning up existing components...")
    try:
        existing_pg = nipyapi.canvas.get_process_group(FLOW_NAMES['process_group'])
        if existing_pg:
            nipyapi.canvas.delete_process_group(existing_pg, force=True)
    except ValueError:
        pass
    
    try:
        existing_client = nipyapi.versioning.get_registry_client(FLOW_NAMES['dev_registry_client'])
        if existing_client:
            nipyapi.versioning.delete_registry_client(existing_client)
    except ValueError:
        pass
    
    try:
        existing_bucket = nipyapi.versioning.get_registry_bucket(FLOW_NAMES['dev_bucket'])
        if existing_bucket:
            nipyapi.versioning.delete_registry_bucket(existing_bucket)
    except ValueError:
        pass
    
    # Create Registry client for version control
    log.info("Creating Registry client...")
    nipyapi.versioning.create_registry_client(
        name=FLOW_NAMES['dev_registry_client'],
        uri='http://registry-single:18080',  # Matches conftest.py working configuration
        description='Development Registry Client'
    )
    
    # Create Registry bucket
    log.info("Creating development bucket...")
    nipyapi.versioning.create_registry_bucket(FLOW_NAMES['dev_bucket'])
    
    # Create the flow
    log.info("Creating demo flow...")
    root_pg = nipyapi.canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id')
    
    process_group = nipyapi.canvas.create_process_group(
        parent_pg=root_pg,
        new_pg_name=FLOW_NAMES['process_group'],
        location=(400.0, 400.0)
    )
    
    nipyapi.canvas.create_processor(
        parent_pg=process_group,
        processor=nipyapi.canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 400.0),
        name=FLOW_NAMES['processor'],
        config=nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period='5s',
            auto_terminated_relationships=['success']
        )
    )
    
    print("""
✅ Development flow created!

In DEV NiFi UI (https://localhost:9443/nifi):
• Process Group: fdlc_demo_flow
• Processor: GenerateFlowFile (5-second interval)
• Status: Not yet under version control

Next: step_3_version_dev_flow() - Put flow under version control
    """)

def step_3_version_dev_flow():
    """
    Step 3: Put development flow under version control
    
    Establishes version control for the flow, creating version 1.
    This is the foundation for promotion workflows.
    """
    print("""
=== STEP 3: Establish Version Control ===

Putting the development flow under version control.
This creates version 1 and enables promotion workflows.
    """)
    
    connect_to_dev()
    
    # Get components
    process_group = nipyapi.canvas.get_process_group(FLOW_NAMES['process_group'])
    registry_client = nipyapi.versioning.get_registry_client(FLOW_NAMES['dev_registry_client'])
    bucket = nipyapi.versioning.get_registry_bucket(FLOW_NAMES['dev_bucket'])
    
    # Save to version control
    log.info("Saving flow to version control...")
    version_info = nipyapi.versioning.save_flow_ver(
        process_group=process_group,
        registry_client=registry_client,
        bucket=bucket,
        flow_name=FLOW_NAMES['versioned_flow'],
        desc='Demo data pipeline for FDLC demonstration',
        comment='Initial version - basic data generation flow'
    )
    
    version = version_info.version_control_information.version
    log.info(f"Flow saved as version {version}")
    
    print(f"""
✅ Flow under version control!

• Flow name: {FLOW_NAMES['versioned_flow']}
• Version: {version}
• Status: Development flow shows green ✓ (up-to-date)

DEV Registry UI (http://localhost:18080/nifi-registry):
• Bucket: {FLOW_NAMES['dev_bucket']} 
• Flow: {FLOW_NAMES['versioned_flow']} (version {version})

Next: step_4_promote_to_prod() - Export and promote to production
    """)

def step_4_promote_to_prod():
    """
    Step 4: Promote flow to production
    
    Export from dev Registry and import into prod Registry.
    This simulates the promotion through CI/CD pipeline.
    """
    print("""
=== STEP 4: Promote to Production ===

Exporting flow from DEVELOPMENT and importing into PRODUCTION.
This simulates promoting through a CI/CD pipeline between environments.
    """)
    
    # Export from development
    connect_to_dev()
    log.info("Exporting flow from development...")
    
    dev_bucket = nipyapi.versioning.get_registry_bucket(FLOW_NAMES['dev_bucket'])
    dev_flow = nipyapi.versioning.get_flow_in_bucket(
        dev_bucket.identifier, 
        identifier=FLOW_NAMES['versioned_flow']
    )
    
    flow_export = nipyapi.versioning.export_flow_version(
        bucket_id=dev_bucket.identifier,
        flow_id=dev_flow.identifier,
        mode='yaml'
    )
    
    # Import to production  
    connect_to_prod()
    log.info("Setting up production Registry...")
    
    # Bootstrap Registry security policies (creates proxy user)
    log.info("Bootstrapping production Registry security...")
    nipyapi.security.bootstrap_security_policies(
        service='registry', 
        nifi_proxy_identity='C=US, O=NiPyAPI, CN=nifi'
    )
    
    # Clean up existing prod components
    try:
        existing_bucket = nipyapi.versioning.get_registry_bucket(FLOW_NAMES['prod_bucket'])
        if existing_bucket:
            nipyapi.versioning.delete_registry_bucket(existing_bucket)
    except ValueError:
        pass
    
    # Create production bucket and import
    prod_bucket = nipyapi.versioning.create_registry_bucket(FLOW_NAMES['prod_bucket'])
    
    log.info("Importing flow into production...")
    imported_flow = nipyapi.versioning.import_flow_version(
        bucket_id=prod_bucket.identifier,
        encoded_flow=flow_export,
        flow_name=FLOW_NAMES['versioned_flow']
    )
    
    print(f"""
✅ Flow promoted to production!

PRODUCTION Registry (https://localhost:18444/nifi-registry):
• Bucket: {FLOW_NAMES['prod_bucket']}
• Flow: {FLOW_NAMES['versioned_flow']} (version 1)
• Status: Available for deployment

This represents the flow moving through your CI/CD pipeline:
DEV Registry → CI/CD → PROD Registry

Next: step_5_deploy_to_prod_nifi() - Deploy flow in production NiFi
    """)

def step_5_deploy_to_prod_nifi():
    """
    Step 5: Deploy flow in production NiFi
    
    Create Registry client in prod NiFi and deploy the versioned flow.
    This makes the flow live in production.
    """
    print("""
=== STEP 5: Deploy to Production NiFi ===

Creating production Registry client and deploying the versioned flow.
This makes the flow live in the production environment.
    """)
    
    connect_to_prod()
    
    # Bootstrap NiFi security policies (grants user permissions)
    log.info("Bootstrapping production NiFi security...")
    nipyapi.security.bootstrap_security_policies(service='nifi')
    
    # Clean up existing prod registry client
    try:
        existing_client = nipyapi.versioning.get_registry_client(FLOW_NAMES['prod_registry_client'])
        if existing_client:
            nipyapi.versioning.delete_registry_client(existing_client)
    except ValueError:
        pass
    
    # Create production Registry client
    log.info("Creating production Registry client...")
    prod_registry_client = nipyapi.versioning.create_registry_client(
        name=FLOW_NAMES['prod_registry_client'],
        uri='https://registry-ldap:18443',  # Matches conftest.py working configuration for secure-ldap
        description='Production Registry Client'
    )
    
    # Deploy the versioned flow
    log.info("Deploying versioned flow to production...")
    prod_bucket = nipyapi.versioning.get_registry_bucket(FLOW_NAMES['prod_bucket'])
    prod_flow = nipyapi.versioning.get_flow_in_bucket(
        prod_bucket.identifier,
        identifier=FLOW_NAMES['versioned_flow']
    )
    
    deployed_pg = nipyapi.versioning.deploy_flow_version(
        parent_id=nipyapi.canvas.get_root_pg_id(),
        location=(400.0, 400.0),
        bucket_id=prod_bucket.identifier,
        flow_id=prod_flow.identifier,
        reg_client_id=prod_registry_client.id,
        version=None  # Deploy latest version
    )
    
    print(f"""
✅ Flow deployed to production!

PRODUCTION NiFi (https://localhost:9444/nifi):
• Process Group: {FLOW_NAMES['versioned_flow']} 
• Status: Green ✓ (deployed from version control)
• Flow is now live and processing data in production

The flow has completed its journey:
DEV (created) → DEV Registry → PROD Registry → PROD NiFi (live)

Next: step_6_make_dev_changes() - Demonstrate change management
    """)

def step_6_make_dev_changes():
    """
    Step 6: Make changes in development
    
    Modify the development flow to simulate ongoing development.
    This demonstrates the iterative nature of flow development.
    """
    print("""
=== STEP 6: Make Development Changes ===

Making changes to the development flow to simulate ongoing development.
This shows the iterative cycle: develop → version → promote.
    """)
    
    connect_to_dev()
    
    # Modify the processor
    log.info("Making changes to development flow...")
    processor = nipyapi.canvas.get_processor(FLOW_NAMES['processor'])
    
    nipyapi.canvas.update_processor(
        processor=processor,
        update=nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period='10s'  # Changed from 5s to 10s
        )
    )
    
    print("""
✅ Development changes made!

DEV NiFi UI (https://localhost:9443/nifi):
• Process Group now shows orange star ★ (uncommitted changes)
• Processor scheduling changed: 5s → 10s
• Status: Local changes not yet versioned

This represents typical development iteration:
• Developer modifies flow configuration
• Changes are local until committed to version control
• Production remains unchanged

Next: step_7_version_changes() - Commit changes as version 2
    """)

def step_7_version_changes():
    """
    Step 7: Version the changes
    
    Commit the development changes to create version 2.
    This establishes the new version for promotion.
    """
    print("""
=== STEP 7: Version the Changes ===

Committing development changes to create version 2.
This establishes the new version for promotion to production.
    """)
    
    connect_to_dev()
    
    # Get components for versioning
    process_group = nipyapi.canvas.get_process_group(FLOW_NAMES['process_group'])
    registry_client = nipyapi.versioning.get_registry_client(FLOW_NAMES['dev_registry_client'])
    dev_bucket = nipyapi.versioning.get_registry_bucket(FLOW_NAMES['dev_bucket'])
    dev_flow = nipyapi.versioning.get_flow_in_bucket(
        dev_bucket.identifier,
        identifier=FLOW_NAMES['versioned_flow']
    )
    
    # Commit changes
    log.info("Committing changes to version control...")
    version_info = nipyapi.versioning.save_flow_ver(
        process_group=process_group,
        registry_client=registry_client,
        bucket=dev_bucket,
        flow_id=dev_flow.identifier,
        comment='Performance tuning - reduced generation frequency from 5s to 10s'
    )
    
    version = version_info.version_control_information.version
    log.info(f"Changes committed as version {version}")
    
    print(f"""
✅ Changes versioned!

DEV NiFi UI:
• Process Group shows green ✓ (changes committed)
• Version: {version}

DEV Registry UI:
• Flow: {FLOW_NAMES['versioned_flow']} 
• Versions: 1 (initial), {version} (performance tuning)
• Latest comment: "Performance tuning - reduced generation frequency"

Ready for promotion to production!

Next: step_8_promote_changes() - Promote version 2 to production
    """)

def step_8_promote_changes():
    """
    Step 8: Promote changes to production
    
    Export version 2 and import into production, then update production deployment.
    This completes the full development lifecycle.
    """
    print("""
=== STEP 8: Promote Changes to Production ===

Promoting version 2 to production and updating the live deployment.
This completes the full development lifecycle demonstration.
    """)
    
    # Export version 2 from development
    connect_to_dev()
    log.info("Exporting version 2 from development...")
    
    dev_bucket = nipyapi.versioning.get_registry_bucket(FLOW_NAMES['dev_bucket'])
    dev_flow = nipyapi.versioning.get_flow_in_bucket(
        dev_bucket.identifier,
        identifier=FLOW_NAMES['versioned_flow']
    )
    
    flow_export_v2 = nipyapi.versioning.export_flow_version(
        bucket_id=dev_bucket.identifier,
        flow_id=dev_flow.identifier,
        mode='yaml'
    )
    
    # Import to production
    connect_to_prod()
    log.info("Importing version 2 to production...")
    
    prod_bucket = nipyapi.versioning.get_registry_bucket(FLOW_NAMES['prod_bucket'])
    prod_flow = nipyapi.versioning.get_flow_in_bucket(
        prod_bucket.identifier,
        identifier=FLOW_NAMES['versioned_flow']
    )
    
    nipyapi.versioning.import_flow_version(
        bucket_id=prod_bucket.identifier,
        encoded_flow=flow_export_v2,
        flow_id=prod_flow.identifier
    )
    
    print(f"""
✅ FDLC cycle completed!

PRODUCTION Status:
• Registry: Version 2 available
• NiFi: Shows red up-arrow ⬆ (new version available)

The complete enterprise development lifecycle:

1. DEV: Created flow → versioned (v1)
2. → PROD: Promoted v1 → deployed to production  
3. ← DEV: Made changes → versioned (v2)
4. → PROD: Promoted v2 → ready for deployment update

Production team can now:
• Review version 2 changes
• Update production deployment 
• Validate the changes in production

This demonstrates the complete iterative development cycle
that's central to enterprise NiFi workflows!

Final step: step_9_cleanup() - Clean up environments
    """)

def step_9_cleanup():
    """
    Step 9: Clean up demonstration environments
    """
    print("""
=== STEP 9: Cleanup ===

Cleaning up demonstration environments.
    """)
    
    log.info("Stopping all containers...")
    run_make_command('down')
    
    print("""
✅ FDLC demonstration completed!

You've seen the complete enterprise flow development lifecycle:

🔄 **The FDLC Rhythm:**
1. **Develop** flows in development environment
2. **Version** changes using Registry  
3. **Promote** through CI/CD pipeline
4. **Deploy** to production environment
5. **Iterate** - make changes and repeat

🏢 **Enterprise Value:**
• Controlled promotion between environments
• Version history and rollback capabilities  
• Audit trails for all changes
• Separation of development and production

📝 **Registry vs Git:**
This demo used NiFi Registry for version control.
Modern deployments increasingly use Git-based persistence
providers as an alternative approach.

Thank you for exploring the Flow Development Lifecycle!
    """)

# Interactive mode
if __name__ == '__main__':
    import sys
    
    print("""
🚀 Flow Development Lifecycle (FDLC) Demo
========================================

This demonstration shows the ITERATIVE WORKFLOW of enterprise NiFi development:
the back-and-forth promotion process between development and production.

🔄 THE WORKFLOW:
DEV: Create → Version → → PROD: Import → Deploy
                       ↗               ↘
DEV: Change → Version ←  ← ← ← ← ←  Update

Two environments:
• DEVELOPMENT: single-user (rapid iteration)  
• PRODUCTION: secure-ldap (enterprise security)

Steps:
1. step_1_setup_environments()     # Quick setup of both environments
2. step_2_create_dev_flow()        # Create flow in development  
3. step_3_version_dev_flow()       # Put under version control (v1)
4. step_4_promote_to_prod()        # Export dev → import prod  
5. step_5_deploy_to_prod_nifi()    # Deploy in production NiFi
6. step_6_make_dev_changes()       # Make changes in development
7. step_7_version_changes()        # Commit changes (v2)
8. step_8_promote_changes()        # Promote v2 to production
9. step_9_cleanup()                # Clean up
    """)
    
    # Check if user wants auto-run mode
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        print("\n🚀 Running complete FDLC demo automatically...\n")
        try:
            step_1_setup_environments()
            step_2_create_dev_flow()
            step_3_version_dev_flow()
            step_4_promote_to_prod()
            step_5_deploy_to_prod_nifi()
            step_6_make_dev_changes()
            step_7_version_changes()
            step_8_promote_changes()
            step_9_cleanup()
            print("\n🎉 Complete FDLC demo finished!")
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            print("You can run step_9_cleanup() to clean up if needed.")
            sys.exit(1)
    else:
        print("""
📖 HOW TO RUN:

Option 1 - Interactive Mode (Recommended):
    python -i examples/fdlc.py
    >>> step_1_setup_environments()
    >>> step_2_create_dev_flow()
    >>> # ... continue with remaining steps
    >>> exit()  # or Ctrl+D to exit when done

Option 2 - Auto Run (Complete Demo):
    python examples/fdlc.py --auto

Option 3 - Import Mode:
    python
    >>> exec(open('examples/fdlc.py').read())
    >>> step_1_setup_environments()
    >>> exit()  # or Ctrl+D to exit when done

💡 TIP: Use interactive mode to go step-by-step and see results!
💡 TIP: Run step_9_cleanup() before exiting to stop Docker containers
💡 TIP: Most steps require infrastructure (step 1) but can be run individually for testing

To start interactively: python -i examples/fdlc.py
        """)