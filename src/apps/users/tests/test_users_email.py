from typing import Any

import pytest
from bs4 import BeautifulSoup
from django.core.mail import EmailMultiAlternatives
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from src.apps.users.models import User


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


def parse_html_message(message: str) -> str:
    soup = BeautifulSoup(message, "html.parser")
    links = soup.find_all("a")
    soup = BeautifulSoup(message, "html.parser")
    links = soup.find_all("a")
    for link in links:
        return link.get("href")


@pytest.mark.django_db()
def test_user_email_verification(
    api_client: type[APIClient], user_data: dict[str, Any], mailoutbox: type[EmailMultiAlternatives]
) -> None:
    client = api_client()
    response = client.post(
        reverse("users:sign-up"),
        data=user_data,
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED, response.data

    user = User.objects.get(pk=response.data["id"])
    assert not user.is_active
    assert len(mailoutbox) == 1, mailoutbox
    message = mailoutbox[0]
    assert message.to == [user.email]

    href = parse_html_message(message.body)
    response_from_verify = client.get(href)
    assert response_from_verify.status_code == status.HTTP_200_OK

    user = User.objects.get(pk=response.data["id"])
    assert user.is_active
