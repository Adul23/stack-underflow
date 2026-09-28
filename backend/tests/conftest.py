import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        kwargs.setdefault("email", "testuser@example.com")
        kwargs.setdefault("first_name", "Test")
        kwargs.setdefault("last_name", "User")
        kwargs.setdefault("password", "StrongPass123!")
        email = kwargs.pop("email")
        password = kwargs.pop("password")
        return django_user_model.objects.create_user(
            email=email, password=password, **kwargs
        )

    return make_user


@pytest.fixture
def user(create_user):
    return create_user()


@pytest.fixture
def another_user(create_user):
    return create_user(email="another@example.com")


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client


@pytest.fixture
def another_auth_client(api_client, another_user):
    client = APIClient()
    refresh = RefreshToken.for_user(another_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client


@pytest.fixture
def tag(db):
    from apps.tags.models import Tag

    return Tag.objects.create(name="Python", slug="python")


@pytest.fixture
def question(db, user, tag):
    from apps.questions.models import Question

    q = Question.objects.create(
        title="How to use serializers in Django?",
        description="Please explain with a simple example.",
        slug="how-to-use-serializers-in-django",
        author=user,
    )
    q.tag.set([tag])
    return q


@pytest.fixture
def comment(db, user, question):
    from apps.comments.models import Comments

    return Comments.objects.create(
        text="This is a test comment.",
        author=user,
        question=question,
    )


@pytest.fixture(autouse=True)
def use_locmem_cache(settings):
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
    from django.core.cache import cache

    cache.clear()
