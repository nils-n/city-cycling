import pytest  # noqa
from icecream import ic  # noqa

from django.core.exceptions import PermissionDenied  # noqa
from django.contrib.messages.storage.fallback import FallbackStorage


def test_authenticated_user_can_access_profile_page(client, django_user_model):
    """
    this tests whether a signed in user can access their profile page
    """
    username = "user"
    password = "1234-abcd"
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    response = client.get("/profiles/1/")
    ic(response)
    assert response.status_code == 200


def test_authenticated_user_cannot_access_profile_page_of_anther_user(
    client, django_user_model, rf, request
):
    """
    this tests whether a signed in user can access their profile page
    pytest-django does not support djangos messages middleware and fails
    the solution was to allow the messages to fail silently
    https://docs.djangoproject.com/en/dev/ref/contrib/messages/#failing-silently-when-the-message-framework-is-disabled
    """

    forbidden_url = "/profiles/2/"

    username = "user1"
    password = "1234-abcd"
    user = django_user_model.objects.create_user(
        username=username, password=password
    )
    other_username = "user2"
    other_password = "1234-abcd"
    user = django_user_model.objects.create_user(
        username=other_username, password=other_password
    )

    client.login(username=username, password=password)
    request = rf.get(forbidden_url)

    request.user = user
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)

    response = client.get("/profiles/2/")
    assert response.status_code == 403


@pytest.mark.parametrize(
    "fixture_name, input_url, expected_status_code",
    [
        ("client", "/wrong-url-1", 404),
        ("client", "/wrong-url-2", 404),
        ("client", "/", 200),
    ],
)
def test_404_is_raised_when_providing_wrong_url(
    fixture_name, input_url, expected_status_code, request, db
):
    """
    this tests whether a 404 error is raised when the website user
    types in a wrong URL
    """
    client = request.getfixturevalue(fixture_name)

    response = client.get(input_url)

    assert response.status_code == expected_status_code
