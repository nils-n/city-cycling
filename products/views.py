from django.shortcuts import render, get_object_or_404
from products.models import Product, Category


def all_products(request):
    """view to display all products in the shop"""
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(
        request,
        "products/products.html",
        context={
            "products": products,
            "categories": categories,
        },
    )


def product_detail(request, product_id):
    """view to display product detail in the shop"""
    product = get_object_or_404(Product, pk=product_id)

    return render(
        request,
        "products/product_detail.html",
        context={
            "product": product,
        },
    )
