# Python imports

# Django imports
from django.urls import include, path

# Rest-Framework imports
from rest_framework.routers import DefaultRouter

# Project imports
from apps.users.views import CustomUserViewSet

router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(prefix="users", viewset=CustomUserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    # path("user/token/refresh/", TokenRefreshView.as_view(), name='token_refresh')
]
