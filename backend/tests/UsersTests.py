import pytest


@pytest.mark.django_db
class TestLogin:
    url = "/api/users/login"

    def test_login_success(self, api_client, user):
        response = api_client.post(
            self.url,
            {
                "email": "testuser@example.com",
                "password": "StrongPass123!",
            },
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_wrong_password(self, api_client, user):
        response = api_client.post(
            self.url,
            {
                "email": "testuser@example.com",
                "password": "WrongPassword!",
            },
        )
        assert response.status_code == 400

    def test_login_nonexistent_user(self, api_client):
        response = api_client.post(
            self.url,
            {
                "email": "nobody@example.com",
                "password": "SomePass123!",
            },
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestRegister:
    url = "/api/users/register"

    def test_register_success(self, api_client):
        response = api_client.post(
            self.url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "newuser@example.com",
                "password": "StrongPass123!",
            },
        )
        assert response.status_code == 201
        assert response.data["email"] == "newuser@example.com"

    def test_register_duplicate_email(self, api_client, user):
        response = api_client.post(
            self.url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "testuser@example.com",
                "password": "StrongPass123!",
            },
        )
        assert response.status_code == 400

    def test_register_missing_fields(self, api_client):
        response = api_client.post(
            self.url,
            {
                "email": "incomplete@example.com",
            },
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestTokenRefresh:
    url = "/api/users/token/refresh"

    def test_refresh_success(self, api_client, user):
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = str(RefreshToken.for_user(user))
        response = api_client.post(self.url, {"refresh": refresh})
        assert response.status_code == 200
        assert "access" in response.data

    def test_refresh_invalid_token(self, api_client):
        response = api_client.post(self.url, {"refresh": "invalidtoken"})
        assert response.status_code == 401

    def test_refresh_missing_token(self, api_client):
        response = api_client.post(self.url, {})
        assert response.status_code == 400
