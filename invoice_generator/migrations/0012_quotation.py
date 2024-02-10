# Generated by Django 5.0.1 on 2024-02-09 20:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_generator', '0011_remove_buyer_address_remove_buyer_buyer_country_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_address', models.CharField(max_length=255)),
                ('seller_country', models.CharField(max_length=255)),
                ('product', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice_generator.buyer')),
            ],
        ),
    ]
