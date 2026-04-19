# Blameless Postmortem Template

Use this template to write a blameless postmortem. Focus on facts, timeline, impact, contributing factors, and action items.

1. Summary
- What happened (one-paragraph summary)
- Impact (users, revenue, duration)

2. Timeline
- Timeline with timestamps (UTC): detection → triage → containment → eradication → recovery → postmortem

3. Root Cause
- Root cause analysis (facts + evidence). Avoid speculation.

4. Contributing Factors
- Systemic issues that made this incident more likely or worse (tests missing, monitoring gaps, single point of failure)

5. Mitigations & Fixes
- Immediate fixes applied during incident

6. Action Items
- Concrete tasks with owners and due dates (e.g., "increase integration timeout to 10s — @alice — 2026-05-01")

7. Lessons Learned
- Operational and engineering learnings

8. Metrics & Follow-up
- How we'll measure the effectiveness of fixes (SLOs, dashboards)
