import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
@pytest.mark.django_db
def create_user() -> User:
    """create an instance of the user model"""
    user = User.objects.create_user(
        "testuser", "testuser@test.com", "testpassword-1234"
    )

    return user
