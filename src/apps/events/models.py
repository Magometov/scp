from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from src.apps.base.models import BaseModel, TimeStampedModel

if TYPE_CHECKING:
    from datetime import datetime

    from src.apps.users.models import User


class Event(BaseModel, TimeStampedModel):
    title: "models.CharField[str, str]" = models.CharField(verbose_name=_("Title"), max_length=100)
    description: "models.CharField[str, str]" = models.CharField(
        verbose_name=_("Description"), max_length=200, blank=True
    )
    author: "models.ForeignKey[User | None, User | None]" = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name=_("Author"), null=True
    )
    start: "models.DateTimeField[datetime, datetime]" = models.DateTimeField(verbose_name=_("Start"))
    end: "models.DateTimeField[datetime, datetime]" = models.DateTimeField(verbose_name=_("End"))

    class Meta(TypedModelMeta):
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        default_related_name = "events"
        constraints = [
            models.CheckConstraint(
                check=models.Q(start__lt=models.F("end")),
                name="%(app_label)s_%(class)s_end_gt_start",
            )
        ]

    def __str__(self) -> str:
        return self.title
