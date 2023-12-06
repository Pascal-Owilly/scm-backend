# Generated by Django 4.2.7 on 2023-12-06 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0010_alter_breadertrade_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='breadertrade',
            options={},
        ),
        migrations.RemoveField(
            model_name='breadertrade',
            name='breed_name',
        ),
        migrations.AddField(
            model_name='breadertrade',
            name='animal_name',
            field=models.CharField(default='eg goats, cows... etc', max_length=255),
        ),
    ]
