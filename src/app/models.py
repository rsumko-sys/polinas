from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SessionData(BaseModel):
    title: str
    date: datetime
    horse: str
    type: str
    duration_min: float
    distance_km: float
    avg_speed: float
    max_speed: float
    feeling: str
    energy_horse: str
    surface: str
    weather: str
    notes_raw: str
    video_url: Optional[str] = None
    gpx_url: Optional[str] = None


class Rune(BaseModel):
    id: Optional[str]
    name: str
    effect: Optional[str] = None
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class GPXMetadata(BaseModel):
    distance_m: float
    duration_s: float
    avg_speed_kmh: float
    max_speed_kmh: float
    start_time: Optional[str]
    end_time: Optional[str]


class VideoMetadata(BaseModel):
    duration_s: float
    fps: float
    resolution: List[int]


class SessionData(BaseModel):
    title: str
    date: datetime
    horse: str
    type: str
    duration_min: float
    distance_km: float
    avg_speed: float
    max_speed: float
    feeling: str
    energy_horse: str
    surface: str
    weather: str
    notes_raw: str
    video_url: Optional[str] = None
    gpx_url: Optional[str] = None
    status: str = "open"


class Issue(BaseModel):
    name: str
    category: str
    description: str
    trigger: str
    severity: str
    pattern: str
    session_id: Optional[str] = None


class Drill(BaseModel):
    name: str
    goal: str
    category: str
    difficulty: str
    instructions: str
    progression: str
    linked_issue: Optional[str] = None


class TrainingPlan(BaseModel):
    title: str
    date: datetime
    session_type: str
    focus_issue: str
    drills: List[str]
    duration_min: int
    notes: str
    completed: bool = False


class OSINTCase(BaseModel):
    title: str
    entities: List[str]
    sources: str
    timeline: str
    geo: str
    confidence_score: float
    status: str = "open"


class Rune(BaseModel):
    id: Optional[str]
    name: str
    sigil: str
    category: Optional[str]
    description: Optional[str]
    effects: Optional[dict] = {}
    triggers: Optional[List[str]] = []
    mapped_targets: Optional[List[dict]] = []
    # spiritual/UX fields for non-linear behavior
    spiritual_effect: Optional[str] = None
    ui_hint: Optional[str] = None
