from typing import TYPE_CHECKING, Any

from django.db import models
from django.db.models.query import QuerySet

if TYPE_CHECKING:
    from src.apps.base.softdelete.models import SoftDeleteModel


class SoftDeleteQuerySet(QuerySet["SoftDeleteModel"]):
    def delete(self) -> None:  # type: ignore
        for obj in self.all():
            obj.delete()
        return

    def hard_delete(self) -> Any:
        return super().delete()


class DeletedQuerySet(QuerySet["SoftDeleteModel"]):
    def restore(self, *args: Any, **kwargs: Any) -> None:
        qs: QuerySet["SoftDeleteModel"] = self.filter(*args, **kwargs)
        for obj in qs:
            obj.restore()
        return


class SoftDeleteManager(models.Manager[models.Model]):
    def get_queryset(self) -> QuerySet["SoftDeleteModel"]:
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class DeletedManager(models.Manager[models.Model]):
    def get_queryset(self) -> QuerySet["SoftDeleteModel"]:
        return DeletedQuerySet(self.model, using=self._db).filter(deleted_at__isnull=False)


class GlobalManager(models.Manager[models.Model]):
    pass
