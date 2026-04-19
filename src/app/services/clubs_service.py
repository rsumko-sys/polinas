from typing import List, Dict, Any, Optional
import math

from app.data.kharkiv_clubs import CLUBS_DATA


class ClubsService:
    """Service responsible for club-related business rules.

    GRASP: Information Expert -> this class owns the logic to find nearest clubs because
    it has the required data (CLUBS_DATA) and algorithms (Haversine).

    This isolates responsibilities from HTTP controllers (`app.main`) and
    makes it easy to test and reuse.
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

    def nearest(self, lat: float, lon: float, limit: int = 1) -> List[Dict[str, Any]]:
        found: List[Dict[str, Any]] = []
        for club in self._clubs:
            lat2 = club.get("latitude")
            lon2 = club.get("longitude")
            if lat2 is None or lon2 is None:
                continue
            try:
                dist = self._haversine(float(lat), float(lon), float(lat2), float(lon2))
            except Exception:
                continue
            entry = dict(club)
            entry["distance_km"] = dist
            found.append(entry)

        found.sort(key=lambda x: x.get("distance_km", float("inf")))
        return found[: max(1, int(limit))]


__all__ = ["ClubsService"]
