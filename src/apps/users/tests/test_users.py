from datetime import timedelta
from typing import Any
from urllib.parse import urlencode, urljoin

import jwt
import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from src.apps.users.models import User


def parse_html_message(message: str) -> Any:
    soup = BeautifulSoup(message, "html.parser")
    links = soup.find_all("a")
    for link in links:
        return link.get("href")


@pytest.mark.django_db()
def test_user_email_verification(
    api_client: type[APIClient],
    user_data: dict[str, str],
    mailoutbox: Any,
) -> None:
    client = api_client()
    response = client.post(reverse("users:sign-up"), data=user_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(id=response.data["id"])
    assert not user.is_active

    assert len(mailoutbox) == 1, mailoutbox
    message = mailoutbox[0]
    assert message.to == [user.email]

    href = parse_html_message(str(message.body))
    response_from_verify = client.get(href)
    assert response_from_verify.status_code == status.HTTP_200_OK

    user = User.objects.get(pk=response.data["id"])
    assert user.is_active


@pytest.mark.django_db()
def test_expired_token(
    api_client: type[APIClient],
    user_create: type[User],
    mailoutbox: Any,
) -> None:
    user = user_create
    client = api_client()
    expired_token = jwt.encode(
        {"user_id": str(user.id), "exp": timezone.now() - timedelta(hours=1)}, settings.SECRET_KEY, algorithm="HS256"
    )
    endpoint = reverse("users:verify-user")
    verify_email_link = urljoin(settings.APP_SITE, endpoint)
    params = {"token": expired_token}
    url_with_params = f"{verify_email_link}?{urlencode(params)}"

    response = client.get(url_with_params)

    assert response.status_code == status.HTTP_410_GONE
    assert len(mailoutbox) == 1, mailoutbox
    message = mailoutbox[0]
    assert message.to == [user.email]
