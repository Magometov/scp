import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from .const import TaskPriority, TaskStatus


class Task(models.Model):
    id = models.UUIDField(verbose_name=_("ID"), primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    status = models.PositiveSmallIntegerField(
        verbose_name=_("Task status"), choices=TaskStatus.choices, default=TaskStatus.backlog
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
        blank=True,
    )
    start = models.DateTimeField(verbose_name=_("Start"), blank=True, null=True)
    end = models.DateTimeField(verbose_name=_("End"), blank=True, null=True)
    priority = models.PositiveSmallIntegerField(
        verbose_name=_("Task priority"), choices=TaskPriority.choices, null=True, blank=True
    )

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

    def __str__(self) -> str:
        return f"Задача {self.id} от {self.author}"