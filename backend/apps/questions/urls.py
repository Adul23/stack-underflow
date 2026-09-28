# Django imports
from django.urls import include, path

# Rest framework imports
from rest_framework.routers import DefaultRouter

# Project imports
from apps.questions.views import QuestionViewSet

router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(prefix="questions", viewset=QuestionViewSet, basename="questions")

urlpatterns = [path("", include(router.urls))]
