# Generated by Django 5.0 on 2023-12-25 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa_payments', '0001_initial'),
        ('transaction', '0005_breadertrade_payment_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Payment',
            new_name='MpesaPayment',
        ),
    ]
