from typing import List, Dict, Any

from app.data.kharkiv_clubs import CLUBS_DATA


def legacy_nearest(lat: float, lon: float, limit: int = 1) -> List[Dict[str, Any]]:
    """A tiny legacy implementation to simulate the old monolith behavior.

    For the purpose of the Strangler Fig flow, this function returns the
    first `limit` clubs that have coordinates. It intentionally differs
    from the new service (no distance calculation) to illustrate a
    migration path.
    """
    out: List[Dict[str, Any]] = []
    for c in CLUBS_DATA:
        if c.get("latitude") is None or c.get("longitude") is None:
            continue
        entry = dict(c)
        entry["distance_km"] = None
        out.append(entry)
        if len(out) >= limit:
            break
    return out


__all__ = ["legacy_nearest"]
