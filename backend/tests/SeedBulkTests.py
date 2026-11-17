import pytest
from django.core.management import call_command

from apps.questions.models import Question

URL = "/api/questions/list"


@pytest.mark.django_db
class TestSeedBulk:
    """US-08: bulk seed used for EXPLAIN ANALYZE measurements."""

    def test_creates_questions_with_tags(self):
        call_command("seed_bulk", count=200)
        bulk = Question.objects.filter(slug__startswith="bulk-")
        assert bulk.count() == 200
        assert all(q.tag_count >= 2 for q in bulk)

    def test_is_idempotent_and_flush_recreates(self):
        call_command("seed_bulk", count=50)
        call_command("seed_bulk", count=50)
        assert Question.objects.filter(slug__startswith="bulk-").count() == 50
        call_command("seed_bulk", count=30, flush=True)
        assert Question.objects.filter(slug__startswith="bulk-").count() == 30

    def test_seeded_data_is_searchable(self, api_client):
        call_command("seed_bulk", count=300)
        response = api_client.get(URL, {"search": "django", "tag": "python"})
        assert response.status_code == 200
        ids = [q["id"] for q in response.data]
        assert ids
        assert len(ids) == len(set(ids))
        for q in Question.objects.filter(id__in=ids):
            text = f"{q.title} {q.description}".lower()
            assert "django" in text
            assert q.tag.filter(slug="python").exists()
