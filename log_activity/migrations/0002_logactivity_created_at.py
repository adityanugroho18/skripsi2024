# Generated by Django 5.0.6 on 2024-07-10 07:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_activity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logactivity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
