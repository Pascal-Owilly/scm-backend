# Generated by Django 5.0 on 2024-01-22 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_generator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyer',
            old_name='username',
            new_name='buyer',
        ),
    ]