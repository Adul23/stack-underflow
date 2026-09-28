# Python imports

# Django imports
# Rest Framework imports
from rest_framework.serializers import ModelSerializer

# Project imports
from apps.tags.models import Tag


class TagBaseSerializer(ModelSerializer):
    """Base Serializer for Tag model."""

    class Meta:
        """Meta class for TagBaseSerializer."""

        model = Tag
        fields = "__all__"


class TagCreateSerializer(TagBaseSerializer):
    """Serializer for creating a tag."""

    class Meta:
        """Meta class for TagCreateSerializer."""

        model = Tag
        fields = ["id", "name"]


class TagDetailSerializer(TagBaseSerializer):
    """Serializer for retrieving a tag."""

    class Meta:
        """Meta class for TagDetailSerializer."""

        model = Tag
        fields = ["id", "name", "slug"]


class TagListSerializer(TagBaseSerializer):
    """Serializer for a list of tags."""

    class Meta:
        """Meta class for TagListSerializer."""

        model = Tag
        fields = ["id", "name", "slug"]
