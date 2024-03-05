# Generated by Django 5.0.1 on 2024-02-29 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0011_alter_customuser_role'),
        ('transaction', '0025_remove_inventory_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_registration.seller'),
        ),
    ]