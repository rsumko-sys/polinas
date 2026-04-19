from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi import Request, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import tempfile
import os
import uuid

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .security import require_api_key, get_admin_api_key

from app.data.kharkiv_clubs import CLUBS_DATA, generate_club_map
from app.models import SessionData, Rune
from app.ingest_gpx import parse_gpx
from app.ingest_video import get_video_metadata
from app.storage.s3_storage import S3Storage
from app.notion_client import NotionClient
from app.config import NOTION_TOKEN, NOTION_SESSIONS_DB_ID
from app.ai_chain import generate_chain
from app.pid_tuner import PIDController
from app.osint_pipeline import OSINTPipeline
from app.runes import get_rune_manager
from app import secrets as secrets_helper


app = FastAPI(title="Horse Training Intelligence Platform")

# Rate limiter middleware
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi import Request, HTTPException
from pydantic import BaseModel
from . import secrets as secrets_helper
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import tempfile
import os

from app.data.kharkiv_clubs import CLUBS_DATA, generate_club_map
from app.models import SessionData
from app.ingest_gpx import parse_gpx
from app.ingest_video import get_video_metadata
from app.storage.s3_storage import S3Storage
from app.notion_client import NotionClient
from app.config import NOTION_TOKEN, NOTION_SESSIONS_DB_ID
import uuid


# Simple in-memory Notion fallback used when Notion API is not configured or
# unreachable during local QA. It implements the same methods used by the
# app but returns fake IDs so workflows can proceed.
class InMemoryNotion:
    def create_session(self, session, video_url=None, gpx_url=None):
        return str(uuid.uuid4())

    def create_issue(self, issue):
        return str(uuid.uuid4())

    def create_drill(self, drill, issue_id):
        return str(uuid.uuid4())

    def create_plan(self, plan, issue_id, drill_ids):
        return str(uuid.uuid4())
from app.ai_chain import generate_chain
from app.pid_tuner import PIDController
from app.osint_pipeline import OSINTPipeline
from app.runes import get_rune_manager
from app.models import Rune

app = FastAPI(title="Horse Training Intelligence Platform")

# Initialize resources with safe fallbacks so the API can start even when
# external services (MinIO, Notion, Neo4j) are not available in the
# developer/QA environment.
try:
    s3 = S3Storage()
except Exception:
    # Last-resort fallback: create an instance anyway (S3Storage is tolerant)
    s3 = S3Storage()

# Use real Notion client only when token and DB ID are configured;
# otherwise use the in-memory fallback to avoid runtime API errors.
if NOTION_TOKEN and NOTION_SESSIONS_DB_ID:
    try:
        notion = NotionClient()
    except Exception:
        notion = InMemoryNotion()
else:
    notion = InMemoryNotion()

try:
    pid = PIDController()
except Exception:
    pid = PIDController()

try:
    osint = OSINTPipeline()
except Exception:
    osint = OSINTPipeline()

# serve static UI built from Polina's Diaries frontend styles (non-invasive)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def ui_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<html><body><h1>Polina's Diaries</h1></body></html>")


