# Generated by Django 4.2.7 on 2023-12-06 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0026_inventorybreed_inventorybreedsales_delete_inventory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorybreed',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]