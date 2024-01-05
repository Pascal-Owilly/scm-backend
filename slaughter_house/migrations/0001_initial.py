# Generated by Django 5.0 on 2024-01-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlaughterhouseRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed', models.CharField(choices=[('goats', 'Goats'), ('sheep', 'Sheep'), ('cows', 'Cows'), ('pigs', 'Pigs')], default='goats', max_length=255)),
                ('slaughter_date', models.DateField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('slaughtered', 'Slaughtered')], default='slaughtered', max_length=255)),
            ],
        ),
    ]
