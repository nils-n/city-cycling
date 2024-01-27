from factories import UserFactory


def test_user_factory(user_factory):
    """test to create an instance of the user model"""
    assert user_factory is UserFactory
