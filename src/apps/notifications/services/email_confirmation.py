from urllib.parse import urlencode, urljoin

from django.conf import settings
from post_office import mail
from post_office.template import render_to_string
from rest_framework.reverse import reverse

from src.apps.api_auth.services.tokens import create_access_token
from src.apps.users.models import User


def send_confirmation_email(user: User) -> None:
    token = create_access_token(user)
    endpoint = reverse("users:verify-user")
    verify_email_link = urljoin(settings.APP_SITE, endpoint)
    params = {"token": token}
    url_with_params = f"{verify_email_link}?{urlencode(params)}"
    body = render_to_string(
        "notifications/email-verification.html",
        {"verify_email_link": url_with_params, "username": user.username},
    )
    mail.send(
        user.email,
        html_message=body,
        subject="Account Verification",
    )
