from typing import Any, Optional


class IntegrationsFacade:
    """Facade that encapsulates external subsystems: Notion, Storage, OpenAI, etc.

    GRASP: Pure Fabrication — this class centralizes cross-cutting calls to unstable
    external services (Protected Variations). Controllers call this facade rather than
    calling services directly.
    """

    def __init__(self, notion_client: Optional[Any] = None, storage: Optional[Any] = None, llm: Optional[Any] = None) -> None:
        self.notion = notion_client
        self.storage = storage
        self.llm = llm

    def create_session_record(self, session_data: dict, video_url: Optional[str] = None, gpx_url: Optional[str] = None) -> str:
        if self.notion:
            return self.notion.create_session(session_data, video_url=video_url, gpx_url=gpx_url)
        # fallback behavior: return an id-like string
        import uuid

        return str(uuid.uuid4())

    def upload_file(self, path: str, key: str) -> str:
        if self.storage:
            return self.storage.upload_file(path, key)
        raise RuntimeError('No storage available')

    def generate_presigned(self, key: str, expires: int = 3600) -> str:
        if self.storage:
            return self.storage.generate_presigned_url(key, expires)
        raise RuntimeError('No storage available')


__all__ = ["IntegrationsFacade"]
