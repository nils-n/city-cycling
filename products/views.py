from icecream import ic

from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Lower

from products.models import Product, Category
from products.forms import ProductForm


def all_products(request):
    """view to display all products in the shop"""
    products = Product.objects.all()
    all_categories = Category.objects.all()
    categories = None
    sort = None
    direction = None
    category = None

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

        if "category" in request.GET:
            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)

    current_sorting = f"{sort}_{direction}"

    return render(
        request,
        "products/products.html",
        context={
            "products": products,
            "current_sorting": current_sorting,
            "all_categories": all_categories,
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


def add_product(request):
    """add a product to the store"""
    form = ProductForm()
    template = "products/add_product.html"

    context = {"form": form}

    return render(request, template, context)
