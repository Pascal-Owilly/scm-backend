# Generated by Django 5.0 on 2024-01-08 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logisticsstatus',
            name='status',
            field=models.CharField(choices=[('ordered', 'Ordered'), ('dispatched', 'Dispatched'), ('shipped', 'Shipped'), ('arrived', 'Arrival'), ('received', 'Received')], max_length=255),
        ),
    ]
