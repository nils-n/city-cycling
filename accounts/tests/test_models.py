import pytest
from icecream import ic  # noqa
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user(create_user):
    """test to create a user
    https://djangostars.com/blog/django-pytest-testing/"""

    assert User.objects.count() == 1


@pytest.mark.django_db
def test_authenticated_user_can_access_profile_page(client, create_user):
    """
    this tests whether a signed in user can access their profile page
    """
    random_user = create_user
    random_user_profile_url = f"/profiles/{random_user.id}/"

    client.force_login(random_user)

    response = client.get(random_user_profile_url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_profile_page(client, create_user):
    """
    this tests whether a signed in user can access their profile page
    """
    random_user = create_user
    random_user_profile_url = f"/profiles/{random_user.id}/"

    response = client.get(random_user_profile_url)

    assert response.status_code == 302
