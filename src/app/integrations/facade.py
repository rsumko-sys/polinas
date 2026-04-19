from typing import Any, Optional
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed


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

    def upload_files(self, pairs: List[Tuple[str, str]], max_workers: int = 4) -> List[str]:
        """Upload multiple files in parallel using a thread pool.

        Accepts a list of `(path, key)` tuples and returns a list of resulting URLs/keys
        in the same order. This reduces wall-clock time when uploading several files
        to a network-backed storage (mitigates chatty per-file sequential uploads).
        """
        if not self.storage:
            raise RuntimeError('No storage available')

        results: List[str] = [""] * len(pairs)
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            future_to_idx = {ex.submit(self.storage.upload_file, p, k): i for i, (p, k) in enumerate(pairs)}
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                results[idx] = future.result()
        return results

    def generate_presigned(self, key: str, expires: int = 3600) -> str:
        if self.storage:
            return self.storage.generate_presigned_url(key, expires)
        raise RuntimeError('No storage available')


__all__ = ["IntegrationsFacade"]
