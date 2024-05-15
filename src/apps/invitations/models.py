from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from src.apps.base.models import BaseModel, TimeStampedModel
from src.apps.invitations.const import InvitationStatus

if TYPE_CHECKING:

    from src.apps.events.models import Event
    from src.apps.users.models import User


class Invitation(BaseModel, TimeStampedModel):
    attendee: "models.ForeignKey[User, User]" = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Attendee")
    )
    status: "models.PositiveSmallIntegerField[InvitationStatus, InvitationStatus]" = models.PositiveSmallIntegerField(
        verbose_name=_("Invitation status"),
        choices=InvitationStatus.choices,
        default=InvitationStatus.pending,
    )
    event: "models.ForeignKey[Event, Event]" = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, verbose_name=_("Event")
    )

    class Meta(TypedModelMeta):
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")
        default_related_name = "invitations"
        constraints = [
            models.UniqueConstraint(
                fields=["attendee", "event"],
                name="%(app_label)s_%(class)s_unique_pair_of_attendee_and_event",
                violation_error_message="This user already has an invitation to the event.",
            ),
            models.CheckConstraint(
                check=~Q(attendee_id=F("event__author_id")),
                name="%(app_label)s_%(class)s_attendee_not_equal_event_author",
                violation_error_message="You can't invite an author to his own event.",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.attendee} -- {self.status}"
