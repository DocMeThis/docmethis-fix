# Security Policy

## Reporting a Vulnerability

Do not open a public issue for a security vulnerability.

Use GitHub's private vulnerability reporting for this repository. Include the
affected public facade revision, runtime commit SHA and artifact SHA-256 when
available, plus a concise impact description and reproduction steps that do not
contain secrets or customer source.

If private reporting is unavailable, contact the DocMeThis maintainers through
the private support channel listed by the organization.

## Secrets

Never commit or paste any of the following into an issue, pull request or
release:

- Gateway keys or bearer tokens;
- private distribution tokens;
- provider API keys;
- signing keys;
- prompts or private source code.
