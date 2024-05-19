from typing import Any, cast

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import AccessToken, Token
from rest_framework_simplejwt.utils import datetime_from_epoch

from src.apps.users.models import User


def create_access_token(user: User) -> Token:
    """Creates an access token for the given user."""
    token = AccessToken.for_user(user)
    token.set_exp(lifetime=jwt_settings.REFRESH_TOKEN_LIFETIME)
    return token


def decode_token(token: str, verify_exp: bool = True) -> dict[str, Any]:  # TODO: make a TypedDict for payload
    """Decodes the JWT token."""
    payload = jwt.decode(
        token,
        key=settings.SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_exp": verify_exp},
    )
    return cast(dict[str, Any], payload)


def is_token_expired(expiration_epoch: int) -> bool:
    """Checks if the token has expired."""
    claim_time = datetime_from_epoch(expiration_epoch)
    return claim_time < timezone.now()
