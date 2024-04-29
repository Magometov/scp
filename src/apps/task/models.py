import uuid

from django.db import models

from src.apps.user.models import User


class Task(models.Model):
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    TASK_STATUS = {
        'd': 'Done',
        'todo': 'Todo',
        'inprogress': 'Inprogress'
    }

    TASK_PRIORITY = {
        'p': 'Prymary',
        's': 'Secondary'
    }

    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=250,
        blank=True
    )
    status = models.CharField(
        verbose_name='Статус',
        choices=TASK_STATUS,
        max_length=12
    )
    author = models.OneToOneField(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='author_tasks',
        blank=True
    )
    start = models.DateField(
        verbose_name='Начало',
        blank=True
    )
    end = models.DateField(
        verbose_name='Окончание',
        blank=True
    )
    priority = models.CharField(
        verbose_name='Приоритет',
        choices=TASK_PRIORITY,
        max_length=1
    )

    def __str__(self) -> str:
        return f"Задача {self.id} от {self.author}"
