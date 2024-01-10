from django.contrib import admin
from products.models import Product, Category, Season
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Season)
