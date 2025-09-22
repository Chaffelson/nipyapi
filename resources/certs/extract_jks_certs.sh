#!/bin/bash
# Extract PEM certificates from Java keystores (JKS/PKCS12)
# Usage:
#   extract_jks_certs.sh <jks_file> <password> [output_dir]
#   extract_jks_certs.sh --properties <properties_file> [output_dir]

set -e

show_usage() {
    echo "Usage:"
    echo "  $0 <jks_file> <password> [output_dir]                 # Direct JKS extraction"
    echo "  $0 --properties <properties_file> [output_dir]        # Extract from NiFi CLI properties"
    echo ""
    echo "Examples:"
    echo "  $0 /path/to/truststore.jks mypassword ./extracted"
    echo "  $0 --properties nifi-cli.properties ./extracted"
}

# Parse arguments
if [ "$1" = "--properties" ]; then
    # Properties file mode
    PROPERTIES_FILE="$2"
    OUTPUT_DIR="${3:-./extracted}"

    if [ -z "$PROPERTIES_FILE" ]; then
        echo "ERROR: Properties file path required"
        show_usage
        exit 1
    fi

    if [ ! -f "$PROPERTIES_FILE" ]; then
        echo "ERROR: Properties file not found: $PROPERTIES_FILE"
        exit 1
    fi

    echo "Parsing truststore from properties file: $PROPERTIES_FILE"

    # Parse truststore path from properties file
    TRUSTSTORE_PATH=$(grep "^truststore=" "$PROPERTIES_FILE" | cut -d'=' -f2- | tr -d '\r')
    TRUSTSTORE_PASSWD=$(grep "^truststorePasswd=" "$PROPERTIES_FILE" | cut -d'=' -f2- | tr -d '\r')

    if [ -z "$TRUSTSTORE_PATH" ]; then
        echo "ERROR: No truststore found in properties file"
        exit 1
    fi

    if [ -z "$TRUSTSTORE_PASSWD" ]; then
        echo "ERROR: No truststorePasswd found in properties file"
        exit 1
    fi

else
    # Direct JKS mode
    TRUSTSTORE_PATH="$1"
    TRUSTSTORE_PASSWD="$2"
    OUTPUT_DIR="${3:-./extracted}"

    if [ -z "$TRUSTSTORE_PATH" ] || [ -z "$TRUSTSTORE_PASSWD" ]; then
        echo "ERROR: Both JKS file and password are required"
        show_usage
        exit 1
    fi
fi

# Validate truststore file exists
if [ ! -f "$TRUSTSTORE_PATH" ]; then
    echo "ERROR: Truststore file not found: $TRUSTSTORE_PATH"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Extracting CA certificate from truststore: $TRUSTSTORE_PATH"

# Get all aliases from truststore
ALIASES=$(keytool -list -keystore "$TRUSTSTORE_PATH" -storepass "$TRUSTSTORE_PASSWD" 2>/dev/null | grep "Certificate fingerprint" -B1 | grep "^[a-zA-Z]" | cut -d',' -f1 || true)

if [ -z "$ALIASES" ]; then
    echo "ERROR: No certificates found in truststore"
    exit 1
fi

# Extract first certificate as CA
FIRST_ALIAS=$(echo "$ALIASES" | head -n1)
echo "Using certificate alias: $FIRST_ALIAS"

keytool -exportcert -alias "$FIRST_ALIAS" -keystore "$TRUSTSTORE_PATH" -storepass "$TRUSTSTORE_PASSWD" -file "$OUTPUT_DIR/ca.pem" -rfc

echo "✅ CA certificate extracted to: $OUTPUT_DIR/ca.pem"
echo "Certificate extraction complete"
