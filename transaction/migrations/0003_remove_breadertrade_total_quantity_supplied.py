# Generated by Django 4.2.7 on 2023-12-07 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_breadertrade_total_quantity_supplied'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='breadertrade',
            name='total_quantity_supplied',
        ),
    ]