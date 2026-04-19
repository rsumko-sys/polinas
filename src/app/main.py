from __future__ import annotations

import os
import uuid
import tempfile
from datetime import datetime
import math
from typing import Any, Dict, List, Optional, Mapping, cast, Callable

from fastapi import FastAPI, UploadFile, File, Form, Depends, Request, HTTPException, Query, Header
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .security import require_api_key

from app.data.kharkiv_clubs import CLUBS_DATA, generate_club_map
from app.services.clubs_service import ClubsService
from app.gateway import dispatch_clubs_nearest
from app.models import SessionData, Rune
from app.notion_client import NotionClient
from app.config import NOTION_TOKEN, NOTION_SESSIONS_DB_ID
from app.ai_chain import generate_chain as _generate_chain
from app.pid_tuner import PIDController
from app.osint_pipeline import OSINTPipeline
from app.runes import get_rune_manager
from app import secrets as secrets_helper

# Optional heavy-dep fallbacks (imported after core imports to satisfy linters)
parse_gpx: Callable[[str], Any]
try:
    from app.ingest_gpx import parse_gpx as _parse_gpx
    parse_gpx = _parse_gpx
except Exception:
    def parse_gpx(path: str) -> Any:
        # lightweight fallback when gpxpy isn't installed
        return {}

get_video_metadata: Callable[[str], Any]
try:
    from app.ingest_video import get_video_metadata as _get_video_metadata
    get_video_metadata = _get_video_metadata
except Exception:
    def get_video_metadata(path: str) -> Any:
        # lightweight fallback when moviepy or ffmpeg isn't available
        return {}

S3Storage: Any
try:
    from app.storage.s3_storage import S3Storage as _RealS3Storage
    S3Storage = _RealS3Storage
except Exception:
    class _FallbackS3Storage:
        def __init__(self, *a: Any, **k: Any) -> None:
            pass
        def upload_file(self, path: str, key: str) -> str:
            return ""
    S3Storage = _FallbackS3Storage


app = FastAPI(title="Horse Training Intelligence Platform")

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, cast(Any, _rate_limit_exceeded_handler))


class InMemoryNotion:
    def create_session(self, session: SessionData, video_url: Optional[str] = None, gpx_url: Optional[str] = None) -> str:
        return str(uuid.uuid4())

    def create_issue(self, issue: Any) -> str:
        return str(uuid.uuid4())

    def create_drill(self, drill: Any, issue_id: str) -> str:
        return str(uuid.uuid4())

    def create_plan(self, plan: Any, issue_id: str, drill_ids: List[str]) -> str:
        return str(uuid.uuid4())


# Initialize resources with safe fallbacks
try:
    s3: Any = S3Storage()
except Exception:
    s3 = S3Storage()

if NOTION_TOKEN and NOTION_SESSIONS_DB_ID:
    try:
        notion: Any = NotionClient()
    except Exception:
        notion = InMemoryNotion()
else:
    notion = InMemoryNotion()

try:
    pid: Any = PIDController()
except Exception:
    pid = PIDController()

try:
    osint: Any = OSINTPipeline()
except Exception:
    osint = OSINTPipeline()


# Static UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def ui_index() -> HTMLResponse:
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<html><body><h1>Polina's Diaries</h1></body></html>")



