import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class Event(models.Model):
    id = models.UUIDField(verbose_name=_("ID"), primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    description = models.CharField(verbose_name=_("Description"), max_length=200, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name=_("Author"), null=True)
    start = models.DateTimeField(verbose_name=_("Start"))
    end = models.DateTimeField(verbose_name=_("End"))

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
