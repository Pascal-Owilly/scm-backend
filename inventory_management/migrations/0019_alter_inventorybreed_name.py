# Generated by Django 4.2.7 on 2023-12-06 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0018_alter_inventorybreed_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorybreed',
            name='name',
            field=models.CharField(choices=[('goats', 'Goats'), ('sheep', 'Sheep'), ('cows', 'Cows'), ('pigs', 'Pigs')], max_length=255, unique=True),
        ),
    ]
