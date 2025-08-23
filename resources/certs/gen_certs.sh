#!/usr/bin/env bash
set -euo pipefail

# Generates a test CA, server certs (with SANs) and PKCS12 keystores/truststores
# for NiFi and NiFi Registry, plus a client cert for mTLS.
#
# Outputs (relative to this directory):
# - ca/ca.key, ca/ca.crt
# - nifi/server.key, nifi/server.crt, nifi/keystore.p12
# - registry/server.key, registry/server.crt, registry/keystore.p12
# - truststore/truststore.p12 (contains CA cert)
# - client/client.key, client/client.crt (PEM), client/client.p12 (optional), client/ca.pem
#
# Keystore/truststore type: PKCS12
# Default password: changeit (override with CERT_PASSWORD env)
#
# SANs include: localhost, 127.0.0.1, nifi-single, nifi-ldap, nifi-mtls, registry-single, registry-ldap, registry-mtls
#
# Requirements: openssl

script_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$script_dir"

PASS="${CERT_PASSWORD:-changeit}"
DAYS="${CERT_DAYS:-3650}"

# Clean existing cert artifacts unless disabled
CLEAN="${CERTS_CLEAN:-1}"
if [[ "$CLEAN" == "1" || "$CLEAN" == "true" ]]; then
  rm -rf ca nifi registry truststore client || true
fi

mkdir -p ca nifi registry truststore client

cat > ca/ca.cnf <<EOF
[ req ]
distinguished_name = dn
x509_extensions = v3_ca
prompt = no
[ dn ]
CN = NiPyAPI Test CA
O = NiPyAPI
C = US
[ v3_ca ]
basicConstraints = critical,CA:TRUE
keyUsage = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
EOF

# Create CA if missing
if [[ ! -f ca/ca.key || ! -f ca/ca.crt ]]; then
  openssl genrsa -out ca/ca.key 4096
  openssl req -x509 -new -nodes -key ca/ca.key -sha256 -days "$DAYS" -out ca/ca.crt -config ca/ca.cnf
fi

create_server() {
  local name="$1"; shift
  local cn="$1"; shift
  mkdir -p "$name"
  # SANs aligned with current docker compose hostnames and localhost
  local san_list="DNS:localhost,IP:127.0.0.1,DNS:nifi-single,DNS:nifi-ldap,DNS:nifi-mtls,DNS:registry-single,DNS:registry-ldap,DNS:registry-mtls"
  openssl genrsa -out "$name/server.key" 2048
  openssl req -new -key "$name/server.key" -subj "/CN=$cn/O=NiPyAPI/C=US" -out "$name/server.csr"
  # Portable issuance of server certificate with SANs via extfile (works on LibreSSL/OpenSSL)
  local extfile="$name/openssl_ext.cnf"
  cat > "$extfile" <<EOF
[v3_req]
basicConstraints=CA:FALSE
keyUsage=digitalSignature, keyEncipherment
extendedKeyUsage=serverAuth, clientAuth
subjectAltName=$san_list
EOF
  openssl x509 -req -in "$name/server.csr" -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
    -out "$name/server.crt" -days "$DAYS" -sha256 \
    -extfile "$extfile" -extensions v3_req
  # Create PKCS12 keystore
  openssl pkcs12 -export -name "$name-server" -inkey "$name/server.key" -in "$name/server.crt" -certfile ca/ca.crt \
    -out "$name/keystore.p12" -passout pass:"$PASS"
  # Make keystore readable by container users (openssl creates with 600 by default)
  chmod 644 "$name/keystore.p12"
}

# Create truststore from CA
create_truststore() {
  # PKCS12 truststore containing only the CA cert
  # Force stronger PBE to avoid RC2 issues on some platforms
  openssl pkcs12 -export -name "nipytca" -in ca/ca.crt -nokeys \
    -certpbe PBE-SHA1-3DES -out truststore/truststore.p12 -passout pass:"$PASS"
  # Make truststore readable by container users (openssl creates with 600 by default)
  chmod 644 truststore/truststore.p12
  # Ensure Java sees a trustedCertEntry inside the PKCS12 (some PKCS12 variants with only certBag show 0 entries)
  if command -v keytool >/dev/null 2>&1; then
    keytool -importcert -noprompt -alias nipyca \
      -file ca/ca.crt \
      -keystore truststore/truststore.p12 \
      -storetype PKCS12 -storepass "$PASS" >/dev/null 2>&1 || true
  fi
}

create_client() {
  # Client cert for mTLS (PEM and optional PKCS12)
  openssl genrsa -out client/client.key 2048
  openssl req -new -key client/client.key -subj "/CN=user1/O=NiPyAPI/C=US" -out client/client.csr
  openssl x509 -req -in client/client.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
    -out client/client.crt -days "$DAYS" -sha256 -extfile <(cat <<EOT
basicConstraints=CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
EOT
)
  # Optional client P12 for tools that want it
  openssl pkcs12 -export -name "client" -inkey client/client.key -in client/client.crt -certfile ca/ca.crt \
    -out client/client.p12 -passout pass:"$PASS"
  cp ca/ca.crt client/ca.pem
}

