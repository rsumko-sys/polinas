import os

CLUBS_DATA = []

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
import json
from pathlib import Path
import logging

import folium

logger = logging.getLogger(__name__)
CLUBS_DATA = [
    {
        "club_id": "KH_001",
        "name": "King Horse",
        "location": {
            "address": "Проспект Науки 65 А, Харків",
            "city": "Kharkiv",
            "gps": {"lat": 50.0677, "lon": 36.2350},
        },
        "arena": {
            "type": "open_field_and_forest",
            "surface": "natural_grass_sand",
            "lighting": True,
            "size_meters": "60x40",
        },
        "training_offerings": ["private_lessons", "forest_trails", "photoshoot"],
        "pricing": {"trail_ride_uah": 500, "training_45min_uah": 550},
        "horses_list": [
            {"name": "Oscar", "level": "advanced", "specialization": "jumping"},
            {"name": "Pharaoh", "level": "medium", "specialization": "trail"},
            {"name": "Gerda", "level": "beginner", "specialization": "dressage"},
            {"name": "Lord", "level": "medium", "specialization": "trail"},
        ],
        "contact": {
            "phone": "+380666222447",
            "website": "https://king-horse.kh.ua",
        },
        "description": "Школа верхової їзди, конкур, прогулянки лісом.",
        "icon_color": "red",
    },
    {
        "club_id": "KH_002",
        "name": "Кінний клуб Оскар",
        "location": {
            "address": "с. Безлюдівка, вул. Перемоги 310а",
            "city": "Kharkiv Oblast",
            "gps": {"lat": 49.8731, "lon": 36.2701},
        },
        "arena": {"type": "outdoor_manege", "surface": "sand", "lighting": False},
        "training_offerings": ["hippotherapy", "training", "trail_rides", "swimming"],
        "pricing": {"trail_ride_uah": 300, "training_45min_uah": 450},
        "horses_count": 15,
        "special_features": ["hippotherapy", "swimming_with_horses"],
        "description": "Іпотерапія, 10 коней, купання.",
        "icon_color": "green",
    },
    {
        "club_id": "KH_003",
        "name": "Mon Ami",
        "location": {
            "address": "вул. Дерев'янко, 4, Олексіївка, Харків",
            "city": "Kharkiv",
            "gps": {"lat": 50.0169, "lon": 36.2138},
        },
        "arena": {"type": "forest_manege", "surface": "mixed_grass", "lighting": False},
        "training_offerings": ["guided_trails", "lessons", "family_rides"],
        "pricing": {"trail_ride_uah": 450, "training_45min_uah": 500},
        "special_features": ["instructor_accompaniment"],
        "description": "15 років досвіду, інструкторський супровід.",
        "icon_color": "blue",
    },
]


def save_club_data_json(output_path: str | Path) -> None:
    target = Path(output_path)
    target.write_text(json.dumps({"data": CLUBS_DATA}, ensure_ascii=False, indent=2), encoding="utf-8")


def generate_club_map(output_path: str | Path | None = None) -> str:
    # Ensure output is placed under the app static folder so the server
    # can serve it directly (static/maps/...)
    static_maps_dir = Path(__file__).resolve().parents[1] / "static" / "maps"
    try:
        static_maps_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        logger.exception("Failed to ensure static maps directory exists")

    if output_path:
        target = Path(output_path)
    else:
        target = static_maps_dir / "kharkiv_horse_clubs_map.html"

    map_horses = folium.Map(location=[50.0, 36.23], zoom_start=11)

    for club in CLUBS_DATA:
        popup_html = f"""
        <b>{club['name']}</b><br>
        📍 {club['location']['address']}<br>
        💰 Ціни: від {club['pricing'].get('trail_ride_uah', 'N/A')} грн<br>
        🐴 {club['description']}<br>
        <a href=\"https://www.google.com/maps/search/?api=1&query={club['location']['gps']['lat']},{club['location']['gps']['lon']}\" target=\"_blank\">Побудувати маршрут</a>
        """

        try:
            folium.Marker(
                location=[club["location"]["gps"]["lat"], club["location"]["gps"]["lon"]],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=club["name"],
                icon=folium.Icon(color=club.get("icon_color", "blue"), icon="horse", prefix="fa"),
            ).add_to(map_horses)
        except Exception:
            # Some environments may lack the font-awesome icons or have
            # issues rendering custom icons — fall back to a plain marker.
            try:
                folium.Marker(
                    location=[club["location"]["gps"]["lat"], club["location"]["gps"]["lon"]],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=club["name"],
                ).add_to(map_horses)
            except Exception:
                logger.exception("Failed to add marker for club %s", club.get("club_id"))
                # Ignore this club if marker creation fails entirely.
                continue

    # Add OpenStreetMap with explicit attribution (safer for headless envs)
    try:
        folium.TileLayer(tiles="OpenStreetMap", attr='© OpenStreetMap contributors').add_to(map_horses)
    except Exception:
        logger.exception("Failed to add OpenStreetMap TileLayer")

    try:
        folium.TileLayer("Stamen Terrain", attr="Stamen").add_to(map_horses)
    except Exception:
        # Some folium / tile providers require explicit attribution; if
        # adding the layer fails, continue with what's available.
        logger.debug("Stamen Terrain TileLayer unavailable, continuing without it")

    try:
        target.write_text(map_horses.get_root().render(), encoding="utf-8")
        return str(target)
    except Exception:
        logger.exception("Folium render failed, writing fallback HTML to %s", target)
        # If folium rendering fails for any reason, write a minimal HTML
        # fallback so the frontend can still open something useful.
        fallback = f"<html><body><h1>Kharkiv Horse Clubs</h1><p>Map generation failed, but club list is available below:</p><ul>"
        for c in CLUBS_DATA:
            lat = c.get("location", {}).get("gps", {}).get("lat")
            lon = c.get("location", {}).get("gps", {}).get("lon")
            href = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else "#"
            fallback += f"<li><a href=\"{href}\">{c.get('name')}</a> — {c.get('description','')}</li>"
        fallback += "</ul></body></html>"
        try:
            target.write_text(fallback, encoding="utf-8")
        except Exception:
            logger.exception("Failed to write fallback HTML to %s", target)
        return str(target)
