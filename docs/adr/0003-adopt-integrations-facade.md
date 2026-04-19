# 3. Centralize external integrations behind a Facade

Date: 2026-04-19

Status: Accepted

Context
-------
External systems (Notion, object storage, LLMs) are unstable and may be absent in developer environments. Call sites were scattered across the codebase.

Decision
--------
Create `src/app/integrations/facade.py` providing `IntegrationsFacade` which offers a small, stable API for operations like `create_session_record`, `upload_file`, and `generate_presigned`.

Consequences
------------
- Protects the codebase from churn in third-party clients (Protected Variations).
- Simplifies stubbing/mocking for tests and allows fallbacks in local dev.

Alternatives considered
-----------------------
- Directly import and call each integration client at call sites: leads to duplication and brittle error handling.
