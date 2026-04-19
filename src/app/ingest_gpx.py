def parse_gpx(path: str):
    # Dev stub: parse is a no-op for smoke checks
    return None
import gpxpy
from app.models import GPXMetadata


def parse_gpx(file_path: str) -> GPXMetadata:
    with open(file_path, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    total_distance = 0.0
    start_time = None
    end_time = None

    for track in gpx.tracks:
        for segment in track.segments:
            points = segment.points
            if points:
                if start_time is None:
                    start_time = points[0].time
                end_time = points[-1].time
            for previous, current in zip(points, points[1:]):
                total_distance += previous.distance_3d(current) or 0.0

    duration_sec = (end_time - start_time).total_seconds() if start_time and end_time else 0
    avg_speed = total_distance / (duration_sec / 3600) if duration_sec > 0 else 0.0
    max_speed = 0.0
    if gpx:
        moving_data = gpx.get_moving_data(raw=False)
        max_speed = moving_data.max_speed or 0.0

    return GPXMetadata(
        distance_m=total_distance,
        duration_s=duration_sec,
        avg_speed_kmh=avg_speed / 1000.0,
        max_speed_kmh=max_speed * 3.6,
        start_time=start_time.isoformat() if start_time else None,
        end_time=end_time.isoformat() if end_time else None,
    )
