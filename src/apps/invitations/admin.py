from typing import TYPE_CHECKING

from django.contrib import admin

from src.apps.invitations.models import Invitation
from src.apps.invitations.services.handle_invitation import handle_invitation_check

if TYPE_CHECKING:
    from typing import Any

    from django.http import HttpRequest


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin[Invitation]):
    list_display: tuple[str, ...] = (
        "attendee",
        "status",
        "event",
        "created",
        "modified",
    )
    list_filter: tuple[str, ...] = ("created", "modified", "attendee", "event")

    def save_model(self, request: "HttpRequest", obj: Invitation, form: "Any", change: "Any") -> None:
        if handle_invitation_check(self, request, obj.event, obj.attendee):
            super().save_model(request, obj, form, change)
