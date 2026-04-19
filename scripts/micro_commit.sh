#!/usr/bin/env bash
set -euo pipefail

MSG="${1:-micro commit $(date -u +"%Y-%m-%dT%H:%M:%SZ")}"

# Stage all changes
git add -A

# If nothing to commit, exit gracefully
if git diff --cached --quiet; then
  echo "No changes to commit"
  exit 0
fi

git commit -m "$MSG"
echo "Committed: $MSG"
