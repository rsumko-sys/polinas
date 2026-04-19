from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class R2DC2:
    """Build prompts using the R²DC² (Role, Result, Goal, Constraint, Context) pattern.

    This lightweight builder produces structured prompts useful for agentic tasks
    and testable generation/verification flows.
    """

    role: str
    result: str
    goal: str
    constraints: List[str] = field(default_factory=list)
    context: Optional[str] = None
    language: str = "uk"

    def build(self) -> str:
        parts: List[str] = []
        parts.append(f"Role: {self.role}")
        parts.append(f"Result: {self.result}")
        parts.append(f"Goal: {self.goal}")
        if self.constraints:
            parts.append("Constraints:")
            for c in self.constraints:
                parts.append(f"- {c}")
        if self.context:
            parts.append("Context:")
            parts.append(self.context)
        parts.append("Invariants: Do not modify the invariants provided in Context.")
        return "\n".join(parts)


__all__ = ["R2DC2"]
