# Generated by Django 5.0.6 on 2024-07-10 08:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_activity', '0003_rename_id_user_logactivity_user_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logactivity',
            name='user_id',
        ),
        migrations.AddField(
            model_name='logactivity',
            name='id_user',
            field=models.ForeignKey(db_column='id_user', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
