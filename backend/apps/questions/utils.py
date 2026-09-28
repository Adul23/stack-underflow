# Python imports
import uuid

# Django imports
from django.utils.text import slugify

# Project imports
from apps.questions.models import Question


def generate_unique_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    while Question.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
    return slug
