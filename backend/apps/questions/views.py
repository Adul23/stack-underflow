# Python imports
import uuid
from logging import getLogger

from django.core.cache import cache
from django.db.models import Q

# Django imports
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)

# Rest-Framework imports
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import ViewSet

# Project imports
from apps.comments.models import Comments
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
from apps.questions.models import AnalyticsEvent, Question
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

error_response = inline_serializer(
    name="QuestionErrorResponse",
    fields={"detail": serializers.CharField()},
)

validation_error_response = inline_serializer(
    name="QuestionValidationErrorResponse",
    fields={
        "title": serializers.ListField(child=serializers.CharField(), required=False),
        "description": serializers.ListField(
            child=serializers.CharField(), required=False
        ),
        "tag": serializers.ListField(child=serializers.CharField(), required=False),
        "text": serializers.ListField(child=serializers.CharField(), required=False),
        "detail": serializers.CharField(required=False),
    },
)
logger = getLogger("django")


# @question_schema
class QuestionViewSet(ViewSet):
    queryset = Question.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]

    def _get_log_context(self, request: DRFRequest) -> dict:
        """Helper to create consistent base logging context."""
        context = {
            "path": request.path,
            "method": request.method,
            "ip_address": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
        }
        if request.user.is_authenticated:
            context["user_id"] = request.user.id
        return context

    @extend_schema(
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
    )
    @action(
        methods=["GET"], permission_classes=(AllowAny,), url_path="list", detail=False
    )
    def list_questions(self, request: DRFRequest, *args, **kwargs) -> DRFResponse:
        query = request.GET.get("q", "").strip()
        if query:
            questions = Question.objects.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(tag__name__icontains=query)
            ).distinct()
            AnalyticsEvent.objects.create(
                event_name="search",
                user=request.user if request.user.is_authenticated else None,
                search_query=query[:255],
            )
            return DRFResponse(QuestionListSerializer(questions, many=True).data)

        log_extra = self._get_log_context(request)
        questions = cache.get("list_questions")
        if questions is not None:
            logger.info("List of Questions were retrieved from Cache", extra=log_extra)
            return DRFResponse(questions, status=HTTP_200_OK)

        questions = Question.objects.all()
        logger.info(
            "List of Questions were retrieved from DB and stored in Cache",
            extra=log_extra,
        )

        serializer = QuestionListSerializer(questions, many=True)
        cache.set("list_questions", serializer.data)
        return DRFResponse(serializer.data, status=HTTP_200_OK)

    @extend_schema(
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
    )
    @action(
        methods=["GET"], permission_classes=[AllowAny], url_path="retrieve", detail=True
    )
    def retrieve_question(
        self, request: DRFRequest, slug: str = None, *args, **kwargs
    ) -> DRFResponse:
        slug = kwargs.get("slug") or kwargs.get("pk") or slug
        log_extra = self._get_log_context(request)
        try:
            question = Question.objects.get(slug=slug)
            logger.info("Retrieval of Questions by SLUG from DB")
            comments = Comments.objects.filter(question=question)
            question_comment_data = {
                "question": QuestionDetailSerializer(question).data,
                "comments": CommentListSerializer(comments, many=True).data,
            }
            AnalyticsEvent.objects.create(
                event_name="question_view",
                question=question,
                user=request.user if request.user.is_authenticated else None,
            )
            logger.info(
                "Retrieval of question and its comments by slug from DB was successful",
                extra=log_extra,
            )
            return DRFResponse(question_comment_data, status=HTTP_200_OK)
        except Question.DoesNotExist:
            logger.warning(
                "Retrieval of question failed: Question does not exist", extra=log_extra
            )
            return DRFResponse(_("Question does not exist"), status=HTTP_404_NOT_FOUND)

    @extend_schema(
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
    )
    @action(
        methods=["DELETE"],
        permission_classes=[IsAuthenticated],
        url_path="destroy",
        detail=True,
    )
    def destroy_question(
        self, request: DRFRequest, slug: str = None, *args, **kwargs
    ) -> DRFResponse:
        log_extra = self._get_log_context(request)

        slug = kwargs.get("slug") or kwargs.get("pk") or slug
        try:
            question = Question.objects.get(slug=slug)
        except Question.DoesNotExist:
            logger.warning(
                "Destruction of question failed: Question does not exist",
                extra=log_extra,
            )
            return DRFResponse(_("Question does not exist"), status=HTTP_404_NOT_FOUND)

        if question.author != request.user:
            logger.warning(
                "Destruction of question failed: You are not the author of this question",
                extra=log_extra,
            )
            return DRFResponse(
                _("You are not the author of this question"), status=HTTP_403_FORBIDDEN
            )

        question.delete()
        cache.delete("list_questions")
        cache.delete(f"question_comment_{slug}")
        logger.info(
            f"Question {slug} deleted from DB and cache cleared", extra=log_extra
        )
        return DRFResponse(status=HTTP_204_NO_CONTENT)

    @extend_schema(
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
    )
    @action(
        methods=["POST"],
        permission_classes=[IsAuthenticated],
        url_path="create",
        detail=False,
    )
    def create_question(self, request: DRFRequest, *args, **kwargs) -> DRFResponse:
        log_extra = self._get_log_context(request)

        serializer = QuestionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        base_slug = slugify(data["title"])[:40] or uuid.uuid4().hex[:12]
        slug = base_slug
        while Question.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

        question = Question.objects.create(
            title=data["title"],
            description=data.get("description", ""),
            slug=slug,
            author=request.user,
        )
        question.tag.set(data.get("tag", []))
        AnalyticsEvent.objects.create(
            event_name="question_created", question=question, user=request.user
        )
        logger.info("Question was created", extra=log_extra)
        cache.delete("list_questions")
        for tag in question.tag.all():
            cache.delete(f"tag_full_detail_{tag.slug}")

        return DRFResponse(
            QuestionDetailSerializer(question).data, status=HTTP_201_CREATED
        )

    @extend_schema(
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
    )
    @action(
        methods=["PATCH"],
        permission_classes=[IsAuthenticated],
        url_path="update",
        detail=True,
    )
    def update_question(
        self, request: DRFRequest, slug: str = None, *args, **kwargs
    ) -> DRFResponse:
        log_extra = self._get_log_context(request)
        slug = kwargs.get("slug") or kwargs.get("pk") or slug
        try:
            question = Question.objects.get(slug=slug)
        except Question.DoesNotExist:
            logger.warning(
                "Update of question failed: The question does not exist",
                extra=log_extra,
            )
            return DRFResponse(
                _("The question does not exist"), status=HTTP_404_NOT_FOUND
            )

        if question.author != request.user:
            logger.warning(
                "Update of question failed: You can edit only your question",
                extra=log_extra,
            )
            return DRFResponse(
                _("You can edit only your question"), status=HTTP_403_FORBIDDEN
            )

        serializer = QuestionUpdateSerializer(
            question, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        cache.delete("list_questions")
        cache.delete(f"question_comment_{slug}")
        for tag in question.tag.all():
            cache.delete(f"tag_full_detail_{tag.slug}")
        logger.info("Question was deleted", extra=log_extra)
        return DRFResponse(
            {
                "details": "The question successfully updated",
                "data": serializer.data,
            },
            status=HTTP_200_OK,
        )

    @extend_schema(
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
    )
    @action(
        methods=["POST"],
        permission_classes=[IsAuthenticated],
        url_path="create_comment",
        detail=True,
    )
    def create_comment(
        self, request: DRFRequest, slug: str = None, *args, **kwargs
    ) -> DRFResponse:
        log_extra = self._get_log_context(request)
        slug = kwargs.get("slug") or kwargs.get("pk") or slug
        try:
            question = Question.objects.get(slug=slug)
        except Question.DoesNotExist:
            logger.warning(
                "Creation of comment: Question does not exist", extra=log_extra
            )
            return DRFResponse(
                {"detail": "Question does not exist"}, status=HTTP_404_NOT_FOUND
            )

        serializer = NestedCommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = Comments.objects.create(
            text=serializer.validated_data["text"],
            author=request.user,
            question=question,
        )

        cache.delete(f"question_comment_{slug}")
        logger.info("Comment was created in Question", extra=log_extra)

        return DRFResponse(CommentListSerializer(comment).data, status=HTTP_201_CREATED)

    @extend_schema(
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
    )
    @action(
        methods=["GET"],
        permission_classes=[AllowAny],
        url_path="list_by_author",
        detail=False,
    )
    def list_questions_by_author(
        self, request: DRFRequest, *args, **kwargs
    ) -> DRFResponse:
        author_id = request.query_params.get("author")
        questions = cache.get("question_by_author")
        if questions is not None:
            return DRFResponse(questions, status=HTTP_200_OK)
        questions = Question.objects.filter(author=author_id)
        serializer = QuestionListSerializer(questions, many=True)

        cache.set("question_by_author", serializer.data, timeout=600)
        return DRFResponse(serializer.data, status=HTTP_200_OK)
