from django.contrib import admin

from src.apps.events.models import Event
from src.apps.invitations.models import Invitation


class InvitationInline(admin.TabularInline):
    model = Invitation
    extra = 1
    exclude = ("status",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [InvitationInline]
    list_display = (
        "created",
        "modified",
        "title",
        "description",
        "author",
        "start",
        "end",
    )
    list_filter = ("created", "modified", "author", "start", "end")
