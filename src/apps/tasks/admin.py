from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "modified",
        "description",
        "status",
        "author",
        "start",
        "end",
        "priority",
    )
    list_filter = ("created", "modified", "author", "start", "end")
