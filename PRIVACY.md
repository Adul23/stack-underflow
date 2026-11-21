# Privacy and Data Security

This document explains what personal data Stack Underflow stores, how it is
protected, and what we plan to improve.

## What data we store

**Account data** (when a user registers):
- email address, first name and last name
- password, stored only as a hash (Django's `set_password`), never as plain text
- optional: avatar image, preferred language and timezone

**Content data:** questions, tags and comments that users post. This content is
public to other users of the forum.

**Usage analytics** (see [docs/analytics.md](docs/analytics.md)):
- events for searches, question views and question creation
- the search text, a timestamp, and the user ID if the user is logged in
- a random session UUID that the browser creates for the current tab

Analytics does **not** copy passwords, JWT tokens, email addresses, request
bodies or other headers.

## How data is protected

- Login uses JWT tokens. Passwords are checked with Django's password validators.
- Secrets (secret key, database password) are kept in a private `.env` file,
  which is ignored by Git. Only `.env.example` with placeholder values is committed.
- In production the settings in [docs/deployment.md](docs/deployment.md) require
  `DEBUG=False`, HTTPS and a fixed list of allowed hosts and CORS origins.
- Only staff users can see analytics events and user records in Django admin.

## Our plans (not built yet)

- Show a short privacy notice on the sign-up page.
- Let users delete their own account and their personal data.
- Automatically delete analytics events after a fixed period (for example 6 months).
- Never sell or share user data with third parties.

## Contact

If you think your data was handled wrongly, contact the maintainers listed in
[CONTRIBUTING.md](CONTRIBUTING.md).
