# Generated by Django 5.0 on 2024-01-25 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_generator', '0002_rename_username_buyer_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='attached_lc_document',
            field=models.FileField(upload_to='invoice_documents/'),
        ),
    ]