@app.get('/ui/dashboard')
def ui_dashboard() -> HTMLResponse:
    path = os.path.join(static_dir, 'ui_dashboard.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse('<html><body><h1>Dashboard</h1></body></html>')


# Serve stub sessions page
@app.get('/ui/sessions')
def ui_sessions() -> HTMLResponse:
    path = os.path.join(static_dir, 'ui_sessions.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse('<html><body><h1>Sessions (stub)</h1></body></html>')

# Serve stub training plans page
@app.get('/ui/trainingplans')
def ui_trainingplans() -> HTMLResponse:
    path = os.path.join(static_dir, 'ui_trainingplans.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse('<html><body><h1>Training Plans (stub)</h1></body></html>')


class SecretIn(BaseModel):
    key: str
    value: str


def _check_admin(request: Request) -> None:
    token = request.headers.get('X-Admin-Token') or request.headers.get('Authorization')
    admin = os.getenv('ADMIN_TOKEN')
    if not admin:
        raise HTTPException(status_code=503, detail='ADMIN_TOKEN not configured on server')
    if token != admin:
        raise HTTPException(status_code=403, detail='Invalid admin token')


@app.get('/admin/secrets')
def list_secrets(api_key: str = Depends(require_api_key)) -> Any:
    return secrets_helper.list_env_masked()


@app.post('/admin/secrets')
def set_secret(s: SecretIn, api_key: str = Depends(require_api_key)) -> Dict[str, str]:
    secrets_helper.set_env_var(s.key, s.value)
    return {'status': 'ok', 'key': s.key}


@app.delete('/admin/secrets/{key}')
def delete_secret(key: str, api_key: str = Depends(require_api_key)) -> Dict[str, str]:
    secrets_helper.delete_env_var(key)
    return {'status': 'deleted', 'key': key}


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/clubs")
def get_clubs() -> Dict[str, Any]:
    return {"data": CLUBS_DATA}


@app.get("/clubs/nearest")
def clubs_nearest(
    lat: float = Query(..., description="Latitude of the user"),
    lon: float = Query(..., description="Longitude of the user"),
    limit: int = Query(1, ge=1, le=50, description="Maximum number of results to return"),
) -> Dict[str, Any]:
    """Controller: delegate to ClubsService (separates HTTP handling from business rules).

    GRASP: Controller - `app.main` acts as a thin controller and delegates responsibilities
    to domain/service objects. ClubsService is the Information Expert for club data.
    """
    svc = ClubsService()
    result = svc.nearest(lat=lat, lon=lon, limit=limit)
    return {"clubs": result}


@app.get("/gateway/clubs/nearest")
def gateway_clubs_nearest(
    lat: float = Query(..., description="Latitude of the user"),
    lon: float = Query(..., description="Longitude of the user"),
    limit: int = Query(1, ge=1, le=50, description="Maximum number of results to return"),
    x_use_legacy: str | None = Header(None, convert_underscores=False),
) -> Dict[str, Any]:
    """Gateway route to demonstrate Strangler Fig routing.

    The header `X-Use-Legacy: true` forces routing to the legacy implementation.
    Otherwise the request is routed to the modern `ClubsService`.
    """
    use_legacy = False
    if x_use_legacy:
        use_legacy = x_use_legacy.lower() in ("1", "true", "yes")
    clubs = dispatch_clubs_nearest(lat=lat, lon=lon, limit=limit, use_legacy=use_legacy)
    return {"clubs": clubs}


@app.post("/clubs/map")
def create_club_map() -> Any:
    try:
        static_dir_local = os.path.join(os.path.dirname(__file__), "static")
        maps_dir = os.path.join(static_dir_local, "maps")
        os.makedirs(maps_dir, exist_ok=True)
        output_file = generate_club_map(os.path.join(maps_dir, "kharkiv_horse_clubs_map.html"))
        return {"map_html": output_file}
    except Exception as e:
        return JSONResponse(content={"error": "failed to generate map", "detail": str(e)}, status_code=500)


@app.get('/runes')
def list_runes() -> Dict[str, List[Dict[str, object]]]:
    mgr = get_rune_manager()
    items = mgr.list()
    return {"runes": items}


@app.post('/runes')
def create_rune(rune: Rune) -> Dict[str, Dict[str, object]]:
    mgr = get_rune_manager()
    created = mgr.create(rune.dict())
    return {"rune": created}


@app.post('/runes/{rune_id}/apply')
def apply_rune(rune_id: str, target_type: str = Form(...), target_id: Optional[str] = Form(None)) -> Dict[str, Dict[str, object]]:
    mgr = get_rune_manager()
    target: Dict[str, Optional[str]] = {"type": target_type, "id": target_id}
    try:
        applied = mgr.apply(rune_id, cast(Mapping[str, object], target))
        return {"applied": applied}
    except KeyError:
        raise HTTPException(status_code=404, detail='rune not found')


@app.post("/ingest/session")
async def ingest_session(
    title: str = Form(...),
    date: str = Form(...),
    horse: str = Form(...),
    session_type: str = Form(..., alias="type"),
    duration_min: float = Form(...),
    distance_km: float = Form(...),
    avg_speed: float = Form(...),
    max_speed: float = Form(...),
    feeling: str = Form(...),
    energy_horse: str = Form(...),
    surface: str = Form(...),
    weather: str = Form(...),
    notes_raw: str = Form(...),
    video: Optional[UploadFile] = File(None),
    gpx: Optional[UploadFile] = File(None),
) -> JSONResponse:
    video_url: Optional[str] = None
    gpx_url: Optional[str] = None

    if video:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(await video.read())
            tmp_path = tmp.name
        get_video_metadata(tmp_path)
        video_url = s3.upload_file(tmp_path, f"videos/{video.filename}")
        os.unlink(tmp_path)

    if gpx:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gpx") as tmp:
            tmp.write(await gpx.read())
            tmp_path = tmp.name
        parse_gpx(tmp_path)
        gpx_url = s3.upload_file(tmp_path, f"gpx/{gpx.filename}")
        os.unlink(tmp_path)

    session = SessionData(
        title=title,
        date=datetime.fromisoformat(date),
        horse=horse,
        session_type=session_type,
        duration_min=duration_min,
        distance_km=distance_km,
        avg_speed=avg_speed,
        max_speed=max_speed,
        feeling=feeling,
        energy_horse=energy_horse,
        surface=surface,
        weather=weather,
        notes_raw=notes_raw,
        video_url=video_url,
        gpx_url=gpx_url,
    )

    session_id = notion.create_session(session, video_url, gpx_url)

    session_dict = session.dict()
    session_dict["date"] = session.date.isoformat()

    # generate_chain is untyped; call via Any to avoid mypy no-untyped-call
    generate_chain_any = cast(Any, _generate_chain)
    issue, drill, plan = generate_chain_any(session_dict)

    # store results in Notion (or in-memory fallback)
    issue.session_id = session_id
    issue_id = notion.create_issue(issue)
    drill_id = notion.create_drill(drill, issue_id)
    plan.focus_issue = issue.name
    plan.drills = [drill_id]
    notion.create_plan(plan, issue_id, [drill_id])

    error_stats = {"noise_variance": 0.5, "bias_trend": 0.2, "anticipation": 0.3}
    pid.tune(error_stats)

    return JSONResponse(content={"session_id": session_id, "issue_id": issue_id, "drill_id": drill_id})


@app.post("/osint/run")
async def run_osint() -> Any:
    try:
        cases = osint.run()
        return {"cases": cases}
    except Exception as e:
        return JSONResponse(content={"cases": [], "warning": str(e)}, status_code=200)


@app.get("/pid/status")
def pid_status() -> Dict[str, Any]:
    return {"Kp": getattr(pid, "Kp", None), "Ki": getattr(pid, "Ki", None), "Kd": getattr(pid, "Kd", None)}
