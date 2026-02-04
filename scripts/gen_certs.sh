#!/usr/bin/env bash
set -euo pipefail

CERT_DIR="./nginx/certs"
CRT="$CERT_DIR/localhost.crt"
KEY="$CERT_DIR/localhost.key"

mkdir -p "$CERT_DIR"

if [[ -f "$CRT" && -f "$KEY" ]]; then
  echo "[ok] certs already exist: $CRT, $KEY"
  exit 0
fi

echo "[info] generating self-signed certs for localhost..."
openssl req -x509 -nodes -newkey rsa:2048   -keyout "$KEY"   -out "$CRT"   -days 365   -subj "/CN=localhost"

echo "[ok] generated: $CRT and $KEY"
