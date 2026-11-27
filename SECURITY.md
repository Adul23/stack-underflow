# Security Policy

Stack Underflow aims to provide a safe educational Q&A environment. This policy explains how to report vulnerabilities, how maintainers should handle reports, and how to configure the application securely.

## Supported versions

| Version | Support |
|---|---|
| Current `main` branch | Intended target for security fixes |
| Older commits and legacy prototypes | No dedicated security maintenance promised |

This is a student-maintained project. No guaranteed response time or long-term support schedule has been established.

## Reporting a vulnerability

Report suspected vulnerabilities privately to the maintainers listed in [CONTRIBUTING.md](CONTRIBUTING.md).

If GitHub private vulnerability reporting is enabled, use the repository's **Security → Report a vulnerability** option. Otherwise, request a private contact from a maintainer without disclosing the vulnerability publicly. A dedicated reporting address has not yet been confirmed.

Include:

- A short description and affected component or commit.
- Steps to reproduce the issue in a local or authorized test environment.
- Expected and actual behavior, and possible impact.
- Sanitized logs or screenshots, if useful.
- A suggested fix, if available.

Do not include real credentials, JWT tokens, personal records or production database dumps. Do not open a public issue containing an unpatched vulnerability or sensitive information.

## Scope and responsible testing

Relevant issues include authentication failures, unauthorized access to accounts or analytics, broken ownership checks, injection, unsafe content rendering, exposed secrets and insecure deployment settings.

Test only your own local instance or systems where you have explicit permission. Use synthetic accounts and data. Do not access other users' records, disrupt services or test third-party infrastructure without authorization.

## Vulnerability handling

The following is the proposed maintainer workflow:

1. Acknowledge the report privately when available.
2. Reproduce the issue safely and assess its impact.
3. Restrict exposure and rotate affected credentials if necessary.
4. Prepare a focused fix and regression tests.
5. Review and release the fix; notify affected operators where appropriate.
6. Coordinate disclosure with the reporter after remediation, without exposing personal data.

The team should prioritize unauthorized access, credential exposure and risks to user data. No fixed remediation deadline or bug bounty is promised.

## Application security controls

| Area | Current documented control |
|---|---|
| Authentication | JWT authentication and Django password hashing |
| Passwords | Django password validators |
| Analytics | Staff-only summary endpoint using `IsAdminUser` |
| Secrets | Private environment configuration; placeholder `.env.example` |
| Database | PostgreSQL for production deployments |
| Production settings | `DEBUG=False`, HTTPS, explicit allowed hosts and CORS origins |

These controls are not a substitute for a full security audit. Production configuration and the complete authorization behavior have not been independently verified.

## Secure deployment checklist

Before publishing an instance:

- [ ] Generate a unique `STACK_UNDERFLOW_SECRET_KEY` and strong database credentials.
- [ ] Keep `.env`, database URLs, tokens and backups out of Git and container images.
- [ ] Use production settings with `DEBUG=False` and PostgreSQL.
- [ ] Configure `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` for the actual deployment.
- [ ] Use HTTPS for the frontend and API; configure `SECURE_SSL_REDIRECT` appropriately.
- [ ] Enable `TRUST_PROXY_HTTPS` only when the trusted proxy replaces incoming forwarded protocol headers correctly.
- [ ] Restrict database and administrator access; use separate accounts where practical.
- [ ] Review dependencies, protect backups and test recovery.
- [ ] Verify ordinary users cannot access staff-only analytics or modify other users' content.
- [ ] Review whether demo seeding is appropriate; disable it with `SEED_DEMO_DATA=False` if not needed.

See [docs/deployment.md](docs/deployment.md) for configuration details.

## Security checks for contributors

Run the relevant checks from the configured backend environment:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python -m pytest tests/AnalyticsTests.py -q
```

Run `python manage.py check --deploy` against production settings in a safe environment. Review warnings before deployment. From `frontend/`, run `npm run build` and review dependency audit results with `npm audit`.

Add regression tests for changed permissions, validation and authentication behavior. These commands are recommended checks, not evidence that the current release has passed a security audit. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution workflow.

## Security improvement roadmap

| Improvement | Status |
|---|---|
| Confirm private vulnerability reporting channel | Proposed |
| Automated dependency and secret scanning | Proposed |
| Expanded authorization and abuse-prevention tests | Proposed |
| Production security review and backup recovery test | Proposed |
| Incident response and privacy request procedures | Proposed |

## Related policies

- [Privacy and Data Security](PRIVACY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contribution Guidelines](CONTRIBUTING.md)
- [Deployment Guide](docs/deployment.md)

This policy supports the project's DPG privacy and safety goals. It does not claim official DPG certification or guarantee that the application is free of vulnerabilities.
