# Generated by Django 5.0.1 on 2024-03-04 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0012_seller_breeders'),
        ('logistics', '0020_controlcenter_total_breed_supply'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='controlcenter',
            constraint=models.CheckConstraint(check=models.Q(('total_breed_supply__gte', 0)), name='total_breed_supply_non_negative'),
        ),
    ]
