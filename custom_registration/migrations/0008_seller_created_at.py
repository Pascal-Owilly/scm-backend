# Generated by Django 5.0.1 on 2024-02-10 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0007_delete_quotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
