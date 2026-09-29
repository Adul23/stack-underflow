# Django imports
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm

# Project imports
from apps.questions.models import AnalyticsEvent, Question

# admin.site.unregister(Question)


class QuestionCreationForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionAdmin(ModelAdmin):
    form = QuestionCreationForm
    filter_vertical = ("tag",)
    list_display = (
        "title",
        "description",
        "slug",
        "display_tags",
        "is_active",
        "author",
    )

    def display_tags(self, obj):
        """Creates a string for the tags to be displayed in the list."""
        return ", ".join([tags.name for tags in obj.tag.all()])

    display_tags.short_description = "Tag"


admin.site.register(Question, QuestionAdmin)


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(ModelAdmin):
    list_display = ("event_name", "user", "question", "search_query", "session_id", "created_at")
    list_filter = ("event_name",)
