# Django imports
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm

# Project imports
from apps.comments.models import Comments


class CommentCreationForm(ModelForm):
    class Meta:
        model = Comments
        fields = "__all__"



class CommentAdmin(ModelAdmin):
    form = CommentCreationForm
    list_display = (
        "question",
        "author",
        "short_text",
    )

    def short_text(self, obj):
        """Truncates comment text for the list view."""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    short_text.short_description = 'Comment Content'


admin.site.register(Comments, CommentAdmin)

# admin.site.unregister(Group)
