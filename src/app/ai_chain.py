try:
    import openai
except Exception:
    openai = None
import re
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models import Issue, Drill, TrainingPlan
from typing import Any
from datetime import datetime
import logging

if openai is not None:
    try:
        openai.api_key = OPENAI_API_KEY
    except Exception:
        pass

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
ЗАДАЧА:
На основі даних сеансу сформулювати одну ключову проблему (issue), одне рішення (drill) та план наступного тренування (plan).

ВХІД:
date: {date}
horse: {horse}
type: {type}
notes: {notes}
metrics: duration={duration_min} min, distance={distance_km} km, avg_speed={avg_speed} km/h

ВИХІД (суворо дотримуйся формату):
====================
ISSUE
====================
NAME: {{назва проблеми}}
CATEGORY: {{position/tempo/control/behavior}}
DESCRIPTION: {{опис проблеми}}
TRIGGER: {{умови прояву}}
SEVERITY: {{low/medium/high}}
PATTERN: {{повторюваність}}
--------------------
====================
DRILL
====================
NAME: {{назва вправи}}
GOAL: {{мета вправи}}
CATEGORY: {{balance/rhythm/jumping/control}}
DIFFICULTY: {{easy/medium/hard}}
INSTRUCTIONS: 1. {{крок 1}} 2. {{крок 2}} ...
PROGRESSION: {{ускладнення}}
--------------------
====================
PLAN (NEXT SESSION)
====================
TYPE: {{flat/jumping/recovery}}
FOCUS: {{назва проблеми}}
STRUCTURE: Warm-up: ... Main block: ... Cooldown: ...
SUCCESS CRITERIA: {{критерій}}
====================
"""


def generate_chain(session_data: dict[str, Any]) -> tuple[Issue, Drill, TrainingPlan]:
    # Build prompt
    prompt = PROMPT_TEMPLATE.format(**session_data)

    # If no API key is configured, skip external call and use deterministic fallback
    if not OPENAI_API_KEY:
        logger.info("OPENAI_API_KEY not set; using local fallback for generate_chain")
        from datetime import datetime as _dt
        issue = Issue(name="No API - posture drift", category="position", description="Fallback issue: horse shortens neck.", trigger="when tired", severity="low", pattern="occasional")
        drill = Drill(name="Stretch trot", goal="Encourage extension", category="rhythm", difficulty="easy", instructions="1. Warm up. 2. Long rein trot.", progression="add poles")
        plan = TrainingPlan(title=f"Plan for {issue.name}", date=_dt.now(), session_type=session_data.get('type','flat'), focus_issue=issue.name, drills=[], duration_min=30, notes="Fallback plan")
        return issue, drill, plan

    # Attempt OpenAI call; on failure, log and fall back to deterministic response
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Ти помічник з навчання верховій їзді. Повертай тільки текст у вказаному форматі."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        # Defensive access to response content
        text = getattr(response, 'choices', [None])[0]
        if text and hasattr(text, 'message') and hasattr(text.message, 'content'):
            text = text.message.content
        else:
            text = str(response)
    except Exception as exc:
        logger.exception("OpenAI call failed in generate_chain; using fallback: %s", exc)
        from datetime import datetime as _dt
        issue = Issue(name="No API - posture drift", category="position", description="Fallback issue: horse shortens neck.", trigger="when tired", severity="low", pattern="occasional")
        drill = Drill(name="Stretch trot", goal="Encourage extension", category="rhythm", difficulty="easy", instructions="1. Warm up. 2. Long rein trot.", progression="add poles")
        plan = TrainingPlan(title=f"Plan for {issue.name}", date=_dt.now(), session_type=session_data.get('type','flat'), focus_issue=issue.name, drills=[], duration_min=30, notes="Fallback plan")
        return issue, drill, plan

    issue_block = re.search(r"====================\nISSUE\n====================(.*?)\n--------------------", text, re.DOTALL)
    drill_block = re.search(r"====================\nDRILL\n====================(.*?)\n--------------------", text, re.DOTALL)
    plan_block = re.search(r"====================\nPLAN.*?\n====================(.*?)\n====================", text, re.DOTALL)

    # Ensure regex matches before calling .group() (satisfy mypy and avoid runtime errors)
    assert issue_block is not None and drill_block is not None and plan_block is not None

    def parse_issue(block: str) -> Issue:
        m = re.search(r"NAME:\s*(.+)", block)
        assert m is not None
        name = m.group(1).strip()
        m = re.search(r"CATEGORY:\s*(.+)", block)
        assert m is not None
        category = m.group(1).strip()
        m = re.search(r"DESCRIPTION:\s*(.+)", block)
        assert m is not None
        description = m.group(1).strip()
        m = re.search(r"TRIGGER:\s*(.+)", block)
        assert m is not None
        trigger = m.group(1).strip()
        m = re.search(r"SEVERITY:\s*(.+)", block)
        assert m is not None
        severity = m.group(1).strip()
        m = re.search(r"PATTERN:\s*(.+)", block)
        assert m is not None
        pattern = m.group(1).strip()
        return Issue(name=name, category=category, description=description, trigger=trigger, severity=severity, pattern=pattern)

    def parse_drill(block: str) -> Drill:
        m = re.search(r"NAME:\s*(.+)", block)
        assert m is not None
        name = m.group(1).strip()
        m = re.search(r"GOAL:\s*(.+)", block)
        assert m is not None
        goal = m.group(1).strip()
        m = re.search(r"CATEGORY:\s*(.+)", block)
        assert m is not None
        category = m.group(1).strip()
        m = re.search(r"DIFFICULTY:\s*(.+)", block)
        assert m is not None
        difficulty = m.group(1).strip()
        m = re.search(r"INSTRUCTIONS:\s*(.+)", block)
        assert m is not None
        instructions = m.group(1).strip()
        m = re.search(r"PROGRESSION:\s*(.+)", block)
        assert m is not None
        progression = m.group(1).strip()
        return Drill(name=name, goal=goal, category=category, difficulty=difficulty, instructions=instructions, progression=progression)

    def parse_plan(block: str) -> TrainingPlan:
        m = re.search(r"TYPE:\s*(.+)", block)
        assert m is not None
        session_type = m.group(1).strip()
        m = re.search(r"FOCUS:\s*(.+)", block)
        assert m is not None
        focus = m.group(1).strip()
        m = re.search(r"STRUCTURE:\s*(.+)", block)
        assert m is not None
        structure = m.group(1).strip()
        m = re.search(r"SUCCESS CRITERIA:\s*(.+)", block)
        assert m is not None
        success = m.group(1).strip()
        notes = f"Structure: {structure}\nSuccess: {success}"
        # Ensure `date` is a datetime for the TrainingPlan model
        raw_date = session_data.get("date")
        plan_date = None
        if isinstance(raw_date, datetime):
            plan_date = raw_date
        elif isinstance(raw_date, str):
            try:
                plan_date = datetime.fromisoformat(raw_date)
            except Exception:
                try:
                    plan_date = datetime.strptime(raw_date, "%Y-%m-%d")
                except Exception:
                    plan_date = datetime.now()
        else:
            plan_date = datetime.now()

        return TrainingPlan(title=f"Plan for {focus}", date=plan_date, session_type=session_type, focus_issue=focus, drills=[], duration_min=30, notes=notes)

    issue = parse_issue(issue_block.group(1))
    drill = parse_drill(drill_block.group(1))
    plan = parse_plan(plan_block.group(1))
    return issue, drill, plan
