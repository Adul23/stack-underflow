# Django imports
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm

# Project imports
from apps.tags.models import Tag

# admin.site.unregister(Question)


class TagCreationForm(ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"


class TagAdmin(ModelAdmin):
    form = TagCreationForm
    list_display = (
        "name",
        "slug",
    )


admin.site.register(Tag, TagAdmin)

# admin.site.unregister(Group)
