# models.py
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

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
    market = models.CharField(max_length=100)
    community = models.CharField(max_length=100)
    head_of_family = models.CharField(max_length=255,default='Example Name')
    country = models.CharField(max_length=50)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username + ' Profile'


