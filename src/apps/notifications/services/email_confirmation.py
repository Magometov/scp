from urllib.parse import urljoin

from django.conf import settings
from post_office import mail
from rest_framework.reverse import reverse

from src.apps.auth.services.tokens import create_access_token
from src.apps.notifications.const import EmailSubject
from src.apps.users.models import User


def send_confirmation_email(user: User) -> None:
    """Sends a confirmation email to the given user."""
    token = create_access_token(user)
    endpoint = reverse("users:verify-email-token", args=[token])
    verify_email_link = urljoin(settings.APP_SITE, endpoint)
    mail.send(
        user.email,
        settings.EMAIL_HOST_USER,
        subject=EmailSubject.VERIFICATION,
        message=verify_email_link,
    )
