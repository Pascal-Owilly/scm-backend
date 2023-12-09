# Generated by Django 4.2.7 on 2023-12-08 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='breedcut',
            name='status',
        ),
        migrations.AlterField(
            model_name='breedcut',
            name='sale_type',
            field=models.CharField(choices=[('export_cut', 'Export Cut'), ('local_sale', 'Local Sale Cut')], max_length=255),
        ),
        migrations.AlterField(
            model_name='inventorybreedsales',
            name='sale_type',
            field=models.CharField(choices=[('export_cut', 'Export Cut'), ('local_sale', 'Local Sale Cut')], max_length=255),
        ),
    ]
