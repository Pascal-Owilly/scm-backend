# Generated by Django 5.0.1 on 2024-02-25 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_generator', '0034_alter_quotation_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='due_date',
        ),
    ]
