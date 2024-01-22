from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        verbose_name_plural = "Categories"


class Season(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    start = models.DateField(
        null=True, blank=True, auto_now=False, auto_now_add=False
    )
    end = models.DateField(
        null=True, blank=True, auto_now=False, auto_now_add=False
    )

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    season = models.ForeignKey(
        "Season", null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    has_comments = models.BooleanField(null=True, blank=True, default=False)
    has_rating = models.BooleanField(default=False, null=True, blank=True)
    has_sizes = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_rating(self):
        """calculate the rating to display in the template"""
        if (self.rating / 100) < 0.1:
            return 0.0
        return self.rating / 100


class ProductRating(models.Model):
    """DB table for a single product rating"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ratings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ratings",
    )
    value = models.IntegerField(default=0, null=True, blank=True)
