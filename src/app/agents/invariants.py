from __future__ import annotations

from typing import Any, Dict, List, Tuple, Optional
from copy import deepcopy


class InvariantStore:
    """Simple invariant store that holds immutable key->value pairs.

    Use `check` to verify that a generated dict did not change protected keys.
    """

    def __init__(self, invariants: Optional[Dict[str, Any]] = None) -> None:
        self._invariants: Dict[str, Any] = deepcopy(invariants or {})

    @property
    def invariants(self) -> Dict[str, Any]:
        return deepcopy(self._invariants)

    def check(self, generated: Any) -> Tuple[bool, List[str]]:
        """Return (ok, mismatched_keys).

        - If `generated` is a dict, compare protected keys and values.
        - Otherwise, we cannot assert invariants and return (True, []).
        """
        if not isinstance(generated, dict):
            return True, []

        mismatches: List[str] = []
        for k, v in self._invariants.items():
            if generated.get(k) != v:
                mismatches.append(k)

        return (len(mismatches) == 0), mismatches


__all__ = ["InvariantStore"]
