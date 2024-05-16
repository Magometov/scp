from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from src.apps.base.models import BaseModel, TimeStampedModel

from .const import InvitationStatus

if TYPE_CHECKING:
    from src.apps.events.models import Event
    from src.apps.users.models import User


class Invitation(BaseModel, TimeStampedModel):
    attendee: "models.ForeignKey[User, User]" = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Attendee"),
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
                violation_error_message="This user already possesses an invitation to the event.",
            )
        ]

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()

        if self.event.author == self.attendee:
            raise ValidationError("You can't invite an author to his own event.")

    def __str__(self) -> str:
        return f"{self.attendee} - {self.status}"
