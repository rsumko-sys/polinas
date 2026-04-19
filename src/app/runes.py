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
        self._load()

    def _load(self):
        try:
            with open(self._file, "r", encoding="utf-8") as fh:
                self._items = json.load(fh)
        except Exception:
            self._items = []

    def _save(self):
        tmp = f"{self._file}.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self._items, fh, ensure_ascii=False, indent=2)
            fh.flush()
            os.fsync(fh.fileno())
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
