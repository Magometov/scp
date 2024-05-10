from typing import TYPE_CHECKING

from django.contrib import messages

from src.apps.invitations.models import Invitation

if TYPE_CHECKING:
    from django.http import HttpRequest

    from src.apps.events.admin import EventAdmin
    from src.apps.events.models import Event
    from src.apps.invitations.admin import InvitationAdmin
    from src.apps.users.models import User


def _handel_sending_messages(self: "InvitationAdmin | EventAdmin", request: "HttpRequest", message: str) -> None:
    self.message_user(request, message, level=messages.ERROR)
    messages.set_level(request, messages.ERROR)


def handle_invitation_check(
    self: "InvitationAdmin | EventAdmin", request: "HttpRequest", event: "Event", attendee: "User"
) -> bool:
    existing_invitation: bool = Invitation.objects.filter(event=event, attendee=attendee, status=1).exists()
    if existing_invitation:
        _handel_sending_messages(self, request, "This user already has an invitation to the event.")
        return False
    elif event.author == attendee:
        _handel_sending_messages(self, request, "You can't invite an author to his own event.")
        return False
    return True
