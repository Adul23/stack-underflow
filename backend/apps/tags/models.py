# Python imports

# Django imports
from django.db import models
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
