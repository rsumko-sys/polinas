# Gitara — Master Plan

Project Vision
--------------
Gitara is a local, privacy-first developer assistant for Git workflows. It runs compact, distilled Small Language Models (SLM) entirely on the user's machine to generate commit messages, assist with diffs, and automate routine Git tasks without sending code to third-party cloud services.

Design Goals
- Privacy: user code never leaves the host machine.
- Low latency: responses < 2s on consumer hardware via quantized SLMs.
- Determinism: clear tests for diff→prompt→commit paths.
- Modular ML backend: swappable adapters for `vLLM`, `llama.cpp`, or HF Transformers.

Quickstart (developer)
----------------------
1. Create a Python venv and install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Run local server (dev):

```bash
export PYTHONPATH=src
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

3. Run tests:

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

Model Architecture (recommended)
--------------------------------
- Target SLMs: Qwen3-0.6B (light) and Qwen3-4B (higher quality)
- Quantization: prefer `fp8` via an automated `llm-compressor` pipeline to reduce memory and enable sub-2s latency on consumer hardware.
- Serving adapters: implement `LLMProvider` (see `src/gitara/llm_provider.py`) with concrete adapters for `vLLM` (GPU), `llama.cpp` (CPU/Apple Silicon), and HF Transformers (fallback).

Data & Prompt Policy
---------------------
- `data/` may only contain curated instruction templates and synthetic few-shot examples.
- Strictly forbid geo/medical/binary datasets inside the main repo; move such files to a separate repository.
- All prompt templates live in `data/templates/` and are versioned.

Repository Layout
-----------------
- `src/` — application and library code (importable)
- `src/gitara/` — core business logic and LLM integration
- `tests/` — unit and integration tests (use pytest)
- `data/` — curated prompts & instruction templates only
- `scripts/` — dev & maintenance scripts (migration, packaging)

Development tooling
-------------------
- `mypy` (strict) for static typing
- `ruff`, `black`, `isort` for linting and formatting
- `pre-commit` hooks: `detect-secrets`, `check-added-large-files`
- CI: GitHub Actions runs `mypy`, `ruff`, `pytest`, `detect-secrets` scan

Sanitization & Archival
-----------------------
Non-code artifacts (HTML maps, SVG telemetry, medical notes) must not remain in the repo. Use the included archiving helper:

```bash
bash scripts/archive_artifacts.sh
```

This moves artifacts into a local `archives/` directory (gitignored). To preserve artifacts permanently, copy them into a dedicated repo such as `polinas-maps`.

Acceptance Criteria
-------------------
- `README.md` + `DATA_POLICY.md` + `SECURITY.md` exist and describe the project intent and constraints.
- No unrelated `.html/.svg/.geojson` files exist in `git ls-files` for the main repo.
- `mypy` passes in `strict` mode for the public interfaces between `git` parsing and `LLMProvider`.
- CI pipeline enforces `detect-secrets` baseline and prevents large weight files being committed.

Next steps
----------
1. Complete repository sanitization and archive non-code artifacts (done via `scripts/archive_artifacts.sh`).
2. Implement `LLMProvider` adapter interface and initial `llama.cpp` adapter in `src/gitara/`.
3. Harden `pre-commit` and CI to enforce `mypy strict`, `ruff`, `black`, and `detect-secrets` scans.

Contact & Governance
--------------------
Create `CONTRIBUTING.md` and `SECURITY.md` documenting expected contributor behavior and secret reporting.
