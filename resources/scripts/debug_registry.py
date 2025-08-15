#!/usr/bin/env python
import os
import json
import sys
import nipyapi
import socket
import ssl as _ssl
import time


def getenv(name: str, default: str | None = None) -> str | None:
    val = os.getenv(name)
    return val if val is not None else default


def main() -> int:
    nifi_url = getenv('NIFI_API_ENDPOINT', 'https://localhost:9443/nifi-api')
    ca_path = getenv('TLS_CA_CERT_PATH') or os.path.join(os.getcwd(), 'resources', 'certs', 'client', 'ca.pem')
    nifi_user = getenv('NIFI_USERNAME', 'einstein')
    nifi_pass = getenv('NIFI_PASSWORD', 'password1234')
    profile = (getenv('PROFILE', 'single-user') or 'single-user').strip()
    reg_user = getenv('REGISTRY_USERNAME', 'einstein')
    reg_pass = getenv('REGISTRY_PASSWORD', 'password')
    cert_password = getenv('CERT_PASSWORD', 'changeit')
    nifi_proxy_identity = getenv('NIFI_PROXY_IDENTITY')

    # Configure TLS verification
    nipyapi.config.nifi_config.verify_ssl = True
    nipyapi.config.nifi_config.ssl_ca_cert = ca_path

    print(f"Using NiFi at {nifi_url}")
    print(f"Using CA at {ca_path}")

    # Authenticate to NiFi using token
    try:
        nipyapi.utils.set_endpoint(
            nifi_url,
            ssl=True,
            login=True,
            username=nifi_user,
            password=nifi_pass,
        )
        print("Token login OK")
        # Bootstrap NiFi policies for current authenticated user (initial admin)
        try:
            nipyapi.security.bootstrap_security_policies(service='nifi')
            print("nifi_bootstrap_policies=OK")
        except Exception as be:
            print("nifi_bootstrap_policies=ERROR", str(be).split('\n')[0])
    except Exception as exc:
        print(f"LOGIN ERROR: {exc}")
        return 2

    # Basic connectivity check: root PG ID
    try:
        root_pg_id = nipyapi.canvas.get_root_pg_id()
        print(f"root_pg_id={root_pg_id}")
    except Exception as exc:
        print(f"ROOT_PG_ERROR: {exc}")
        return 3

    # Ensure a Flow Registry Client exists and matches the profile
    def _desired_registry_url(prof: str) -> str:
        # Base URL without webapp context path
        if prof == 'single-user':
            return 'http://registry-single:18080'
        if prof == 'secure-ldap':
            return 'https://registry-ldap:18443'
        if prof == 'secure-mtls':
            return 'https://registry-mtls:18443'
        return 'http://registry-single:18080'

    desired_url = _desired_registry_url(profile)
    client_name = 'nipyapi_test_reg_client'
    try:
        existing = nipyapi.versioning.get_registry_client(client_name, 'name')
        if existing:
            # Replace if URL differs
            comp = existing.component
            current_url = None
            if hasattr(comp, 'properties') and comp.properties:
                current_url = comp.properties.get('url')
            if current_url != desired_url:
                nipyapi.versioning.delete_registry_client(existing)
                existing = None
        if not existing:
            created = nipyapi.versioning.create_registry_client(
                name=client_name,
                uri=desired_url,
                description=f'{desired_url}',
            )
            print(f"created_registry_client={created.id}")
        else:
            created = existing
            print(f"using_existing_registry_client={created.id}")
    except Exception as exc:
        print(f"REG_CLIENT_ERROR: {exc}")
        return 4

    # Prepare SSL Context Service (applied after policies are in place)
    ssl_ctx = None
    if profile in ('secure-ldap', 'secure-mtls'):
        try:
            parent_pg = nipyapi.canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id')
            ssl_name = 'nipyapi_test_ssl_controller'
            ssl_ctx = nipyapi.canvas.get_controller(ssl_name, 'name')
            if ssl_ctx is None:
                ssl_ctx = nipyapi.security.create_ssl_context_controller_service(
                    parent_pg=parent_pg,
                    name=ssl_name,
                    keystore_file='/certs/nifi/keystore.p12',
                    keystore_password=cert_password,
                    truststore_file='/certs/truststore/truststore.p12',
                    truststore_password=cert_password,
                    keystore_type='PKCS12', truststore_type='PKCS12',
                    ssl_service_type='org.apache.nifi.ssl.StandardSSLContextService'
                )
            nipyapi.canvas.schedule_controller(ssl_ctx, scheduled=True, refresh=True)
        except Exception as e:
            print('ssl_context_prepare=ERROR', str(e).split('\n')[0])

    # List Flow Registry Clients
    try:
        clients_entity = nipyapi.versioning.list_registry_clients()
        clients = getattr(clients_entity, 'registries', []) or []
        print(f"registry_clients_count={len(clients)}")
        for c in clients:
            comp = c.component
            # Attempt to fetch latest details for properties/validation
            detailed = nipyapi.nifi.ControllerApi().get_flow_registry_client(c.id)
            dcomp = detailed.component
            # Coerce nested DTOs to dicts for JSON output
            descriptors = getattr(dcomp, 'descriptors', None) or {}
            if isinstance(descriptors, dict):
                descriptors = {k: (v.to_dict() if hasattr(v, 'to_dict') else str(v))
                               for k, v in descriptors.items()}
            properties = getattr(dcomp, 'properties', None) or {}
            payload = {
                'id': c.id,
                'name': getattr(comp, 'name', None),
                'uri': getattr(dcomp, 'uri', getattr(comp, 'uri', None)),
                'description': getattr(comp, 'description', None),
                'validationStatus': getattr(dcomp, 'validation_status', None),
                'validationErrors': getattr(dcomp, 'validation_errors', None),
                'properties': properties,
                'descriptors': descriptors,
            }
            print(json.dumps(payload, indent=2))
    except Exception as exc:
        print(f"LIST_CLIENTS_ERROR: {exc}")
        return 4

    # Connect to Registry API and bootstrap baseline policies for current user
    try:
        if profile == 'single-user':
            reg_api = 'http://localhost:18080/nifi-registry-api'
            ssl_flag = False
        elif profile == 'secure-ldap':
            reg_api = 'https://localhost:18444/nifi-registry-api'
            ssl_flag = True
        else:
            reg_api = 'https://localhost:18445/nifi-registry-api'
            ssl_flag = True

        if ssl_flag:
            nipyapi.config.registry_config.verify_ssl = True
            nipyapi.config.registry_config.ssl_ca_cert = ca_path
        nipyapi.utils.set_endpoint(reg_api, ssl=ssl_flag, login=True, username=reg_user, password=reg_pass)
        # Explicit version probe to validate auth/TLS
        try:
            ver = nipyapi.registry.AboutApi().get_version()
            print("registry_version=", ver)
        except Exception as ve:
            print("registry_version_probe=ERROR", str(ve).split('\n')[0])
        try:
            kw = {'service': 'registry'}
            if nifi_proxy_identity:
                kw['nifi_proxy_identity'] = nifi_proxy_identity
            nipyapi.security.bootstrap_security_policies(**kw)
            print("registry_bootstrap_policies=OK")
        except Exception as be:
            print("registry_bootstrap_policies=ERROR", str(be).split('\n')[0])
        # Inspect registry users and /proxy policies
        try:
            users = nipyapi.security.list_service_users('registry') or []
            print('registry_users=', [getattr(u, 'identity', None) for u in users])
        except Exception as ue:
            print('registry_list_users=ERROR', str(ue).split('\n')[0])
        # Ensure LDAP user has read/write on all existing buckets (helps fix UI errors on older PGs)
        try:
            reg_u = nipyapi.security.create_service_user(identity=reg_user, service='registry', strict=False)
            for b in (nipyapi.versioning.list_registry_buckets() or []):
                for action in ('read','write'):
                    pol = nipyapi.security.get_access_policy_for_resource(
                        resource=f'/buckets/{b.identifier}', action=action, service='registry', auto_create=True
                    )
                    nipyapi.security.add_user_to_access_policy(user=reg_u, policy=pol, service='registry', strict=False)
            print('registry_bucket_policies_hardened=OK')
        except Exception as be:
            print('registry_bucket_policies_hardened=ERROR', str(be).split('\n')[0])
        # Ensure both DN representations are present in /proxy (ordering differences)
        try:
            dn_variants = set()
            if nifi_proxy_identity:
                dn_variants.add(nifi_proxy_identity.strip())
                parts = [p.strip() for p in nifi_proxy_identity.split(',') if '=' in p]
                keys = [p.split('=')[0].strip().upper() for p in parts]
                if set(keys) == {'CN','O','C'}:
                    # CN-first
                    cn_first = f"CN={ [p for p in parts if p.strip().upper().startswith('CN=')][0].split('=')[1].strip() }, O={ [p for p in parts if p.strip().upper().startswith('O=')][0].split('=')[1].strip() }, C={ [p for p in parts if p.strip().upper().startswith('C=')][0].split('=')[1].strip() }"
                    # C-first
                    c_first = f"C={ [p for p in parts if p.strip().upper().startswith('C=')][0].split('=')[1].strip() }, O={ [p for p in parts if p.strip().upper().startswith('O=')][0].split('=')[1].strip() }, CN={ [p for p in parts if p.strip().upper().startswith('CN=')][0].split('=')[1].strip() }"
                    dn_variants.update({cn_first, c_first})
            for dn in dn_variants:
                u = nipyapi.security.create_service_user(identity=dn, service='registry', strict=False)
                for action in ('read','write','delete'):
                    pol = nipyapi.security.get_access_policy_for_resource(resource='/proxy', action=action, service='registry', auto_create=True)
                    nipyapi.security.add_user_to_access_policy(user=u, policy=pol, service='registry', strict=False)
                # Also grant global bucket management required for NiFi proxy
                for action in ('read','write'):
                    polb = nipyapi.security.get_access_policy_for_resource(resource='/buckets', action=action, service='registry', auto_create=True)
                    nipyapi.security.add_user_to_access_policy(user=u, policy=polb, service='registry', strict=False)
            print('proxy_dn_variants_applied=', list(dn_variants))
        except Exception as e:
            print('proxy_dn_variants_error=', str(e).split('\n')[0])
        try:
            from nipyapi.security import get_access_policy_for_resource
            for action in ('read', 'write', 'delete'):
                pol = get_access_policy_for_resource('/proxy', action, service='registry', auto_create=False)
                if pol is None:
                    print(f'proxy_policy_{action}=None')
                else:
                    user_identities = [u.identity for u in (pol.users or [])]
                    print(f'proxy_policy_{action}_users=', user_identities)
        except Exception as pe:
            print('registry_proxy_policies=ERROR', str(pe).split('\n')[0])
    except Exception as exc:
        print(f"registry_connect_error: {exc}")

    # Attach SSL Context to Registry Client if created and context available
    try:
        if ssl_ctx is not None:
            target_client = created if 'created' in locals() else existing
            reg_client = nipyapi.nifi.ControllerApi().get_flow_registry_client(target_client.id)
            comp = reg_client.component.to_dict()
            props = comp.get('properties') or {}
            props['url'] = _desired_registry_url(profile)
            props['ssl-context-service'] = ssl_ctx.id
            comp['properties'] = props
            _ = nipyapi.nifi.ControllerApi().update_flow_registry_client(
                id=reg_client.id,
                body={'component': comp, 'revision': {'version': reg_client.revision.version}}
            )
            print('registry_client_ssl_context=OK')
        else:
            print('registry_client_ssl_context=SKIP (no ssl context)')
    except Exception as e:
        print('registry_client_ssl_context=ERROR', str(e).split('\n')[0])

    # Create a Registry Bucket via authenticated Registry API (LDAP user)
    bucket_name = 'nipyapi_test_bucket'
    bucket = None
    try:
        try:
            bucket = nipyapi.versioning.create_registry_bucket(bucket_name)
            print('registry_bucket_create=OK', bucket.identifier)
        except ValueError as ve:
            if 'already exists' in str(ve):
                buckets = nipyapi.versioning.list_registry_buckets()
                for b in buckets:
                    if b.name == bucket_name:
                        bucket = b
                        print('registry_bucket_reuse=OK', bucket.identifier)
                        break
        # Ensure LDAP user has read/write on this bucket
        if bucket is not None:
            reg_u = nipyapi.security.create_service_user(identity=reg_user, service='registry', strict=False)
            # Global list buckets (optional, helps NiFi list via Flow API)
            pol_global = nipyapi.security.get_access_policy_for_resource(
                resource='/buckets', action='read', service='registry', auto_create=True
            )
            nipyapi.security.add_user_to_access_policy(user=reg_u, policy=pol_global, service='registry', strict=False)
            # Bucket-specific read/write/delete
            for action in ('read', 'write', 'delete'):
                pol = nipyapi.security.get_access_policy_for_resource(
                    resource=f'/buckets/{bucket.identifier}', action=action,
                    service='registry', auto_create=True
                )
                nipyapi.security.add_user_to_access_policy(user=reg_u, policy=pol, service='registry', strict=False)
            # Show effective users on bucket policies
            try:
                for action in ('read','write','delete'):
                    pol = nipyapi.security.get_access_policy_for_resource(
                        resource=f'/buckets/{bucket.identifier}', action=action, service='registry', auto_create=False
                    )
                    users = [u.identity for u in (pol.users or [])] if pol else []
                    print(f'registry_bucket_{action}_users=', users)
            except Exception as pe:
                print('registry_bucket_policy_dump=ERROR', str(pe).split('\n')[0])
    except Exception as e:
        print('registry_bucket_setup_error=', str(e).split('\n')[0])

    # Create a simple Process Group in NiFi
    pg = None
    try:
        root = nipyapi.canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id')
        name = 'nipyapi_test_pg'
        pg = nipyapi.canvas.create_process_group(root, name, (400.0, 400.0))
        print('nifi_pg_create=OK', pg.id)
        # Immediately fetch Version Control Info (should be empty/None if not under VC yet)
        try:
            vci = nipyapi.nifi.VersionsApi().get_version_information(pg.id)
            print('nifi_vci_initial=', vci and vci.version_control_information)
        except Exception as e:
            print('nifi_vci_initial=ERROR', str(e).split('\n')[0])
    except Exception as e:
        print('nifi_pg_create=ERROR', str(e).split('\n')[0])

    # Use NiFi Flow API to list buckets via the Registry Client (proxies LDAP identity)
    try:
        if 'created' in locals():
            client_id = created.id
        else:
            client_id = existing.id
        buckets = nipyapi.nifi.FlowApi().get_buckets(client_id)
        names = [getattr(b, 'name', None) for b in getattr(buckets, 'buckets', [])]
        print('nifi_flowapi_get_buckets=OK', names)
    except Exception as e:
        print('nifi_flowapi_get_buckets=ERROR', str(e).split('\n')[0])

    # Attempt a save to flow registry (end-to-end) and then retrieve
    flow_id = None
    try:
        if pg is not None and bucket is not None:
            flow_name = f"nipyapi_test_flow_{int(time.time())}"
            try:
                info = nipyapi.versioning.save_flow_ver(
                    process_group=pg,
                    registry_client=(created if 'created' in locals() else existing),
                    bucket=bucket,
                    flow_name=flow_name,
                    comment='debug save',
                    desc='debug save'
                )
            except ValueError as ve:
                if 'already exists' in str(ve):
                    flow_name = flow_name + '_2'
                    info = nipyapi.versioning.save_flow_ver(
                        process_group=pg,
                        registry_client=(created if 'created' in locals() else existing),
                        bucket=bucket,
                        flow_name=flow_name,
                        comment='debug save',
                        desc='debug save'
                    )
                else:
                    raise
            flow_id = info.version_control_information.flow_id
            print('nifi_save_flow_ver=OK', flow_id)
    except Exception as e:
        print('nifi_save_flow_ver=ERROR', str(e).split('\n')[0])

    # Query flows in bucket via NiFi Flow API (proxies LDAP identity)
    try:
        if 'created' in locals():
            client_id = created.id
        else:
            client_id = existing.id
        flows = nipyapi.nifi.FlowApi().get_flows(registry_id=client_id, bucket_id=bucket.identifier)
        flow_names = [getattr(f, 'name', None) for f in getattr(flows, 'flows', [])]
        print('nifi_flowapi_get_flows=OK', flow_names)
    except Exception as e:
        print('nifi_flowapi_get_flows=ERROR', str(e).split('\n')[0])

    # Query versions via NiFi Flow API
    try:
        if 'created' in locals() and flow_id:
            client_id = created.id
            vers = nipyapi.nifi.FlowApi().get_versions(registry_id=client_id, bucket_id=bucket.identifier, flow_id=flow_id)
            vers_list = [getattr(v, 'version', None) for v in getattr(vers, 'versions', [])]
            print('nifi_flowapi_get_versions=OK', vers_list)
    except Exception as e:
        print('nifi_flowapi_get_versions=ERROR', str(e).split('\n')[0])

    # Retrieve latest version JSON
    try:
        if flow_id:
            latest = nipyapi.versioning.get_latest_flow_ver(bucket.identifier, flow_id)
            print('nifi_get_latest_flow_ver=OK', latest.snapshot_metadata.version)
    except Exception as e:
        print('nifi_get_latest_flow_ver=ERROR', str(e).split('\n')[0])

    # After save, re-check Version Control Info and report any sync errors
    try:
        if pg is not None:
            vci2 = nipyapi.nifi.VersionsApi().get_version_information(pg.id)
            vinfo = vci2.version_control_information
            # Summarize VCI for diagnosis
            summary = {
                'state': getattr(vinfo, 'state', None),
                'registry_id': getattr(vinfo, 'registry_id', None) or getattr(vinfo, 'registryId', None),
                'bucket_id': getattr(vinfo, 'bucket_id', None) or getattr(vinfo, 'bucketId', None),
                'flow_id': getattr(vinfo, 'flow_id', None) or getattr(vinfo, 'flowId', None),
                'version': getattr(vinfo, 'version', None)
            }
            print('nifi_vci_post_save=', summary)
            # if NiFi stores error messages, surface them
            err = getattr(vinfo, 'stateExplanation', None) or getattr(vinfo, 'error', None) or getattr(vinfo, 'message', None)
            if err:
                print('nifi_vci_post_save_error=', err)
            # Dump raw VCI for deep debug
            try:
                print('nifi_vci_post_save_raw=', vci2.to_dict())
            except Exception:
                pass
    except Exception as e:
        print('nifi_vci_post_save=ERROR', str(e).split('\n')[0])

    return 0


if __name__ == '__main__':
    raise SystemExit(main())


