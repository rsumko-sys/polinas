#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python -m pip install --upgrade pip
if [ -f requirements-dev.txt ]; then
  pip install -r requirements-dev.txt
fi
pre-commit install --install-hooks
echo "pre-commit installed"
