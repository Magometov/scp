
from django.contrib import admin

from src.apps.invitations.models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin[Invitation]):
    list_display: tuple = (
        "attendee",
        "status",
        "event",
        "created",
        "modified",
    )
    list_filter: tuple = ("created", "modified", "attendee", "event")

    # def save_model(self, request: "HttpRequest", obj: Invitation, form: "Any", change: "Any") -> None:
    #     if handle_invitation_check(self, request, obj.event, obj.attendee):
    #         super().save_model(request, obj, form, change)
