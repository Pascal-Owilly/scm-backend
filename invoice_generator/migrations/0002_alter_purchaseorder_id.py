# Generated by Django 5.0 on 2024-01-16 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_generator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
