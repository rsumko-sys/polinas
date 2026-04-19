# Data Policy for Gitara

Purpose
-------
This document defines what data may be stored in the Gitara repository, how it
must be curated, and how to handle any artifacts that are unrelated to the
project's purpose (for example: maps, telemetry, medical notes).

Scope
-----
- Allowed in-repo: source code (`src/`), deterministic test fixtures in `tests/`,
  small instruction templates and prompt examples in `data/instructions/` or
  `data/templates/` that have been sanitized from PII/PHI and proprietary data.
- Disallowed in-repo: uncurated external datasets, geospatial HTML/SVG files,
  telemetry routes, medical records, proprietary model weights, and any
  binary model checkpoint files (e.g. `*.gguf`, `*.safetensors`, `*.pt`,
  `*.bin`). These must not be committed.

Archival and migration
----------------------
- If you discover files that belong to other projects (e.g., `kharkiv_horse_clubs_map.html`),
  move them to a dedicated archive folder outside the repository, or to a
  separate repository (example: `polinas-maps`). Use `scripts/archive_artifacts.sh`
  to perform safe archival.
- The `archives/` directory in this repository is a temporary holding area and is
  gitignored; it is not a long‑term storage solution. Move artifacts to a
  dedicated artifact repo or object store (S3/MinIO/DVC) if they must be preserved.

Data curation process (recommended)
-----------------------------------
1. Inspect: identify source, licenses and sensitivity (PII/PHI).
2. Sanitize: remove or redact PII/PHI; anonymize where appropriate.
3. Validate: run automated checks for file types, sizes and suspicious tokens.
4. Human review: a human must review curated data before it is used for
   fine-tuning or included in `data/` inside the project.
5. Approve and document provenance: add a short `METADATA.md` describing
   origin, license, cleaning steps and reviewer initials.

Pre-commit and CI enforcement
-----------------------------
- Pre-commit hooks must block commits that add:
  - files matched by `*.html`, `*.svg`, `*.geojson`, `*.shp` at repository root
  - large files above threshold (`check-added-large-files`)
  - secrets discovered by `detect-secrets`
- CI must run `detect-secrets scan --baseline .secrets.baseline.json`,
  and fail if new secrets are detected.

Model weights and publishing
----------------------------
- Large model artifacts must not be stored in the Git repository. Use one of:
  - Artifact registry (GitHub Releases, GitLab Package Registry)
  - Object storage (S3 or MinIO) + DVC or manifest file
- Include checksums and license metadata in the repository (small text files).

Acceptance criteria for data
----------------------------
- No disallowed file types in `git ls-files` output.
- All entries in `data/` are accompanied by `METADATA.md` describing
  provenance and cleaning steps.
- `detect-secrets` baseline updated and CI passes.

Commands and utilities
----------------------
- Archive known artifacts (example):
```bash
bash scripts/archive_artifacts.sh
```
- Find potentially dangerous files:
```bash
git ls-files | egrep '\.(html|svg|geojson|shp|gguf|safetensors|pt|bin)$'
```

Questions about this policy? Create an issue tagged `data-policy`.
