from __future__ import annotations

import time
import logging
from typing import Callable, Any, List, Dict, Optional, Tuple
from copy import deepcopy
import traceback

try:
    from app.agents.invariants import InvariantStore  # type: ignore
except Exception:
    InvariantStore = None

try:
    from app.agents.guardrails import Guardrails  # type: ignore
except Exception:
    Guardrails = None

Generator = Callable[[str], Any]
Verifier = Callable[[Any], Tuple[bool, Any]]


class Agent:
    """Lightweight agent framework implementing generate-then-verify.

    Principles applied:
    - Separation: generator (stimulation) is separated from verifier (validation).
    - Rigor: verifier returns boolean + optional confidence/message.
    - Epistemic aggregation: returned confidence is t-norm (min) of per-iteration confidences.
    - Guardrails: optional sanitizer to block dangerous outputs.
    - Iteration limits + idempotence checks to ensure bounded behaviour.
    """

    def __init__(
        self,
        name: str,
        generator: Generator,
        verifier: Verifier,
        max_iterations: int = 3,
        guardrails: Optional[Guardrails] = None,
    ) -> None:
        self.name = name
        self.generator = generator
        self.verifier = verifier
        self.max_iterations = max_iterations
        self.guardrails = guardrails
        self.log = logging.getLogger(f"agent.{name}")
        self.trace: List[Dict[str, Any]] = []
        self._last_result: Optional[Any] = None

    def _record(self, role: str, output: Any) -> None:
        self.trace.append({"timestamp": time.time(), "role": role, "output": deepcopy(output)})

    def run(self, prompt: str, invariants: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run the agent with a `generate -> verify` loop.

        Returns a dict containing at least: `result`, `ok`, `confidence`, `trace`.
        """
        confidences: List[float] = []
        last_generated: Any = None
        invariant_store = InvariantStore(invariants) if (InvariantStore is not None and invariants) else None

        for i in range(1, max(1, int(self.max_iterations)) + 1):
            # Generation (stimulation)
            try:
                gen_out = self.generator(prompt)
            except Exception:
                stack = traceback.format_exc()
                # record minimal generate exception trace and return safe error payload
                self._record("generate_exception", stack)
                return {"ok": False, "error_stack": stack, "invariants": invariants or {}, "trace": list(self.trace)}

            # Guardrails sanitize output before verification
            if self.guardrails is not None:
                try:
                    gen_out = self.guardrails.sanitize(gen_out)
                except Exception:
                    self.log.exception("guardrails failed during sanitize")

            self._record("generate", gen_out)
            last_generated = deepcopy(gen_out)

            # Invariant check: fail fast if generated output modifies protected invariants
            if invariant_store is not None:
                ok_inv, mismatches = invariant_store.check(gen_out)
                if not ok_inv:
                    msg = f"invariant_violation: modified keys {mismatches}"
                    confidences.append(0.0)
                    self._record("verify", {"ok": False, "message": msg, "confidence": 0.0})
                    # continue to next iteration to allow retry
                    continue

            # Verification
            try:
                ok, info = self.verifier(gen_out)
            except Exception:
                stack = traceback.format_exc()
                self._record("verify_exception", stack)
                # For verifier exceptions we return a minimal payload (only stack + invariants)
                return {"ok": False, "error_stack": stack, "invariants": invariants or {}, "trace": list(self.trace)}

            # Interpret verifier info: support (confidence, message) or simple message
            if isinstance(info, tuple) and isinstance(info[0], (int, float)):
                conf = float(info[0])
                message = info[1] if len(info) > 1 else ""
            else:
                conf = 1.0 if ok else 0.0
                message = str(info)

            confidences.append(conf)
            self._record("verify", {"ok": ok, "message": message, "confidence": conf})

            # If verifier reports ok, double-check invariants still hold (defense-in-depth)
            if ok and invariant_store is not None:
                ok_inv, mismatches = invariant_store.check(gen_out)
                if not ok_inv:
                    ok = False
                    message = f"invariant_violation_after_verify: modified keys {mismatches}"
                    # record the change
                    confidences.append(0.0)
                    self._record("verify", {"ok": False, "message": message, "confidence": 0.0})
                    # continue loop
                    continue

            if ok:
                # Idempotence guard: if same as last successful result, short-circuit
                result_copy = deepcopy(last_generated)
                if self._last_result is not None and self._last_result == result_copy:
                    # already had this result
                    return {"result": result_copy, "ok": True, "confidence": float(min(confidences)), "trace": list(self.trace)}
                self._last_result = deepcopy(result_copy)
                return {"result": result_copy, "ok": True, "confidence": float(min(confidences)), "trace": list(self.trace)}

            # not ok -> iterate again (generate a new proposal)

        # exhausted iterations
        return {"result": deepcopy(last_generated), "ok": False, "confidence": float(min(confidences)) if confidences else 0.0, "trace": list(self.trace), "error": "verification_failed"}


__all__ = ["Agent"]
