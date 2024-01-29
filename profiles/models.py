from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class Comment(models.Model):
    """
    Generic Comment Class to allow users to comment on both products and routes
    based on: https://www.youtube.com/watch?v=Wt4_7ZAE8dI
    (Generic Foreign Keys in Django / GenericForeignKey / GenericRelation)
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments",
    )
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    is_approved = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
