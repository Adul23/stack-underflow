# Contributing to Stack Underflow

Thank you for your interest in Stack Underflow! We are building an open-source Q&A platform where university students can share knowledge, ask technical questions and help each other. Both developers and non-developers are welcome to contribute.

## Table of Contents

- [Maintainers](#maintainers)
- [Before you start](#before-you-start)
- [Types of contributions](#types-of-contributions)
- [Local setup](#local-setup)
- [Branch naming](#branch-naming)
- [Commit style](#commit-style)
- [Backend changes](#backend-changes)
- [Frontend changes](#frontend-changes)
- [Database and analytics changes](#database-and-analytics-changes)
- [Documentation changes](#documentation-changes)
- [Pull request flow](#pull-request-flow)
- [Reporting bugs and requesting features](#reporting-bugs-and-requesting-features)
- [Security and privacy](#security-and-privacy)

## Maintainers

| Maintainer | Responsibilities |
|---|---|
| Boris Dubovoy | Issue coordination, contribution review and project decisions |
| Adil Yergazy | Issue coordination, contribution review and project decisions |

The maintainers review pull requests and make final merge decisions. External contributors can propose changes through issues and pull requests.

## Before you start

- Read the [README](README.md) for project scope and installation instructions.
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md).
- Check the [existing issues](https://github.com/Adul23/stack-underflow/issues) before starting work.
- Only submit work you have the right to contribute. Contributions are intended to be distributed under the project's [MIT License](LICENSE).
- Keep each pull request focused on one problem.

## Types of contributions

| Type | Examples |
|---|---|
| Bug fixes | Incorrect search results, broken tag filters, login errors |
| New features | Improvements to question browsing or student collaboration |
| Backend | API validation, permissions, Django models and tests |
| Frontend | Angular components, accessibility and responsive layouts |
| Database | PostgreSQL indexes, query performance and migrations |
| Analytics | Event counting, reporting queries and staff dashboard improvements |
| Documentation | Installation instructions, API examples and user guides |
| Testing | Reproduction steps, regression tests and usability feedback |

You do not need programming experience to report a bug, improve instructions or suggest a usability improvement.

## Local setup

Requirements: Python 3.12, Node.js 18 with npm, Git and Docker Compose. The following commands use a POSIX-compatible shell.

Fork the [repository](https://github.com/Adul23/stack-underflow) on GitHub, then replace `YOUR_USERNAME` with your GitHub username:

```bash
git clone https://github.com/YOUR_USERNAME/stack-underflow.git
cd stack-underflow
git remote add upstream https://github.com/Adul23/stack-underflow.git
```

Create a local environment file only if one does not already exist:

```bash
test -f backend/.env || cp backend/.env.example backend/.env
python3 -c 'import secrets; print(secrets.token_urlsafe(48))'
```

Set `STACK_UNDERFLOW_SECRET_KEY` to the generated value and choose a private `DB_PASSWORD` in `backend/.env`. Follow the local database settings in the [README](README.md#local-setup-with-postgresql). Never commit the environment file.

Start PostgreSQL and Django from the repository root:

```bash
docker compose --env-file backend/.env up -d db
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements/base.txt
cd backend
python manage.py check
python manage.py migrate
python manage.py runserver
```

In another terminal, from the repository root:

```bash
cd frontend
npm ci
npm start
```

| Service | Local address |
|---|---|
| Angular application | http://localhost:4200 |
| Django API documentation | http://127.0.0.1:8000/api/docs/ |
| Django admin | http://127.0.0.1:8000/admin/ |

See the README for Docker backend setup, demo data and optional superuser creation. The legacy chat and worker services are not required for the MVP.

## Branch naming

Use the following naming convention for new contributions:

| Type | Pattern | Example |
|---|---|---|
| Feature | `feat/<description>` | `feat/question-filters` |
| Bug fix | `fix/<description>` | `fix/search-tags` |
| Documentation | `docs/<description>` | `docs/installation` |
| Tests | `test/<description>` | `test/search-regression` |
| Refactoring | `refactor/<description>` | `refactor/question-service` |
| Maintenance | `chore/<description>` | `chore/update-dependencies` |

Start from the latest upstream `main`:

```bash
git fetch upstream
git switch -c fix/search-tags upstream/main
```

## Commit style

Use [Conventional Commits](https://www.conventionalcommits.org/) for new changes:

```text
<type>(<optional scope>): <short summary>
```

Examples:

```text
feat(questions): add a new question filter
fix(search): handle empty search terms
docs: clarify PostgreSQL setup
test(analytics): cover event counting
refactor(api): simplify question validation
chore: update dependencies
```

Use one commit per logical change. Avoid unrelated formatting changes and do not include credentials or generated build files.

## Backend changes

The backend uses Django and Django REST Framework.

| Directory | Purpose |
|---|---|
| `backend/apps/users/` | User accounts and authentication |
| `backend/apps/questions/` | Questions and search |
| `backend/apps/tags/` | Tags and categorization |
| `backend/apps/comments/` | Comments |
| `backend/apps/analytics/` | Usage analytics |
| `backend/tests/` | Automated backend tests |

When changing backend code:

- Follow existing Python and Django conventions.
- Validate input and preserve authentication and permission checks.
- Add regression tests for bug fixes and tests for new behavior.
- Include Django migrations when changing models.
- Update API documentation when changing request or response formats.

With the virtual environment active, run from `backend/`:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python -m pytest tests/MVPTests.py tests/QuestionsTests.py tests/SearchTests.py tests/SeedBulkTests.py tests/UsersTests.py tests/TagsTests.py tests/CommentsTests.py -q
```

For analytics changes, also run:

```bash
python -m pytest tests/AnalyticsTests.py tests/SeedAnalyticsTests.py -q
```

The PostgreSQL test user needs permission to create a test database. Legacy chat tests are outside the MVP checks above. Report any failed or unavailable checks in the PR.

## Frontend changes

The frontend uses Angular and TypeScript.

| Directory | Purpose |
|---|---|
| `frontend/src/app/components/` | User interface components |
| `frontend/src/app/services/` | Application services and API calls |
| `frontend/src/app/directives/` | Angular directives |
| `frontend/src/app/utils/` | Shared utilities |

Keep components focused, use existing services and avoid unnecessary dependencies. Check loading, empty and error states. Use accessible labels, keyboard navigation and readable layouts. Do not hard-code production API URLs or secrets.

From `frontend/`, run:

```bash
npm ci
npm run build
npm test -- --watch=false --browsers=ChromeHeadless --include=src/app/components/questions/questions.component.spec.ts --include=src/app/app.component.spec.ts
```

Chrome is required for browser tests. The production build may require internet access for Google Fonts. Run additional relevant specs when changing other components. The current package does not define an `npm run lint` script.

## Database and analytics changes

- Use migrations for schema changes rather than undocumented manual edits.
- Test changes against PostgreSQL using local or synthetic data.
- Explain the purpose of new indexes and include `EXPLAIN ANALYZE` evidence for performance claims.
- Preserve existing analytics definitions or document intentional changes to counting rules.
- Keep staff-only analytics protected by appropriate permissions.
- Never include real user data in examples, screenshots or test fixtures.

Relevant references: [database schema](docs/database_schema.md), [performance measurements](docs/explain_analyze.md), [analytics documentation](docs/analytics.md) and [analytics SQL](docs/analytics_queries.sql).

## Documentation changes

Documentation contributions are welcome even without code changes.

- Use clear English and descriptive headings.
- Use relative links for files inside the repository.
- Verify commands against the current application and dependencies.
- Clearly separate implemented features from planned improvements.
- Keep README, API descriptions and technical documentation consistent with code changes.
- Remove secrets and personal information from screenshots.

## Pull request flow

1. Find or open an issue and comment that you would like to work on it.
2. Fork the repository and create a branch from upstream `main`.
3. Implement a focused change and update relevant documentation and tests.
4. Run the relevant checks and review your diff.
5. Commit and push your branch:

```bash
git status
git diff
git add <changed-files>
git commit -m "fix(search): handle empty search terms"
git push -u origin fix/search-tags
```

Replace `<changed-files>` with the actual paths before running the command.

6. Open a pull request from your fork into `Adul23/stack-underflow:main`.
7. Respond to review comments and make requested changes.
8. A maintainer decides whether the contribution is ready to merge.

### Pull request description example

```markdown
## Summary
Fix empty search terms in the question list.

## Related issue
Closes #12

## Changes
- Handle empty search input.
- Add a regression test.

## Testing
- List the commands actually run and their results.
- Explain any checks that could not be completed.

## Screenshots
Add screenshots if the user interface changed.
```

The issue number above is illustrative; use the actual issue number or omit it.

### Review checklist

- [ ] The change addresses a clear problem.
- [ ] Unrelated changes are excluded.
- [ ] Relevant tests and documentation are updated.
- [ ] Test results and limitations are reported honestly.
- [ ] No secrets or personal data are included.
- [ ] The contribution follows the license and Code of Conduct.

## Reporting bugs and requesting features

For a bug, open an issue with a descriptive title, reproduction steps, expected behavior, actual behavior, environment details and sanitized screenshots or logs when useful.

For a feature request, describe the problem, intended users, proposed solution and possible alternatives. Discuss larger changes with maintainers before implementing them.

## Security and privacy

Do not report sensitive vulnerabilities or exposed credentials in public issues or pull requests. Contact a maintainer privately instead. A dedicated private reporting channel still needs to be established; if you cannot reach a maintainer privately, do not publish sensitive details while arranging contact.

See [PRIVACY.md](PRIVACY.md) for data handling and planned privacy improvements. Follow the [Code of Conduct](CODE_OF_CONDUCT.md) in all project interactions.

Thank you for helping make Stack Underflow a more useful, accessible and welcoming educational project.
