# Generated by Django 5.0.1 on 2024-02-28 05:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0011_alter_customuser_role'),
        ('invoice_generator', '0042_alter_letterofcredit_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='letterofcredit',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_registration.seller'),
        ),
        migrations.AlterField(
            model_name='letterofcredit',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('sent_to_bank', 'Sent to bank'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='sent_to_bank', max_length=255),
        ),
    ]
