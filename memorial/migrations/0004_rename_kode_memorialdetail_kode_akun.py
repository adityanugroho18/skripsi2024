# Generated by Django 5.0.6 on 2024-07-11 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memorial', '0003_memorialdetail_kode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memorialdetail',
            old_name='kode',
            new_name='kode_akun',
        ),
    ]
