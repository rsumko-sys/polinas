from __future__ import annotations
from typing import Protocol


class Storage(Protocol):
    """Abstract storage interface (Strategy / Bridge target).

    Use this protocol where storage is needed. Concrete implementations
    implement S3, local FS, or any other backend.
    """

    def upload_file(self, path: str, key: str) -> str:
        ...

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        ...


def get_storage_type_from_env() -> str:
    import os

    return os.environ.get('STORAGE_BACKEND', 's3')


__all__ = ["Storage", "get_storage_type_from_env"]
