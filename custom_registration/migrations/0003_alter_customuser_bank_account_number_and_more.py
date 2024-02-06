# Generated by Django 5.0.1 on 2024-02-02 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_registration', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bank_account_number',
            field=models.CharField(default=1234567891011, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='community',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='county',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='head_of_family',
            field=models.CharField(default='Example Name', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id_number',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='market',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
