import pytest

from apps.questions.models import AnalyticsEvent

pytestmark = pytest.mark.django_db
URL = "/api/analytics/summary/"


def test_summary_permissions(api_client, user):
    assert api_client.get(URL).status_code == 401
    api_client.force_authenticate(user)
    assert api_client.get(URL).status_code == 403


def test_summary(api_client, user, question):
    user.is_staff = True
    user.save()
    api_client.force_authenticate(user)
    assert api_client.get(URL).data == {
        "totals": {"question_view": 0, "question_create": 0, "search": 0},
        "top_questions": [],
    }
    AnalyticsEvent.objects.create(event_name="question_view", question=question)
    AnalyticsEvent.objects.create(event_name="question_created", question=question)
    AnalyticsEvent.objects.create(event_name="search", search_query="django")
    response = api_client.get(URL)
    assert response.status_code == 200
    assert response.data["totals"] == {"question_view": 1, "question_create": 1, "search": 1}
    assert response.data["top_questions"][0]["slug"] == question.slug
    assert response.data["top_questions"][0]["views"] == 1


def test_top_five_excludes_deleted_and_null(api_client, user, question):
    from apps.questions.models import Question
    user.is_staff = True
    user.save()
    api_client.force_authenticate(user)
    for i in range(7):
        q = Question.objects.create(title=f"Question {i}", slug=f"rank-{i}", author=user)
        AnalyticsEvent.objects.bulk_create([
            AnalyticsEvent(event_name="question_view", question=q) for _ in range(i + 1)
        ])
    question.delete()
    AnalyticsEvent.objects.create(event_name="question_view", question=question)
    AnalyticsEvent.objects.create(event_name="question_view")
    data = api_client.get(URL).data
    assert len(data["top_questions"]) == 5
    assert [q["views"] for q in data["top_questions"]] == [7, 6, 5, 4, 3]
    assert data["totals"]["question_view"] == 30
