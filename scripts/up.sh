#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

./scripts/gen_certs.sh
docker compose pull
docker compose up -d --build

echo
echo "[ok] Open:"
echo "  https://localhost/            (app)"
echo "  https://localhost/grafana/    (grafana)"
echo "  https://localhost/prometheus/ (prometheus)"
