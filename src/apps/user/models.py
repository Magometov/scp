import uuid

from django.db import models


class User(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=50,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=50,
        unique=True
    )

    def __str__(self) -> str:
        return f"Пользователь {self.id}-{self.username}"
