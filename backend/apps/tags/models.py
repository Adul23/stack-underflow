# Python imports

# Django imports
from django.db import models
from django.db.models.functions import Upper
from django.utils.translation import gettext_lazy as _

# Project imports
from apps.abstract.models import AbstractBaseModel


class Tag(AbstractBaseModel):
    MAX_NAME_LENGTH = 255

    name = models.CharField(
        max_length=MAX_NAME_LENGTH, help_text=_("The name of the tag.")
    )

    slug = models.SlugField(unique=True, help_text=_("The slug of the tag."))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        # US-08: ?tag=<value> does case-insensitive (UPPER(...) = UPPER(...)) lookups.
        # The question<->tag M2M table already has Django's indexes on both FKs
        # plus a unique (question_id, tag_id) index, so it needs nothing extra.
        indexes = [
            models.Index(Upper("name"), name="tag_name_upper_idx"),
            models.Index(Upper("slug"), name="tag_slug_upper_idx"),
        ]
