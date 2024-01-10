from django.shortcuts import render



def all_products(request):
    """view to display all products in the shop"""
    return render(request, "products/products.html", {})
