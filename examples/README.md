# NiPyAPI Examples

This directory contains practical examples demonstrating NiPyAPI usage patterns and best practices.

## Available Examples

### [`fdlc.py`](fdlc.py) - Flow Development Lifecycle
**Purpose:** Complete iterative workflow for enterprise NiFi development using NiFi Registry version control.

**What it demonstrates:**
- DEV → PROD flow promotion patterns
- Registry-based version control
- Multi-environment workflow management
- Enterprise development best practices

**Usage:** `python examples/fdlc.py`

---

### [`sandbox.py`](sandbox.py) - Multi-Profile Environment Setup
**Purpose:** Comprehensive authentication and environment setup across all supported profile types.

**What it demonstrates:**
- Multi-profile authentication (single-user, secure-ldap, secure-mtls, secure-oidc)
- SSL/TLS configuration and certificate handling
- Security policy bootstrapping for secure environments
- Registry client setup with Docker networking
- Sample object creation (buckets, flows, versioning)

**Usage:** `python examples/sandbox.py <profile>` or `make sandbox NIPYAPI_PROFILE=single-user` from project root.

**Supported profiles:** `single-user`, `secure-ldap`, `secure-mtls`, `secure-oidc`

---

### [`profiles.yml`](profiles.yml) - Configuration Template
**Purpose:** Example configuration file showing all supported authentication methods and settings.

**What it contains:**
- Complete profile configuration examples
- Authentication method templates
- SSL/TLS configuration patterns
- Environment variable override examples

**Usage:** Copy and modify for your own environments, then use with `nipyapi.config.default_profiles_file = 'path/to/your/profiles.yml'`

## Getting Started

1. **For new users:** Start with the Docker-based quick start in the main README, then try `sandbox.py`
2. **For enterprise workflows:** Study `fdlc.py` for development lifecycle patterns
3. **For configuration:** Use `profiles.yml` as a template for your environments

## Documentation

For complete API documentation and detailed guides, see:
- [Profiles Documentation](../docs/profiles.rst) - Configuration and authentication
- [Security Documentation](../docs/security.rst) - SSL/TLS and authentication setup
- [Migration Guide](../docs/migration.rst) - Upgrading from 0.x to 1.x
