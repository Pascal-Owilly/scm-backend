# Generated by Django 4.2.7 on 2023-12-09 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0002_remove_breedcut_status_alter_breedcut_sale_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorybreed',
            name='total_breed_supply',
        ),
    ]