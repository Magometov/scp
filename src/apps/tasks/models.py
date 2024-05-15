from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from src.apps.base.models import BaseModel, TimeStampedModel

if TYPE_CHECKING:
    from datetime import datetime
    from src.apps.users.models import User
    from typing import Any

from .const import TaskPriority, TaskStatus


class MyQuerySet(models.query.QuerySet):
    def delete(self):
        self.update(status=TaskStatus.cancelled)


class NoDeleteManager(models.Manager):
    def get_queryset(self):
        return MyQuerySet(self.model, using=self._db)


class Task(BaseModel, TimeStampedModel):
    title: "models.CharField[str, str]" = models.CharField(verbose_name=_("Title"), max_length=50)
    description: "models.TextField[str, str]" = models.TextField(verbose_name=_("Description"), blank=True)
    status: "models.PositiveSmallIntegerField[TaskStatus, TaskStatus]" = models.PositiveSmallIntegerField(
        verbose_name=_("Task status"), choices=TaskStatus.choices, default=TaskStatus.backlog
    )
    author: "models.ForeignKey[User, User]" = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
        blank=True,
    )
    start: "models.DateTimeField[datetime | None, datetime | None]" = models.DateTimeField(
        verbose_name=_("Start"), blank=True, null=True
    )
    end: "models.DateTimeField[datetime | None, datetime | None]" = models.DateTimeField(
        verbose_name=_("End"), blank=True, null=True
    )
    priority: "models.PositiveSmallIntegerField[TaskPriority | None, TaskPriority | None]" = (
        models.PositiveSmallIntegerField(
            verbose_name=_("Task priority"), choices=TaskPriority.choices, null=True, blank=True
        )
    )

    objects = NoDeleteManager()

    class Meta(TypedModelMeta):
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        default_related_name = "tasks"
        constraints = [
            models.CheckConstraint(
                check=models.Q(start__lt=models.F("end")),
                name="%(app_label)s_%(class)s_end_gt_start",
            ),
            models.CheckConstraint(
                check=models.Q(start__isnull=True, end__isnull=True) | models.Q(start__isnull=False, end__isnull=False),
                name="%(app_label)s_%(class)s_end_start_both_or_none",
            ),
        ]

    def delete(self, *args: "Any", **kwargs: "Any") -> None:  # type: ignore
        self.status = TaskStatus.cancelled
        self.save()

    def __str__(self) -> str:
        return f"Task from {self.author}"

    def __repr__(self) -> str:
        return f"<Task: {self}>"
