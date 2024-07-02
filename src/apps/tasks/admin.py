from typing import TYPE_CHECKING

from django.contrib import admin, messages

from src.apps.base.helper import sending_messages_in_admin_panel
from src.apps.tasks.const import TaskStatus

from .models import Task

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.db.models import QuerySet
    from django.http import HttpRequest


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin[Task]):
    list_display = (
        "description",
        "status",
        "author",
        "start",
        "end",
        "priority",
        "created",
        "modified",
    )
    list_filter = ("created", "modified", "author", "start", "end")

    actions = [
        "make_cancelled",
    ]

    def get_actions(self, request: "HttpRequest") -> dict[str, tuple["Callable[..., str]", str, str] | None]:
        actions: dict[str, tuple["Callable[..., str]", str, str] | None] = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def delete_model(self, request: "HttpRequest", obj: Task) -> None:
        obj.status = TaskStatus.cancelled
        obj.save()
        sending_messages_in_admin_panel(
            self,
            request=request,
            message=f"Status of the {obj} has been successfully moved to canceled.",
            level=messages.DEBUG,
        )

    @admin.action(description="Mark selected tasks as cancelled")
    def make_cancelled(self, request: "HttpRequest", queryset: "QuerySet[Task]") -> None:
        updated = queryset.update(status=TaskStatus.cancelled)
        sending_messages_in_admin_panel(
            self,
            request=request,
            message=f"Statuses have been successfully changed for {updated} tasks.",
            level=messages.SUCCESS,
        )
