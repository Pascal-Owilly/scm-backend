# Generated by Django 4.2.7 on 2023-12-05 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0014_inventorybreed_original_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorybreed',
            name='original_quantity',
        ),
    ]
