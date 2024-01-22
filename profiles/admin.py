from django.contrib import admin

# Register your models here.
from profiles.models import Comment


class CommentAdmin(admin.ModelAdmin):
    """admin for generic comments
    based on https://www.youtube.com/watch?v=Wt4_7ZAE8dI
    Generic Foreign Keys in Django / GenericForeignKey / GenericRelation
    """

    list_display = ("text", "object_id", "content_type", "content_object")


admin.site.register(Comment, CommentAdmin)
