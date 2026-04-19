#!/usr/bin/env python3
"""
Write or update a .env.override file in the repo root with key=value pairs.

This helper is intentionally non-destructive: it writes to `.env.override` and prints recommended restart commands
instead of performing restarts automatically.

Usage:
  python3 scripts/incident/set_env_override.py KEY VALUE

Examples:
  python3 scripts/incident/set_env_override.py NOTION_TOKEN ""
  python3 scripts/incident/set_env_override.py USE_LEGACY true
"""
import os
import sys
from pathlib import Path


def load_override(path: Path) -> dict:
    data = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                data[k.strip()] = v.strip()
    return data


def save_override(path: Path, data: dict) -> None:
    lines = [f"{k}={v}" for k, v in data.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: set_env_override.py KEY VALUE")
        return 2
    key = argv[1]
    value = argv[2]

    repo_root = Path(__file__).resolve().parents[2]
    override_path = repo_root / ".env.override"

    env = load_override(override_path)
    env[key] = value
    save_override(override_path, env)

    print(f"Wrote {key} to {override_path}")
    print()
    print("Suggested next steps (pick appropriate command for your deployment):")
    print("- Docker Compose:")
    print("    docker-compose restart web")
    print("- Kubernetes (example):")
    print("    kubectl rollout restart deployment/web -n prod")
    print("- Systemd (example):")
    print("    sudo systemctl restart polinas.service")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
