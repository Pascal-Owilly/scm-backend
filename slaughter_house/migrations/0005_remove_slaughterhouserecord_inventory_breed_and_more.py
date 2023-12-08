# Generated by Django 4.2.7 on 2023-12-07 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slaughter_house', '0004_slaughterhouserecord_part_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slaughterhouserecord',
            name='inventory_breed',
        ),
        migrations.AddField(
            model_name='slaughterhouserecord',
            name='sale_type',
            field=models.CharField(choices=[('sold', 'Sold'), ('in_warehouse', 'In the warehouse')], default='in_warehouse', max_length=255),
        ),
    ]
