from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


def profile(request):
    """Display user profile
    https://learndjango.com/tutorials/django-best-practices-referencing-user-model
    """
    profile = get_object_or_404(User, id=request.user.id)

    template = "profiles/profile.html"
    context = {"profile": profile}

    return render(request, template, context)
