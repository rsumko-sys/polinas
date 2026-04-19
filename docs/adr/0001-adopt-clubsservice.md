# 1. Adopt `ClubsService` as Information-Expert for club operations

Date: 2026-04-19

Status: Accepted

Context
-------
We have business logic for finding nearest clubs embedded in HTTP handlers (`src/app/main.py`). Tests and UI changes require reusing the logic outside the controller layer and improving testability.

Decision
--------
Create `src/app/services/clubs_service.py` containing `ClubsService` which owns club-related business rules (distance calculation, filtering, sorting).

Consequences
------------
- Controllers become thin: they delegate to `ClubsService` (Controller pattern).
- Code is easier to unit test and reuse from other entry points (CLI, background jobs).
- Follows GRASP Information Expert: the class that has the data/algorithms owns the logic.

Alternatives considered
-----------------------
- Keep logic in controllers (status quo): simpler short-term but increases coupling and makes reuse harder.
- Put logic in `app.data` module: blended concerns; data module should remain passive.

Supersedes
---------
None
