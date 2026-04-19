import pytest

from app.agents.agent_core import Agent
from app.agents.guardrails import Guardrails


def test_invariants_are_protected():
    # invariants: protected key 'version'
    invariants = {"version": 1, "protected": "keep"}

    def gen(prompt: str):
        # Attempts to modify invariant 'version'
        return {"version": 2, "protected": "keep", "value": 123}

    def ver(out):
        return True, (0.9, "ok")

    ag = Agent("inv", gen, ver, max_iterations=2, guardrails=Guardrails())
    res = ag.run("x", invariants=invariants)
    assert res["ok"] is False
    assert res.get("error") == "verification_failed"
    # trace should contain verify entries indicating invariant violations
    msgs = [t for t in res["trace"] if t.get("role") == "verify"]
    assert any("invariant_violation" in str(m.get("output") or m) for m in msgs)


def test_generator_exception_returns_stack_only():
    invariants = {"version": 1}

    def gen(prompt: str):
        raise ValueError("boom")

    def ver(out):
        return True, (1.0, "ok")

    ag = Agent("err", gen, ver, max_iterations=1, guardrails=Guardrails())
    res = ag.run("y", invariants=invariants)
    assert res["ok"] is False
    assert "error_stack" in res and isinstance(res["error_stack"], str)
    # preserves invariants only in the payload (no generated result)
    assert res.get("invariants") == invariants
