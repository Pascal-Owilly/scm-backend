# Generated by Django 4.2.7 on 2023-12-06 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory_management', '0029_remove_inventorybreed_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorybreed',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]