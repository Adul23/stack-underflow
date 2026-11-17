"""
US-08: print EXPLAIN ANALYZE for the question search queries (PostgreSQL only).

    python manage.py explain_search
    python manage.py explain_search --runs 5

Each query is executed `--runs` times as warm-up and the plan of the final run
is printed, so timings are not dominated by a cold cache. Used by
scripts/explain_analyze.sh to produce the before/after numbers in
docs/explain_analyze.md.
"""

import re

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.models import Q
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from apps.questions.models import Question
from apps.questions.views import QuestionViewSet

# (label, query params for GET /api/questions/list)
CASES = [
    ("search=deadlock (rare keyword)", {"search": "deadlock"}),
    ("search=django&tag=python (keyword + tag)", {"search": "django", "tag": "python"}),
    ("tag=kubernetes (tag only)", {"tag": "kubernetes"}),
    ("q=deadlock (legacy search box, LIMIT 50)", {"q": "deadlock"}),
]


def build_queryset(params):
    if "q" in params:
        # Mirrors the legacy ?q= branch of QuestionViewSet.list_questions.
        query = params["q"]
        return (
            Question.objects.filter(deleted_at__isnull=True)
            .filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(tag__name__icontains=query)
            )
            .distinct()
            .order_by("-created_at", "-id")[:50]
        )
    request = Request(APIRequestFactory().get("/api/questions/list", params))
    return QuestionViewSet().search_queryset(request)


class Command(BaseCommand):
    help = "EXPLAIN ANALYZE the question search queries (PostgreSQL only)."

    def add_arguments(self, parser):
        parser.add_argument("--runs", type=int, default=3, help="Warm-up runs before the measured one")

    def handle(self, *args, runs, **options):
        if connection.vendor != "postgresql":
            raise CommandError("explain_search needs PostgreSQL (run it inside Docker).")

        total = Question.objects.filter(deleted_at__isnull=True).count()
        self.stdout.write(f"questions (not deleted): {total}\n")

        for label, params in CASES:
            qs = build_queryset(params)
            for _ in range(runs):
                len(list(qs.all()))  # warm up buffers
            plan = qs.explain(analyze=True, buffers=True)
            rows = len(list(qs.all()))
            exec_ms = re.search(r"Execution Time: ([\d.]+) ms", plan)
            self.stdout.write(f"### {label}\n")
            self.stdout.write(f"rows returned: {rows}; execution time: {exec_ms.group(1) if exec_ms else '?'} ms\n")
            self.stdout.write("```\n" + plan + "\n```\n")
