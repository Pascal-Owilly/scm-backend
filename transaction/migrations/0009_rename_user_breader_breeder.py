# Generated by Django 5.0.1 on 2024-02-20 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0008_remove_breadertrade_tag_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='breader',
            old_name='user',
            new_name='breeder',
        ),
    ]