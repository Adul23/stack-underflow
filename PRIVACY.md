# Privacy and Data Security

Stack Underflow is an open-source educational Q&A platform. This policy explains what data the application stores, why it is needed, how it is protected, and which privacy improvements are still planned. It supports DPG criterion 7 (Privacy and Data Security).

## Table of Contents

- [Data we collect](#data-we-collect)
- [Usage analytics](#usage-analytics)
- [Data access and sharing](#data-access-and-sharing)
- [Data protection](#data-protection)
- [Retention and user requests](#retention-and-user-requests)
- [Independent deployments](#independent-deployments)
- [Privacy roadmap](#privacy-roadmap)
- [Contact](#contact)

## Data we collect

| Data | Purpose | Visibility |
|---|---|---|
| Email, first name and last name | Account registration and identification | Account data; administrators may access records |
| Password hash | Authentication | Backend only; passwords must not be published |
| Optional avatar, language and timezone | Profile and preferences | Depends on the profile interface |
| Questions, tags and comments | Knowledge sharing and discussion | Public forum content |
| Usage events | Understand search and question activity | Restricted analytics access |

Passwords are stored as hashes using Django's password handling, not as plain text. Users should not include private information, credentials or other people's personal data in questions, comments or search queries.

## Usage analytics

Analytics is stored in the application's database rather than sent to a separate analytics service.

| Event | When recorded |
|---|---|
| `search` | A nonempty keyword search, including suggestion requests |
| `question_view` | A successful question detail request |
| `question_created` | Successful question creation by an authenticated user |

Events may include a timestamp, user ID (when authenticated), question ID, search text (up to 255 characters), session UUID and limited backend-generated metadata such as search source and tag filter.

The Angular application generates a random session UUID in `sessionStorage` for the current browser tab. It sends this identifier to the configured API through `X-Session-ID`. The identifier survives reloads in the same tab. Requests without it can still work.

Analytics does not intentionally copy passwords, JWT tokens, email fields, request bodies or arbitrary headers. However, search text is stored as entered within the length limit, so it may contain personal information if a user types it. Session IDs and user IDs are not a guarantee of anonymity.

The staff-only analytics dashboard displays aggregate event totals and popular questions. Counts represent requests, not necessarily unique people. Synthetic demo events must not be treated as real user activity.

See [analytics documentation](docs/analytics.md) for fields and counting rules.

## Data access and sharing

- Forum content is visible to other users. Do not treat posts as private messages.
- Django admin restricts access to authorized staff; the analytics summary API explicitly requires staff access.
- The project policy is not to sell user data or use it for advertising. This is a policy commitment, not an independently audited guarantee.
- Hosting and database providers may process data as part of operating a deployment. The operator must explain any such arrangements to users.
- The existing frontend uses an external Google Fonts stylesheet. External resource requests may disclose connection information to the provider. Self-hosting fonts is a proposed improvement.

## Data protection

| Measure | Status |
|---|---|
| Django password hashing and password validators | Documented application controls |
| JWT authentication | Implemented authentication mechanism |
| Staff-only analytics summary | Implemented API permission check |
| Private `.env` and placeholder `.env.example` | Documented configuration practice |
| HTTPS, `DEBUG=False`, restricted allowed hosts and CORS origins | Production configuration requirements; live deployment not verified |
| Backup protection and access reviews | Recommended operational controls; not verified |

Operators should restrict database access, protect backups, rotate exposed secrets and keep dependencies updated. See [SECURITY.md](SECURITY.md) and [deployment instructions](docs/deployment.md).

## Retention and user requests

The project does not currently document an enforced automatic retention period for analytics. A six-month retention period is proposed, subject to team approval and implementation.

Self-service account deletion and automated personal-data removal are not yet confirmed as implemented. Users may contact the maintainers or deployment operator to request access, correction or deletion of their data. The operator should verify the requester's identity privately and explain what can be removed, including any limitations involving public posts, historical events or backups.

Never submit personal records, passwords or identity documents in public GitHub issues.

## Independent deployments

The MIT license allows others to run their own instances. Each operator is responsible for its own privacy notice, access permissions, hosting arrangements, retention rules and applicable legal requirements. This document does not establish legal compliance for every deployment.

## Privacy roadmap

| Improvement | Status |
|---|---|
| Privacy notice on registration | Planned |
| Self-service account deletion | Planned |
| Automatic analytics retention (proposed six months) | Planned |
| Private contact for privacy requests | To be confirmed |
| Review external resources and self-host fonts where practical | Proposed |
| Review production access, backups and deletion procedures | Proposed |

## Contact

Contact the maintainers listed in [CONTRIBUTING.md](CONTRIBUTING.md). A dedicated private reporting channel has not yet been confirmed. Ask for a private contact without publishing sensitive details. For vulnerabilities, follow [SECURITY.md](SECURITY.md).

This policy describes the current documented project and proposed improvements; it does not claim that Stack Underflow is officially certified as a Digital Public Good.
