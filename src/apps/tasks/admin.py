from django.contrib import admin
from django.http import HttpRequest

from src.apps.tasks.const import TaskStatus

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):  # type: ignore
    list_display: tuple[str, ...] = (
        "description",
        "status",
        "author",
        "start",
        "end",
        "priority",
        "created",
        "modified",
    )
    list_filter: tuple[str, ...] = ("created", "modified", "author", "start", "end")

    def delete_model(self, request: HttpRequest, obj: Task) -> None:
        obj.status = TaskStatus.cancelled
        obj.save()
