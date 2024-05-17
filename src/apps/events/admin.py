from django.contrib import admin

from src.apps.events.models import Event
from src.apps.invitations.models import Invitation


class InvitationInline(admin.TabularInline[Invitation, Event]):
    model = Invitation
    parent_model = Event
    extra = 1
    readonly_fields = ("status",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin[Event]):
    inlines = [InvitationInline]
    list_display = (
        "title",
        "description",
        "author",
        "start",
        "end",
        "created",
        "modified",
    )
    list_filter = ("created", "modified", "author", "start", "end")
