# Django imports
from django.urls import include, path

# Rest framework imports
from rest_framework.routers import DefaultRouter

# Project imports
from apps.tags.views import TagViewSet

router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(prefix="tags", viewset=TagViewSet, basename="tags")

urlpatterns = [path("", include(router.urls))]
