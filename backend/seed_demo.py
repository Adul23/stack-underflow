"""Insert repeatable demo questions and tags: python seed_demo.py."""

import os

import django
from decouple import config

DEMO_EMAIL = "demo@stack-underflow.example"
DEMO_TAGS = (
    "python", "django", "postgresql", "angular", "docker", "typescript", "git", "rest-api",
)
DEMO_QUESTIONS = (
    (
        "demo-django-serializers",
        "How do Django REST Framework serializers work?",
        "I am building a Python API with Django REST Framework. How does a ModelSerializer "
        "validate incoming JSON and save a model? When should I call is_valid() and save()?",
        ("python", "django", "rest-api"),
    ),
    (
        "demo-postgresql-unique-constraint",
        "How can I prevent duplicate rows in PostgreSQL?",
        "Two requests can try to register the same email at the same time. I want PostgreSQL "
        "to guarantee uniqueness. How do a UNIQUE constraint and INSERT ON CONFLICT help?",
        ("postgresql",),
    ),
    (
        "demo-angular-component-communication",
        "How can Angular components share data?",
        "A parent Angular component shows a list of questions and a child component contains "
        "the search form. Should I use Input and Output or a shared TypeScript service?",
        ("angular", "typescript"),
    ),
    (
        "demo-docker-postgresql-connection",
        "How do I connect Django to PostgreSQL in Docker Compose?",
        "My Python backend and PostgreSQL run in separate Docker containers. Connecting to "
        "localhost fails. Which hostname should Django use, and how do I wait for the database?",
        ("docker", "postgresql", "django", "python"),
    ),
    (
        "demo-python-virtual-environment",
        "How do I create a Python virtual environment?",
        "I want each Python project to have its own dependencies. How do I create and activate "
        "a virtual environment, install requirements.txt and keep the environment out of Git?",
        ("python", "git"),
    ),
    (
        "demo-django-jwt-authentication",
        "How do access and refresh JWT tokens work in Django?",
        "My Django REST API returns access and refresh tokens after login. What should the "
        "frontend do when an access token expires, and which requests need an Authorization header?",
        ("django", "rest-api", "angular"),
    ),
    (
        "demo-postgresql-left-join",
        "When should I use LEFT JOIN instead of INNER JOIN?",
        "I need a PostgreSQL query that lists every question with its number of comments, "
        "including questions with zero comments. Which JOIN and COUNT expression should I use?",
        ("postgresql",),
    ),
    (
        "demo-angular-search-debounce",
        "How do I debounce an Angular search input?",
        "My Angular search form sends an API request on every keypress. I want to wait 300 ms "
        "after typing and ignore old responses. How can RxJS debounceTime and switchMap help?",
        ("angular", "typescript", "rest-api"),
    ),
    (
        "demo-django-database-migrations",
        "What is the difference between makemigrations and migrate?",
        "I added a field to a Django model, but PostgreSQL still has the old table structure. "
        "Which migration commands should I run locally and when deploying the Python backend?",
        ("django", "postgresql", "python"),
    ),
    (
        "demo-git-merge-conflicts",
        "How can I resolve a Git merge conflict?",
        "Two branches changed the same lines of a file. Git stopped the merge and added "
        "conflict markers. How can I combine both changes, check the result and finish the merge?",
        ("git",),
    ),
    (
        "demo-docker-environment-variables",
        "How should I pass environment variables to a Docker container?",
        "My Django application needs a database URL and a secret key. How can Docker Compose "
        "supply these settings without copying a private .env file into the Docker image?",
        ("docker", "django"),
    ),
    (
        "demo-django-many-to-many-tags",
        "How do I add tags to a Django many-to-many relationship?",
        "A question can have several tags and each tag can belong to many questions. "
        "How does Django store this in PostgreSQL, and when should I use add() or set()?",
        ("django", "postgresql", "python"),
    ),
)


def seed_demo_data():
    """Add missing examples atomically, preserving existing rows and edits."""
    from django.contrib.auth.hashers import make_password
    from django.db import connection, transaction

    from apps.questions.models import Question
    from apps.tags.models import Tag
    from apps.users.models import CustomUser

    counts = {"users": 0, "tags": 0, "questions": 0}
    with transaction.atomic():
        # Serialize simultaneous container starts on the same PostgreSQL database.
        if connection.vendor == "postgresql":
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_advisory_xact_lock(%s)", [734003381])

        author, created = CustomUser.objects.get_or_create(
            email=DEMO_EMAIL,
            defaults={
                "first_name": "Demo",
                "last_name": "Author",
                "password": make_password(None),
            },
        )
        counts["users"] += int(created)

        tags = {}
        for name in DEMO_TAGS:
            tag, created = Tag.objects.get_or_create(slug=name, defaults={"name": name})
            tags[name] = tag
            counts["tags"] += int(created)

        for slug, title, description, tag_names in DEMO_QUESTIONS:
            question, created = Question.objects.get_or_create(
                slug=slug,
                defaults={"title": title, "description": description, "author": author},
            )
            if created:
                question.tag.add(*(tags[name] for name in tag_names))
                counts["questions"] += 1

    return counts


def main():
    env_id = config("STACK_UNDERFLOW_ENV_ID")
    if env_id not in ("local", "prod"):
        raise ValueError("STACK_UNDERFLOW_ENV_ID must be local or prod")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"stack_underflow.env.{env_id}")
    django.setup()
    counts = seed_demo_data()
    print(
        f"Demo data ready: created {counts['questions']} questions, "
        f"{counts['tags']} tags, {counts['users']} authors. Existing records preserved.",
        flush=True,
    )


if __name__ == "__main__":
    main()
