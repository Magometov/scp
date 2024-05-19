import jwt
from rest_framework.generics import get_object_or_404

from src.apps.auth.services.tokens import decode_token, is_token_expired
from src.apps.notifications.services.email_confirmation import send_confirmation_email
from src.apps.users.const import VerificationResponse
from src.apps.users.models import User


def verify_email_token(token: str) -> VerificationResponse:
    """Verifies the given JWT token for email confirmation."""
    try:
        payload = decode_token(token=token, verify_exp=False)
    except jwt.InvalidSignatureError:
        return VerificationResponse.INVALID

    user = get_object_or_404(User, id=payload["user_id"])
    if user.is_active:
        return VerificationResponse.ALREADY_VERIFIED

    if is_token_expired(payload["exp"]):
        send_confirmation_email(user)
        return VerificationResponse.EXPIRED

    return VerificationResponse.SUCCESS
