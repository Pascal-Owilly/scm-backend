# Generated by Django 5.0 on 2024-01-01 06:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0005_alter_breadertrade_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='breadertrade',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]