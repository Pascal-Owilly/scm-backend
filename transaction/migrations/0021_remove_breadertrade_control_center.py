# Generated by Django 5.0.1 on 2024-02-29 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0020_breadertrade_control_center'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='breadertrade',
            name='control_center',
        ),
    ]