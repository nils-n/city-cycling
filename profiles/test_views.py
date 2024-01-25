def test_authenticated_user_can_access_profile_page(client, django_user_model):
    """
    this tests whether a signed in user can access their profile page
    """
    username = "pytestuser2"
    password = "1234-abcd"
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    response = client.get("/profiles/1")
    assert response.status_code == 200
