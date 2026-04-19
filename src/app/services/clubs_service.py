from typing import List, Dict, Any, Optional
import math
from functools import lru_cache

from app.data.kharkiv_clubs import CLUBS_DATA


class ClubsService:
    """Service responsible for club-related business rules.

    Added an input-quantized caching layer for `nearest` to reduce repeated
    CPU/network pressure when clients frequently ask for nearby clubs from
    similar coordinates (addresses chatty I/O from repeated requests).
    """

    def __init__(self, clubs: Optional[List[Dict[str, Any]]] = None) -> None:
        self._clubs = clubs if clubs is not None else CLUBS_DATA

    @staticmethod
    def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

    @staticmethod
    def _quantize(value: float, precision: int = 4) -> float:
        """Reduce float precision to create a stable cache key.

        4 decimal places ~= 11m, which is a reasonable granularity for "nearest" UX.
        """
        return round(float(value), precision)

    @staticmethod
    @lru_cache(maxsize=1024)
    def _nearest_cached(lat_q: float, lon_q: float, limit: int) -> List[Dict[str, Any]]:
        """Module-level cached calculation that uses the global CLUBS_DATA.

        Note: returning mutable structures is okay here because the cache stores
        the object references; callers receive copies to avoid accidental mutation.
        """
        found: List[Dict[str, Any]] = []
        for club in CLUBS_DATA:
            lat2 = club.get("latitude")
            lon2 = club.get("longitude")
            if lat2 is None or lon2 is None:
                continue
            try:
                dist = ClubsService._haversine(float(lat_q), float(lon_q), float(lat2), float(lon2))
            except Exception:
                continue
            entry = dict(club)
            entry["distance_km"] = dist
            found.append(entry)

        found.sort(key=lambda x: x.get("distance_km", float("inf")))
        # Return a plain list (cache will hold the reference)
        return found[: max(1, int(limit))]

    def nearest(self, lat: float, lon: float, limit: int = 1) -> List[Dict[str, Any]]:
        lat_q = self._quantize(lat)
        lon_q = self._quantize(lon)
        cached = self._nearest_cached(lat_q, lon_q, int(limit))
        # Return shallow copies so callers cannot mutate the cache contents
        return [dict(x) for x in cached]


__all__ = ["ClubsService"]
