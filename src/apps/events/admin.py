from django.contrib import admin

from src.apps.events.models import Event
from src.apps.invitations.models import Invitation
from src.apps.invitations.services.handle_invitation import handle_invitation_check


class InvitationInline(admin.TabularInline[Invitation, Event]):
    model = Invitation
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

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        if not instances:
            super().save_formset(request, form, formset, change)
        for instance in instances:
            if handle_invitation_check(self, request, instance.event, instance.attendee):
                super().save_formset(request, form, formset, change)
