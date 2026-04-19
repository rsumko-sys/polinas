#!/usr/bin/env bash
# Collect common runtime artifacts into /tmp/incident-artifacts-<timestamp>
set -euo pipefail

OUTDIR="/tmp/incident-artifacts-$(date +%Y%m%dT%H%M%S)"
mkdir -p "$OUTDIR"

echo "Collecting docker-compose ps..." 
docker-compose ps > "$OUTDIR/docker-compose-ps.txt" 2>&1 || true

echo "Collecting recent logs (web)..."
docker-compose logs --tail 500 web > "$OUTDIR/web.logs.txt" 2>&1 || true

echo "Collecting system journal (last 500 lines)..."
journalctl -n 500 > "$OUTDIR/journalctl.txt" 2>&1 || true

echo "Collecting env files..."
cp .env* "$OUTDIR/" 2>/dev/null || true

echo "Artifacts written to: $OUTDIR"
