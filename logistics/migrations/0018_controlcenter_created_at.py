# Generated by Django 5.0.1 on 2024-02-26 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0017_collateralmanager_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlcenter',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
