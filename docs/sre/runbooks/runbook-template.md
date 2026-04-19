# Runbook Template

Use this template for any operational alert. Keep instructions concise and repeatable.

## Title
- Short descriptive name for the alert (e.g. API 5xx spike)

## Alert Trigger / Detection
- Alert name: 
- Metric / expression: (e.g. rate(http_requests_total{status=~"5.."}) / rate(http_requests_total) > 0.05 over 5m)
- Alerting system: (Prometheus / Datadog / PagerDuty)

## Symptoms
- What an on-call engineer observes (errors, latency, customer impact)

## Severity (SEV)
- Map to SEV1..SEV4 with clear criteria

## Incident Commander (IC)
- Who to page first, escalation path, Slack/Teams/room channel name

## Verification steps
1. Check dashboard: link to Grafana panel(s)
2. Confirm error logs: `grep "ERROR" /var/log/...` or `docker-compose logs --tail 200 web`
3. Confirm scope: is it single endpoint, single region, or global?

## Immediate Containment (fast, reversible)
- Goal: reduce customer impact quickly. Prefer configuration toggles, traffic routing, or disabling non-critical integrations.
- Example steps (pick the ones relevant):
  - Scale up replicas: `docker-compose up -d --scale web=3` or `kubectl scale deployment/web --replicas=3`
  - Toggle gateway to legacy: set `USE_LEGACY=true` in an override env and restart (see `scripts/incident/set_env_override.py`)
  - Disable Notion integration (set `NOTION_TOKEN=` in override env) to remove downstream 3rd-party failures
  - Put service into read-only mode (if supported)

## Containment verification
1. Check error rate decreased to baseline
2. Monitor latency and user-facing errors

## Eradication (root cause fixes)
- After containment and stabilization: collect artifacts, run root-cause analysis, patch code or infra.
- Common tasks: roll back a deploy, fix a bad DB migration, patch a hot loop, fix credential expiry.

## Recovery
- Gradually revert containment steps once fix is deployed and verified.

## Post-Incident Actions / Postmortem
- File a blameless postmortem in `docs/sre/postmortem-template.md` with timelines, impact, root cause, and action items.
- Create actionable JIRA/GitHub issues for fixes and add to backlog with priority.
