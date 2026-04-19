from typing import Any
from app.storage.interface import get_storage_type_from_env

try:
    from app.storage.s3_storage import S3Storage
except Exception:
    S3Storage = None

try:
    from app.storage.local_storage import LocalStorage
except Exception:
    LocalStorage = None


def get_storage(**kwargs: Any):
    typ = get_storage_type_from_env().lower()
    if typ == 'local' and LocalStorage is not None:
        return LocalStorage(**kwargs)
    if S3Storage is not None:
        return S3Storage(**kwargs)
    # fallback
    if LocalStorage is not None:
        return LocalStorage(**kwargs)
    raise RuntimeError('No storage backend available')


__all__ = ["get_storage"]
