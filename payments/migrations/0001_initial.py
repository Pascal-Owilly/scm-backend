# Generated by Django 5.0 on 2023-12-27 05:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquityBankPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=20)),
                ('payment_status', models.CharField(default='pending', max_length=20)),
                ('breeder_trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.breadertrade')),
                ('payer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.abattoir')),
            ],
        ),
    ]
