from django.shortcuts import render
from products.models import Product


def all_products(request):
    """view to display all products in the shop"""
    test_product = Product.objects.first()

    return render(
        request,
        "products/products.html",
        {
            "test_product": test_product,
        },
    )
