from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from icecream import ic
from products.models import Product


def view_bag(request):
    """view content of shopping bag"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """add a product to the shopping bag"""

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    size = None

    if "product_size" in request.POST:
        size = request.POST.get("product_size")

    # get bag from session if it exists
    bag = request.session.get("bag", {})

    # allow for multiple size of a product that has sizes
    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]["items_by_size"].keys():
                bag[item_id]["items_by_size"][size] += quantity
            else:
                bag[item_id]["items_by_size"][size] = quantity
        else:
            bag[item_id] = {"items_by_size": {size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
            messages.success(request, f"Added { product.name} to your bag")

    request.session["bag"] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """update quantity of a product in the shopping bag"""

    quantity = int(request.POST.get("quantity"))
    size = None

    if "product_size" in request.POST:
        size = request.POST.get("product_size")

    # get bag from session if it exists
    bag = request.session.get("bag", {})

    # allow for multiple size of a product that has sizes
    if size:
        if quantity > 0:
            bag[item_id]["items_by_size"][size] = quantity
        else:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session["bag"] = bag

    return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """remove a product from the shopping bag"""

    try:
        size = None

        if "product_size" in request.POST:
            size = request.POST.get("product_size")

        # get bag from session if it exists
        bag = request.session.get("bag", {})

        # allow for multiple size of a product that has sizes
        if size:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session["bag"] = bag

        return HttpResponse(status=200)

    except Exception as e:
        ic(e)
        return HttpResponse(status=500)
