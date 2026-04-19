# 4. Use Strangler Fig via an API Gateway for incremental migration

Date: 2026-04-19

Status: Proposed

Context
-------
We will incrementally replace legacy monolith behavior with new modular services. To avoid a Big Bang rewrite, we need a routing/facade layer that can route requests to the legacy implementation or the new module.

Decision
--------
Introduce a lightweight gateway/dispatch layer (see `src/app/gateway.py`) that can route specific API calls to legacy or new implementations. Feature toggles (headers or environment variables) will control routing.

Consequences
------------
- Allows gradual extraction of functionality from the monolith.
- Enables live traffic splitting and rollback by switching a header or environment flag.

Alternatives considered
-----------------------
- Do a single Big Bang rewrite and cutover: high risk, long downtime.
