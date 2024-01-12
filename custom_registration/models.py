# models.py
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
import uuid
import random
import string
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Status(models.Model):
    is_dormant = models.BooleanField()  
    status_title = models.CharField(max_length=100)
    status_id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField()
    status_narration = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Status - {self.status_id}"

class Bank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=50)
    bank_code = models.CharField(max_length=50, unique=True)
    bank_abbreviation = models.CharField(max_length=50)
    swift_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.bank_name 

class BankBranch(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    bank_branch_id = models.AutoField(primary_key=True)
    bank_branch_name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=50, unique=True)
    head_office = models.CharField(max_length=100)

    def __str__(self):
        return self.bank_branch_name  


class Payment(models.Model):

    SENT_TO_BANK = 'payment_initiated'
    DISBURSED = 'disbursed'
    PAID = 'paid'

    STATUS_CHOICES = [
        (SENT_TO_BANK, 'Sent to Bank for Payment Processing'),
        (DISBURSED, 'Disbursed'),
        (PAID, 'Paid'),
    ]

    payments_id = models.AutoField(primary_key=True)
    payment_code = models.CharField(max_length=50, unique=True, editable=False)
    payment_initiation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default=SENT_TO_BANK, max_length=100)
    breeder_trade = models.ForeignKey('transaction.BreaderTrade', on_delete=models.CASCADE)

    def process_payment(self):
        # Example: Update payment status to 'Paid'
        self.status = self.SENT_TO_BANK
        self.save()

        # Add additional payment processing logic here
        # For example, interact with a payment gateway, log payment details, etc.

        # Return True if the payment was successful
        return True

    def generate_payment_code(self):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(7))

    def save(self, *args, **kwargs):
        if not self.payment_code:
            self.payment_code = self.generate_payment_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment - {self.payments_id}"

class CustomUser(AbstractUser):
    NO_ROLE = 'no_role'
    ABATTOIR = 'abattoir'
    EMPLOYEE= 'employee'
    SUPERUSER = 'superuser'
    BREEDER = 'breeder'
    REGULAR = 'regular'
    BUYER = 'buyer'
    WAREHOUSE_PERSONNEL = 'warehouse_personnel'
    INVENTORY_MANAGER = 'inventory_manager'
    ADMIN = 'admin'
    SLAUGHTERHOUSE_MANAGER = 'slaughterhouse_manager'
    # WAREHOUSE_MANAGER = 'warehouse_manager'

    ROLE_CHOICES = [
        (NO_ROLE, 'No Role'),
        (ABATTOIR, 'Abattoir'),
        (EMPLOYEE, 'employee'),
        (SUPERUSER, 'Superuser'),
        (BREEDER, 'Breeder'),
        (REGULAR, 'regular'),
        (BUYER, 'Buyer'),
        (WAREHOUSE_PERSONNEL, 'Warehouse Personnel'),
        (INVENTORY_MANAGER, 'Inventory Manager'),
        (ADMIN, 'Admin'),
        (SLAUGHTERHOUSE_MANAGER, 'Slaughterhouse Manager'),
        # (WAREHOUSE_MANAGER, 'Warehouse Manager'),
    ]

    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default=NO_ROLE)  # Default role can be changed

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    id_number = models.PositiveIntegerField(default=0)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(null=True)
    bank_account_number = models.CharField(max_length=30, default=1234567891011)
    market = models.CharField(max_length=100)
    community = models.CharField(max_length=100)
    head_of_family = models.CharField(max_length=255,default='Example Name')
    county = models.CharField(max_length=50)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)



    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class BankTeller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    bank_branch = models.ForeignKey(BankBranch, on_delete=models.CASCADE)  

    def __str__(self):

        return self.user.first_name

class CustomerService(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username + ' Profile'



