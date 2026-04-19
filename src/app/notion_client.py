from typing import Any, List, Optional

try:
    from notion_client import Client
except Exception:
    Client = None

from app.config import (
    NOTION_TOKEN,
    NOTION_SESSIONS_DB_ID,
    NOTION_ISSUES_DB_ID,
    NOTION_DRILLS_DB_ID,
    NOTION_ANALYSIS_DB_ID,
    NOTION_PLAN_DB_ID,
)
from app.models import SessionData, Issue, Drill, TrainingPlan


class NotionClient:
    def __init__(self) -> None:
        self.client: Any = Client(auth=NOTION_TOKEN) if Client else None
        self.sessions_db: Optional[str] = NOTION_SESSIONS_DB_ID
        self.issues_db: Optional[str] = NOTION_ISSUES_DB_ID
        self.drills_db: Optional[str] = NOTION_DRILLS_DB_ID
        self.analysis_db: Optional[str] = NOTION_ANALYSIS_DB_ID
        self.plan_db: Optional[str] = NOTION_PLAN_DB_ID

    def create_session(self, session: SessionData, video_url: Any = None, gpx_url: Any = None) -> str:
        props = {
            "Session Name": {"title": [{"text": {"content": session.title}}]},
            "Date": {"date": {"start": session.date.isoformat()}},
            "Horse": {"select": {"name": session.horse}},
            "Type": {"select": {"name": session.session_type}},
            "Duration_min": {"number": session.duration_min},
            "Distance_km": {"number": session.distance_km},
            "Avg_speed": {"number": session.avg_speed},
            "Max_speed": {"number": session.max_speed},
            "Feeling": {"select": {"name": session.feeling}},
            "Energy_horse": {"select": {"name": session.energy_horse}},
            "Surface": {"select": {"name": session.surface}},
            "Weather": {"rich_text": [{"text": {"content": session.weather}}]},
            "Notes_raw": {"rich_text": [{"text": {"content": session.notes_raw}}]},
            "Status": {"select": {"name": session.status}},
        }
        if video_url:
            props["Video"] = {
                "files": [{"name": "video", "type": "external", "external": {"url": video_url}}]
            }
        if gpx_url:
            props["Track_GPX"] = {
                "files": [{"name": "track", "type": "external", "external": {"url": gpx_url}}]
            }
        page = self.client.pages.create(parent={"database_id": self.sessions_db}, properties=props)
        return str(page.get("id"))

    def create_issue(self, issue: Issue) -> str:
        props = {
            "Name": {"title": [{"text": {"content": issue.name}}]},
            "Category": {"select": {"name": issue.category}},
            "Description": {"rich_text": [{"text": {"content": issue.description}}]},
            "Trigger": {"rich_text": [{"text": {"content": issue.trigger}}]},
            "Severity": {"select": {"name": issue.severity}},
            "Pattern": {"rich_text": [{"text": {"content": issue.pattern}}]},
            "Status": {"select": {"name": "open"}},
        }
        if issue.session_id:
            props["Detected_in"] = {"relation": [{"id": issue.session_id}]}
        page = self.client.pages.create(parent={"database_id": self.issues_db}, properties=props)
        return str(page.get("id"))

    def create_drill(self, drill: Drill, issue_id: str) -> str:
        props = {
            "Name": {"title": [{"text": {"content": drill.name}}]},
            "Goal": {"rich_text": [{"text": {"content": drill.goal}}]},
            "Category": {"select": {"name": drill.category}},
            "Difficulty": {"select": {"name": drill.difficulty}},
            "Instructions": {"rich_text": [{"text": {"content": drill.instructions}}]},
            "Progression": {"rich_text": [{"text": {"content": drill.progression}}]},
            "Linked Issue": {"relation": [{"id": issue_id}]},
        }
        page = self.client.pages.create(parent={"database_id": self.drills_db}, properties=props)
        return str(page.get("id"))

    def create_plan(self, plan: TrainingPlan, issue_id: str, drill_ids: List[str]) -> str:
        props = {
            "Title": {"title": [{"text": {"content": plan.title}}]},
            "Date": {"date": {"start": plan.date.isoformat()}},
            "Session_Type": {"select": {"name": plan.session_type}},
            "Focus_Issue": {"relation": [{"id": issue_id}]},
            "Drills": {"relation": [{"id": did} for did in drill_ids]},
            "Duration_min": {"number": plan.duration_min},
            "Notes": {"rich_text": [{"text": {"content": plan.notes}}]},
            "Completed": {"checkbox": plan.completed},
        }
        page = self.client.pages.create(parent={"database_id": self.plan_db}, properties=props)
        return str(page.get("id"))
