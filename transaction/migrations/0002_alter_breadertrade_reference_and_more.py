# Generated by Django 5.0 on 2023-12-29 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breadertrade',
            name='reference',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='breadertrade',
            name='transaction_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]