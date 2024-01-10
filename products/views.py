from django.shortcuts import render
from icecream import ic
# Create your views here.


def all_products(request):
    """view to display all products in the shop"""
    ic()
    return render(request, "products/products.html", {})
