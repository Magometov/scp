from src.apps.tasks.models import Task


class TaskService:
    def __init__(self, task: Task) -> None:
        self.task = task

    def __str__(self) -> str:
        return f"Задача {self.task.id} от {self.task.author} at {self.task.created}"
