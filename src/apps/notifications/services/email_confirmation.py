from urllib.parse import urlencode, urljoin

from django.conf import settings
from post_office import mail
from post_office.models import PRIORITY
from rest_framework.reverse import reverse

from src.apps.api_auth.services.tokens import create_access_token
from src.apps.notifications.const import EmailSubject
from src.apps.users.models import User


def send_confirmation_email(user: User) -> None:
    """Sends a confirmation email to the given user."""
    token = create_access_token(user)
    endpoint = reverse("users:verify-user")
    verify_email_link = urljoin(settings.APP_SITE, endpoint)
    params = {"token": token}
    url_with_params = f"{verify_email_link}?{urlencode(params)}"
    mail.send(
        user.email,
        settings.EMAIL_HOST_USER,
        subject=EmailSubject.VERIFICATION,
        message=url_with_params,
        priority=PRIORITY.now,
    )
