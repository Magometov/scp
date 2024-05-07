from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import Combinable
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from src.apps.base.models import BaseModel


class User(AbstractUser, BaseModel):
    email: "models.EmailField[str | int | Combinable, str]" = models.EmailField(
        verbose_name=_("Email"), max_length=50, unique=True
    )

    class Meta(TypedModelMeta):
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_related_name = "users"

    def __str__(self) -> str:
        return f"Пользователь {self.id}-{self.username}"
