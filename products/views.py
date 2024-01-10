from django.shortcuts import render
from products.models import Product


def all_products(request):
    """view to display all products in the shop"""
    products = Product.objects.all()

    return render(
        request,
        "products/products.html",
        context={
            "products": products,
        },
    )
