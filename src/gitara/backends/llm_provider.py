"""Abstract LLM provider interface and a lightweight CPU stub adapter.

This module provides a small, deterministic stub implementation suitable for
local development and unit tests. Replace `LlamaCppProvider` with a real
integration to `llama.cpp`, `vLLM`, or another inference backend when ready.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
import re


class LLMProvider(ABC):
    @abstractmethod
    def generate_commit_message(self, diff_text: str, examples: Optional[List[Dict]] = None, **kwargs) -> str:
        """Generate a commit message from unified diff text.

        Args:
            diff_text: The git-style diff text.
            examples: Optional few-shot examples.

        Returns:
            A short commit message string.
        """


class LlamaCppProvider(LLMProvider):
    """Lightweight deterministic CPU stub (placeholder for llama.cpp).

    This implementation intentionally avoids heavy ML deps so it can be used
    reliably in CI and unit tests as a deterministic provider.
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path

    def generate_commit_message(self, diff_text: str, examples: Optional[List[Dict]] = None, **kwargs) -> str:
        # Try to extract a filename from `diff --git a/... b/...` headers
        files = re.findall(r'diff --git a/([^ ]+) b/[^ ]+', diff_text)
        if files:
            basename = files[0].split("/")[-1]
            return f"chore: update {basename}"

        # Fallback: use the first added line (minus leading '+') as a hint
        for line in diff_text.splitlines():
            if line.startswith('+') and not line.startswith('+++'):
                snippet = line[1:].strip().split()
                if snippet:
                    title = " ".join(snippet[:6])
                    return f"chore: update {title}"

        # Last resort deterministic message
        return "chore: update code (auto-generated)"
