# Generated by Django 4.2.7 on 2023-12-06 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slaughter_house', '0002_slaughterhouserecord_associated_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slaughterhouserecord',
            name='associated_sale',
        ),
    ]
