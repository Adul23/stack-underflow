from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from apps.comments.serializers import (
    CommentListSerializer,
    NestedCommentCreateSerializer,
)
from apps.common.responses import (
    ERROR_401,
    ERROR_403,
    ERROR_404,
    ERROR_429,
    VALIDATION_400,
)
from apps.questions.serializers import (
    QuestionCreateSerializer,
    QuestionDetailSerializer,
    QuestionListSerializer,
    QuestionUpdateSerializer,
)

question_retrieve_response = inline_serializer(
    name="QuestionRetrieveResponse",
    fields={
        "question": QuestionDetailSerializer(),
        "comments": CommentListSerializer(many=True),
    },
)

question_update_response = inline_serializer(
    name="QuestionUpdateResponse",
    fields={
        "details": serializers.CharField(),
        "data": QuestionUpdateSerializer(),
    },
)


question_schema = extend_schema_view(
    list_questions=extend_schema(
        tags=["Questions"],
        summary="List all questions",
        description="Returns a list of all questions. Authentication is not required.",
        responses={
            200: OpenApiResponse(
                response=QuestionListSerializer(many=True),
                description="Questions were returned successfully.",
            ),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "List questions response example",
                response_only=True,
                status_codes=["200"],
                value=[
                    {
                        "id": 1,
                        "title": "How to use serializers in Django?",
                        "slug": "how-to-use-serializers-in-django",
                    },
                    {
                        "id": 2,
                        "title": "How to connect JWT auth?",
                        "slug": "how-to-connect-jwt-auth",
                    },
                ],
            ),
        ],
    ),
    retrieve_question=extend_schema(
        tags=["Questions"],
        summary="Retrieve question by slug",
        description="Returns detailed information about a single question and all comments related to it.",
        responses={
            200: OpenApiResponse(
                response=question_retrieve_response,
                description="Question and related comments were returned successfully.",
            ),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "Retrieve question response example",
                response_only=True,
                status_codes=["200"],
                value={
                    "question": {
                        "id": 1,
                        "title": "How to use serializers in Django?",
                        "description": "I want to understand why serializers are needed.",
                        "slug": "how-to-use-serializers-in-django",
                    },
                    "comments": [
                        {"id": 1, "text": "They validate and transform data."}
                    ],
                },
            ),
            OpenApiExample(
                "Question not found example",
                response_only=True,
                status_codes=["404"],
                value={"detail": "Question does not exist"},
            ),
        ],
    ),
    destroy_question=extend_schema(
        tags=["Questions"],
        summary="Delete question by slug",
        description="Deletes a question by its slug. Only the author can delete it.",
        responses={
            204: OpenApiResponse(description="Question was deleted successfully."),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "Delete forbidden example",
                response_only=True,
                status_codes=["403"],
                value={"detail": "You are not the author of this question"},
            ),
        ],
    ),
    create_question=extend_schema(
        tags=["Questions"],
        summary="Create a new question",
        description="Creates a new question. Authentication is required.",
        request=QuestionCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=QuestionDetailSerializer,
                description="Question was created successfully.",
            ),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "Create question request example",
                request_only=True,
                value={
                    "title": "How to use serializers in Django?",
                    "description": "Please explain with a simple example.",
                    "tag": [1, 2],
                },
            ),
            OpenApiExample(
                "Create question response example",
                response_only=True,
                status_codes=["201"],
                value={
                    "id": 1,
                    "title": "How to use serializers in Django?",
                    "description": "Please explain with a simple example.",
                    "slug": "how-to-use-serializers-in-django",
                },
            ),
        ],
    ),
    update_question=extend_schema(
        tags=["Questions"],
        summary="Update question by slug",
        description="Partially updates a question by its slug. Only the author can update it.",
        request=QuestionUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=question_update_response,
                description="Question was updated successfully.",
            ),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "Update question request example",
                request_only=True,
                value={"title": "How do serializers work in Django REST Framework?"},
            ),
            OpenApiExample(
                "Update question response example",
                response_only=True,
                status_codes=["200"],
                value={
                    "details": "The question successfully updated",
                    "data": {
                        "title": "How do serializers work in Django REST Framework?"
                    },
                },
            ),
            OpenApiExample(
                "Update forbidden example",
                response_only=True,
                status_codes=["403"],
                value={"detail": "You can edit only your question"},
            ),
        ],
    ),
    create_comment=extend_schema(
        tags=["Questions"],
        summary="Create comment for a question",
        description="Creates a new comment for the selected question. Authentication is required.",
        request=NestedCommentCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=CommentListSerializer,
                description="Comment was created successfully.",
            ),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "Create comment request example",
                request_only=True,
                value={
                    "text": "You should use serializers for validation and transformation."
                },
            ),
            OpenApiExample(
                "Create comment response example",
                response_only=True,
                status_codes=["201"],
                value={
                    "id": 1,
                    "text": "You should use serializers for validation and transformation.",
                },
            ),
        ],
    ),
    list_questions_by_author=extend_schema(
        tags=["Questions"],
        summary="List questions by author",
        description="Returns questions by a specific author. Pass author ID as a query parameter.",
        parameters=[
            OpenApiParameter(
                name="author",
                type=int,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Author user ID",
            )
        ],
        responses={
            200: OpenApiResponse(
                response=QuestionListSerializer(many=True),
                description="Questions by author were returned successfully.",
            ),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "List questions by author response example",
                response_only=True,
                status_codes=["200"],
                value=[
                    {
                        "id": 3,
                        "title": "How to create JWT login?",
                        "slug": "how-to-create-jwt-login",
                    }
                ],
            ),
        ],
    ),
)
