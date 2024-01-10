from django.contrib import admin
from products.models import Product, Category, Season
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "season", "price", "rating", "image")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("friendly_name", "name")


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Season)
