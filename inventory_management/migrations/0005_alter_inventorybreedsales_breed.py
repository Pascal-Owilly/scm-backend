# Generated by Django 5.0 on 2023-12-10 15:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0004_alter_inventorybreedsales_breed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorybreedsales',
            name='breed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='inventory_management.breedcut'),
        ),
    ]
