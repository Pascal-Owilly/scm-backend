# Generated by Django 5.0 on 2023-12-18 04:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BreedCut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed', models.CharField(choices=[('goats', 'Goats'), ('sheep', 'Sheep'), ('cows', 'Cows'), ('pigs', 'Pigs')], max_length=255)),
                ('part_name', models.CharField(choices=[('ribs', 'Ribs'), ('thighs', 'Thighs'), ('loin', 'Loin'), ('shoulder', 'Shoulder'), ('shanks', 'Shanks'), ('organ_meat', 'Organ Meat'), ('intestines', 'Intestines'), ('tripe', 'Tripe'), ('sweetbreads', 'Sweetbreads')], max_length=255)),
                ('sale_type', models.CharField(choices=[('export_cut', 'Export Cut'), ('local_sale', 'Local Sale Cut')], max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('quantity_left', models.PositiveIntegerField(default=0, editable=False)),
                ('sale_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryBreed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed', models.CharField(choices=[('goats', 'Goats'), ('sheep', 'Sheep'), ('cows', 'Cows'), ('pigs', 'Pigs')], default='goats', max_length=255)),
                ('status', models.CharField(choices=[('in_the warehouse', 'In The Warehouse'), ('slaughtered', 'Slaughtered'), ('sold', 'Sold')], default='in_yard', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryBreedSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_name', models.CharField(choices=[('ribs', 'Ribs'), ('thighs', 'Thighs'), ('loin', 'Loin'), ('shoulder', 'Shoulder'), ('shanks', 'Shanks'), ('organ_meat', 'Organ Meat'), ('intestines', 'Intestines'), ('tripe', 'Tripe'), ('sweetbreads', 'Sweetbreads')], default='shanks', max_length=255)),
                ('sale_type', models.CharField(choices=[('export_cut', 'Export Cut'), ('local_sale', 'Local Sale Cut')], max_length=255)),
                ('status', models.CharField(choices=[('in_the warehouse', 'In The Warehouse'), ('slaughtered', 'Slaughtered'), ('sold', 'Sold')], default='in_the_warehouse', max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('sale_date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='inventory_management.breedcut')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
