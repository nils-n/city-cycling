from django.urls import path

from products.views import (
    all_products,
    product_detail,
    add_product,
    edit_product,
)

urlpatterns = [
    path("", all_products, name="products"),
    path("<int:product_id>/", product_detail, name="product_detail"),
    path("add/", add_product, name="add_product"),
    path("edit/<int:product_id>", edit_product, name="edit_product"),
]
