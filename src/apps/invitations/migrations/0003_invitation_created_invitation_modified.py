# Generated by Django 5.0.4 on 2024-05-02 20:17

import django.utils.timezone
import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("invitations", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="invitation",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True, default=django.utils.timezone.now, verbose_name="created"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="invitation",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
        ),
    ]
