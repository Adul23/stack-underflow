import pytest


@pytest.fixture(autouse=True)
def clear_cache():
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()


@pytest.mark.django_db
class TestListQuestions:
    url = "/api/questions/list"

    def test_list_questions_success(self, api_client, question):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_list_questions_empty(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert response.data == []

    def test_list_questions_wrong_method(self, api_client):
        response = api_client.post(self.url, {})
        assert response.status_code == 405


@pytest.mark.django_db
class TestRetrieveQuestion:
    def test_retrieve_question_success(self, api_client, question):
        response = api_client.get(f"/api/questions/{question.slug}/retrieve")
        assert response.status_code == 200
        assert response.data["question"]["slug"] == question.slug
        assert "comments" in response.data

    def test_retrieve_question_not_found(self, api_client):
        response = api_client.get("/api/questions/nonexistent-slug/retrieve")
        assert response.status_code == 404

    def test_retrieve_question_wrong_method(self, api_client, question):
        response = api_client.post(f"/api/questions/{question.slug}/retrieve", {})
        assert response.status_code == 405


@pytest.mark.django_db
class TestCreateQuestion:
    url = "/api/questions/create"

    def test_create_question_success(self, auth_client, tag):
        response = auth_client.post(
            self.url,
            {
                "title": "How to use Django signals?",
                "description": "Please explain with an example.",
                "tag": [tag.id],
            },
        )
        assert response.status_code == 201
        assert response.data["title"] == "How to use Django signals?"

    def test_create_question_unauthenticated(self, api_client, tag):
        response = api_client.post(
            self.url,
            {
                "title": "How to use Django signals?",
                "description": "Please explain with an example.",
                "tag": [tag.id],
            },
        )
        assert response.status_code == 401

    def test_create_question_missing_title(self, auth_client):
        response = auth_client.post(
            self.url,
            {
                "description": "No title provided.",
            },
        )
        assert response.status_code == 400

    def test_create_question_cache_hit(self, auth_client, tag):
        response = auth_client.post(
            self.url,
            {
                "title": "How to use Django signals?",
                "description": "Please explain with an example.",
                "tag": [tag.id],
            },
        )
        assert response.status_code == 201

        from django.core.cache import cache

        assert cache.get("tags_list") is None


@pytest.mark.django_db
class TestDestroyQuestion:
    def test_destroy_question_success(self, auth_client, question):
        response = auth_client.delete(f"/api/questions/{question.slug}/destroy")
        assert response.status_code == 204

    def test_destroy_question_not_author(self, another_auth_client, question):
        response = another_auth_client.delete(f"/api/questions/{question.slug}/destroy")
        assert response.status_code == 403

    def test_destroy_question_unauthenticated(self, api_client, question):
        response = api_client.delete(f"/api/questions/{question.slug}/destroy")
        assert response.status_code == 401


@pytest.mark.django_db
class TestUpdateQuestion:
    def test_update_question_success(self, auth_client, question):
        response = auth_client.patch(
            f"/api/questions/{question.slug}/update", {"title": "Updated title"}
        )
        assert response.status_code == 200
        assert response.data["data"]["title"] == "Updated title"

    def test_update_question_not_author(self, another_auth_client, question):
        response = another_auth_client.patch(
            f"/api/questions/{question.slug}/update", {"title": "Hacked title"}
        )
        assert response.status_code == 403

    def test_update_question_not_found(self, auth_client):
        response = auth_client.patch(
            "/api/questions/nonexistent-slug/update", {"title": "Updated title"}
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestCreateCommentOnQuestion:
    def test_create_comment_success(self, auth_client, question):
        response = auth_client.post(
            f"/api/questions/{question.slug}/create_comment",
            {"text": "Great question!"},
        )
        assert response.status_code == 201
        assert response.data["text"] == "Great question!"

    def test_create_comment_unauthenticated(self, api_client, question):
        response = api_client.post(
            f"/api/questions/{question.slug}/create_comment",
            {"text": "Great question!"},
        )
        assert response.status_code == 401

    def test_create_comment_question_not_found(self, auth_client):
        response = auth_client.post(
            "/api/questions/nonexistent-slug/create_comment",
            {"text": "Great question!"},
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestListQuestionsByAuthor:
    url = "/api/questions/list_by_author"

    def test_list_by_author_success(self, api_client, user, question):
        response = api_client.get(self.url, {"author": user.id})
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_list_by_author_no_questions(self, api_client, another_user):
        response = api_client.get(self.url, {"author": another_user.id})
        assert response.status_code == 200
        assert response.data == []

    def test_list_by_author_missing_param(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestCacheInvalidation:

    def test_create_question_clears_list_cache(self, auth_client, tag):
        from django.core.cache import cache

        cache.set("list_questions", [{"title": "Old Question"}])

        auth_client.post(
            "/api/questions/create",
            {
                "title": "New Cache Breaking Question",
                "description": "Required question description",
                "tag": [tag.id],
            },
        )

        assert cache.get("list_questions") is None

    def test_update_question_clears_detail_cache(self, auth_client, question):
        from django.core.cache import cache

        cache_key = f"question_comment_{question.slug}"

        cache.set(cache_key, {"title": "Cached Title"})

        auth_client.patch(
            f"/api/questions/{question.slug}/update", {"title": "Real Title"}
        )

        assert cache.get(cache_key) is None

    def test_create_comment_clears_question_cache(self, auth_client, question):
        from django.core.cache import cache

        cache_key = f"question_comment_{question.slug}"

        cache.set(cache_key, {"question": "info", "comments": []})

        auth_client.post(
            f"/api/questions/{question.slug}/create_comment", {"text": "New Comment"}
        )

        assert cache.get(cache_key) is None
