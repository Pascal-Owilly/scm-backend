# Generated by Django 5.0.1 on 2024-02-20 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0010_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('no_role', 'No Role'), ('abattoir', 'Abattoir'), ('employee', 'employee'), ('superuser', 'Superuser'), ('breeder', 'Breeder'), ('regular', 'regular'), ('buyer', 'Buyer'), ('seller', 'Seller'), ('warehouse_personnel', 'Warehouse Personnel'), ('inventory_manager', 'Inventory Manager'), ('admin', 'Admin'), ('slaughterhouse_manager', 'Slaughterhouse Manager'), ('collateral_manager', 'Collateral Manager')], default='no_role', max_length=255),
        ),
    ]