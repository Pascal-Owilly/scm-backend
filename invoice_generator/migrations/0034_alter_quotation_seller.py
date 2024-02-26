# Generated by Django 5.0.1 on 2024-02-23 11:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0011_alter_customuser_role'),
        ('invoice_generator', '0033_alter_quotation_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_registration.seller'),
        ),
    ]
