# Generated by Django 4.2.7 on 2023-12-01 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0005_abattoirpayment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='breadertrade',
            name='community',
            field=models.CharField(default='Example ABC Community', max_length=255),
        ),
        migrations.AddField(
            model_name='breadertrade',
            name='goat_weight',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='breadertrade',
            name='head_of_family',
            field=models.CharField(default='Example ABC Family', max_length=255),
        ),
        migrations.AddField(
            model_name='breadertrade',
            name='market',
            field=models.CharField(default='ABC Market', max_length=255),
        ),
        migrations.AddField(
            model_name='breadertrade',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='breadertrade',
            name='vaccinated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='breadertrade',
            name='breads_supplied',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
