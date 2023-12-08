# Generated by Django 4.2.7 on 2023-12-07 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slaughter_house', '0008_rename_sale_type_slaughterhouserecord_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slaughterhouserecord',
            name='status',
            field=models.CharField(choices=[('slaughtered', 'Slaughtered'), ('in_the warehouse', 'In The Warehouse'), ('sold', 'Sold')], default='slaughtered', max_length=255),
        ),
    ]
