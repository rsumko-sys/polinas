Repository artifact archive

The repository previously contained several non-code artifacts (HTML maps, SVG telemetry)
that are semantically unrelated to the Gitara project and present a risk of poisoning
model training data. Those files have been moved into the local `archives/` directory
by `scripts/archive_artifacts.sh`.

Notes:
- The `archives/` directory is ignored by Git (see `.gitignore`) and is intended as a
  temporary holding area for migration. Move valuable artifacts to a separate repo
  (e.g., `polinas-maps`) if they must be preserved under version control.
- To re-run the archival step locally, run:

```bash
bash scripts/archive_artifacts.sh
```

The script records the last archive path in `.last_archive`.
