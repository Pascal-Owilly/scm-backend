# Generated by Django 5.0.1 on 2024-02-25 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_generator', '0038_invoice_buyer_invoice_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='seller',
        ),
    ]
