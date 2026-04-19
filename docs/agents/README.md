# Agent Framework & QA Patterns

This folder documents the lightweight agent framework included in the codebase.

Principles
- Generate-then-verify: separate generation (stimulation) from verification (validators/invariants).
- R²DC² prompt engineering: use Role, Result, Goal, Constraints, Context for prompt structure.
- Guardrails: local sanitizers to prevent dangerous outputs; integrate with production guardrail systems for stronger guarantees.
- Iteration limits + idempotence: bound the number of generation attempts and avoid non-deterministic repeated side effects.
- Observability: each agent run produces a trace of generate/verify events for auditing.

Files
- `src/app/agents/agent_core.py` — Agent class implementing the generate-then-verify loop and tracing.
- `src/app/agents/prompt.py` — R2DC2 prompt builder.
- `src/app/agents/guardrails.py` — simple output sanitizer (demo only).

Testing
- See `tests/test_agent_generate_verify.py` for practical examples and invariants.
