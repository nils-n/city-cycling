""" view function for the bag app"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from products.models import Product
import json


def view_bag(request):
    """view content of shopping bag"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """add a product to the shopping bag"""

    product = get_object_or_404(Product, pk=item_id)
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
                messages.success(
                    request,
                    f"Added size {size.upper()} {product.name} \
                        quantity to { bag[item_id]['items_by_size'][size]}",
                )

            else:
                bag[item_id]["items_by_size"][size] = quantity
                messages.success(
                    request,
                    f"Added size { size.upper()} {product.name} to your bag",
                )

        else:
            bag[item_id] = {"items_by_size": {size: quantity}}
            messages.success(
                request,
                f"Added size { size.upper()} {product.name} to your bag",
            )

    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(
                request,
                f"Updated { product.name} quantity to { bag[item_id] }",
            )
        else:
            bag[item_id] = quantity
            messages.success(request, f"Added { product.name} to your bag")

    request.session["bag"] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """update quantity of a product in the shopping bag"""

    product = get_object_or_404(Product, pk=item_id)
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
            messages.success(
                request,
                f"Updated size {size.upper()} {product.name} \
                quantity to { bag[item_id]['items_by_size'][size]}",
            )
        else:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
            messages.success(
                request,
                f"Removed size { size.upper()} {product.name} from your bag",
            )
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(
                request,
                f"Updated { product.name} quantity to { bag[item_id] }",
            )
        else:
            bag.pop(item_id)
            messages.success(request, f"Removed { product.name} from your bag")

    request.session["bag"] = bag

    return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """
    remove a product from the shopping bag
    retrieving POST parameters from fetch API using :
    https://forum.djangoproject.com/t/send-views-py-request-post-with-javascript/23146/8
    """
    product = get_object_or_404(Product, pk=item_id)

    try:
        size = None

        post_data = json.loads(request.body.decode("utf-8"))
        if "content" in post_data:
            size = post_data["content"]

        # get bag from session if it exists
        bag = request.session.get("bag", {})

        # allow for multiple size of a product that has sizes
        if size:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
            messages.success(
                request,
                f"Removed size { size.upper()} {product.name} from your bag",
            )
        else:
            bag.pop(item_id)
            messages.success(request, f"Removed { product.name} from your bag")

        request.session["bag"] = bag

        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f"Error removing items: {e}")
        return HttpResponse(status=500)
