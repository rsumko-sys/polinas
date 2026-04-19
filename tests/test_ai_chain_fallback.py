import importlib
import datetime

import app.ai_chain as ai_chain
from app.models import Issue, Drill, TrainingPlan


def test_generate_chain_fallback():
    importlib.reload(ai_chain)
    # Force fallback path
    ai_chain.OPENAI_API_KEY = ""
    session_data = {
        "date": datetime.datetime.now().isoformat(),
        "horse": "TestHorse",
        "type": "flat",
        "notes": "Test notes",
        "duration_min": 30,
        "distance_km": 5.0,
        "avg_speed": 10.0,
    }
    issue, drill, plan = ai_chain.generate_chain(session_data)
    assert isinstance(issue, Issue)
    assert isinstance(drill, Drill)
    assert isinstance(plan, TrainingPlan)
    assert issue.name.startswith("No API")
    assert drill.name == "Stretch trot"
    assert plan.title.startswith("Plan for")
