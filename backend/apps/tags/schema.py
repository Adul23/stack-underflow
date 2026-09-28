from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)

from apps.common.responses import (
    ERROR_401,
    ERROR_403,
    ERROR_404,
    ERROR_429,
    VALIDATION_400,
)
from apps.questions.serializers import QuestionListSerializer
from apps.tags.serializers import (
    TagCreateSerializer,
    TagDetailSerializer,
    TagListSerializer,
)

tag_retrieve_response = inline_serializer(
    name="TagRetrieveResponse",
    fields={
        "tag": TagDetailSerializer(),
        "questions": QuestionListSerializer(many=True),
    },
)


tag_schema = extend_schema_view(
    list_tags=extend_schema(
        tags=["Tags"],
        summary="List all tags",
        description="Returns a list of all tags. Authentication is not required.",
        responses={
            200: OpenApiResponse(
                response=TagListSerializer(many=True),
                description="Tags were returned successfully.",
            ),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "List tags response example",
                response_only=True,
                status_codes=["200"],
                value=[
                    {"id": 1, "name": "Python", "slug": "python"},
                    {"id": 2, "name": "Django", "slug": "django"},
                ],
            ),
        ],
    ),
    create_tag=extend_schema(
        tags=["Tags"],
        summary="Create a new tag",
        description="Creates a new tag. If a tag with the same name exists, the existing tag is returned.",
        request=TagCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=TagDetailSerializer,
                description="Tag was created successfully.",
            ),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "Create tag request example",
                request_only=True,
                value={"name": "Machine Learning"},
            ),
            OpenApiExample(
                "Create tag response example",
                response_only=True,
                status_codes=["201"],
                value={"id": 3, "name": "Machine Learning", "slug": "machine-learning"},
            ),
        ],
    ),
    retrieve_tag=extend_schema(
        tags=["Tags"],
        summary="Retrieve tag by slug",
        description="Returns detailed information about a tag and the list of questions linked to it.",
        responses={
            200: OpenApiResponse(
                response=tag_retrieve_response,
                description="Tag and related questions were returned successfully.",
            ),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "Retrieve tag response example",
                response_only=True,
                status_codes=["200"],
                value={
                    "tag": {"id": 1, "name": "Django", "slug": "django"},
                    "questions": [
                        {
                            "id": 10,
                            "title": "How to use serializers?",
                            "slug": "how-to-use-serializers",
                        }
                    ],
                },
            ),
            OpenApiExample(
                "Retrieve tag not found example",
                response_only=True,
                status_codes=["404"],
                value={"detail": "Tag does not exist"},
            ),
        ],
    ),
)
