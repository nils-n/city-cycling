from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Lower
from products.models import Product, Category
from icecream import ic


def all_products(request):
    """view to display all products in the shop"""
    products = Product.objects.all()
    categories = Category.objects.all()
    sort = None
    direction = None

    if request.GET:
        ic()
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("name"))
                ic(products)
        if "direction" in request.GET:
            direction = request.GET["direction"]
            if direction == "desc":
                sortkey = f"-{sortkey}"
            products = products.order_by(sortkey)

    current_sorting = f"{sort}_{direction}"

    return render(
        request,
        "products/products.html",
        context={
            "products": products,
            "categories": categories,
            "current_sorting": current_sorting,
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
