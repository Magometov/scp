from django.contrib import messages

from src.apps.invitations.models import Invitation


def handle_invitation_check(self, request, event, attendee):
    existing_invitation = Invitation.objects.filter(event=event, attendee=attendee, status=1).exists()
    if existing_invitation:
        self.message_user(request, "This user already has an invitation to the event.", level=messages.ERROR)
        messages.set_level(request, messages.ERROR)
        return False
    elif event.author == attendee:
        self.message_user(request, "You can't invite an author to his own event.", level=messages.ERROR)
        messages.set_level(request, messages.ERROR)
        return False
    return True
