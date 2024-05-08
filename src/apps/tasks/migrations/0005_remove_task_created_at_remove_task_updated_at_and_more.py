# Generated by Django 5.0.4 on 2024-05-07 09:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0004_remove_task_created_remove_task_modified_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="task",
            name="updated_at",
        ),
        migrations.AddField(
            model_name="task",
            name="created",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name="created"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="modified",
            field=models.DateTimeField(auto_now=True, verbose_name="modified"),
        ),
    ]
