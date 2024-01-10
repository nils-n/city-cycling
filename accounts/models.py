from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Based on: https://learndjango.com/tutorials/django-custom-user-model
    """

    pass
    # add additional fields in here

    def __str__(self):
        return self.username
