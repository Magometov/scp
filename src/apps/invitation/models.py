import uuid

from django.db import models

from src.apps.event.models import Event
from src.apps.user.models import User


class Invitation(models.Model):
    class Meta:
        verbose_name = 'Приглашения'
        verbose_name_plural = 'Приглашения'

    INVITATION_STATUS = {
        'p': 'Pending',
        'a': 'Accepted',
        'd': 'Declined',
        'c': 'Cancelled'
    }
    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    attended = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    status = models.CharField(
        verbose_name='Статус',
        choices=INVITATION_STATUS,
        max_length=1,
        default='p'
    )
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
