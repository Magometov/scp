import uuid
from typing import Any

from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(verbose_name=_("ID"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class DateTimeAbstractModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_("Created"), default=timezone.now, null=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated"), default=timezone.now, null=True)

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.updated_at = make_aware(timezone.now())
        super().save(*args, **kwargs)
