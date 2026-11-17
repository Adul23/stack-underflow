# Python imports

# Django imports
from django.db.models import CASCADE, PROTECT, ForeignKey, Index, Manager, TextField

from apps.abstract.models import AbstractBaseModel

# Project imports
from apps.questions.models import Question
from apps.users.models import CustomUser


class CommentManager(Manager):
    def get_queryset(self):
        """
        Optimization:
        We use select_related for both 'author' and 'question' because
        both are ForeignKeys (Many-to-One). This performs a SQL JOIN.
        """

        return super().get_queryset().select_related('author', 'question') # Adil.Yergazy 08.05.2026

class Comments(AbstractBaseModel):
    MAX_TEXT_LENGTH = 300

    question = ForeignKey(
        to=Question,
        on_delete=CASCADE
    )

    author = ForeignKey(
        to=CustomUser,
        on_delete=PROTECT
    )

    text = TextField(
        max_length=MAX_TEXT_LENGTH
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        # US-08: comments of a question, in chronological order
        indexes = [Index(fields=["question", "created_at"], name="comment_question_created_idx")]
