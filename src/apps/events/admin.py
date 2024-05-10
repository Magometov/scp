from typing import TYPE_CHECKING

from django.contrib import admin

from src.apps.events.models import Event
from src.apps.invitations.models import Invitation
from src.apps.invitations.services.handle_invitation import handle_invitation_check

if TYPE_CHECKING:
    from typing import Any

    from django.http import HttpRequest


class InvitationInline(admin.TabularInline[Invitation, Event]):
    model = Invitation
    parent_model = Event
    extra = 1
    readonly_fields = ("status",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin[Event]):
    inlines = [InvitationInline]
    list_display: tuple[str, ...] = (
        "title",
        "description",
        "author",
        "start",
        "end",
        "created",
        "modified",
    )
    list_filter: tuple[str, ...] = ("created", "modified", "author", "start", "end")

    def save_formset(self, request: "HttpRequest", form: "Any", formset: "Any", change: "Any") -> None:
        instances = formset.save(commit=False)
        if not instances:
            super().save_formset(request, form, formset, change)
        for instance in instances:
            if handle_invitation_check(self, request, instance.event, instance.attendee):
                super().save_formset(request, form, formset, change)
