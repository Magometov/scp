import jwt
from rest_framework.generics import get_object_or_404

from src.apps.api_auth.services.tokens import decode_token, is_token_expired
from src.apps.notifications.services.email_confirmation import send_confirmation_email
from src.apps.users.const import VerificationResponse
from src.apps.users.models import User


def verify_email_token(token: str) -> VerificationResponse:
    try:
        payload = decode_token(token=token, verify_exp=False)
    except (jwt.InvalidSignatureError, jwt.exceptions.DecodeError):
        return VerificationResponse.INVALID

    user = get_object_or_404(User, id=payload["user_id"])
    if user.is_active:
        return VerificationResponse.ALREADY_VERIFIED

    if is_token_expired(payload["exp"]):
        send_confirmation_email(user)
        return VerificationResponse.EXPIRED

    return VerificationResponse.SUCCESS


def activate_user_by_token(token: str) -> None:
    payload = decode_token(token=token)
    User.objects.filter(id=payload["user_id"]).update(is_active=True)
