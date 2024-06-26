from django.contrib import admin

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
