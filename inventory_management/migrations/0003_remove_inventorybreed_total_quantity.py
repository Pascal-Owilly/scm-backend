# Generated by Django 4.2.7 on 2023-12-08 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0002_rename_quantity_inventorybreed_total_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorybreed',
            name='total_quantity',
        ),
    ]