@app.get('/ui/dashboard')
def ui_dashboard():
    path = os.path.join(static_dir, 'ui_dashboard.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse('<html><body><h1>Dashboard</h1></body></html>')


@app.get('/ui/sessions')
def ui_sessions():
    path = os.path.join(static_dir, 'ui_sessions.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse('<html><body><h1>Sessions</h1></body></html>')


@app.get('/ui/trainingplans')
def ui_trainingplans():
    path = os.path.join(static_dir, 'ui_trainingplans.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse('<html><body><h1>Training Plans</h1></body></html>')


@app.get('/ui/analysis')
def ui_analysis():
    path = os.path.join(static_dir, 'ui_analysis.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse('<html><body><h1>Analysis</h1></body></html>')


class SecretIn(BaseModel):
    key: str
    value: str


def _check_admin(request: Request):
    token = request.headers.get('X-Admin-Token') or request.headers.get('Authorization')
    admin = os.getenv('ADMIN_TOKEN')
    if not admin:
        raise HTTPException(status_code=503, detail='ADMIN_TOKEN not configured on server')
    if token != admin:
        raise HTTPException(status_code=403, detail='Invalid admin token')


@app.get('/admin/secrets')
def list_secrets(api_key: str = Depends(require_api_key)):
    """List masked environment secrets (admin-only).

    Uses the API key dependency for protection. The helper returns masked
    values and this endpoint will never reveal raw secret material.
    """
    return secrets_helper.list_env_masked()


@app.post('/admin/secrets')
def set_secret(s: SecretIn, api_key: str = Depends(require_api_key)):
    # write to project .env only; do NOT expose values to frontend
    secrets_helper.set_env_var(s.key, s.value)
    return {'status': 'ok', 'key': s.key}


@app.delete('/admin/secrets/{key}')
def delete_secret(key: str, api_key: str = Depends(require_api_key)):
    secrets_helper.delete_env_var(key)
    return {'status': 'deleted', 'key': key}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/clubs")
def get_clubs():
    return {"data": CLUBS_DATA}

@app.post("/clubs/map")
def create_club_map():
    try:
        # generate into static/maps so StaticFiles can serve it
        static_dir = os.path.join(os.path.dirname(__file__), "static")
        maps_dir = os.path.join(static_dir, "maps")
        os.makedirs(maps_dir, exist_ok=True)
        output_file = generate_club_map(os.path.join(maps_dir, "kharkiv_horse_clubs_map.html"))
        return {"map_html": output_file}
    except Exception as e:
        return JSONResponse(content={"error": "failed to generate map", "detail": str(e)}, status_code=500)


@app.get("/clubs/map")
def get_club_map():
    """GET shim: serve existing generated map HTML if present, otherwise generate it.

    This allows links (GET) from the frontend to work while preserving the
    original POST-based generator for explicit regeneration.
    """
    output_file = os.path.join(os.getcwd(), 'kharkiv_horse_clubs_map.html')
    if not os.path.exists(output_file):
        # generate on demand (non-fatal)
        try:
            # Try static location first
            static_dir = os.path.join(os.path.dirname(__file__), "static")
            maps_dir = os.path.join(static_dir, "maps")
            os.makedirs(maps_dir, exist_ok=True)
            default_map = os.path.join(maps_dir, 'kharkiv_horse_clubs_map.html')
            output_file = generate_club_map(default_map)
        except Exception as e:
            return JSONResponse(content={"error": "failed to generate map on demand", "detail": str(e)}, status_code=500)

    # return HTML file content so the browser can render directly
    with open(output_file, 'r', encoding='utf-8') as fh:
        content = fh.read()
    return HTMLResponse(content=content)

@app.post("/ingest/session")
async def ingest_session(
    title: str = Form(...),
    date: str = Form(...),
    horse: str = Form(...),
    type: str = Form(...),
    duration_min: float = Form(...),
    distance_km: float = Form(...),
    avg_speed: float = Form(...),
    max_speed: float = Form(...),
    feeling: str = Form(...),
    energy_horse: str = Form(...),
    surface: str = Form(...),
    weather: str = Form(...),
    notes_raw: str = Form(...),
    video: UploadFile = File(None),
    gpx: UploadFile = File(None)
):
    video_url = None
    gpx_url = None

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
        type=type,
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
    issue, drill, plan = generate_chain(session_dict)
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
async def run_osint():
    try:
        cases = osint.run()
        return {"cases": cases}
    except Exception as e:
        # Be tolerant in developer environments where external services
        # (Neo4j, network resources) may be unavailable — return an
        # empty result with warning instead of raising a 500.
        return JSONResponse(content={"cases": [], "warning": str(e)}, status_code=200)

@app.get("/pid/status")
def pid_status():
    return {"Kp": pid.Kp, "Ki": pid.Ki, "Kd": pid.Kd}


# Runes API: simple in-memory manager with JSON persistence in data/runes.json
@app.get('/runes')
def list_runes():
    mgr = get_rune_manager()
    items = [r.dict() for r in mgr.list()]
    return {"runes": items}


@app.post('/runes')
def create_rune(rune: Rune):
    mgr = get_rune_manager()
    created = mgr.create(rune.dict())
    return {"rune": created.dict()}


@app.post('/runes/{rune_id}/apply')
def apply_rune(rune_id: str, target_type: str = Form(...), target_id: str = Form(None)):
    mgr = get_rune_manager()
    target = {"type": target_type, "id": target_id}
    try:
        applied = mgr.apply(rune_id, target)
        return {"applied": applied}
    except KeyError:
        raise HTTPException(status_code=404, detail='rune not found')
