from django.shortcuts import render, redirect
from icecream import ic


def view_bag(request):
    """view content of shopping bag"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """add a product to the shopping bag"""

    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")

    # get bag from session if it exists
    bag = request.session.get("bag", {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session["bag"] = bag

    # for testing, log out the content the console
    ic(bag)

    return redirect(redirect_url)
