from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.questions.models import AnalyticsEvent

from .serializers import SummarySerializer


class SummaryView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=["Analytics"],
        responses=SummarySerializer,
        description=("Staff-only lifetime totals and five most viewed live questions. "
                     "question_create includes legacy question_created events."),
    )
    def get(self, request):
        totals = {"question_view": 0, "question_create": 0, "search": 0}
        for row in AnalyticsEvent.objects.values("event_name").annotate(total=Count("id")):
            name = "question_create" if row["event_name"] == "question_created" else row["event_name"]
            if name in totals:
                totals[name] += row["total"]
        top = (
            AnalyticsEvent.objects.filter(
                event_name="question_view",
                question__isnull=False,
                question__deleted_at__isnull=True,
            )
            .values("question_id", "question__title", "question__slug")
            .annotate(views=Count("id"))
            .order_by("-views", "question_id")[:5]
        )
        return Response(SummarySerializer({"totals": totals, "top_questions": top}).data)
