"""Celery config"""

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")
app = Celery("scp")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = "Europe/Moscow"

app.conf.imports = [
    "src.apps.celery_tasks.tasks.email.send_email_tasks",
]

app.conf.beat_schedule = {
    "test_celery_task": {
        "task": "test_celery_task",
        "schedule": crontab(hour="22", minute="15"),
        "options": {
            "queue": "periodic",
        },
    },
}
