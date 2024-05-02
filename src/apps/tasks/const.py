from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskStatus(models.IntegerChoices):
    backlog = 1, _("Backlog")
    todo = 2, _("Todo")
    in_progress = 3, _("In Progress")
    in_review = 4, _("In review")
    release = 5, _("Release")
    done = 6, _("Done")
    cancelled = 7, _("Cancelled")


class TaskPriority(models.IntegerChoices):
    high = 1, _("High")
    medium = 2, _("Medium")
    low = 3, _("Low")

    __empty__ = _("No priority")
