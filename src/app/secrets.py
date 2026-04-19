import os
from typing import Dict


def list_env_masked() -> Dict[str, str]:
    keys = [
        "ADMIN_API_KEY",
        "NOTION_TOKEN",
        "OPENAI_API_KEY",
        "MINIO_SECRET_KEY",
        "NEO4J_PASSWORD",
    ]
    out = {}
    for k in keys:
        v = os.environ.get(k)
        out[k] = "SET" if v else "UNSET"
    return out


def set_env_var(key: str, value: str) -> None:
    # For local dev we set in-process env only. Production should use a secrets store.
    os.environ[key] = value


def delete_env_var(key: str) -> None:
    os.environ.pop(key, None)
import os
from typing import Dict

ENV_PATH = os.path.join(os.getcwd(), '.env')


def _read_lines(path: str = ENV_PATH):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()


def _write_lines(lines, path: str = ENV_PATH):
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def list_env(path: str = ENV_PATH) -> Dict[str, str]:
    """Return a dict of KEY -> VALUE (raw) from an env file."""
    res = {}
    for line in _read_lines(path):
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        res[k.strip()] = v
    return res


def set_env_var(key: str, value: str, path: str = ENV_PATH):
    """Set or update an env var in the env file. Creates the file if missing."""
    lines = _read_lines(path)
    key_line = f"{key}={value}\n"
    found = False
    out = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            out.append(key_line)
            found = True
        else:
            out.append(line)
    if not found:
        out.append(key_line)
    _write_lines(out, path)


def delete_env_var(key: str, path: str = ENV_PATH):
    lines = _read_lines(path)
    out = [l for l in lines if not l.strip().startswith(f"{key}=")]
    _write_lines(out, path)


def mask_value(v: str) -> str:
    if not v:
        return ''
    if len(v) <= 6:
        return '*' * len(v)
    return '*' * (len(v) - 4) + v[-4:]


def list_env_masked(path: str = ENV_PATH) -> Dict[str, str]:
    raw = list_env(path)
    return {k: mask_value(v) for k, v in raw.items()}
