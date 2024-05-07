from django.contrib import admin

from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "modified",
        "attendee",
        "status",
        "event",
    )
    list_filter = ("created", "modified", "attendee", "event")

    def get_exclude(self, request, obj=None):
        if obj:
            return ()
        else:
            return ("status",)