create_server nifi nifi
create_server registry registry
create_truststore
create_client

# Optionally emit JKS stores for compatibility if keytool is available
if command -v keytool >/dev/null 2>&1; then
  keytool -importkeystore -noprompt \
    -srckeystore nifi/keystore.p12 -srcstoretype PKCS12 -srcstorepass "$PASS" \
    -destkeystore nifi/keystore.jks -deststoretype JKS -deststorepass "$PASS" >/dev/null 2>&1 || true
  chmod 644 nifi/keystore.jks 2>/dev/null || true
  keytool -importkeystore -noprompt \
    -srckeystore registry/keystore.p12 -srcstoretype PKCS12 -srcstorepass "$PASS" \
    -destkeystore registry/keystore.jks -deststoretype JKS -deststorepass "$PASS" >/dev/null 2>&1 || true
  chmod 644 registry/keystore.jks 2>/dev/null || true
  keytool -importkeystore -noprompt \
    -srckeystore truststore/truststore.p12 -srcstoretype PKCS12 -srcstorepass "$PASS" \
    -destkeystore truststore/truststore.jks -deststoretype JKS -deststorepass "$PASS" >/dev/null 2>&1 || true
  chmod 644 truststore/truststore.jks 2>/dev/null || true
fi

cat > ./certs.env <<ENV
# Generated by gen_certs.sh
NIFI_SECURITY_KEYSTORE=/certs/nifi/keystore.p12
NIFI_SECURITY_KEYSTORE_TYPE=PKCS12
NIFI_SECURITY_KEYSTORE_PASSWD=$PASS
# Some images map camelCase segments; include both forms for safety
NIFI_SECURITY_KEYSTORE_PASSWORD=$PASS
NIFI_SECURITY_TRUSTSTORE=/certs/truststore/truststore.p12
NIFI_SECURITY_TRUSTSTORE_TYPE=PKCS12
NIFI_SECURITY_TRUSTSTORE_PASSWD=$PASS
NIFI_SECURITY_TRUSTSTORE_PASSWORD=$PASS
# Key password matches keystore by default in our generation
NIFI_SECURITY_KEY_PASSWD=$PASS

NIFI_REGISTRY_SECURITY_KEYSTORE=/certs/registry/keystore.p12
NIFI_REGISTRY_SECURITY_KEYSTORE_TYPE=PKCS12
NIFI_REGISTRY_SECURITY_KEYSTORE_PASSWD=$PASS
NIFI_REGISTRY_SECURITY_KEYSTORE_PASSWORD=$PASS
NIFI_REGISTRY_SECURITY_TRUSTSTORE=/certs/truststore/truststore.p12
NIFI_REGISTRY_SECURITY_TRUSTSTORE_TYPE=PKCS12
NIFI_REGISTRY_SECURITY_TRUSTSTORE_PASSWD=$PASS
NIFI_REGISTRY_SECURITY_TRUSTSTORE_PASSWORD=$PASS
NIFI_REGISTRY_SECURITY_KEY_PASSWD=$PASS

# Client-side (for tests)
TLS_CA_CERT_PATH=$(pwd)/client/ca.pem
MTLS_CLIENT_CERT=$(pwd)/client/client.crt
MTLS_CLIENT_KEY=$(pwd)/client/client.key
MTLS_CLIENT_KEY_PASSWORD=
ENV

# Service-specific env files to avoid cross-pollution
cat > ./nifi.env <<ENV
NIFI_SECURITY_KEYSTORE=/certs/nifi/keystore.p12
NIFI_SECURITY_KEYSTORE_TYPE=PKCS12
NIFI_SECURITY_KEYSTORE_PASSWD=$PASS
NIFI_SECURITY_KEYSTORE_PASSWORD=$PASS
NIFI_SECURITY_TRUSTSTORE=/certs/truststore/truststore.p12
NIFI_SECURITY_TRUSTSTORE_TYPE=PKCS12
NIFI_SECURITY_TRUSTSTORE_PASSWD=$PASS
NIFI_SECURITY_TRUSTSTORE_PASSWORD=$PASS
NIFI_SECURITY_KEY_PASSWD=$PASS
ENV

cat > ./registry.env <<ENV
NIFI_REGISTRY_SECURITY_KEYSTORE=/certs/registry/keystore.p12
NIFI_REGISTRY_SECURITY_KEYSTORE_TYPE=PKCS12
NIFI_REGISTRY_SECURITY_KEYSTORE_PASSWD=$PASS
NIFI_REGISTRY_SECURITY_KEYSTORE_PASSWORD=$PASS
NIFI_REGISTRY_SECURITY_TRUSTSTORE=/certs/truststore/truststore.p12
NIFI_REGISTRY_SECURITY_TRUSTSTORE_TYPE=PKCS12
NIFI_REGISTRY_SECURITY_TRUSTSTORE_PASSWD=$PASS
NIFI_REGISTRY_SECURITY_TRUSTSTORE_PASSWORD=$PASS
NIFI_REGISTRY_SECURITY_KEY_PASSWD=$PASS
ENV

echo "Certificates and stores generated under: $script_dir"
echo "Keystore/Truststore password: $PASS"
