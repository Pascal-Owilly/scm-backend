# Generated by Django 4.2.7 on 2023-12-06 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0014_remove_breadertrade_animal_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='breadertrade',
            old_name='breed_name',
            new_name='animal_name',
        ),
    ]