#!/usr/bin/env bash
set -euo pipefail

# Delete rotated app logs older than 7 days
# (requests.log.1, requests.log.2, ...)
DAYS="${1:-7}"

docker compose exec -T app sh -lc "find /var/log/app -type f -name 'requests.log.*' -mtime +${DAYS} -delete || true"
echo "[ok] cleaned rotated logs older than ${DAYS} days"
