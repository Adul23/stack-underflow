from decouple import config
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.comments.models import Comments
from apps.questions.models import Question
from apps.tags.models import Tag
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Seed the database with sample data for all models"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        password = config("STACK_UNDERFLOW_SEED_PASSWORD")
        if options["flush"]:
            self.stdout.write(self.style.WARNING("Flushing existing data..."))
            Comments.objects.all().delete()
            Question.objects.all().delete()
            Tag.objects.all().delete()
            CustomUser.objects.filter(is_superuser=False).delete()
            self.stdout.write("  Cleared comments, questions, tags, and non-admin users")

        if CustomUser.objects.filter(email="new1234@gmail.com").exists():
            self.stdout.write(self.style.WARNING("Seed data already exists. Use --flush to recreate."))
            return

        self.stdout.write("Seeding database...\n")

        # ── Users ──
        users = []
        user_data = [
            ("new1234@gmail.com", "Test", "One"),
            ("real1234@gmail.com", "Test", "Two"),
            ("test1234@gmail.com", "Test", "Three"),
        ]
        for email, first, last in user_data:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first,
                last_name=last,
            )
            users.append(user)
        self.stdout.write(f"  Created {len(users)} users")

        # ── Tags ──
        tag_names = ["python", "django", "celery", "docker", "redis"]
        tags = {}
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(
                slug=slugify(name),
                defaults={"name": name},
            )
            tags[name] = tag
        self.stdout.write(f"  Created {len(tags)} tags")

        # ── Questions ──
        q1 = Question.objects.create(
            title="Set up celery",
            description="Backend background tasks. How to do them",
            author=users[0],
            slug="how-to-set-up-celery12",
        )
        q1.tag.add(tags["python"], tags["django"], tags["celery"])

        q2 = Question.objects.create(
            title="Docker. How to configure",
            description="How to create dockerfiles",
            author=users[1],
            slug="how-to-set-up-docker12",
        )
        q2.tag.add(tags["python"], tags["django"], tags["celery"])

        q3 = Question.objects.create(
            title="Redis. How to configure",
            description="Redis connection",
            author=users[2],
            slug="how-to-set-up-redis12",
        )
        q3.tag.add(tags["python"], tags["django"], tags["docker"])

        self.stdout.write("  Created 3 questions (with M2M tag relations)")

        # ── Comments ──
        Comments.objects.create(
            question=q1,
            author=users[1],
            text="Install celery and configure the broker URL in settings.",
        )
        Comments.objects.create(
            question=q2,
            author=users[2],
            text="Use docker compose with proper service names for networking.",
        )
        Comments.objects.create(
            question=q3,
            author=users[0],
            text="Make sure Redis is running and the host is set correctly.",
        )
        self.stdout.write("  Created 3 comments (with FK relations)\n")

        # ── Summary ──
        self.stdout.write(
            self.style.SUCCESS(
                "Seeding complete!\n"
                f"  Users:     {len(users)}\n"
                f"  Tags:      {len(tags)}\n"
                f"  Questions: 3\n"
                f"  Comments:  3\n"
                f"  FK links:  question->author, comment->author, comment->question\n"
                f"  M2M links: question->tags"
            )
        )
