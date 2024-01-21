from icecream import ic

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


@login_required
def add_product(request):
    """add a product to the store"""

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product successfully added.")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request, "Failed to add product. Check if your form is valid."
            )
    else:
        form = ProductForm()

    template = "products/add_product.html"

    context = {"form": form}

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """edit a product in the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)

    if request.POST:
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product successfully edited.")
            return redirect(
                reverse(
                    "product_detail",
                    args=[product.id],
                )
            )
        else:
            form = ProductForm(instance=product)
            messages.error(
                request,
                "Faild to update Product. Have you entered the form correctly?",
            )

    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You are editing {product.name}")

    template = "products/edit_product.html"

    context = {"form": form, "product": product}

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """delete a product form the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()

    messages.success(request, "Product successfully deleted.")

    return redirect(reverse("products"))
