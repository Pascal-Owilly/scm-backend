# Generated by Django 5.0.1 on 2024-02-06 11:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_alter_breadertrade_breeder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breadertrade',
            name='breeder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.breader'),
        ),
    ]