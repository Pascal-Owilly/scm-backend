# Generated by Django 4.2.7 on 2023-11-26 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_rename_supplier_breader_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='breadertransaction',
            old_name='supplier',
            new_name='breader',
        ),
        migrations.RenameField(
            model_name='breadertransaction',
            old_name='goats_supplied',
            new_name='breads_supplied',
        ),
    ]
