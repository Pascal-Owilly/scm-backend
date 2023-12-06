# Generated by Django 4.2.7 on 2023-12-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0023_inventorybreed_created_at_inventorybreed_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed_name', models.CharField(choices=[('goats', 'Goats'), ('sheep', 'Sheep'), ('cows', 'Cows'), ('pigs', 'Pigs')], default='goats', max_length=255)),
                ('status', models.CharField(choices=[('in_yard', 'In Yard'), ('sold', 'Sold'), ('slaughtered', 'Slaughtered')], default='in_yard', max_length=20)),
                ('quantity_total', models.PositiveIntegerField(default=0)),
                ('quantity_left', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PartsSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed_name', models.CharField(choices=[('goats', 'Goats'), ('sheep', 'Sheep'), ('cows', 'Cows'), ('pigs', 'Pigs')], default='goats', max_length=255)),
                ('quantity_sold', models.PositiveIntegerField(default=0)),
                ('sale_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SlaughteredParts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed_name', models.CharField(choices=[('goats', 'Goats'), ('sheep', 'Sheep'), ('cows', 'Cows'), ('pigs', 'Pigs')], default='goats', max_length=255)),
                ('purpose', models.CharField(choices=[('export_parts', 'Export Parts'), ('local_sales', 'Parts for Local Sales')], default='export_parts', max_length=20)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('inventory_status', models.CharField(choices=[('in_yard', 'In Yard'), ('sold', 'Sold'), ('slaughtered', 'Slaughtered')], default='in_yard', max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='inventorybreedsales',
            name='breed',
        ),
        migrations.RemoveField(
            model_name='inventorybreedsales',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='InventoryBreed',
        ),
        migrations.DeleteModel(
            name='InventoryBreedSales',
        ),
    ]
