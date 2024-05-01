import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class User(AbstractUser):
    id = models.UUIDField(verbose_name=_("ID"), primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name=_("Email"), max_length=50, unique=True)

    class Meta(TypedModelMeta):
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_related_name = "users"

    def __str__(self) -> str:
        return f"Пользователь {self.id}-{self.username}"
