# Generated by Django 4.2.7 on 2023-12-06 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0032_alter_inventorybreedsales_part_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorybreed',
            name='status',
            field=models.CharField(choices=[('in_yard', 'In Yard'), ('slaughtered', 'Slaughtered'), ('sold', 'Sold')], default='sold', max_length=20),
        ),
    ]
