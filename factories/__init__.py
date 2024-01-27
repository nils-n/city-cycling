from django.conf import settings
import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory used to create a user to be used for unittest
    to make tests independent from DB connection
    """

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = fake.name()
    password = fake.password()
    email = fake.email()
