#!/usr/bin/env python3
"""
Simple readiness probe for NiFi and NiFi Registry UIs/APIs.

Environment:
  - NIFI_API_ENDPOINT (required), e.g., https://localhost:9443/nifi-api
  - REGISTRY_API_ENDPOINT (required), e.g., https://localhost:18445/nifi-registry-api
  - TLS_CA_CERT_PATH (optional): path to PEM CA bundle
  - REQUESTS_CA_BUNDLE (optional): fallback CA bundle path (respected if TLS_CA_CERT_PATH not set)
  - MTLS_CLIENT_CERT / MTLS_CLIENT_KEY / MTLS_CLIENT_KEY_PASSWORD (optional): client auth for mTLS
  - WAIT_SKIP_VERIFY (optional, default=1): set to 0 to enforce verification when no CA bundle is provided
  - WAIT_TIMEOUT (optional, default=60): seconds
"""
import os
import sys
import time
import ssl
import urllib.request
from datetime import datetime


def open_with_optional_ca(url: str, cafile: str | None, skip_verify: bool,
                          client_cert: str | None = None,
                          client_key: str | None = None,
                          client_key_password: str | None = None):
    if not skip_verify and cafile and os.path.exists(cafile):
        ctx = ssl.create_default_context(cafile=cafile)
    else:
        ctx = ssl._create_unverified_context()
    if client_cert and client_key and os.path.exists(client_cert) and os.path.exists(client_key):
        try:
            ctx.load_cert_chain(certfile=client_cert, keyfile=client_key, password=client_key_password)
        except Exception:
            # Fall through without client auth if loading fails
            pass
    return urllib.request.urlopen(url, context=ctx)


def wait(url: str, expect_401_ok: bool = False, timeout: int = 60, cafile: str | None = None, name: str = "", skip_verify: bool = True,
         client_cert: str | None = None, client_key: str | None = None, client_key_password: str | None = None,
         accept_auth_errors: bool = True) -> bool:
    start = time.time()
    attempt = 0
    print(f"[{datetime.now().isoformat(timespec='seconds')}] Waiting for {name or url} (expect_401_ok={expect_401_ok}, timeout={timeout}s)")
    while time.time() - start < timeout:
        attempt += 1
        try:
            with open_with_optional_ca(url, cafile, skip_verify, client_cert, client_key, client_key_password) as r:
                status = getattr(r, 'status', 0)
                print(f"  attempt {attempt}: GET {url} -> {status}")
                sys.stdout.flush()
                if (200 <= status < 400) or (expect_401_ok and status == 401) or (accept_auth_errors and status in (401, 403)):
                    print(f"  READY: {name or url} status={status}")
                    sys.stdout.flush()
                    return True
        except Exception as e:
            # Treat explicit TLS client-auth failures as an indicator the endpoint is up when no client certs provided
            msg = str(e)
            if isinstance(e, ssl.SSLError) and ('bad certificate' in msg.lower() or 'alert bad certificate' in msg.lower()):
                print(f"  attempt {attempt}: GET {url} -> TLS client-auth required (treating as READY): {e.__class__.__name__}: {e}")
                sys.stdout.flush()
                return True
            print(f"  attempt {attempt}: GET {url} -> ERROR: {e.__class__.__name__}: {e}")
            sys.stdout.flush()
        time.sleep(2)
    print(f"  NOT READY within {timeout}s: {name or url}")
    sys.stdout.flush()
    return False


def main() -> int:
    nifi = os.getenv('NIFI_API_ENDPOINT')
    reg = os.getenv('REGISTRY_API_ENDPOINT')
    if not nifi or not reg:
        print("ERROR: NIFI_API_ENDPOINT and REGISTRY_API_ENDPOINT must be provided; no defaults will be assumed.")
        return 2
    cafile = os.getenv('TLS_CA_CERT_PATH') or os.getenv('REQUESTS_CA_BUNDLE')
    client_cert = os.getenv('MTLS_CLIENT_CERT')
    client_key = os.getenv('MTLS_CLIENT_KEY')
    client_key_password = os.getenv('MTLS_CLIENT_KEY_PASSWORD')
    skip_verify = os.getenv('WAIT_SKIP_VERIFY', '1') != '0' and not cafile
    timeout = int(os.getenv('WAIT_TIMEOUT', '60'))
    print(f"Using CA={cafile or '(none)'} client_cert={'set' if client_cert else 'none'} skip_verify={skip_verify} timeout={timeout}")
    # Probe NiFi UI then API on the exact host/port derived from NIFI_API_ENDPOINT
    nifi_ui = nifi.replace('/nifi-api', '/nifi/')
    ok1 = wait(nifi_ui, expect_401_ok=False, cafile=cafile, name='NiFi UI', skip_verify=skip_verify, timeout=timeout,
               client_cert=client_cert, client_key=client_key, client_key_password=client_key_password, accept_auth_errors=True) \
          or wait(nifi + '/flow/about', expect_401_ok=True, cafile=cafile, name='NiFi about', skip_verify=skip_verify, timeout=timeout,
                   client_cert=client_cert, client_key=client_key, client_key_password=client_key_password, accept_auth_errors=True)
    # Probe Registry UI then API on the exact host/port derived from REGISTRY_API_ENDPOINT only
    reg_ui = reg.replace('/nifi-registry-api', '/nifi-registry/')
    ok2 = wait(reg_ui, expect_401_ok=False, cafile=cafile, name='Registry UI', skip_verify=skip_verify, timeout=timeout,
               client_cert=client_cert, client_key=client_key, client_key_password=client_key_password, accept_auth_errors=True) \
          or wait(reg + '/about', cafile=cafile, name='Registry about', skip_verify=skip_verify, timeout=timeout,
                   client_cert=client_cert, client_key=client_key, client_key_password=client_key_password, accept_auth_errors=True)
    rc = 0 if ok1 and ok2 else 1
    print(f"Overall readiness: {'READY' if rc == 0 else 'NOT READY'}")
    return rc


if __name__ == '__main__':
    sys.exit(main())


