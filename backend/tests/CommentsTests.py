import pytest
from django.core.cache import cache


@pytest.mark.django_db
class TestListComments:
    url = "/api/comments/list"

    def test_list_comments_success(self, api_client, comment):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_list_comments_empty(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert response.data == []

    def test_list_comments_wrong_method(self, api_client):
        response = api_client.delete(self.url)
        assert response.status_code == 405


@pytest.mark.django_db
class TestCreateComment:
    url = "/api/comments/create"

    def test_create_comment_success(self, auth_client, question):
        response = auth_client.post(
            self.url,
            {
                "text": "This is a new comment.",
                "question": question.id,
            },
        )
        assert response.status_code == 201
        assert response.data["text"] == "This is a new comment."

    def test_create_comment_unauthenticated(self, api_client, question):
        response = api_client.post(
            self.url,
            {
                "text": "This is a new comment.",
                "question": question.id,
            },
        )
        assert response.status_code == 401

    def test_create_comment_missing_text(self, auth_client, question):
        response = auth_client.post(
            self.url,
            {
                "question": question.id,
            },
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestUpdateComment:
    def test_update_comment_success(self, auth_client, comment):
        response = auth_client.patch(
            f"/api/comments/{comment.id}/update", {"text": "Updated comment text."}
        )
        assert response.status_code == 200
        assert response.data["data"]["text"] == "Updated comment text."

    def test_update_comment_not_author(self, another_auth_client, comment):
        response = another_auth_client.patch(
            f"/api/comments/{comment.id}/update", {"text": "Hacked comment."}
        )
        assert response.status_code == 403

    def test_update_comment_not_found(self, auth_client):
        response = auth_client.patch(
            "/api/comments/99999/update", {"text": "Updated comment text."}
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestListCommentsByAuthor:
    url = "/api/comments/list_by_author"

    def test_list_by_author_success(self, api_client, user, comment):
        response = api_client.get(self.url, {"author": user.id})
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_list_by_author_no_comments(self, api_client, another_user):
        response = api_client.get(self.url, {"author": another_user.id})
        assert response.status_code == 200
        assert response.data == []

    def test_list_by_author_missing_param(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 400

    def test_update_comment_clears_author_list_cache(self, auth_client, comment, user):
        cache_key = f"comment_by_author_{user.id}"
        cache.set(cache_key, [{"text": "cached data"}])

        auth_client.patch(f"/api/comments/{comment.pk}/update", {"text": "Updated"})

        assert cache.get(cache_key) is None


@pytest.mark.django_db
class TestCommentCacheHits:

    def test_retrieve_comment_is_cached(self, api_client, comment):
        url = f"/api/comments/{comment.pk}/retrieve"
        cache_key = f"comment_pk_{comment.pk}"

        api_client.get(url)
        assert cache.get(cache_key) is not None

        comment_pk = comment.pk
        comment_text = comment.text
        comment.delete()

        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["data"]["text"] == comment_text

    def test_list_comments_by_author_is_cached(self, api_client, user, comment):
        url = f"/api/comments/list_by_author?author={user.id}"
        cache_key = f"comment_by_author_{user.id}"

        api_client.get(url)

        cached_data = cache.get(cache_key)
        assert cached_data is not None
        assert cached_data[0]["text"] == comment.text


@pytest.mark.django_db
class TestCommentCacheInvalidation:

    def test_create_comment_invalidates_related_keys(self, auth_client, question):

        cache.set("list_comments", [{"text": "old data"}])
        cache.set(f"question_comment_{question.slug}", [{"text": "old data"}])

        auth_client.post(
            "/api/comments/create", {"text": "Fresh comment", "question": question.id}
        )

        assert cache.get("list_comments") is None
        assert cache.get(f"question_comment_{question.slug}") is None

    def test_update_comment_invalidates_all_keys(self, auth_client, comment):

        pk = comment.pk
        slug = comment.question.slug
        cache.set(f"comment_pk_{pk}", {"text": "old text"})
        cache.set(f"question_comment_{slug}", [{"text": "old text"}])

        auth_client.patch(f"/api/comments/{pk}/update", {"text": "New Text"})

        assert cache.get(f"comment_pk_{pk}") is None
        assert cache.get(f"question_comment_{slug}") is None


@pytest.mark.django_db
class TestRetrieveComment:

    def test_retrieve_comment_success_and_caching(self, api_client, comment):
        """
        Tests that a GET request retrieves the comment and populates the cache.
        """
        pk = comment.pk
        cache_key = f"comment_pk_{pk}"
        url = f"/api/comments/{pk}/retrieve"

        # Ensure cache is empty before starting
        cache.delete(cache_key)

        # Cache Miss (Hits DB)
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["data"]["text"] == comment.text

        # Verify the data was stored in cache
        cached_data = cache.get(cache_key)
        assert cached_data is not None
        assert cached_data["text"] == comment.text

    def test_retrieve_comment_cache_hit_persistence(self, api_client, comment):
        """
        Tests that if data is in cache, the view returns it even if the DB record is gone.
        """
        pk = comment.pk
        url = f"/api/comments/{pk}/retrieve"

        # Pre-populate the cache manually
        fake_data = {"id": pk, "text": "I am from the cache"}
        cache.set(f"comment_pk_{pk}", fake_data, timeout=600)

        # Delete the actual object from the database
        comment_text_in_db = comment.text
        comment.delete()

        # still succeed with cached data
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["data"]["text"] == "I am from the cache"
        assert response.data["data"]["text"] != comment_text_in_db

    def test_retrieve_comment_not_found(self, api_client):
        """
        Tests that requesting a non-existent ID returns 404 and does not cache None.
        """
        non_existent_pk = 9999
        url = f"/api/comments/{non_existent_pk}/retrieve"

        response = api_client.get(url)

        assert response.status_code == 404
        assert cache.get(f"comment_pk_{non_existent_pk}") is None
