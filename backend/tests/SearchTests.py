import pytest

from apps.questions.models import AnalyticsEvent, Question
from apps.tags.models import Tag

URL = "/api/questions/list"


@pytest.fixture
def other_question(db, user):
    """A second question with a different tag, so filters have something to exclude."""
    js = Tag.objects.create(name="JavaScript", slug="javascript")
    q = Question.objects.create(
        title="Angular routing basics",
        description="How do lazy loaded modules work?",
        slug="angular-routing-basics",
        author=user,
    )
    q.tag.set([js])
    return q


@pytest.mark.django_db
class TestQuestionSearch:
    """US-03: keyword + tag search on the questions list endpoint."""

    @pytest.mark.parametrize("term", ["django", "SERIALIZERS", "simple example"])
    def test_keyword_match(self, api_client, question, other_question, term):
        response = api_client.get(URL, {"search": term})
        assert response.status_code == 200
        assert [q["id"] for q in response.data] == [question.id]

    @pytest.mark.parametrize("tag_value", ["python", "Python"])
    def test_tag_match_by_slug_or_name(self, api_client, question, other_question, tag_value):
        response = api_client.get(URL, {"tag": tag_value})
        assert response.status_code == 200
        assert [q["id"] for q in response.data] == [question.id]

    def test_keyword_and_tag_combined(self, api_client, question, other_question):
        response = api_client.get(URL, {"search": "django", "tag": "python"})
        assert [q["id"] for q in response.data] == [question.id]
        # keyword matches, but tag does not -> nothing
        response = api_client.get(URL, {"search": "django", "tag": "javascript"})
        assert response.data == []

    @pytest.mark.parametrize(
        "params",
        [{"search": "kubernetes"}, {"tag": "rust"}, {"search": "angular", "tag": "python"}],
    )
    def test_no_match(self, api_client, question, other_question, params):
        response = api_client.get(URL, params)
        assert response.status_code == 200
        assert response.data == []

    def test_deleted_questions_are_excluded(self, api_client, auth_client, question):
        assert auth_client.delete(f"/api/questions/{question.slug}/destroy").status_code == 204
        assert api_client.get(URL, {"search": "django"}).data == []
        assert api_client.get(URL, {"tag": "python"}).data == []

    def test_results_are_not_duplicated(self, api_client, question):
        question.tag.add(Tag.objects.create(name="Django", slug="django"))
        response = api_client.get(URL, {"search": "django"})
        assert len(response.data) == 1

    def test_search_does_not_poison_list_cache(self, api_client, question, other_question):
        api_client.get(URL, {"search": "django"})
        assert len(api_client.get(URL).data) == 2


@pytest.mark.django_db
class TestSearchAnalytics:
    """Submitted ?search= requests are recorded like the legacy ?q= submit."""

    def test_keyword_search_logs_event(self, auth_client, user, question):
        auth_client.get(URL, {"search": " django ", "tag": "python"})
        event = AnalyticsEvent.objects.get()
        assert event.event_name == "search"
        assert event.search_query == "django"
        assert event.user == user
        assert event.metadata == {"source": "submit", "tag": "python"}

    def test_tag_only_filter_logs_nothing(self, api_client, question):
        api_client.get(URL, {"tag": "python"})
        assert not AnalyticsEvent.objects.exists()
