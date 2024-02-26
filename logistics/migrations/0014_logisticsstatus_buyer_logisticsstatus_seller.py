# Generated by Django 5.0.1 on 2024-02-25 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0011_alter_customuser_role'),
        ('invoice_generator', '0040_invoice_buyer_invoice_seller'),
        ('logistics', '0013_remove_logisticsstatus_buyer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='logisticsstatus',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice_generator.buyer'),
        ),
        migrations.AddField(
            model_name='logisticsstatus',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_registration.seller'),
        ),
    ]
