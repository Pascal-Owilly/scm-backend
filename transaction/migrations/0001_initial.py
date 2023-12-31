# Generated by Django 5.0 on 2024-01-08 03:40

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Abattoir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Breader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BreaderTrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField(auto_now_add=True)),
                ('breed', models.CharField(choices=[('goats', 'Goats'), ('sheep', 'Sheep'), ('cows', 'Cows'), ('pigs', 'Pigs')], default='goats', max_length=255)),
                ('breeds_supplied', models.PositiveIntegerField(default=0)),
                ('goat_weight', models.PositiveIntegerField(default=0)),
                ('vaccinated', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('id_number', models.PositiveIntegerField(null=True)),
                ('bank_account_number', models.CharField(default=1234567891011, max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('reference', models.CharField(editable=False, max_length=20, unique=True)),
                ('abattoir', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.abattoir')),
                ('breeder', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AbattoirPaymentToBreader',
            fields=[
                ('payments_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_code', models.CharField(editable=False, max_length=50, unique=True)),
                ('payment_initiation_date', models.DateTimeField(auto_now_add=True)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('breeder_trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.breadertrade')),
            ],
        ),
    ]
