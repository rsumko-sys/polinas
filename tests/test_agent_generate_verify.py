import pytest

from app.agents.agent_core import Agent
from app.agents.guardrails import Guardrails


def test_generate_then_verify_success():
    calls = {"i": 0}

    def generator(prompt: str) -> str:
        calls["i"] += 1
        if calls["i"] == 1:
            return "intermediate"
        return "final_ok"

    def verifier(output: str):
        if "final_ok" in output:
            return True, (0.9, "good")
        return False, (0.1, "not ready")

    ag = Agent("test1", generator, verifier, max_iterations=3, guardrails=Guardrails())
    res = ag.run("do work")
    assert res["ok"] is True
    # confidence is min(0.1, 0.9) == 0.1 (t-norm: min)
    assert pytest.approx(res["confidence"], rel=1e-6) == 0.1
    assert "trace" in res and len(res["trace"]) >= 2


def test_iteration_limit_and_failure():
    def gen(prompt: str) -> str:
        return "bad"

    def ver(output: str):
        return False, (0.0, "always fail")

    ag = Agent("test2", gen, ver, max_iterations=2, guardrails=Guardrails())
    res = ag.run("x")
    assert res["ok"] is False
    # generator+verifier entries per iteration
    assert len(res["trace"]) == 4


def test_guardrails_blocking():
    def gen(prompt: str) -> str:
        return "rm -rf /tmp"

    def ver(output: str):
        # verifier should see the sanitized output
        if "BLOCKED_PATTERN" in output:
            return False, (0.0, "blocked")
        return True, (1.0, "ok")

    ag = Agent("test3", gen, ver, max_iterations=1, guardrails=Guardrails())
    res = ag.run("y")
    assert res["ok"] is False
    assert "REDACTED" in str(res["result"]) or res["result"] == "[REDACTED:BLOCKED_PATTERN]"
