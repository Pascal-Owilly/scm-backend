# Generated by Django 5.0.1 on 2024-03-05 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slaughter_house', '0004_slaughterhouserecord_control_center'),
    ]

    operations = [
        migrations.AddField(
            model_name='slaughterhouserecord',
            name='confirm',
            field=models.BooleanField(default=False),
        ),
    ]