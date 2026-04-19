"""LLM provider abstractions and lightweight adapters.

This module defines a small, well-typed interface `LLMProvider` that the
business logic can call to generate commit messages from diffs. A simple
`StubLLMProvider` is provided as a deterministic, dependency-free fallback
useful for testing and local development.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """Abstract interface for language-model backends used by Gitara.

    Implementations should be lightweight adapters around concrete serving
    frameworks (vLLM, llama.cpp, HF Transformers, etc.).
    """

    name: str = "abstract"

    @abstractmethod
    def generate_commit_message(self, diff_text: str, max_tokens: int = 128, **kwargs: Any) -> str:
        """Return a short commit message derived from `diff_text`.

        Implementations must return a short subject/body string suitable for
        direct use as a git commit message.
        """


class StubLLMProvider(LLMProvider):
    """Deterministic, dependency-free provider for tests and local runs.

    This stub creates a simple commit subject by taking the first non-empty
    meaningful tokenized line from the diff. It is intentionally trivial and
    should be replaced by real adapters for production.
    """

    name = "stub"

    def generate_commit_message(self, diff_text: str, max_tokens: int = 128, **kwargs: Any) -> str:
        if not diff_text:
            return "chore: empty diff"

        # Find a usable line from diff (skip @@ headers and metadata)
        for raw in diff_text.splitlines():
            line = raw.strip()
            if not line:
                continue
            # ignore diff metadata lines
            if line.startswith("@@") or line.startswith("diff --git") or line.startswith("Index:"):
                continue
            # Prefer added lines
            if line.startswith("+"):
                content = line.lstrip("+").strip()
                if content:
                    return f"feat: {content[:max_tokens]}"
            # Fallback to any non-metadata line
            return f"chore: {line[:max_tokens]}"

        return "chore: update"


def get_provider(name: str | None = None) -> LLMProvider:
    """Factory for simple providers.

    Currently only a `StubLLMProvider` is available. This function centralizes
    provider selection and can later instantiate real adapters based on
    configuration.
    """
    if name is None or name == "stub":
        return StubLLMProvider()
    raise ValueError(f"Unknown provider: {name}")
