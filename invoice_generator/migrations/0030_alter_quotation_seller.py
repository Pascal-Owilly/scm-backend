# Generated by Django 5.0.1 on 2024-02-23 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0011_alter_customuser_role'),
        ('invoice_generator', '0029_remove_documenttoseller_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='custom_registration.seller'),
        ),
    ]