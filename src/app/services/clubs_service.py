from typing import List, Dict, Any, Optional
import math
import os
import psycopg2
from psycopg2.extras import RealDictCursor

class ClubsService:
    def __init__(self, dsn: Optional[str] = None) -> None:
        self.dsn = dsn or os.environ.get("POSTGRES_DSN", "postgresql://user:pass@db:5432/horse_db")

    def get_all_clubs(self) -> List[Dict[str, Any]]:
        try:
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT * FROM horse_clubs WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
                    rows = cur.fetchall()
                    results = []
                    for row in rows:
                        d = dict(row)
                        if d.get('latitude') is not None:
                            d['latitude'] = float(d['latitude'])
                        if d.get('longitude') is not None:
                            d['longitude'] = float(d['longitude'])
                        if d.get('created_at') is not None:
                            d['created_at'] = str(d['created_at'])
                        results.append(d)
                    return results
        except Exception as e:
            print(f"DB Error: {e}")
            return []

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
        clubs = self.get_all_clubs()
        for club in clubs:
            try:
                dist = self._haversine(float(lat), float(lon), club['latitude'], club['longitude'])
                club['distance_km'] = dist
            except Exception:
                club['distance_km'] = float("inf")

        clubs.sort(key=lambda x: x.get("distance_km", float("inf")))
        return clubs[: max(1, int(limit))]

__all__ = ["ClubsService"]
