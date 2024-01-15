from django.shortcuts import render, redirect


def view_bag(request):
    """view content of shopping bag"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """add a product to the shopping bag"""

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

    request.session["bag"] = bag

    return redirect(redirect_url)
