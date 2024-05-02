from django.db import models
from django.utils.translation import gettext_lazy as _


class InvitationStatus(models.IntegerChoices):
    pending = 1, _("Pending")
    accepted = 2, _("Accepted")
    declined = 3, _("Declined")
    cancelled = 4, _("Cancelled")
