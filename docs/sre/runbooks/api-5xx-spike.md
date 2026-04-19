# Runbook: API 5xx Spike

Alert trigger
- Name: `API_5xx_Spike`
- Expression: `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05`
- Severity mapping: SEV2 if >5% for 5m; SEV1 if >10% or impacting >10% of users

Symptoms
- Increased 5xx responses across multiple endpoints; key customer flows failing; spike seen in Grafana panel `API / 5xx %`

Verification
1. Confirm alert in Grafana/Prometheus.
2. Check logs for common error signatures: timeouts, upstream 502/504, exceptions with stack traces.
3. Determine scope: single endpoint, service-wide, region-specific.

Immediate Containment (fast, reversible)
1. Redirect traffic to legacy or stable version:
   - If using gateway feature flag: set `USE_LEGACY=true` in an override env and restart (see `scripts/incident/set_env_override.py`).
2. Disable non-critical downstream integrations (Notion, S3 metadata sync): set `NOTION_TOKEN=` and/or `S3_ENABLED=false` in override env.
3. Scale replicas to absorb load: `docker-compose up -d --scale web=3` or `kubectl scale deployment/web --replicas=3`.

Containment verification
- Expect 5xx rate to drop within 2–5 minutes after restart/flag flip. Watch Grafana panel and logs.

Eradication
1. Collect artifacts (see `scripts/incident/collect_artifacts.sh`): recent logs, slow traces, recent deploys, config changes.
2. Check recent deploys: `git log -n 5 --pretty=oneline` and CI/CD deploy timestamps.
3. Inspect third-party responses (Notion/S3 latency/errors). If downstream system reports issues, coordinate with provider.
4. If error is code-related, produce minimal reproducer and prepare hotfix rollback or patch.

Recovery
1. Deploy fix to canary / staging; monitor for errors.
2. Gradually revert containment (unset `USE_LEGACY`, re-enable Notion) once stable for 30m.

Post-Incident
1. Open postmortem using `docs/sre/postmortem-template.md`.
2. Add action items with owners and due dates. Prioritize fixes that reduce blast radius.

Commands & snippets (examples)
- Write an override env (safe — does not edit production env in-place):
  - `python3 scripts/incident/set_env_override.py NOTION_TOKEN ''`
  - Then restart via Docker Compose: `docker-compose restart web`

- Collect docker logs (example):
  - `docker-compose logs --tail 500 web > /tmp/web.logs.txt`

- Kubernetes example (inspect pods):
  - `kubectl get pods -A | grep web`
  - `kubectl logs deployment/web -n prod --tail=200`
