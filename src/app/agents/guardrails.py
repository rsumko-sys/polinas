from __future__ import annotations

import logging
from typing import Any, List, Optional


class Guardrails:
    """Simple guardrails implementation to filter dangerous outputs.

    This is a lightweight, local-only sandbox: it is not a replacement for
    production-grade guardrail systems (NeMo Guardrails, GuardrailsAI), but it
    demonstrates the pattern and enforces simple invariants.
    """

    def __init__(self, banned_patterns: Optional[List[str]] = None, max_output_len: int = 10_000) -> None:
        self.banned_patterns = banned_patterns or ["rm -rf", "import os", "__import__", "open(", "subprocess"]
        self.max_output_len = max_output_len
        self.log = logging.getLogger("guardrails")

    def sanitize(self, output: Any) -> Any:
        if isinstance(output, str):
            if len(output) > self.max_output_len:
                self.log.warning("Truncating output exceeding max_output_len")
                return output[: self.max_output_len] + "...[TRUNCATED]"
            for pat in self.banned_patterns:
                if pat in output:
                    self.log.warning("Blocking banned pattern in output: %s", pat)
                    return "[REDACTED:BLOCKED_PATTERN]"
            return output

        if isinstance(output, dict):
            return {k: self.sanitize(v) for k, v in output.items()}
        if isinstance(output, list):
            return [self.sanitize(v) for v in output]
        return output


__all__ = ["Guardrails"]
