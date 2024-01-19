from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages

from profiles.forms import UserProfileForm

User = get_user_model()


def profile(request):
    """Display user profile
    https://learndjango.com/tutorials/django-best-practices-referencing-user-model
    """
    user_profile = get_object_or_404(User, id=request.user.id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "User Profile successfully updated.")

    form = UserProfileForm(instance=user_profile)
    orders = user_profile.orders.all()
    hide_bag_preview = True

    template = "profiles/profile.html"
    context = {
        "orders": orders,
        "form": form,
        "hide_bag_preview": hide_bag_preview,
    }

    return render(request, template, context)
