# Python imports

# Django imports
from django.db import models
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    Count,
    ForeignKey,
    Manager,
    ManyToManyField,
    SlugField,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from apps.abstract.models import AbstractBaseModel

# Project imports
from apps.tags.models import Tag
from apps.users.models import CustomUser


class QuestionManager(Manager):
    def get_queryset(self):
        # Optimization: select_related for FK, prefetch_related for M2M
        """
        select_related works by creating a SQL JOIN in your initial query. It follows "one-to-one" or "many-to-one" relationships to pull in the related object's data immediately.
        How it works: It fetches everything in one single SQL query.
        When to use: Use it for ForeignKey and OneToOneField.
        """

        # Annotation: adding a 'tag_count' field dynamically
        """
        How Count works with prefetch_related:
            annotate happens at the Database level (SQL).
            prefetch_related happens at the Python level (after the first query).
        
        Because we have tag_count in the annotation, the database calculates the number of tags. 
        Because we have prefetch_related('tag'), Django also downloads the full tag objects. 
        This is perfectly fine and exactly what we need if our API endpoint needs to show both the total number of tags and the list of tag names.
        """
        return (
            super()
            .get_queryset()
            .select_related("author")
            .prefetch_related("tag")
            .annotate(tag_count=Count("tag"))
        )


class Question(AbstractBaseModel):
    """Model representing a question."""

    MAX_TITLE_LENGTH = 255

    title = CharField(
        max_length=MAX_TITLE_LENGTH, help_text=_("The title of the question.")
    )

    description = TextField(
        blank=True, null=True, help_text=_("The description of the question.")
    )

    slug = SlugField(
        verbose_name=_("Slug"), unique=True, help_text=_("The slug of the question.")
    )

    tag = ManyToManyField(
        Tag,
        related_name="questions",
        help_text=_("The tags of the question."),
        blank=True,
    )

    is_active = BooleanField(
        default=True, help_text=_("Whether the question is active or not.")
    )

    author = ForeignKey(to=CustomUser, on_delete=CASCADE, related_name="questions")

    objects = QuestionManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        """Meta class for Question model."""

        verbose_name = "Question"
        verbose_name_plural = "Questions"


class AnalyticsEvent(models.Model):
    event_name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=64, null=True, blank=True)
    search_query = models.CharField(max_length=255, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
