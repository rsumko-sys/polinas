# Security Policy for Gitara

Purpose
-------
This document gives quick operational guidance for handling secrets, reporting
vulnerabilities, and responding to incidents related to the Gitara repository.

Reporting vulnerabilities
-------------------------
- If you find a security issue, create a private issue labeled `security` and
  notify the maintainers directly. Do not disclose the issue publicly until it
  has been triaged and a fix has been prepared.

Secret management
-----------------
- Never commit secrets (API keys, tokens, passwords) into the repository.
- Use environment variables, GitHub Secrets, or a secrets manager (Vault).
- Add `.env` to `.gitignore` (already configured).
- Use `detect-secrets` in pre-commit and CI to catch accidental inclusions.

Removing secrets from history
-----------------------------
- If a secret is committed, rotate the secret immediately with the provider
  (AWS, GitHub, third-party) and remove the secret from git history.
- To remove secrets from history safely, prefer `git filter-repo` (recommended)
  over `git filter-branch`. Example:
```bash
pip install git-filter-repo
git filter-repo --invert-paths --paths-forbidden secrets_to_remove.txt
```
- After rewriting history, coordinate with collaborators to reclone or force
  reset local clones. Follow the provider-specific steps to rotate compromised
  tokens.

Pre-commit and CI
-----------------
- Pre-commit hooks include `detect-secrets` and `check-added-large-files` and
  must run locally before pushing.
- CI runs `detect-secrets scan` with the committed baseline and blocks PRs with
  new secrets.

Access control and least privilege
---------------------------------
- Limit access to artifact storage (S3, GHCR) and CI secrets to specific
  service accounts and maintainers. Use short-lived tokens where possible.

Incident response (brief)
-------------------------
1. Triage: identify scope and affected resources.
2. Contain: rotate keys and disable compromised services.
3. Eradicate: remove secrets from history and secure the repo.
4. Recover: restore services with new credentials and monitor logs.
5. Review: produce an incident report and update policies.

Contact
-------
- Create a private issue `security` and ping repository maintainers.
