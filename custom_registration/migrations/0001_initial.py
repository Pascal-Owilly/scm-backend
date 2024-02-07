# Generated by Django 5.0.1 on 2024-02-06 11:11

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('bank_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=50)),
                ('bank_code', models.CharField(max_length=50, unique=True)),
                ('bank_abbreviation', models.CharField(max_length=50)),
                ('swift_code', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payments_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_code', models.CharField(editable=False, max_length=50, unique=True)),
                ('payment_initiation_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('payment_initiated', 'Sent to Bank for Payment Processing'), ('disbursed', 'Disbursed'), ('paid', 'Paid')], default='payment_initiated', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('is_dormant', models.BooleanField()),
                ('status_title', models.CharField(max_length=100)),
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField()),
                ('status_narration', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('no_role', 'No Role'), ('abattoir', 'Abattoir'), ('employee', 'employee'), ('superuser', 'Superuser'), ('breeder', 'Breeder'), ('regular', 'regular'), ('buyer', 'Buyer'), ('warehouse_personnel', 'Warehouse Personnel'), ('inventory_manager', 'Inventory Manager'), ('admin', 'Admin'), ('slaughterhouse_manager', 'Slaughterhouse Manager')], default='no_role', max_length=255)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('id_number', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('bank_account_number', models.CharField(default=1234567891011, max_length=30, null=True)),
                ('market', models.CharField(blank=True, max_length=100, null=True)),
                ('community', models.CharField(blank=True, max_length=100, null=True)),
                ('head_of_family', models.CharField(blank=True, default='Example Name', max_length=255, null=True)),
                ('county', models.CharField(blank=True, max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BankBranch',
            fields=[
                ('bank_branch_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_branch_name', models.CharField(max_length=100)),
                ('branch_code', models.CharField(max_length=50, unique=True)),
                ('head_office', models.CharField(max_length=100)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_registration.bank')),
            ],
        ),
        migrations.CreateModel(
            name='BankTeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_registration.bank')),
                ('bank_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_registration.bankbranch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
