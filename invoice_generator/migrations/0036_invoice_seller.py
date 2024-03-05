# Generated by Django 5.0.1 on 2024-02-25 04:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0011_alter_customuser_role'),
        ('invoice_generator', '0035_remove_invoice_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_registration.seller'),
        ),
    ]