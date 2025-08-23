#!/usr/bin/env python3
"""
Readiness probe for NiFi and NiFi Registry using nipyapi profiles and client functions.

Environment:
  - NIPYAPI_PROFILE (required): Profile name to configure endpoints and SSL settings
  - WAIT_TIMEOUT (optional, default=60): Timeout in seconds for readiness checks

Endpoints and SSL configuration are read from the specified profile.
Tests both UI and API endpoints with fallback logic using enhanced client functions.
"""
import os
import sys
import logging
from datetime import datetime

import nipyapi.utils
import nipyapi.profiles

# Configure logging to show nipyapi connection attempt details
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)


def wait_for_endpoint(url: str, name: str, timeout: int = 60) -> bool:
    """Wait for an endpoint to be ready using nipyapi client functions."""
    print(f"[{datetime.now().isoformat(timespec='seconds')}] Waiting for {name} (timeout={timeout}s)")

    try:
        result = nipyapi.utils.wait_to_complete(
            nipyapi.utils.is_endpoint_up,
            url,
            nipyapi_delay=3,
            nipyapi_max_wait=timeout
        )
        if result:
            print(f"  READY: {name}")
            return True
    except ValueError:  # Timeout
        pass

    print(f"  NOT READY within {timeout}s: {name}")
    return False


def main() -> int:
    profile_name = os.getenv('NIPYAPI_PROFILE')
    timeout = int(os.getenv('WAIT_TIMEOUT', '60'))

    if not profile_name:
        print("ERROR: NIPYAPI_PROFILE must be set")
        return 2

    # Configure using profile system (default file resolution handled automatically)
    try:
        nipyapi.profiles.switch(profile_name, login=False)
        config = nipyapi.profiles.resolve_profile_config(profile_name=profile_name)
        print(f"Using profile: {profile_name}")
        nifi_url = config.get('nifi_url')
        registry_url = config.get('registry_url')
    except Exception as e:
        print(f"ERROR: Failed to configure profile {profile_name}: {e}")
        return 2

    results = []

    # Check NiFi if configured
    if nifi_url:
        nifi_ui = nifi_url.replace('/nifi-api', '/nifi/')
        ok1 = (wait_for_endpoint(nifi_ui, 'NiFi UI', timeout) or
               wait_for_endpoint(nifi_url + '/flow/about', 'NiFi API', timeout))
        results.append(ok1)

    # Check Registry if configured
    if registry_url:
        registry_ui = registry_url.replace('/nifi-registry-api', '/nifi-registry/')
        ok2 = (wait_for_endpoint(registry_ui, 'Registry UI', timeout) or
               wait_for_endpoint(registry_url + '/about', 'Registry API', timeout))
        results.append(ok2)

    if not results:
        print("ERROR: No endpoints configured in profile")
        return 2

    rc = 0 if all(results) else 1
    print(f"Overall readiness: {'READY' if rc == 0 else 'NOT READY'}")
    return rc


if __name__ == '__main__':
    sys.exit(main())
