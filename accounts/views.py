""" view function for the accounts app"""
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from django.contrib import messages
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        messages.success(self.request, "Signup successful!")
        return super().form_valid(form)


def notify_after_login(sender, user, request, **kwargs):
    """send a toast notification after successful login"""
    messages.success(
        request,
        "Login successful",
        fail_silently=True,
    )


def notify_after_logout(sender, user, request, **kwargs):
    """send a toast notification after successful logout"""
    messages.success(
        request,
        "Logout successful",
        fail_silently=True,
    )


def notify_after_failed_login(sender, credentials, request, **kwargs):
    """send a toast notification after unsuccessful login"""
    messages.error(
        request,
        "Login failed",
        fail_silently=True,
    )


user_logged_in.connect(notify_after_login)
user_logged_out.connect(notify_after_logout)
user_login_failed.connect(notify_after_failed_login)
