from datetime import datetime
from typing import Any

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from src.apps.base.softdelete.managers import (
    DeletedManager,
    GlobalManager,
    SoftDeleteManager,
)


class SoftDeleteModel(models.Model):

    objects = SoftDeleteManager()
    deleted_objects = DeletedManager()
    global_objects = GlobalManager()

    restored_at: "models.DateTimeField[datetime | None, datetime | None]" = models.DateTimeField(
        _("restored_at"), blank=True, null=True, editable=False
    )
    deleted_at: "models.DateTimeField[datetime | None, datetime | None]" = models.DateTimeField(
        _("deleted_at"), blank=True, null=True, editable=False
    )

    class Meta(TypedModelMeta):
        abstract = True

    def delete(self, *args: Any, **kwargs: Any) -> None:  # type: ignore
        self.deleted_at = timezone.now()
        self.restored_at = None
        self.save(update_fields=["deleted_at", "restored_at"])

    def restore(self, *args: Any, **kwargs: Any) -> None:
        self.restored_at = timezone.now()
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "restored_at"])
