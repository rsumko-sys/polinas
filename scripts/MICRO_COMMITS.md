Micro Commit Helper
===================

This repository includes a small helper script `scripts/micro_commit.sh` to make quick, small commits of workspace changes.

Usage
-----

Run from the repository root:

```bash
./scripts/micro_commit.sh "your short message"
```

If no message is provided, the script commits with a timestamped message.

Scheduling
----------

To run periodic micro commits locally, add a cron entry (example: hourly):

```cron
0 * * * * cd /path/to/repo && /usr/bin/env bash ./scripts/micro_commit.sh "scheduled micro-commit $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
```

Notes
-----

- Scheduled commits should be used with caution — avoid committing build artifacts or secrets. Ensure `.gitignore` is configured properly.
- Committing automatically from CI is possible (using `GITHUB_TOKEN`), but can create loops and should be designed carefully.
