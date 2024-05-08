from django.contrib import admin

from src.apps.invitations.services.handle_invitation import handle_invitation_check

from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin[Invitation]):
    list_display = (
        "attendee",
        "status",
        "event",
        "created",
        "modified",
    )
    list_filter = ("created", "modified", "attendee", "event")

    def save_model(self, request, obj, form, change):
        if handle_invitation_check(self, request, obj.event, obj.attendee):
            super().save_model(request, obj, form, change)
