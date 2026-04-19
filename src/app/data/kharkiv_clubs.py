import os
from typing import List, Dict, Any

CLUBS_DATA: List[Dict[str, Any]] = []

def generate_club_map(output_path: str) -> str:
    """Create a minimal HTML file representing the clubs map.

    This is a lightweight stub used for local development and smoke checks.
    It writes a simple HTML file to `output_path` and returns that path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    html = """<!doctype html>
<html><head><meta charset='utf-8'><title>Clubs Map</title></head>
<body><h1>Kharkiv Horse Clubs (dev stub)</h1></body></html>"""
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return output_path
