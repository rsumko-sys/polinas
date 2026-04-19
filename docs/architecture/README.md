# Architecture (C4 + Supporting Docs)

This folder contains architecture-as-code and supporting docs.

- `structurizr.dsl`: a minimal starting workspace for C4 diagrams (Context & Container).
- `README.md`: guidance on what to capture in each C4 level.

Recommended workflow:

1. Keep C4 diagrams in `structurizr.dsl` and generate visualizations with Structurizr CLI.
2. Use ADRs in `docs/adr/` to record decisions.
3. Add fitness tests under `tests/` to codify architectural constraints.
