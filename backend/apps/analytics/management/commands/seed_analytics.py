import random
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.questions.models import AnalyticsEvent, Question


class Command(BaseCommand):
    help = "Create clearly marked synthetic demo events; reruns replace only these events."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=500)

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["count"]
        if not 1 <= count <= 100000:
            raise CommandError("count must be between 1 and 100000")
        questions = list(Question.objects.filter(deleted_at__isnull=True).order_by("id")[:100])
        if not questions:
            raise CommandError("Run seed_demo.py or seed_bulk first.")
        AnalyticsEvent.objects.filter(session_id="demo-analytics-seed").delete()
        rng = random.Random(42)
        events = []
        for _ in range(count):
            kind = rng.choices(["question_view", "question_created", "search"], [7, 1, 2])[0]
            events.append(
                AnalyticsEvent(
                    event_name=kind,
                    question=rng.choice(questions) if kind != "search" else None,
                    search_query=rng.choice(["django", "python", "docker", "angular"]) if kind == "search" else None,
                    session_id="demo-analytics-seed",
                    metadata={"synthetic": True},
                )
            )
        AnalyticsEvent.objects.bulk_create(events)
        now = timezone.now()
        for event in events:
            event.created_at = now - timedelta(minutes=rng.randrange(7 * 24 * 60))
        AnalyticsEvent.objects.bulk_update(events, ["created_at"])
        self.stdout.write(self.style.SUCCESS(f"Seeded {count} synthetic analytics events."))
