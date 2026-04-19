import os
import json
import uuid
from typing import List

_MANAGER = None


def _data_file_path() -> str:
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "runes.json")


class RuneManager:
    def __init__(self):
        self._file = _data_file_path()
        self._items = []
        self._load()

    def _load(self):
        try:
            # Use advisory file lock on POSIX to avoid concurrent readers/writers
            import fcntl

            with open(self._file, "a+", encoding="utf-8") as fh:
                fh.seek(0)
                try:
                    fcntl.flock(fh, fcntl.LOCK_SH)
                    content = fh.read()
                    if content:
                        self._items = json.loads(content)
                    else:
                        self._items = []
                finally:
                    try:
                        fcntl.flock(fh, fcntl.LOCK_UN)
                    except Exception:
                        pass
        except FileNotFoundError:
            self._items = []
        except Exception:
            # Fallback to empty if anything goes wrong during load
            self._items = []

    def _save(self):
        tmp = f"{self._file}.tmp"
        # Write to temp file then atomically replace the main file. Also
        # use an exclusive lock on the target file while replacing it.
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self._items, fh, ensure_ascii=False, indent=2)
            fh.flush()
            try:
                os.fsync(fh.fileno())
            except Exception:
                pass

        # Ensure the replace is done while holding lock on the target file
        try:
            import fcntl

            # Open (or create) target file and lock it while replacing
            with open(self._file, "a+", encoding="utf-8") as target_fh:
                try:
                    fcntl.flock(target_fh, fcntl.LOCK_EX)
                    os.replace(tmp, self._file)
                finally:
                    try:
                        fcntl.flock(target_fh, fcntl.LOCK_UN)
                    except Exception:
                        pass
        except Exception:
            # If fcntl not available (e.g., Windows) or locking fails,
            # fallback to atomic replace without explicit lock.
            os.replace(tmp, self._file)

    def list(self) -> List[dict]:
        return list(self._items)

    def create(self, data: dict) -> dict:
        item = dict(data)
        item.setdefault("id", str(uuid.uuid4()))
        self._items.append(item)
        self._save()
        return item

    def apply(self, rune_id: str, target: dict) -> dict:
        for r in self._items:
            if r.get("id") == rune_id:
                # For dev: return combined dict
                return {"rune": r, "target": target}
        raise KeyError("rune not found")


def get_rune_manager():
    global _MANAGER
    if _MANAGER is None:
        _MANAGER = RuneManager()
    return _MANAGER
