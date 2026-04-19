# SRE Runbooks & Incident Management

This folder contains runbooks, incident playbooks, postmortem templates and small automation helpers to support on-call responders.

Principles
- Follow the SRE incident lifecycle: Detect → Triage → Contain → Eradicate → Recover → Learn.
- Each alert must link to a runbook with verification and containment steps.
- Use generate-then-verify for automation: scripts should be idempotent and safe by default (no automatic destructive actions).
- Blameless postmortems: focus on systemic fixes, not individuals.

Structure
- `runbooks/` — runbook templates and concrete runbooks for common alerts.
- `postmortems/` — postmortem templates and archived reports.
- `scripts/incident/` — helper scripts for containment and artifact collection (non-destructive by default).

How to use
1. On alert, open the matching runbook in `runbooks/`.
2. Follow the verification steps to confirm the symptom.
3. Execute containment steps (scripts provided are safe; they write an override env file and print recommended restart commands).
4. After service is stable, follow eradication and recovery steps, then create a postmortem in `postmortems/`.
