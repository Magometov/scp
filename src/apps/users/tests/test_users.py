import re
from datetime import timedelta
from typing import TYPE_CHECKING, cast
from urllib.parse import urlencode, urljoin

import pytest
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.safestring import SafeString
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import Token

from src.apps.api_auth.services.tokens import create_access_token
from src.apps.users.models import User
from src.conftest import UserData

if TYPE_CHECKING:
    from freezegun.api import FrozenDateTimeFactory

JWT_PATTERN = r"[\w\.-]+"
USER_VERIFY_ENDPOINT = reverse("users:verify-user")
VERIFICATION_URL_PATTERN = rf"{settings.APP_SITE}{USER_VERIFY_ENDPOINT}\?token={JWT_PATTERN}"


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

    text = cast(SafeString, message.body)
    assert (match := re.search(VERIFICATION_URL_PATTERN, text))
    response_from_verify = client.get(match.group(0))
    assert response_from_verify.status_code == status.HTTP_200_OK

    user = User.objects.get(pk=response.data["id"])
    assert user.is_active


@pytest.mark.django_db()
def test_expired_token(
    api_client: type[APIClient],
    user: User,
    mailoutbox: list[EmailMultiAlternatives],
    freezer: "FrozenDateTimeFactory",
) -> None:
    user = user
    client = api_client()

    token = create_access_token(user)
    freezer.move_to(jwt_settings.REFRESH_TOKEN_LIFETIME + timedelta(hours=1))
    endpoint = reverse("users:verify-user")
    verify_email_link = urljoin(settings.APP_SITE, endpoint)
    params = {"token": token}
    url_with_params = f"{verify_email_link}?{urlencode(params)}"

    response = client.get(url_with_params)

    assert response.status_code == status.HTTP_410_GONE
    assert len(mailoutbox) == 1, mailoutbox
    message = mailoutbox[0]
    assert message.to == [user.email]


@pytest.mark.django_db()
def test_invalid_token(
    api_client: type[APIClient],
    user: User,
    mailoutbox: list[EmailMultiAlternatives],
) -> None:
    user = user
    client = api_client()

    _ = create_access_token(user)
    endpoint = reverse("users:verify-user")
    verify_email_link = urljoin(settings.APP_SITE, endpoint)
    params = {"token": "invalid"}
    url_with_params = f"{verify_email_link}?{urlencode(params)}"

    response = client.get(url_with_params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not mailoutbox


@pytest.fixture()
def token(
    user: User,
    monkeypatch: pytest.MonkeyPatch,
) -> Token:
    old_key = jwt_settings.SIGNING_KEY
    monkeypatch.setattr(jwt_settings, "SIGNING_KEY", "hello")
    assert jwt_settings.SIGNING_KEY == "hello"
    token = create_access_token(user)
    monkeypatch.setattr(jwt_settings, "SIGNING_KEY", old_key)
    return token


@pytest.mark.django_db()
def test_invalid_signature(
    api_client: type[APIClient],
    user: User,
    mailoutbox: list[EmailMultiAlternatives],
    token: str,
) -> None:
    user = user
    client = api_client()

    _ = create_access_token(user)
    endpoint = reverse("users:verify-user")
    verify_email_link = urljoin(settings.APP_SITE, endpoint)
    params = {"token": str(token)}
    url_with_params = f"{verify_email_link}?{urlencode(params)}"

    response = client.get(url_with_params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not mailoutbox
