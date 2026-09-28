from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from apps.comments.serializers import CommentCreateSerializer, CommentListSerializer, CommentUpdateSerializer
from apps.common.responses import ERROR_401, ERROR_403, ERROR_404, ERROR_429, VALIDATION_400

comment_update_response = inline_serializer(
    name="CommentUpdateResponse",
    fields={
        "details": serializers.CharField(),
        "data": CommentListSerializer(),
    },
)


comment_schema = extend_schema_view(
    list=extend_schema(
        tags=["Comments"],
        summary="List all comments",
        description="Returns a list of all comments. Authentication is not required.",
        responses={
            200: OpenApiResponse(response=CommentListSerializer(many=True), description="Comments were returned successfully."),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample(
                "List comments response example",
                response_only=True,
                status_codes=["200"],
                value=[
                    {"id": 1, "text": "You should use serializers for validation."},
                    {"id": 2, "text": "JWT is useful for stateless authentication."},
                ],
            ),
        ],
    ),
    create_comment=extend_schema(
        tags=["Comments"],
        summary="Create a new comment",
        description="Creates a new comment. Authentication is required.",
        request=CommentCreateSerializer,
        responses={
            201: OpenApiResponse(response=CommentListSerializer, description="Comment was created successfully."),
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
                value={"text": "I think serializers are needed for validation and representation.", "question": 1},
            ),
            OpenApiExample(
                "Create comment response example",
                response_only=True,
                status_codes=["201"],
                value={"id": 1, "text": "I think serializers are needed for validation and representation."},
            ),
        ],
    ),
    update_comment=extend_schema(
        tags=["Comments"],
        summary="Update comment by id",
        description="Partially updates a comment by its id. Only the author can update it.",
        request=CommentUpdateSerializer,
        responses={
            200: OpenApiResponse(response=comment_update_response, description="Comment was updated successfully."),
            400: VALIDATION_400,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample("Update comment request example", request_only=True, value={"text": "Updated comment text"}),
            OpenApiExample(
                "Update comment response example",
                response_only=True,
                status_codes=["200"],
                value={"details": "The comment successfully updated", "data": {"id": 1, "text": "Updated comment text"}},
            ),
            OpenApiExample("Update comment forbidden example", response_only=True, status_codes=["403"], value={"detail": "You can edit only your comment"}),
            OpenApiExample("Update comment not found example", response_only=True, status_codes=["404"], value={"detail": "The comment does not exist"}),
        ],
    ),
    list_comments_by_author=extend_schema(
        tags=["Comments"],
        summary="List comments by author",
        description="Returns comments by a specific author. Pass author ID as a query parameter.",
        parameters=[
            OpenApiParameter(name="author", type=int, location=OpenApiParameter.QUERY, required=True, description="Author user ID")
        ],
        responses={
            200: OpenApiResponse(response=CommentListSerializer(many=True), description="Comments by author were returned successfully."),
            400: ERROR_401,
            401: ERROR_401,
            403: ERROR_403,
            404: ERROR_404,
            429: ERROR_429,
        },
        examples=[
            OpenApiExample("List comments by author response example", response_only=True, status_codes=["200"], value=[{"id": 3, "text": "This is my comment."}]),
            OpenApiExample("Author query param missing example", response_only=True, status_codes=["400"], value={"detail": "author is required"}),
        ],
    ),
)
