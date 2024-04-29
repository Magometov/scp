import uuid

from django.db import models

from src.apps.user.models import User


class Event(models.Model):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=100
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=200,
        blank=True
    )
    author = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name='events',
        null=True
    )
    start = models.DateField(
        verbose_name='Начало'
    )
    end = models.DateField(
        verbose_name='Окончание'
    )
