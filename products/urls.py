from django.urls import path

from products.views import (
    all_products,
    product_detail,
    add_product,
    edit_product,
    delete_product,
    rate_product,
    comment_product,
)

urlpatterns = [
    path("", all_products, name="products"),
    path("<int:product_id>/", product_detail, name="product_detail"),
    path("add/", add_product, name="add_product"),
    path("edit/<int:product_id>", edit_product, name="edit_product"),
    path("delete/<int:product_id>", delete_product, name="delete_product"),
    path("rate/<int:product_id>", rate_product, name="rate_product"),
    path("comment/<int:product_id>", comment_product, name="comment_product"),
]
