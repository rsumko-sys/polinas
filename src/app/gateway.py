"""API Gateway helpers to support Strangler-Fig incremental migration.

This module exposes a small dispatch function that controllers can call.
It decides whether to route to legacy implementations or the new services
based on an explicit flag or environment variable. The fast path is
to call the modern service; the legacy path keeps old behaviour until
we decommission it.
"""
import os
from typing import List, Dict, Any

from app.services.clubs_service import ClubsService
from app.legacy.legacy_clubs import legacy_nearest


def dispatch_clubs_nearest(lat: float, lon: float, limit: int = 1, use_legacy: bool = False) -> List[Dict[str, Any]]:
    """Dispatch to legacy or new nearest-club implementation.

    Resolution order:
    - explicit `use_legacy` argument (highest priority)
    - environment variable `USE_LEGACY` (if set to 'true')
    - default: use new `ClubsService`
    """
    if use_legacy or os.getenv("USE_LEGACY", "false").lower() in ("1", "true", "yes"):
        return legacy_nearest(lat, lon, limit=limit)

    svc = ClubsService()
    return svc.nearest(lat=lat, lon=lon, limit=limit)


__all__ = ["dispatch_clubs_nearest"]
