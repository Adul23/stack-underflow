import pytest


@pytest.mark.django_db
class TestListTags:
    url = "/api/tags/list"

    @pytest.fixture(autouse=True)
    def setup_cache(self, settings):
        settings.CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }
        from django.core.cache import cache

        cache.clear()

    def test_list_tags_cache_hit(self, api_client, tag):
        api_client.get(self.url)

        tag.delete()

        response = api_client.get(self.url)
        assert response.status_code == 200
        assert len(response.data) > 0
        assert response.data[0]["slug"] == "python"

    def test_list_tags_success(self, api_client, tag):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_list_tags_empty(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert response.data == []

    def test_list_tags_wrong_method(self, api_client):
        response = api_client.post(self.url, {})
        assert response.status_code == 401  # unauthenticated


@pytest.mark.django_db
class TestRetrieveTag:
    def test_retrieve_tag_success(self, api_client, tag, question):
        response = api_client.get(f"/api/tags/{tag.slug}/retrieve")
        assert response.status_code == 200
        assert response.data["tag"]["slug"] == tag.slug
        assert "questions" in response.data

    def test_retrieve_tag_not_found(self, api_client):
        response = api_client.get("/api/tags/nonexistent-slug/retrieve")
        assert response.status_code == 404

    def test_retrieve_tag_wrong_method(self, api_client, tag):
        response = api_client.post(f"/api/tags/{tag.slug}/retrieve", {})
        assert response.status_code == 405  # POST is not allowed (405)

    def test_retrieve_tag_cache_hit(self, api_client, tag, question):
        url = f"/api/tags/{tag.slug}/retrieve"
        first_response = api_client.get(url)
        assert first_response.status_code == 200

        tag.delete()
        question.delete()
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["tag"]["slug"] == tag.slug
        assert "questions" in response.data


@pytest.mark.django_db
class TestCreateTag:
    url = "/api/tags/create"

    def test_create_tag_success(self, auth_client):
        response = auth_client.post(self.url, {"name": "Django"})
        assert response.status_code == 201
        assert response.data["name"] == "Django"
        assert response.data["slug"] == "django"

    def test_create_tag_unauthenticated(self, api_client):
        response = api_client.post(self.url, {"name": "Django"})
        assert response.status_code == 401

    def test_create_tag_missing_name(self, auth_client):
        response = auth_client.post(self.url, {})
        assert response.status_code == 400

    def test_create_tag_cache_hit(self, auth_client):
        response = auth_client.post(self.url, {"name": "Django"})
        assert response.status_code == 201
        from django.core.cache import cache

        assert cache.get("tags_list") is None
