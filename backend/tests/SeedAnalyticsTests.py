import pytest
from django.core.management import call_command

from apps.questions.models import AnalyticsEvent

pytestmark = pytest.mark.django_db


def test_seed_is_repeatable(question):
    real = AnalyticsEvent.objects.create(event_name="search", search_query="real")
    call_command("seed_analytics", count=30)
    call_command("seed_analytics", count=30)
    assert AnalyticsEvent.objects.count() == 31
    assert AnalyticsEvent.objects.filter(pk=real.pk).exists()


