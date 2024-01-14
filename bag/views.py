from django.shortcuts import render


def view_bag(request):
    """view content of shopping bag"""

    return render(request, "bag/bag.html")
