import pytest
from rest_framework.test import APIClient

from src.apps.users.models import User


@pytest.fixture()
def api_client() -> type[APIClient]:
    return APIClient


@pytest.fixture()
def user_data() -> dict[str, str]:
    return {
        "username": "test_user",
        "email": "test_user@ya.ru",
        "first_name": "test",
        "last_name": "user",
        "password": "jfijfwe08fwuj430f1ienueh230jfiwe",
        "repeat_of_password": "jfijfwe08fwuj430f1ienueh230jfiwe",
    }


@pytest.fixture()
def user_create() -> User:
    user = User.objects.create_user(
        username="Test",
        email="test@gmail.com",
        password="testtest.",
        is_active=False,
    )
    return user
