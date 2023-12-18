# Generated by Django 5.0 on 2023-12-18 05:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_generator', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buyer',
            options={},
        ),
        migrations.AlterModelManagers(
            name='buyer',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='country',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='password',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='username',
        ),
        migrations.AddField(
            model_name='buyer',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
