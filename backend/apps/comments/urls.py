# Django imports
from django.urls import include, path

# Rest framework imports
from rest_framework.routers import DefaultRouter

# Project imports
from apps.comments.views import CommentViewSet

router : DefaultRouter = DefaultRouter(
    trailing_slash = False
)

router.register(
    prefix='comments',
    viewset=CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path("", include(router.urls))
]

