from typing import TypedDict

import pytest
from rest_framework.test import APIClient

from src.apps.users.models import User


class UserData(TypedDict):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    repeat_of_password: str


@pytest.fixture()
def api_client() -> type[APIClient]:
    return APIClient


@pytest.fixture()
def user_data() -> UserData:
    return {
        "username": "test_user",
        "email": "test_user@ya.ru",
        "first_name": "test",
        "last_name": "user",
        "password": "jfijfwe08fwuj430f1ienueh230jfiwe",
        "repeat_of_password": "jfijfwe08fwuj430f1ienueh230jfiwe",
    }


@pytest.fixture()
def user() -> User:
    user = User.objects.create_user(
        username="Test",
        email="test@gmail.com",
        password="testtest.",
        is_active=False,
    )
    return user


@pytest.fixture()
def invalid_token() -> str:
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
        eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.\
            SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
