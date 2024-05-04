from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from src.apps.base.models import BaseModel, TimeStampedModel

from .const import InvitationStatus


class Invitation(BaseModel, TimeStampedModel):
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Attendee"))
    status = models.PositiveSmallIntegerField(
        verbose_name=_("Invitation status"),
        choices=InvitationStatus.choices,
        default=InvitationStatus.pending,
    )
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, verbose_name=_("Event"))

    class Meta(TypedModelMeta):
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")
        default_related_name = "invitations"

    def __str__(self) -> str:
        return f"{self.attendee} -- {self.status}"
