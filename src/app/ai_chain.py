class _Stub:
    def __init__(self, name="stub"):
        self.name = name


def generate_chain(session_dict):
    """Return a simple (issue, drill, plan) tuple for local testing.

    Each element is a lightweight object with attributes accessed by
    `app.main` so the flow can proceed without AI integrations.
    """
    issue = _Stub("issue")
    drill = _Stub("drill")
    plan = _Stub("plan")
    return issue, drill, plan
import openai
import re
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models import Issue, Drill, TrainingPlan
from datetime import datetime

openai.api_key = OPENAI_API_KEY

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


def generate_chain(session_data: dict) -> tuple[Issue, Drill, TrainingPlan]:
    # Attempt an OpenAI call if available; if anything fails, fall back to a
    # deterministic local response so QA and local tests can run without
    # external API access. This also allows tests to monkeypatch
    # `openai.ChatCompletion.create` even when `OPENAI_API_KEY` is not set.
    try:
        prompt = PROMPT_TEMPLATE.format(**session_data)
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Ти помічник з навчання верховій їзді. Повертай тільки текст у вказаному форматі."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        text = response.choices[0].message.content
    except Exception:
        from datetime import datetime as _dt
        issue = Issue(name="No API - posture drift", category="position", description="Fallback issue: horse shortens neck.", trigger="when tired", severity="low", pattern="occasional")
        drill = Drill(name="Stretch trot", goal="Encourage extension", category="rhythm", difficulty="easy", instructions="1. Warm up. 2. Long rein trot.", progression="add poles")
        plan = TrainingPlan(title=f"Plan for {issue.name}", date=_dt.now(), session_type=session_data.get('type','flat'), focus_issue=issue.name, drills=[], duration_min=30, notes="Fallback plan")
        return issue, drill, plan

    issue_block = re.search(r"====================\nISSUE\n====================(.*?)\n--------------------", text, re.DOTALL)
    drill_block = re.search(r"====================\nDRILL\n====================(.*?)\n--------------------", text, re.DOTALL)
    plan_block = re.search(r"====================\nPLAN.*?\n====================(.*?)\n====================", text, re.DOTALL)

    def parse_issue(block: str) -> Issue:
        name = re.search(r"NAME:\s*(.+)", block).group(1).strip()
        category = re.search(r"CATEGORY:\s*(.+)", block).group(1).strip()
        description = re.search(r"DESCRIPTION:\s*(.+)", block).group(1).strip()
        trigger = re.search(r"TRIGGER:\s*(.+)", block).group(1).strip()
        severity = re.search(r"SEVERITY:\s*(.+)", block).group(1).strip()
        pattern = re.search(r"PATTERN:\s*(.+)", block).group(1).strip()
        return Issue(name=name, category=category, description=description, trigger=trigger, severity=severity, pattern=pattern)

    def parse_drill(block: str) -> Drill:
        name = re.search(r"NAME:\s*(.+)", block).group(1).strip()
        goal = re.search(r"GOAL:\s*(.+)", block).group(1).strip()
        category = re.search(r"CATEGORY:\s*(.+)", block).group(1).strip()
        difficulty = re.search(r"DIFFICULTY:\s*(.+)", block).group(1).strip()
        instructions = re.search(r"INSTRUCTIONS:\s*(.+)", block).group(1).strip()
        progression = re.search(r"PROGRESSION:\s*(.+)", block).group(1).strip()
        return Drill(name=name, goal=goal, category=category, difficulty=difficulty, instructions=instructions, progression=progression)

    def parse_plan(block: str) -> TrainingPlan:
        session_type = re.search(r"TYPE:\s*(.+)", block).group(1).strip()
        focus = re.search(r"FOCUS:\s*(.+)", block).group(1).strip()
        structure = re.search(r"STRUCTURE:\s*(.+)", block).group(1).strip()
        success = re.search(r"SUCCESS CRITERIA:\s*(.+)", block).group(1).strip()
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
