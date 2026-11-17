"""
US-08: bulk-seed the database so index/EXPLAIN measurements are meaningful.

    python manage.py seed_bulk                 # 5,000 questions (default)
    python manage.py seed_bulk --count 20000
    python manage.py seed_bulk --flush         # remove previous bulk data first

Only touches data it created itself: questions with the `bulk-` slug prefix and
the `bulk-seed@example.com` author. Data is deterministic (fixed RNG seed), so
EXPLAIN runs on different machines see the same rows.
"""

import random
import secrets

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils.text import slugify

from apps.questions.models import Question
from apps.tags.models import Tag
from apps.users.models import CustomUser

SLUG_PREFIX = "bulk-"
AUTHOR_EMAIL = "bulk-seed@example.com"

TAGS = [
    "python", "django", "drf", "celery", "redis", "postgresql", "sql", "docker",
    "kubernetes", "linux", "git", "angular", "typescript", "javascript", "rxjs",
    "html", "css", "nginx", "jwt", "rest", "websocket", "pytest", "asyncio",
    "aws", "ci-cd", "graphql", "orm", "caching", "security", "performance",
]
VERBS = [
    "configure", "debug", "optimize", "test", "deploy", "migrate", "secure",
    "cache", "paginate", "serialize", "validate", "log", "profile", "refactor",
]
OBJECTS = [
    "a model", "the settings", "a viewset", "a query", "a container", "a pipeline",
    "a form", "a component", "a service", "a migration", "an index", "a router",
    "authentication", "file uploads", "background jobs", "environment variables",
]
PROBLEMS = [
    "I keep getting a timeout.", "The error message is not helpful.",
    "It works locally but fails in production.", "Performance is very slow.",
    "The docs did not answer this.", "Tests pass but the app crashes.",
    "I tried the official example without luck.", "Memory usage keeps growing.",
]
# Rare words (~1% of questions) give EXPLAIN a selective search term.
RARE = ["flamegraph", "idempotency", "backpressure", "deadlock", "tombstone"]


class Command(BaseCommand):
    help = "Bulk-create ~5,000 questions with tags for performance testing (US-08)."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=5000, help="Number of questions (default 5000)")
        parser.add_argument("--flush", action="store_true", help="Delete previously bulk-seeded data first")
        parser.add_argument("--seed", type=int, default=42, help="RNG seed (default 42)")

    @transaction.atomic
    def handle(self, *args, count, flush, seed, **options):
        rng = random.Random(seed)

        if flush:
            deleted, _ = Question.objects.filter(slug__startswith=SLUG_PREFIX).delete()
            self.stdout.write(self.style.WARNING(f"Removed {deleted} bulk rows"))
        elif Question.objects.filter(slug__startswith=SLUG_PREFIX).exists():
            self.stdout.write(self.style.WARNING("Bulk data already exists. Use --flush to recreate."))
            return

        author = CustomUser.objects.filter(email=AUTHOR_EMAIL).first()
        if author is None:
            author = CustomUser.objects.create_user(
                email=AUTHOR_EMAIL,
                first_name="Bulk",
                last_name="Seed",
                password=secrets.token_urlsafe(24),
            )
            author.set_unusable_password()
            author.save(update_fields=["password"])

        tags = []
        for name in TAGS:
            tag, _ = Tag.objects.get_or_create(slug=slugify(name), defaults={"name": name})
            tags.append(tag)

        questions = []
        tag_choices = []
        for i in range(count):
            main, other = rng.sample(tags, 2)
            title = f"How to {rng.choice(VERBS)} {rng.choice(OBJECTS)} with {main.name} and {other.name}?"
            description = " ".join(rng.sample(PROBLEMS, 2))
            if rng.random() < 0.01:
                description += f" Could this be related to {rng.choice(RARE)}?"
            questions.append(
                Question(
                    title=title[: Question.MAX_TITLE_LENGTH],
                    description=description,
                    slug=f"{SLUG_PREFIX}{i:06d}",
                    author=author,
                )
            )
            tag_choices.append([main, other] + rng.sample(tags, rng.randint(0, 2)))

        created = Question.objects.bulk_create(questions, batch_size=1000)

        Through = Question.tag.through
        links = {
            (q.pk, t.pk) for q, q_tags in zip(created, tag_choices) for t in q_tags
        }
        Through.objects.bulk_create(
            [Through(question_id=q_id, tag_id=t_id) for q_id, t_id in links],
            batch_size=5000,
        )

        # Refresh planner statistics so EXPLAIN reflects the new data.
        if connection.vendor == "postgresql":
            with connection.cursor() as cursor:
                cursor.execute("ANALYZE")

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(created)} questions, {len(links)} tag links, {len(tags)} tags")
        )
