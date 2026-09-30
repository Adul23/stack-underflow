from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch

import pytest
from django.db import close_old_connections, connection

from apps.questions.models import AnalyticsEvent, Question
from apps.tags.models import Tag
from apps.users.models import CustomUser
from seed_demo import DEMO_EMAIL, DEMO_QUESTIONS, DEMO_TAGS, seed_demo_data


@pytest.mark.django_db
def test_demo_data_survives_repeated_startup_without_duplicates():
    assert seed_demo_data() == {"users": 1, "tags": 8, "questions": 12}
    original_rows = list(Question.objects.order_by("id").values())
    original_links = list(Question.tag.through.objects.order_by("id").values())

    assert seed_demo_data() == {"users": 0, "tags": 0, "questions": 0}
    assert list(Question.objects.order_by("id").values()) == original_rows
    assert list(Question.tag.through.objects.order_by("id").values()) == original_links
    assert Question.objects.count() == len(DEMO_QUESTIONS)
    assert Tag.objects.count() == len(DEMO_TAGS)
    for slug, title, description, names in DEMO_QUESTIONS:
        question = Question.objects.get(slug=slug)
        assert question.title == title
        assert question.description == description
        assert set(question.tag.values_list("name", flat=True)) == set(names)
    author = CustomUser.objects.get(email=DEMO_EMAIL)
    assert not author.has_usable_password()
    assert not author.is_staff
    assert not author.is_superuser
    assert not AnalyticsEvent.objects.exists()


@pytest.mark.django_db
def test_demo_data_preserves_real_content_edits_and_soft_deletions(question, tag):
    original_title = question.title
    seed_demo_data()
    example = Question.objects.get(slug=DEMO_QUESTIONS[0][0])
    example.description = "Edited by the teacher."
    example.save(update_fields=["description"])
    example.tag.clear()
    deleted = Question.objects.get(slug=DEMO_QUESTIONS[1][0])
    deleted.delete()

    seed_demo_data()

    question.refresh_from_db()
    example.refresh_from_db()
    deleted.refresh_from_db()
    tag.refresh_from_db()
    assert question.title == original_title
    assert list(question.tag.all()) == [tag]
    assert tag.name == "Python"
    assert example.description == "Edited by the teacher."
    assert not example.tag.exists()
    assert deleted.deleted_at is not None
    assert Question.objects.count() == len(DEMO_QUESTIONS) + 1


@pytest.mark.django_db
def test_failed_seed_rolls_back_instead_of_leaving_a_partial_dataset():
    original_get_or_create = Question.objects.get_or_create

    def fail_on_second_question(*args, **kwargs):
        if kwargs["slug"] == DEMO_QUESTIONS[1][0]:
            raise RuntimeError("Simulated interrupted startup")
        return original_get_or_create(*args, **kwargs)

    with patch.object(Question.objects, "get_or_create", side_effect=fail_on_second_question):
        with pytest.raises(RuntimeError, match="interrupted startup"):
            seed_demo_data()

    assert not CustomUser.objects.exists()
    assert not Tag.objects.exists()
    assert not Question.objects.exists()
    assert not Question.tag.through.objects.exists()
    assert seed_demo_data()["questions"] == len(DEMO_QUESTIONS)


@pytest.mark.django_db(transaction=True)
def test_two_postgresql_startups_create_one_dataset():
    if connection.vendor != "postgresql":
        pytest.skip("Concurrent container startup uses a PostgreSQL advisory lock")
    barrier = Barrier(2)

    def start_container():
        close_old_connections()
        try:
            barrier.wait(timeout=10)
            return seed_demo_data()
        finally:
            connection.close()

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: start_container(), range(2)))

    assert sum(result["questions"] for result in results) == len(DEMO_QUESTIONS)
    assert Question.objects.count() == len(DEMO_QUESTIONS)
    assert CustomUser.objects.count() == 1
    assert Tag.objects.count() == len(DEMO_TAGS)
