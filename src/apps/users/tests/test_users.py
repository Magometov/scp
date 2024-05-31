import re
from datetime import timedelta
from typing import Any
from urllib.parse import urlencode, urljoin

import pytest
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from src.apps.api_auth.services.tokens import create_access_token
from src.apps.users.models import User
from src.conftest import UserData


def get_link_from_message(message: str) -> Any:
    pattern = rf"{settings.APP_SITE}{reverse("users:verify-user")}\?token=[\w\.-]+"
    matches = re.findall(pattern, message)
    return matches[0] if matches else None


@pytest.mark.django_db()
def test_user_email_verification(
    api_client: type[APIClient],
    user_data: UserData,
    mailoutbox: list[EmailMultiAlternatives],
) -> None:
    client = api_client()
    response = client.post(reverse("users:sign-up"), data=user_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(id=response.data["id"])
    assert not user.is_active

    assert len(mailoutbox) == 1, mailoutbox
    message = mailoutbox[0]
    assert message.to == [user.email]

    href = get_link_from_message(str(message.body))
    response_from_verify = client.get(href)
    assert response_from_verify.status_code == status.HTTP_200_OK

    user = User.objects.get(pk=response.data["id"])
    assert user.is_active


@pytest.mark.django_db()
def test_expired_token(
    api_client: type[APIClient],
    user_create: User,
    mailoutbox: list[EmailMultiAlternatives],
    freezer: Any,
) -> None:
    user = user_create
    client = api_client()
    initial_datetime = timezone.now()
    token = create_access_token(user)
    freezer.move_to(initial_datetime + timedelta(days=2))
    endpoint = reverse("users:verify-user")
    verify_email_link = urljoin(settings.APP_SITE, endpoint)
    params = {"token": token}
    url_with_params = f"{verify_email_link}?{urlencode(params)}"

    response = client.get(url_with_params)

    assert response.status_code == status.HTTP_410_GONE
    assert len(mailoutbox) == 1, mailoutbox
    message = mailoutbox[0]
    assert message.to == [user.email]
