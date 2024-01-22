from django.contrib import admin
from products.models import Product, Category, Season, ProductRating
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "season", "price", "rating", "image")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("friendly_name", "name")


class ProductRatingAdmin(admin.ModelAdmin):
    """to display the ratings in the Django admin page"""

    list_display = ("user", "product", "value")


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Season)
admin.site.register(ProductRating, ProductRatingAdmin)
