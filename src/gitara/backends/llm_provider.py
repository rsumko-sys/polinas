"""Abstract LLM provider interface and lightweight adapters.

This module provides a small, deterministic stub implementation suitable for
local development and unit tests (`LlamaCppProvider`) and a thin adapter for
OpenAI (optional runtime dependency). The OpenAI adapter is defensive so the
package can be imported even if the `openai` package is not installed or the
API key is not configured.

Keep this module minimal and deterministic so CI/tests remain stable.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import re
import os

# try to import the OpenAI SDK at runtime; if missing we fall back to the
# deterministic CPU stub implementation below.
try:
    import openai as _openai
except Exception:
    _openai = None


class LLMProvider(ABC):
    @abstractmethod
    def generate_commit_message(self, diff_text: str, examples: Optional[List[Dict[str, object]]] = None, **kwargs: Any) -> str:
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

    def __init__(self, model_path: Optional[str] = None) -> None:
        self.model_path: Optional[str] = model_path

    def generate_commit_message(self, diff_text: str, examples: Optional[List[Dict[str, object]]] = None, **kwargs: Any) -> str:
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


class OpenAIProvider(LLMProvider):
    """Simple OpenAI adapter. If the SDK or API key is not available this
    adapter will fall back to `LlamaCppProvider` to remain deterministic.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._openai = _openai
        if self._openai and self.api_key:
            try:
                # set key if SDK supports it (defensive)
                setattr(self._openai, "api_key", self.api_key)
            except Exception:
                pass

    def generate_commit_message(
        self, diff_text: str, examples: Optional[List[Dict[str, object]]] = None, **kwargs: Any
    ) -> str:
        # If OpenAI SDK isn't present or there's no API key, fall back.
        if not self._openai or not self.api_key:
            return LlamaCppProvider().generate_commit_message(diff_text, examples=examples, **kwargs)

        try:
            prompt = f"Generate a short commit message for the following git diff:\n\n{diff_text}"
            response = self._openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )

            # Defensive extraction of content from response
            choices = getattr(response, "choices", None)
            if not choices:
                return LlamaCppProvider().generate_commit_message(diff_text, examples=examples, **kwargs)

            first = choices[0]
            content = None
            # compatibility with different SDK shapes
            if hasattr(first, "message") and hasattr(first.message, "content"):
                content = first.message.content
            elif isinstance(first, dict):
                msg = first.get("message") or first.get("delta")
                if isinstance(msg, dict):
                    content = msg.get("content") or msg.get("text")
                content = content or first.get("text")

            if content:
                # return first line trimmed
                return str(content).strip().splitlines()[0][:200]

            return LlamaCppProvider().generate_commit_message(diff_text, examples=examples, **kwargs)
        except Exception:
            return LlamaCppProvider().generate_commit_message(diff_text, examples=examples, **kwargs)


def get_default_provider(prefer_openai: bool = True) -> LLMProvider:
    """Return a sensible default provider.

    - If `prefer_openai` and OpenAI SDK + API key are available, return
      `OpenAIProvider`.
    - Otherwise return the deterministic `LlamaCppProvider`.
    """
    if prefer_openai and _openai and os.getenv("OPENAI_API_KEY"):
        return OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    return LlamaCppProvider()


__all__ = ["LLMProvider", "LlamaCppProvider", "OpenAIProvider", "get_default_provider"]
