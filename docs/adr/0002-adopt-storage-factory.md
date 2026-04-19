# 2. Adopt `Storage` protocol + factory for storage backends

Date: 2026-04-19

Status: Accepted

Context
-------
Multiple storage backends are possible (local FS, S3/MinIO). Consumers need a stable API and we must avoid import-time failures when optional heavy dependencies are absent.

Decision
--------
Introduce a `Storage` protocol (`src/app/storage/interface.py`) and a `factory.get_storage()` to instantiate the appropriate backend at runtime.

Consequences
------------
- Decouples callers from concrete storage implementations (Factory/Strategy patterns).
- Enables safe fallback to local FS when `boto3`/S3 is unavailable.
- Eases testing by allowing in-memory or stub implementations.

Alternatives considered
-----------------------
- Hard-code a single storage implementation: simpler but brittle and less testable.
