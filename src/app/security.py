from typing import Optional
import os

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

API_KEY_HEADER_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)


def get_admin_api_key() -> Optional[str]:
    """Return API key from environment, or None if unset."""
    return os.environ.get("ADMIN_API_KEY")


async def require_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """Dependency that validates presence of API key in request headers.

    Reads expected key from `ADMIN_API_KEY` env var. Raises 401 on mismatch.
    """
    expected = get_admin_api_key()
    if expected is None:
        raise HTTPException(status_code=500, detail="Admin API key not configured")
    if not api_key or api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return api_key
