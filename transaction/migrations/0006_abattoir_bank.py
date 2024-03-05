# Generated by Django 5.0.1 on 2024-02-06 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0002_initial'),
        ('transaction', '0005_abattoir_breeders'),
    ]

    operations = [
        migrations.AddField(
            model_name='abattoir',
            name='bank',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='custom_registration.bank'),
        ),
    ]