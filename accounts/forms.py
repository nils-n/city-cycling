from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Based on: https://learndjango.com/tutorials/django-custom-user-model
    """

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    """
    Based on: https://learndjango.com/tutorials/django-custom-user-model
    """

    class Meta:
        model = CustomUser
        fields = ("username", "email")
