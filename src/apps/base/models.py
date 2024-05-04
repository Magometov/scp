import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class BaseModel(models.Model):
    id = models.UUIDField(verbose_name=_("ID"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(TypedModelMeta):
        abstract = True


class TimeStampedModel(models.Model):
    """
    TimeStampedModel

    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """

    created = models.DateTimeField(_("created"), auto_now_add=True, editable=False, blank=True)
    modified = models.DateTimeField(_("modified"), auto_now=True, editable=False, blank=True)

    class Meta(TypedModelMeta):
        get_latest_by = "modified"
        abstract = True
